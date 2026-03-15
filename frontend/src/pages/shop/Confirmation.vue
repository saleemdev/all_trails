<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { GlassAlert, GlassButton, GlassCard } from '../../components/glass'
import { useMerchandiseStore } from '../../stores/merchandiseStore'

const route = useRoute()
const router = useRouter()
const store = useMerchandiseStore()

const orderId = String(route.params.orderId || '')
const order = computed(() => store.currentOrder)

onMounted(async () => {
  if (!store.currentOrder || store.currentOrder.id !== orderId) {
    await store.fetchOrderById(orderId)
  }
})
</script>

<template>
  <div class="layout-shell page-block">
    <template v-if="order">
      <GlassCard tone="hero">
        <p class="text-xs font-semibold uppercase tracking-[0.22em] text-white/55">Order confirmed</p>
        <h1 class="mt-3 text-[clamp(2.2rem,5vw,3.8rem)] font-semibold leading-[0.98] tracking-[-0.04em] text-white">Thanks, {{ order.customer_name.split(' ')[0] || 'Explorer' }}.</h1>
        <p class="mt-4 max-w-2xl text-base leading-8 text-white/76">
          Order <span class="font-semibold text-white">{{ order.order_number }}</span> is now in the system. We will
          keep the order timeline updated as payment clears and fulfillment advances.
        </p>
        <div class="mt-8 grid gap-4 sm:grid-cols-3">
          <div class="rounded-[1.2rem] bg-white/10 px-5 py-5">
            <p class="text-xs uppercase tracking-[0.18em] text-white/55">Payment</p>
            <p class="mt-3 text-2xl font-semibold">{{ order.payment_status }}</p>
          </div>
          <div class="rounded-[1.2rem] bg-white/10 px-5 py-5">
            <p class="text-xs uppercase tracking-[0.18em] text-white/55">Fulfillment</p>
            <p class="mt-3 text-2xl font-semibold">{{ order.fulfillment_status }}</p>
          </div>
          <div class="rounded-[1.2rem] bg-white/10 px-5 py-5">
            <p class="text-xs uppercase tracking-[0.18em] text-white/55">Total</p>
            <p class="mt-3 text-2xl font-semibold">KES {{ order.total_amount.toLocaleString() }}</p>
          </div>
        </div>
      </GlassCard>

      <div class="mt-6 grid gap-6 lg:mt-8 lg:grid-cols-[1fr_0.95fr] lg:gap-8">
        <GlassCard tone="strong">
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">What happens next</p>
          <div class="mt-5 space-y-4">
            <article
              v-for="event in order.timeline"
              :key="`${event.label}-${event.happened_at}`"
              class="rounded-[1.2rem] bg-white/80 px-5 py-4"
            >
              <div class="flex items-start justify-between gap-4">
                <div>
                  <h2 class="font-semibold text-slate-950">{{ event.label }}</h2>
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
            <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Delivery destination</p>
            <h2 class="mt-3 text-2xl font-semibold text-slate-950">{{ order.delivery_city }}</h2>
            <p class="mt-3 text-sm leading-6 text-slate-600">
              {{ order.delivery_address }}
            </p>
            <p v-if="order.delivery_notes" class="mt-3 text-sm leading-6 text-slate-500">
              {{ order.delivery_notes }}
            </p>
            <div class="mt-4 rounded-[1.2rem] bg-slate-950 px-4 py-3 text-sm text-white">
              Estimated window: {{ order.estimated_delivery_window }}
            </div>
          </GlassCard>

          <GlassCard tone="strong">
            <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Items in this order</p>
            <div class="mt-4 space-y-4">
              <div
                v-for="line in order.items"
                :key="`${line.item_code}-${line.selected_color}-${line.selected_size}`"
                class="flex items-center justify-between gap-4 rounded-[1.1rem] bg-white/80 px-4 py-3"
              >
                <div>
                  <p class="font-semibold text-slate-950">{{ line.item_name }}</p>
                  <p class="text-sm text-slate-500">Qty {{ line.quantity }}</p>
                </div>
                <span class="text-sm font-semibold text-slate-900">KES {{ line.line_total.toLocaleString() }}</span>
              </div>
            </div>
          </GlassCard>

          <div class="flex flex-wrap gap-3">
            <GlassButton @click="router.push(`/shop/tracking/${order.id}`)">Track order</GlassButton>
            <GlassButton variant="secondary" @click="router.push('/shop')">Back to shop</GlassButton>
          </div>
        </div>
      </div>
    </template>

    <GlassAlert v-else tone="error" title="Order unavailable">
      We could not load that order confirmation. Open the tracking page and search by order number if needed.
    </GlassAlert>
  </div>
</template>
