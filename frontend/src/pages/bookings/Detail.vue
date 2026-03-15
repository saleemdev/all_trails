<script setup lang="ts">
import { onMounted, onUnmounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookingsStore } from '../../stores/bookingsStore'
import { useUiStore } from '../../stores/uiStore'
import type { MpesaPaymentState } from '../../types/index'
import { apiService } from '../../services/api'
import { getMpesaProgressModel } from '../../utils/mpesaStatus'
import { isValidKenyanMpesaPhone, normalizeKenyanMpesaPhone } from '../../utils/payments'

const route = useRoute()
const router = useRouter()
const bookingsStore = useBookingsStore()
const uiStore = useUiStore()

const booking = computed(() => bookingsStore.selectedBooking)
const isLoading = computed(() => bookingsStore.isLoading)

const paymentState = ref<MpesaPaymentState | null>(null)
const mpesaPhone = ref('')
const isInitiatingPayment = ref(false)
const isRefreshingPayment = ref(false)
const isCancellingBooking = ref(false)
const pollingStatus = ref(false)

let pollingHandle: ReturnType<typeof setInterval> | null = null
let pollAttemptCount = 0
const maxPollAttempts = 60

const isPaymentComplete = computed(() => {
  const status = booking.value?.payment_status || ''
  return status === 'Paid' || status === 'Completed'
})

const isBookingClosed = computed(() => {
  const status = booking.value?.status || ''
  return status === 'Cancelled' || status === 'Completed'
})

const canCancelBooking = computed(() => {
  const status = booking.value?.status || ''
  return status === 'Pending' || status === 'Confirmed'
})

const canInitiatePayment = computed(() => {
  if (!booking.value || isBookingClosed.value || isPaymentComplete.value) {
    return false
  }
  return !isInitiatingPayment.value && !isRefreshingPayment.value
})

const paymentProgress = computed(() =>
  getMpesaProgressModel({
    paymentStatus: paymentState.value?.status || booking.value?.payment_status,
    ticketStatus: paymentState.value?.ticket_status,
    fallbackStatus: 'Pending',
    message: paymentState.value?.message,
  })
)

const hasPaymentFailure = computed(() => {
  const status = booking.value?.payment_status || ''
  return status === 'Failed' || status === 'Cancelled' || status === 'Timeout'
})

const paymentLabel = computed(() => {
  if (hasPaymentFailure.value) {
    return 'Retry Payment'
  }
  return 'Pay Now'
})

const latestAttempt = computed(() => {
  const history = paymentState.value?.attempt_history || []
  if (!history.length) {
    return null
  }
  return history[history.length - 1]
})

const formatDate = (date: string | undefined) => {
  if (!date) {
    return '—'
  }
  return new Date(date).toLocaleDateString('en-KE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(price)
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    Confirmed: 'bg-green-100 text-green-800 border-green-300',
    Pending: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    Cancelled: 'bg-red-100 text-red-800 border-red-300',
    Completed: 'bg-blue-100 text-blue-800 border-blue-300',
  }
  return colors[status] || 'bg-gray-100 text-gray-800 border-gray-300'
}

const getPaymentStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    Completed: 'text-green-700',
    Paid: 'text-green-700',
    Pending: 'text-yellow-700',
    'Prompt Sent': 'text-blue-700',
    'Callback Received': 'text-blue-700',
    Failed: 'text-red-700',
    Cancelled: 'text-red-700',
    Timeout: 'text-red-700',
  }
  return colors[status] || 'text-gray-700'
}

const clearPolling = () => {
  if (pollingHandle) {
    clearInterval(pollingHandle)
    pollingHandle = null
  }
  pollAttemptCount = 0
  pollingStatus.value = false
}

const shouldPoll = () => {
  const status = paymentState.value?.status || booking.value?.payment_status || ''
  return ['Pending', 'Prompt Sent', 'Callback Received'].includes(status)
}

const refreshPaymentStatus = async (silent = false) => {
  if (!booking.value) {
    return
  }

  if (!silent) {
    isRefreshingPayment.value = true
  }

  try {
    const payload = await apiService.getBookingPaymentStatus(booking.value.id)
    paymentState.value = payload.payment
    bookingsStore.selectedBooking = payload.booking

    if (isPaymentComplete.value) {
      clearPolling()
    }
  } catch (error: any) {
    if (!silent) {
      uiStore.showError(error?.message || 'Unable to refresh payment status')
    }
  } finally {
    if (!silent) {
      isRefreshingPayment.value = false
    }
  }
}

const startPolling = async () => {
  if (!shouldPoll()) {
    clearPolling()
    return
  }

  clearPolling()
  pollingStatus.value = true

  const poll = async () => {
    pollAttemptCount += 1
    await refreshPaymentStatus(true)

    if (!shouldPoll() || pollAttemptCount >= maxPollAttempts) {
      clearPolling()
    }
  }

  await poll()

  if (shouldPoll()) {
    pollingHandle = setInterval(() => {
      void poll()
    }, 3000)
  }
}

