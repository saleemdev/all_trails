<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMerchandiseStore } from '../../stores/merchandiseStore'
import {
  GlassAlert,
  GlassButton,
  GlassCard,
  GlassCart,
  GlassProductCard,
} from '../../components/glass'

const router = useRouter()
const store = useMerchandiseStore()

const recommendations = computed(() => store.featuredItems.slice(0, 3))

const applyCoupon = async (code: string) => {
  if (!code.trim()) {
    return
  }

  await store.applyCoupon(code)
}

onMounted(async () => {
  if (!store.featuredItems.length) {
    await store.fetchCatalog()
  }
})
</script>

<template>
  <div class="dense-ui layout-shell-wide page-block">
    <div class="mb-4 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="page-kicker">Your basket</p>
        <h1 class="page-title">Cart and checkout prep</h1>
      </div>
      <GlassButton size="sm" variant="secondary" @click="router.push('/shop')">Continue shopping</GlassButton>
    </div>

    <div v-if="store.error" class="mb-4">
      <GlassAlert tone="warning" title="Cart note">
        {{ store.error }}
      </GlassAlert>
    </div>

    <div class="grid gap-4 lg:grid-cols-[minmax(0,1.18fr)_minmax(18.5rem,0.82fr)]">
      <div>
        <GlassCart
          :items="store.cart"
          :subtotal="store.subtotal"
          :shipping="store.shipping"
          :discount="store.discount"
          :total="store.total"
          :coupon="store.activeCoupon"
          compact
          @increment="store.updateQuantity($event, (store.cart.find((line) => line.line_id === $event)?.quantity || 0) + 1)"
          @decrement="store.updateQuantity($event, (store.cart.find((line) => line.line_id === $event)?.quantity || 0) - 1)"
          @remove="store.removeFromCart"
          @apply-coupon="applyCoupon"
          @clear-coupon="store.removeCoupon"
        />
      </div>

      <div class="space-y-3.5 lg:sticky lg:top-24 lg:self-start">
        <GlassCard tone="strong">
          <p class="tone-kicker">Why this flow works</p>
          <h2 class="mt-2 text-[1.25rem] font-medium tone-heading">Fast checkout, flexible payment</h2>
          <ul class="mt-3 space-y-2 text-[13px] leading-5 tone-body">
            <li>Standard delivery is free above KES 15,000.</li>
            <li>BNPL splits eligible baskets into two equal payments with no interest.</li>
            <li>Orders move to confirmation immediately after payment success or manual verification.</li>
          </ul>
          <div class="mt-3.5 space-y-2">
            <GlassButton block :disabled="!store.cart.length" @click="router.push('/shop/checkout')">
              Proceed to checkout
            </GlassButton>
            <GlassButton block variant="ghost" :disabled="!store.cart.length" @click="store.clearCart()">
              Clear cart
            </GlassButton>
          </div>
        </GlassCard>

        <GlassCard v-if="store.bnplAvailable" tone="strong">
          <p class="tone-kicker">BNPL unlocked</p>
          <h3 class="mt-2 text-[1.2rem] font-medium tone-heading">Split this order into two payments.</h3>
          <p class="mt-2 text-[13px] leading-5 tone-body">
            Pay half now and the balance in 30 days. The checkout flow will calculate the deposit automatically once
            BNPL is selected.
          </p>
        </GlassCard>
      </div>
    </div>

    <section v-if="recommendations.length" class="mt-9 sm:mt-10">
      <div class="mb-4 flex items-end justify-between gap-4">
        <div>
          <p class="tone-kicker">Keep building the kit</p>
          <h2 class="app-section-title">Recommended add-ons</h2>
        </div>
      </div>

      <div class="grid gap-3.5 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
        <GlassProductCard
          v-for="item in recommendations"
          :key="item.item_code"
          :item="item"
          @add-to-cart="store.addToCart($event, 1, { selected_color: $event.available_colors[0], selected_size: $event.available_sizes[0] })"
        />
      </div>
    </section>
  </div>
</template>
