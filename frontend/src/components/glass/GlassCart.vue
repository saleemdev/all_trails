<script setup lang="ts">
import { ref } from 'vue'
import GlassButton from './GlassButton.vue'
import GlassCard from './GlassCard.vue'
import type { CartLineItem, CouponValidationResult } from '../../types/shop'

const props = withDefaults(
  defineProps<{
    items: CartLineItem[]
    subtotal: number
    shipping: number
    discount: number
    total: number
    coupon?: CouponValidationResult | null
    compact?: boolean
  }>(),
  {
    coupon: null,
    compact: false,
  }
)

const emit = defineEmits<{
  increment: [lineId: string]
  decrement: [lineId: string]
  remove: [lineId: string]
  'apply-coupon': [code: string]
  'clear-coupon': []
}>()

const couponCode = ref('')
</script>

<template>
  <GlassCard tone="strong" :padded="!props.compact">
    <div :class="props.compact ? 'space-y-3 px-3 py-3 sm:px-3.5' : 'space-y-4'">
      <div class="flex items-start justify-between gap-3">
        <div>
          <h3 :class="props.compact ? 'text-[1.12rem] font-medium leading-tight tone-heading' : 'text-[1.55rem] font-medium tone-heading'">Cart summary</h3>
          <p :class="props.compact ? 'text-[12px] tone-muted' : 'text-[13px] tone-muted'">{{ props.items.length }} line items reserved</p>
        </div>
        <span
          :class="[
            'surface-active rounded-full text-[color:var(--color-primary-dark)]',
            props.compact
              ? 'px-2.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.12em]'
              : 'px-3 py-1 text-xs font-medium uppercase tracking-[0.18em]',
          ]"
        >
          Ready to ship
        </span>
      </div>

      <div v-if="props.items.length" :class="props.compact ? 'space-y-3' : 'space-y-4'">
        <article
          v-for="line in props.items"
          :key="line.line_id"
          :class="[
            'surface-control flex items-start',
            props.compact ? 'gap-2.5 rounded-[0.9rem] p-2.5' : 'gap-4 rounded-[1.15rem] p-3 sm:p-4',
          ]"
        >
          <img
            :src="line.product.image_url"
            :alt="line.product.item_name"
            :class="props.compact ? 'h-12 w-12 rounded-lg object-cover' : 'h-20 w-20 rounded-xl object-cover'"
          />
          <div class="min-w-0 flex-1">
            <div class="flex items-start justify-between gap-2">
              <div>
                <h4 :class="props.compact ? 'text-[13px] font-medium leading-4 tone-heading [display:-webkit-box] [-webkit-box-orient:vertical] [-webkit-line-clamp:2] overflow-hidden' : 'text-[15px] font-medium tone-heading'">
                  {{ line.product.item_name }}
                </h4>
                <p :class="props.compact ? 'mt-0.5 text-[11px] leading-4 tone-muted' : 'text-[13px] tone-muted'">
                  {{ line.selected_color || 'Standard finish' }}
                  <span v-if="line.selected_size"> / {{ line.selected_size }}</span>
                </p>
              </div>
              <button :class="props.compact ? 'text-[11px] font-medium tone-muted hover:text-red-600' : 'text-[13px] font-medium tone-muted hover:text-red-600'" @click="emit('remove', line.line_id)">
                Remove
              </button>
            </div>

            <div :class="props.compact ? 'mt-2 flex items-center justify-between gap-2' : 'mt-3 flex items-center justify-between gap-3'">
              <div :class="props.compact ? 'inline-flex items-center rounded-full border border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)] p-0.5' : 'inline-flex items-center rounded-full border border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)] p-1'">
                <button :class="props.compact ? 'h-6 w-6 rounded-full text-[13px] tone-body hover:bg-[color:var(--color-surface-muted)]' : 'h-8 w-8 rounded-full tone-body hover:bg-[color:var(--color-surface-muted)]'" @click="emit('decrement', line.line_id)">
                  -
                </button>
                <span :class="props.compact ? 'w-7 text-center text-[12px] font-medium tone-heading' : 'w-10 text-center text-sm font-medium tone-heading'">{{ line.quantity }}</span>
                <button :class="props.compact ? 'h-6 w-6 rounded-full text-[13px] tone-body hover:bg-[color:var(--color-surface-muted)]' : 'h-8 w-8 rounded-full tone-body hover:bg-[color:var(--color-surface-muted)]'" @click="emit('increment', line.line_id)">
                  +
                </button>
              </div>

              <span :class="props.compact ? 'text-[14px] font-medium tone-heading' : 'text-base font-medium tone-heading'">
                KES {{ ((line.product.discount_price ?? line.product.selling_price) * line.quantity).toLocaleString() }}
              </span>
            </div>
          </div>
        </article>
      </div>

      <div v-else :class="props.compact ? 'rounded-[0.95rem] border border-dashed border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)] px-4 py-5 text-center text-[13px] tone-body' : 'rounded-[1.1rem] border border-dashed border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)] px-5 py-7 text-center text-sm tone-body'">
        Your cart is empty. Add a few trail-tested pieces and come back here to check out.
      </div>

      <div :class="props.compact ? 'surface-control rounded-[0.9rem] p-3' : 'surface-control rounded-[1.15rem] p-4'">
        <div :class="props.compact ? 'mb-2 flex items-center justify-between' : 'mb-3 flex items-center justify-between'">
          <p :class="props.compact ? 'text-[11px] font-medium uppercase tracking-[0.14em] tone-muted' : 'text-sm font-medium uppercase tracking-[0.18em] tone-muted'">Coupon</p>
          <button
            v-if="props.coupon?.valid"
            :class="props.compact ? 'text-[10px] font-medium uppercase tracking-[0.12em] tone-muted hover:text-[color:var(--color-text-primary)]' : 'text-xs font-medium uppercase tracking-[0.18em] tone-muted hover:text-[color:var(--color-text-primary)]'"
            @click="emit('clear-coupon')"
          >
            Remove
          </button>
        </div>

        <div v-if="props.coupon?.valid" :class="props.compact ? 'surface-active rounded-[0.85rem] px-3 py-2.5 text-[13px] text-[color:var(--color-primary-dark)]' : 'surface-active rounded-2xl px-4 py-3 text-sm text-[color:var(--color-primary-dark)]'">
          <p :class="props.compact ? 'font-medium' : 'font-semibold'">{{ props.coupon.code }}</p>
          <p>{{ props.coupon.description }}</p>
        </div>

        <div v-else class="flex gap-2">
          <input v-model="couponCode" type="text" :class="props.compact ? 'soft-input h-9 flex-1 rounded-[0.8rem]' : 'soft-input flex-1 rounded-2xl'" placeholder="Enter code" />
          <GlassButton size="sm" variant="secondary" @click="emit('apply-coupon', couponCode)">
            Apply
          </GlassButton>
        </div>
      </div>

      <div :class="props.compact ? 'cart-total-panel space-y-2 rounded-[0.95rem] px-3.5 py-3.5' : 'cart-total-panel space-y-3 rounded-[1.2rem] px-5 py-5'">
        <div :class="props.compact ? 'cart-total-muted flex items-center justify-between text-[13px]' : 'cart-total-muted flex items-center justify-between text-sm'">
          <span>Subtotal</span>
          <span>KES {{ props.subtotal.toLocaleString() }}</span>
        </div>
        <div :class="props.compact ? 'cart-total-muted flex items-center justify-between text-[13px]' : 'cart-total-muted flex items-center justify-between text-sm'">
          <span>Shipping</span>
          <span>{{ props.shipping === 0 ? 'Free' : `KES ${props.shipping.toLocaleString()}` }}</span>
        </div>
        <div :class="props.compact ? 'cart-total-accent flex items-center justify-between text-[13px]' : 'cart-total-accent flex items-center justify-between text-sm'">
          <span>Discount</span>
          <span>- KES {{ props.discount.toLocaleString() }}</span>
        </div>
        <div :class="props.compact ? 'flex items-center justify-between border-t border-[color:var(--color-summary-border)] pt-2.5' : 'flex items-center justify-between border-t border-[color:var(--color-summary-border)] pt-3'">
          <span :class="props.compact ? 'cart-total-muted text-[11px] uppercase tracking-[0.12em]' : 'cart-total-muted text-sm uppercase tracking-[0.18em]'">Total</span>
          <span :class="props.compact ? 'text-xl font-medium' : 'text-[1.45rem] font-medium'">KES {{ props.total.toLocaleString() }}</span>
        </div>
      </div>
    </div>
  </GlassCard>
</template>