const loadBooking = async () => {
  const bookingId = route.params.id as string
  await bookingsStore.fetchBookingById(bookingId)

  if (!booking.value) {
    return
  }

  if (booking.value.mpesa_phone_number) {
    mpesaPhone.value = booking.value.mpesa_phone_number
  }

  await refreshPaymentStatus(true)
  if (shouldPoll()) {
    await startPolling()
  }
}

const handleInitiatePayment = async () => {
  if (!booking.value) {
    return
  }

  if (!mpesaPhone.value) {
    uiStore.showError('Enter your MPESA phone number to continue')
    return
  }

  const normalizedPhone = normalizeKenyanMpesaPhone(mpesaPhone.value)
  if (!isValidKenyanMpesaPhone(normalizedPhone)) {
    uiStore.showError('Use a valid MPESA number (2547XXXXXXXX)')
    return
  }

  isInitiatingPayment.value = true
  try {
    const payload = await apiService.initiateBookingPayment(booking.value.id, normalizedPhone)
    mpesaPhone.value = normalizedPhone
    bookingsStore.selectedBooking = payload.booking
    if (payload.payment) {
      paymentState.value = payload.payment
    }

    uiStore.showSuccess(payload.message || 'Payment prompt sent. Confirm on your phone.')
    await startPolling()
  } catch (error: any) {
    uiStore.showError(error?.message || 'Unable to initiate payment')
  } finally {
    isInitiatingPayment.value = false
  }
}

const handleCancelBooking = async () => {
  if (!booking.value) {
    return
  }

  const reason = window.prompt('Provide a short cancellation reason (optional):') || ''

  isCancellingBooking.value = true
  try {
    await bookingsStore.cancelBooking(booking.value.id, reason)
    await bookingsStore.fetchBookingById(booking.value.id)
    uiStore.showSuccess('Booking cancelled successfully')
    clearPolling()
  } catch (error: any) {
    uiStore.showError(error?.message || 'Unable to cancel booking')
  } finally {
    isCancellingBooking.value = false
  }
}

onMounted(() => {
  void loadBooking()
})

onUnmounted(() => {
  clearPolling()
})
</script>

