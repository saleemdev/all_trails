<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useMerchandiseStore } from '../../stores/merchandiseStore'
import {
  GlassAlert,
  GlassButton,
  GlassCard,
  GlassCheckoutFlow,
  GlassInput,
} from '../../components/glass'
import type { CheckoutStep } from '../../types/shop'

const router = useRouter()
const store = useMerchandiseStore()

const steps: CheckoutStep[] = [
  {
    id: 'delivery',
    title: 'Delivery',
    description: 'Customer identity, phone, and where the package should land.',
  },
  {
    id: 'payment',
    title: 'Payment',
    description: 'Choose between MPESA, BNPL, or cash-on-delivery verification.',
  },
  {
    id: 'review',
    title: 'Review',
    description: 'Confirm basket, address, and payment instructions before final submit.',
  },
]

const currentStep = ref<CheckoutStep['id']>('delivery')

const stepIndex = computed(() => steps.findIndex((step) => step.id === currentStep.value))
const isDeliveryValid = computed(
  () =>
    !!store.checkoutDraft.customer_name &&
    !!store.checkoutDraft.customer_email &&
    !!store.checkoutDraft.customer_phone &&
    !!store.checkoutDraft.delivery_address &&
    !!store.checkoutDraft.delivery_city
)
const isPaymentValid = computed(() => {
  if (store.checkoutDraft.payment_method === 'Cash on Delivery') {
    return true
  }

  return !!store.checkoutDraft.mpesa_phone_number
})

const nextStep = () => {
  if (currentStep.value === 'delivery' && !isDeliveryValid.value) {
    return
  }

  if (currentStep.value === 'payment' && !isPaymentValid.value) {
    return
  }

  const next = steps[stepIndex.value + 1]
  if (next) {
    currentStep.value = next.id
  }
}

const previousStep = () => {
  const previous = steps[stepIndex.value - 1]
  if (previous) {
    currentStep.value = previous.id
  }
}

const selectPaymentMethod = (value: typeof store.checkoutDraft.payment_method) => {
  store.checkoutDraft.payment_method = value
}

const placeOrder = async () => {
  const order = await store.submitOrder()
  if (!order) {
    return
  }

  if (order.payment_method === 'Cash on Delivery') {
    router.push(`/shop/confirmation/${order.id}`)
    return
  }

  router.push(`/shop/payment/${order.id}`)
}

onMounted(() => {
  if (!store.cart.length) {
    return
  }

  if (!store.checkoutDraft.mpesa_phone_number) {
    store.checkoutDraft.mpesa_phone_number = store.checkoutDraft.customer_phone
  }

  if (store.checkoutDraft.payment_method === 'BNPL' && !store.bnplAvailable) {
    store.checkoutDraft.payment_method = 'MPESA'
  }
})

watch(
  () => store.checkoutDraft.customer_phone,
  (value) => {
    if (!store.checkoutDraft.mpesa_phone_number) {
      store.checkoutDraft.mpesa_phone_number = value
    }
  }
)
</script>

