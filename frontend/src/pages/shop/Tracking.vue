<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { GlassAlert, GlassButton, GlassCard } from '../../components/glass'
import { useMerchandiseStore } from '../../stores/merchandiseStore'

const route = useRoute()
const router = useRouter()
const store = useMerchandiseStore()
const searchValue = ref(String(route.params.orderId || ''))

const order = computed(() => store.currentOrder)

const loadOrder = async (orderId: string) => {
  if (!orderId) {
    return
  }

  await store.fetchOrderById(orderId)
}

const trackOrder = async () => {
  if (!searchValue.value.trim()) {
    return
  }

  await router.replace(`/shop/tracking/${searchValue.value.trim()}`)
}

onMounted(() => {
  loadOrder(String(route.params.orderId || ''))
})

watch(
  () => route.params.orderId,
  (value) => {
    searchValue.value = String(value || '')
    loadOrder(searchValue.value)
  }
)
</script>

<template>
  <div class="layout-shell-narrow page-block">
    <div class="mb-8 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Tracking portal</p>
        <h1 class="page-title">Follow your merchandise order</h1>
      </div>

      <div class="flex w-full max-w-xl gap-2">
        <input
          v-model="searchValue"
          type="text"
          class="soft-input flex-1 rounded-[1.1rem] bg-white/80"
          placeholder="Enter order id or order number"
          @keyup.enter="trackOrder"
        />
        <GlassButton @click="trackOrder">Track</GlassButton>
      </div>
    </div>

    <template v-if="order">
      <div class="grid gap-8 lg:grid-cols-[1fr_0.92fr]">
        <GlassCard tone="strong">
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Order overview</p>
              <h2 class="mt-2 text-3xl font-semibold text-slate-950">{{ order.order_number }}</h2>
              <p class="mt-2 text-sm text-slate-500">Placed on {{ new Date(order.created_at).toLocaleString() }}</p>
            </div>
            <div class="rounded-[1.2rem] bg-slate-950 px-4 py-3 text-white">
              <p class="text-xs uppercase tracking-[0.18em] text-white/55">Total</p>
              <p class="mt-2 text-2xl font-semibold">KES {{ order.total_amount.toLocaleString() }}</p>
            </div>
          </div>

          <div class="mt-8 grid gap-4 sm:grid-cols-3">
            <div class="rounded-[1.15rem] bg-white/80 px-4 py-4">
              <p class="text-xs uppercase tracking-[0.18em] text-slate-500">Payment</p>
              <p class="mt-2 text-lg font-semibold text-slate-950">{{ order.payment_status }}</p>
            </div>
            <div class="rounded-[1.15rem] bg-white/80 px-4 py-4">
              <p class="text-xs uppercase tracking-[0.18em] text-slate-500">Fulfillment</p>
              <p class="mt-2 text-lg font-semibold text-slate-950">{{ order.fulfillment_status }}</p>
            </div>
            <div class="rounded-[1.15rem] bg-white/80 px-4 py-4">
              <p class="text-xs uppercase tracking-[0.18em] text-slate-500">Destination</p>
              <p class="mt-2 text-lg font-semibold text-slate-950">{{ order.delivery_city }}</p>
            </div>
          </div>

          <div class="mt-8 space-y-4">
            <article
              v-for="event in order.timeline"
              :key="`${event.label}-${event.happened_at}`"
              class="rounded-[1.2rem] bg-white/80 px-5 py-4"
            >
              <div class="flex items-start justify-between gap-4">
                <div>
                  <h3 class="font-semibold text-slate-950">{{ event.label }}</h3>
                  <p class="mt-2 text-sm leading-6 text-slate-600">{{ event.detail }}</p>
                </div>
                <span class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                  {{ new Date(event.happened_at).toLocaleDateString() }}
                </span>
              </div>
            </article>
          </div>
        </GlassCard>

        <div class="space-y-5">
          <GlassCard tone="strong">
            <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Items</p>
            <div class="mt-4 space-y-4">
              <div
                v-for="line in order.items"
                :key="`${line.item_code}-${line.selected_color}-${line.selected_size}`"
                class="rounded-[1.1rem] bg-white/80 px-4 py-4"
              >
                <div class="flex items-center justify-between gap-4">
                  <div>
                    <p class="font-semibold text-slate-950">{{ line.item_name }}</p>
                    <p class="text-sm text-slate-500">
                      Qty {{ line.quantity }}
                      <span v-if="line.selected_color"> / {{ line.selected_color }}</span>
                      <span v-if="line.selected_size"> / {{ line.selected_size }}</span>
                    </p>
                  </div>
                  <span class="text-sm font-semibold text-slate-950">KES {{ line.line_total.toLocaleString() }}</span>
                </div>
              </div>
            </div>
          </GlassCard>

          <GlassCard tone="strong">
            <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Need another order?</p>
            <p class="mt-3 text-sm leading-6 text-slate-600">
              This view supports both the local mock orders used during development and the Frappe-backed order
              records once the shop DocTypes are migrated.
            </p>
            <div class="mt-5 flex flex-wrap gap-3">
              <GlassButton variant="secondary" @click="router.push('/shop')">Back to catalog</GlassButton>
              <GlassButton variant="ghost" @click="router.push('/shop/cart')">Open cart</GlassButton>
            </div>
          </GlassCard>
        </div>
      </div>
    </template>

    <GlassAlert v-else tone="info" title="No order loaded">
      Enter an order id or order number to load the latest status.
    </GlassAlert>
  </div>
</template>