<template>
  <div class="page-shell w-full min-h-screen">
    <div class="layout-shell-wide page-block-tight">
      <button @click="router.back()" class="soft-button-secondary px-5 py-3 mb-6">
        ← Back to Bookings
      </button>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="soft-spinner mb-4"></div>
        <p class="text-lg text-slate-600 font-medium mb-0">Loading booking details...</p>
      </div>

      <div v-else-if="booking" class="space-y-6">
        <section class="page-header rounded-[2rem] overflow-hidden text-white relative">
          <div class="absolute inset-0 hero-grid opacity-25"></div>
          <div class="relative z-10 p-6 sm:p-8 lg:p-10">
            <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-8">
              <div>
                <span class="soft-kicker mb-4">Booking confirmation</span>
                <h1 class="text-[clamp(2rem,4vw,3.2rem)] font-semibold leading-[1.02] tracking-[-0.04em] mb-3">Your trail reservation</h1>
                <p class="text-white/80 text-base sm:text-lg mb-0">This page reflects live backend booking and payment status.</p>
              </div>
              <div class="glass-panel rounded-[1.5rem] px-6 py-5 text-left min-w-[18rem]">
                <div class="text-xs uppercase tracking-[0.22em] text-white/60 mb-2">Confirmation code</div>
                <div class="text-3xl font-semibold text-white mb-3">{{ booking.confirmation_code }}</div>
                <div :class="['inline-flex px-3 py-1.5 rounded-full font-bold text-sm border backdrop-blur-sm', getStatusColor(booking.status)]">
                  {{ booking.status }}
                </div>
              </div>
            </div>
          </div>
        </section>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <section class="surface-card-lg">
            <h2 class="text-2xl font-semibold text-slate-900 mb-5">Booking Information</h2>
            <div class="space-y-4">
              <div class="surface-muted rounded-[1.25rem] p-4 flex justify-between items-center gap-4">
                <span class="text-sm text-slate-600 font-medium">Booking Date</span>
                <span class="text-sm font-bold text-slate-900">{{ formatDate(booking.booking_date) }}</span>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4 flex justify-between items-center gap-4">
                <span class="text-sm text-slate-600 font-medium">Trail</span>
                <span class="text-sm font-bold text-slate-900">{{ booking.trail_title || booking.trail_id }}</span>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4 flex justify-between items-center gap-4">
                <span class="text-sm text-slate-600 font-medium">Spots Booked</span>
                <span class="text-sm font-bold text-slate-900">{{ booking.spots_booked }}</span>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4 flex justify-between items-center gap-4">
                <span class="text-sm text-slate-600 font-medium">Status</span>
                <span :class="['px-3 py-1 rounded-full font-bold text-xs border', getStatusColor(booking.status)]">
                  {{ booking.status }}
                </span>
              </div>
            </div>
          </section>

          <section class="surface-card-lg">
            <h2 class="text-2xl font-semibold text-slate-900 mb-5">Payment Information</h2>
            <div class="space-y-4">
              <div class="surface-muted rounded-[1.25rem] p-4 flex justify-between items-center gap-4">
                <span class="text-sm text-slate-600 font-medium">Payment Status</span>
                <span :class="['font-bold text-sm', getPaymentStatusColor(booking.payment_status)]">
                  {{ booking.payment_status }}
                </span>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4 flex justify-between items-center gap-4">
                <span class="text-sm text-slate-600 font-medium">Total Amount</span>
                <span class="text-2xl font-semibold brand-text">{{ formatPrice(booking.total_price) }}</span>
              </div>
              <div v-if="booking.mpesa_receipt_number" class="surface-muted rounded-[1.25rem] p-4 flex justify-between items-center gap-4">
                <span class="text-sm text-slate-600 font-medium">Receipt</span>
                <span class="text-sm font-semibold text-slate-900">{{ booking.mpesa_receipt_number }}</span>
              </div>
              <div v-if="latestAttempt" class="surface-muted rounded-[1.25rem] p-4">
                <p class="text-xs uppercase tracking-[0.12em] text-slate-500 mb-2">Current attempt</p>
                <p class="text-sm font-medium text-slate-800 mb-1">Attempt #{{ latestAttempt.attempt_no }}</p>
                <p v-if="latestAttempt.checkout_request_id" class="text-xs text-slate-600 mb-0 break-all">Checkout ID: {{ latestAttempt.checkout_request_id }}</p>
              </div>
            </div>
          </section>
        </div>

        <section class="surface-card-lg space-y-5">
          <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
            <div>
              <h2 class="text-2xl font-semibold text-slate-900">MPESA Payment</h2>
              <p class="text-sm text-slate-600 mb-0">Initiate or retry payment from this booking only. Status is synced from backend callbacks.</p>
            </div>
            <div class="surface-muted rounded-[1.1rem] px-4 py-3 min-w-[14rem]">
              <p class="text-xs uppercase tracking-[0.12em] text-slate-500 mb-1">Progress</p>
              <p class="text-base font-semibold text-slate-900 mb-0">{{ paymentProgress.title }}</p>
            </div>
          </div>

          <div class="surface-muted rounded-[1.5rem] p-5 border border-slate-200/80">
            <p class="text-sm text-slate-700 mb-3">{{ paymentProgress.detail }}</p>
            <div class="w-full h-2 rounded-full bg-slate-200/80">
              <div class="h-2 rounded-full bg-[linear-gradient(135deg,var(--color-primary),#7a998d)] transition-all duration-500" :style="{ width: `${paymentProgress.progress}%` }"></div>
            </div>
            <p class="text-xs text-slate-500 mt-2 mb-0">{{ paymentProgress.progress }}% complete</p>
          </div>

          <div v-if="canInitiatePayment" class="grid grid-cols-1 lg:grid-cols-[1fr_auto_auto] gap-3">
            <input
              v-model="mpesaPhone"
              type="tel"
              placeholder="2547XXXXXXXX"
              class="soft-input"
            />
            <button
              class="brand-button px-6 py-3 disabled:opacity-60"
              :disabled="!canInitiatePayment"
              @click="handleInitiatePayment"
            >
              <span v-if="!isInitiatingPayment">{{ paymentLabel }}</span>
              <span v-else class="flex items-center gap-2">
                <span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                Processing
              </span>
            </button>
            <button
              class="soft-button-secondary px-6 py-3"
              :disabled="isRefreshingPayment"
              @click="refreshPaymentStatus()"
            >
              <span v-if="!isRefreshingPayment">Refresh Status</span>
              <span v-else>Refreshing...</span>
            </button>
          </div>

          <div v-else class="flex flex-wrap gap-3">
            <button class="soft-button-secondary px-6 py-3" :disabled="isRefreshingPayment" @click="refreshPaymentStatus()">
              <span v-if="!isRefreshingPayment">Refresh Status</span>
              <span v-else>Refreshing...</span>
            </button>
            <span v-if="isPaymentComplete" class="soft-badge soft-badge--neutral">Payment completed</span>
            <span v-else-if="isBookingClosed" class="soft-badge soft-badge--neutral">Booking is closed</span>
          </div>

          <p v-if="pollingStatus" class="text-xs text-blue-700 mb-0">Auto-refresh is active while payment is pending.</p>
        </section>

        <section class="surface-card-lg">
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              v-if="canCancelBooking"
              class="soft-button-secondary px-8 py-4 text-red-700 border-red-200 bg-red-50 hover:bg-red-100 disabled:opacity-60"
              :disabled="isCancellingBooking"
              @click="handleCancelBooking"
            >
              <span v-if="!isCancellingBooking">Cancel Booking</span>
              <span v-else>Cancelling...</span>
            </button>
            <button class="brand-button px-8 py-4" @click="router.push('/trails')">
              Book Another Trail
            </button>
          </div>
        </section>
      </div>

      <div v-else class="surface-card-lg text-center">
        <h3 class="text-3xl font-semibold text-slate-900 mb-3">Booking Not Found</h3>
        <p class="mb-7 text-base text-slate-600">We couldn't find the booking you're looking for.</p>
        <button @click="router.push('/bookings')" class="brand-button px-8 py-4">
          View All Bookings
        </button>
      </div>
    </div>
  </div>
</template>
