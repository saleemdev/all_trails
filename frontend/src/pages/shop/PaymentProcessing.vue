<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { GlassAlert, GlassButton, GlassCard, GlassSpinner } from '../../components/glass'
import { useMerchandiseStore } from '../../stores/merchandiseStore'
import { shopApi } from '../../services/shopApi'
import type { MerchandiseOrder } from '../../types/shop'
import { getMpesaProgressModel } from '../../utils/mpesaStatus'

const route = useRoute()
const router = useRouter()
const store = useMerchandiseStore()

const orderId = String(route.params.orderId || '')
const order = ref<MerchandiseOrder | null>(null)
const pollAttempts = ref(0)
const maxPollAttempts = 120
const pollIntervalMs = 3000
const isPolling = ref(false)
const pollError = ref<string | null>(null)
let pollTimer: ReturnType<typeof setInterval> | null = null

const paymentDetail = computed(() => order.value?.payment_detail)
const progress = computed(() =>
  getMpesaProgressModel({
    paymentStatus: paymentDetail.value?.status || order.value?.payment_status,
    ticketStatus: paymentDetail.value?.ticket_status,
    fallbackStatus: order.value?.payment_status,
    message: paymentDetail.value?.message,
  })
)

const hasPaymentSession = computed(() => !!order.value?.mpesa_payment_id)
const hasSucceeded = computed(
  () =>
    progress.value.isSuccess ||
    order.value?.payment_status === 'Paid' ||
    order.value?.payment_status === 'Partially Paid'
)

const stopPolling = () => {
  if (!pollTimer) {
    return
  }
  clearInterval(pollTimer)
  pollTimer = null
  isPolling.value = false
}

const refreshOrder = async () => {
  const latest = await store.fetchOrderById(orderId)
  order.value = latest
  return latest
}

const handlePaid = () => {
  stopPolling()
  void router.replace(`/shop/confirmation/${orderId}`)
}

const pollPaymentStatus = async () => {
  pollAttempts.value += 1
  pollError.value = null

  try {
    const latest = await refreshOrder()
    if (!latest) {
      pollError.value = 'Order not found. Open tracking to search by order number.'
      stopPolling()
      return
    }

    if (hasSucceeded.value) {
      handlePaid()
      return
    }

    if (progress.value.isTerminal) {
      stopPolling()
      return
    }

    if (pollAttempts.value >= maxPollAttempts) {
      pollError.value = 'Still waiting for MPESA callback. Keep this page open and check again shortly.'
      stopPolling()
    }
  } catch (reason) {
    pollError.value = reason instanceof Error ? reason.message : 'Unable to refresh payment status.'
    if (pollAttempts.value >= maxPollAttempts) {
      stopPolling()
    }
  }
}

const startPolling = async () => {
  stopPolling()
  pollAttempts.value = 0
  isPolling.value = true
  await pollPaymentStatus()
  if (!progress.value.isTerminal && hasPaymentSession.value) {
    pollTimer = setInterval(() => {
      void pollPaymentStatus()
    }, pollIntervalMs)
  } else {
    isPolling.value = false
  }
}

onMounted(async () => {
  const loadedOrder = await refreshOrder()
  if (!loadedOrder) {
    pollError.value = 'Order not found. Open tracking to locate it manually.'
    return
  }

  if (shopApi.usesMockData()) {
    await store.confirmMockPayment(orderId)
    handlePaid()
    return
  }

  if (hasSucceeded.value) {
    handlePaid()
    return
  }

  if (!hasPaymentSession.value) {
    pollError.value = 'No MPESA payment session was found for this order.'
    return
  }

  await startPolling()
})

onUnmounted(stopPolling)
</script>

<template>
  <div class="layout-shell page-block">
    <GlassCard tone="strong" class="text-center">
      <p class="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Payment handoff</p>
      <h1 class="page-title">{{ progress.title }}</h1>
      <p class="mx-auto mt-4 max-w-2xl text-sm leading-7 text-slate-600">
        {{ progress.detail }}
      </p>

      <div v-if="!progress.isTerminal" class="mt-10">
        <GlassSpinner size="lg" label="Checking payment state" />
      </div>

      <div class="mx-auto mt-8 max-w-xl rounded-full bg-slate-200">
        <div
          class="h-3 rounded-full transition-all duration-500"
          :class="progress.tone === 'success' ? 'bg-[linear-gradient(135deg,#16803c,#36aa65)]' : progress.tone === 'error' ? 'bg-[linear-gradient(135deg,#b91c1c,#ef4444)]' : progress.tone === 'warning' ? 'bg-[linear-gradient(135deg,#a16207,#f59e0b)]' : 'bg-[linear-gradient(135deg,var(--color-primary),#7a998d)]'"
          :style="{ width: `${progress.progress}%` }"
        />
      </div>

      <div class="mt-4 text-sm font-semibold text-slate-600">
        {{ progress.progress }}% complete · {{ paymentDetail?.status || order?.payment_status || 'Pending' }}
      </div>

      <div v-if="paymentDetail || order" class="mx-auto mt-6 max-w-2xl rounded-[1rem] bg-white/80 p-4 text-left text-sm text-slate-700">
        <p class="mb-1 font-semibold text-slate-900">Payment references</p>
        <p v-if="order?.mpesa_payment_id">Payment ID: {{ order.mpesa_payment_id }}</p>
        <p v-if="paymentDetail?.ticket_id">Ticket: {{ paymentDetail.ticket_id }} ({{ paymentDetail.ticket_status || 'Unknown' }})</p>
        <p v-if="paymentDetail?.checkout_request_id">Checkout Request: {{ paymentDetail.checkout_request_id }}</p>
        <p v-if="paymentDetail?.receipt_number">Receipt: {{ paymentDetail.receipt_number }}</p>
        <p v-if="paymentDetail?.provider_status_code">Gateway code: {{ paymentDetail.provider_status_code }}</p>
      </div>

      <GlassAlert v-if="paymentDetail?.failure_reason" tone="error" title="MPESA error" class="mx-auto mt-6 max-w-2xl text-left">
        {{ paymentDetail.failure_reason }}
      </GlassAlert>

      <GlassAlert v-if="pollError" tone="warning" title="Payment status note" class="mx-auto mt-6 max-w-2xl text-left">
        {{ pollError }}
      </GlassAlert>

      <GlassAlert tone="info" title="MPESA note" class="mx-auto mt-6 max-w-2xl text-left">
        If the prompt does not arrive, confirm the selected Safaricom line is active and has transaction limit headroom.
      </GlassAlert>

      <div class="mt-8 flex flex-wrap justify-center gap-3">
        <GlassButton
          v-if="hasPaymentSession && !progress.isTerminal"
          variant="secondary"
          :loading="isPolling"
          @click="pollPaymentStatus"
        >
          Check again
        </GlassButton>
        <GlassButton variant="secondary" @click="router.push(`/shop/tracking/${orderId}`)">Track manually</GlassButton>
        <GlassButton variant="ghost" @click="router.push('/shop')">Back to catalog</GlassButton>
      </div>
    </GlassCard>
  </div>
</template>