<template>
  <div class="dense-ui layout-shell-wide page-block">
    <div class="mb-4">
      <p class="page-kicker">Checkout flow</p>
      <h1 class="page-title">Complete your merchandise order</h1>
    </div>

    <GlassAlert v-if="!store.cart.length" tone="warning" title="Cart required">
      You need at least one item in the cart before checkout. Return to the catalog to continue.
      <div class="mt-4">
        <GlassButton @click="router.push('/shop')">Go back to the shop</GlassButton>
      </div>
    </GlassAlert>

    <template v-else>
      <GlassCheckoutFlow :steps="steps" :current-step="currentStep" />

      <div v-if="store.error" class="mt-4">
        <GlassAlert tone="error" title="Checkout issue">
          {{ store.error }}
        </GlassAlert>
      </div>

      <div class="mt-4 grid gap-3.5 lg:mt-5 lg:grid-cols-[minmax(0,1.12fr)_minmax(18rem,0.88fr)] lg:gap-4">
        <GlassCard tone="strong">
          <template v-if="currentStep === 'delivery'">
            <p class="tone-kicker">Step 1</p>
            <h2 class="app-section-title">Delivery and contact</h2>
            <div class="mt-3.5 grid gap-2.5 md:grid-cols-2">
              <GlassInput v-model="store.checkoutDraft.customer_name" label="Customer name" placeholder="Jane Wambui" required />
              <GlassInput v-model="store.checkoutDraft.customer_email" label="Email address" type="email" placeholder="jane@example.com" required />
              <GlassInput v-model="store.checkoutDraft.customer_phone" label="Primary phone" placeholder="2547XXXXXXXX" required />
              <GlassInput v-model="store.checkoutDraft.delivery_city" label="City" placeholder="Nairobi" required />
            </div>
            <div class="mt-2.5">
              <GlassInput
                v-model="store.checkoutDraft.delivery_address"
                label="Delivery address"
                placeholder="Apartment, estate, street, landmark"
                required
              />
            </div>
            <div class="mt-2.5">
              <GlassInput
                v-model="store.checkoutDraft.delivery_notes"
                label="Delivery notes"
                textarea
                help="Gate code, best time to call, or any route note the rider should know."
              />
            </div>
          </template>

          <template v-else-if="currentStep === 'payment'">
            <p class="tone-kicker">Step 2</p>
            <h2 class="app-section-title">Payment method</h2>
            <div class="mt-3.5 grid gap-2.5">
              <button
                class="rounded-[0.9rem] border px-3.5 py-3 text-left transition-all"
                :class="store.checkoutDraft.payment_method === 'MPESA' ? 'border-[color:var(--color-border-strong)] bg-[color:var(--color-surface-overlay)]' : 'border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)]'"
                @click="selectPaymentMethod('MPESA')"
              >
                <p class="text-[15px] font-medium tone-heading">MPESA</p>
                <p class="mt-1 text-[13px] leading-5 tone-body">Send an STK prompt to the selected phone and confirm instantly.</p>
              </button>

              <button
                class="rounded-[0.9rem] border px-3.5 py-3 text-left transition-all"
                :class="store.checkoutDraft.payment_method === 'BNPL' ? 'border-[color:var(--color-border-strong)] bg-[color:var(--color-surface-overlay)]' : 'border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)]'"
                :disabled="!store.bnplAvailable"
                @click="selectPaymentMethod('BNPL')"
              >
                <p class="text-[15px] font-medium tone-heading">BNPL</p>
                <p class="mt-1 text-[13px] leading-5 tone-body">
                  Split the order into 2 equal payments. Available only for eligible baskets above the BNPL threshold.
                </p>
                <p class="mt-2 text-[11px] font-medium uppercase tracking-[0.13em]" :class="store.bnplAvailable ? 'text-[color:var(--color-primary)]' : 'text-slate-400'">
                  {{ store.bnplAvailable ? 'Available for this basket' : 'Not available for this basket' }}
                </p>
              </button>

              <button
                class="rounded-[0.9rem] border px-3.5 py-3 text-left transition-all"
                :class="store.checkoutDraft.payment_method === 'Cash on Delivery' ? 'border-[color:var(--color-border-strong)] bg-[color:var(--color-surface-overlay)]' : 'border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)]'"
                @click="selectPaymentMethod('Cash on Delivery')"
              >
                <p class="text-[15px] font-medium tone-heading">Cash on Delivery</p>
                <p class="mt-1 text-[13px] leading-5 tone-body">Reserve stock now and complete payment after manual team confirmation.</p>
              </button>
            </div>

            <div v-if="store.checkoutDraft.payment_method !== 'Cash on Delivery'" class="mt-3.5">
              <GlassInput
                v-model="store.checkoutDraft.mpesa_phone_number"
                label="Payment phone number"
                placeholder="2547XXXXXXXX"
                help="Use the Safaricom line that should receive the STK prompt."
                required
              />
            </div>
          </template>

          <template v-else>
            <p class="tone-kicker">Step 3</p>
            <h2 class="app-section-title">Review order</h2>

            <div class="mt-3.5 space-y-2.5">
              <div class="surface-control rounded-[0.9rem] p-3.5">
                <p class="tone-kicker">Delivery</p>
                <p class="mt-1.5 text-[15px] font-medium tone-heading">{{ store.checkoutDraft.customer_name }}</p>
                <p class="text-sm tone-body">{{ store.checkoutDraft.customer_email }}</p>
                <p class="text-sm tone-body">{{ store.checkoutDraft.customer_phone }}</p>
                <p class="mt-2 text-[13px] leading-5 tone-body">
                  {{ store.checkoutDraft.delivery_address }}, {{ store.checkoutDraft.delivery_city }}
                </p>
              </div>

              <div class="surface-control rounded-[0.9rem] p-3.5">
                <p class="tone-kicker">Payment</p>
                <p class="mt-1.5 text-[15px] font-medium tone-heading">{{ store.checkoutDraft.payment_method }}</p>
                <p class="text-[13px] tone-body">
                  {{ store.checkoutDraft.payment_method === 'Cash on Delivery' ? 'Team verification before dispatch' : store.checkoutDraft.mpesa_phone_number }}
                </p>
              </div>

              <GlassAlert tone="info" title="Before you submit">
                Standard fulfillment begins as soon as payment clears. BNPL orders confirm after the deposit lands and
                the second installment is scheduled automatically.
              </GlassAlert>
            </div>
          </template>

          <div class="mt-4 flex flex-wrap gap-2">
            <GlassButton variant="ghost" :disabled="stepIndex === 0" @click="previousStep">Back</GlassButton>
            <GlassButton
              v-if="currentStep !== 'review'"
              :disabled="(currentStep === 'delivery' && !isDeliveryValid) || (currentStep === 'payment' && !isPaymentValid)"
              @click="nextStep"
            >
              Continue
            </GlassButton>
            <GlassButton v-else :loading="store.isSubmitting" @click="placeOrder">Place order</GlassButton>
          </div>
        </GlassCard>

        <GlassCard tone="strong" class="lg:sticky lg:top-24 lg:self-start">
          <p class="tone-kicker">Order snapshot</p>
          <div class="mt-3.5 space-y-2.5">
            <article
              v-for="line in store.cart"
              :key="line.line_id"
              class="surface-control flex items-center gap-2 rounded-[0.9rem] px-2.5 py-2"
            >
              <img :src="line.product.image_url" :alt="line.product.item_name" class="h-10 w-10 rounded-md object-cover" />
              <div class="min-w-0 flex-1">
                <p class="text-[13px] font-medium leading-4 tone-heading [display:-webkit-box] [-webkit-box-orient:vertical] [-webkit-line-clamp:2] overflow-hidden">
                  {{ line.product.item_name }}
                </p>
                <p class="text-[12px] tone-muted">Qty {{ line.quantity }}</p>
              </div>
              <span class="text-[12px] font-medium tone-heading">
                KES {{ ((line.product.discount_price ?? line.product.selling_price) * line.quantity).toLocaleString() }}
              </span>
            </article>
          </div>

          <div class="cart-total-panel mt-3.5 space-y-2 rounded-[0.9rem] px-3.5 py-3.5">
            <div class="cart-total-muted flex items-center justify-between text-sm">
              <span>Subtotal</span>
              <span>KES {{ store.subtotal.toLocaleString() }}</span>
            </div>
            <div class="cart-total-muted flex items-center justify-between text-sm">
              <span>Shipping</span>
              <span>{{ store.shipping === 0 ? 'Free' : `KES ${store.shipping.toLocaleString()}` }}</span>
            </div>
            <div class="cart-total-accent flex items-center justify-between text-sm">
              <span>Discount</span>
              <span>- KES {{ store.discount.toLocaleString() }}</span>
            </div>
            <div class="flex items-center justify-between border-t border-[color:var(--color-summary-border)] pt-2">
              <span class="cart-total-muted text-[11px] font-medium uppercase tracking-[0.12em]">Total</span>
              <span class="text-lg font-medium">KES {{ store.total.toLocaleString() }}</span>
            </div>
          </div>

          <div v-if="store.checkoutDraft.payment_method === 'BNPL' && store.bnplAvailable" class="surface-active mt-3.5 rounded-[0.9rem] px-3.5 py-2.5 text-[13px] text-[color:var(--color-primary-dark)]">
            Pay KES {{ Math.round(store.total / 2).toLocaleString() }} now, then the remaining
            KES {{ (store.total - Math.round(store.total / 2)).toLocaleString() }} in 30 days.
          </div>
        </GlassCard>
      </div>
    </template>
  </div>
</template>
