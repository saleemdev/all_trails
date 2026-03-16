<script setup lang="ts">
import GlassButton from './GlassButton.vue'
import GlassCard from './GlassCard.vue'
import type { MerchandiseItem } from '../../types/shop'

const props = defineProps<{
  item: MerchandiseItem
}>()

const emit = defineEmits<{
  'add-to-cart': [item: MerchandiseItem]
}>()

const publicPrice = (props.item.discount_price ?? props.item.selling_price).toLocaleString()
</script>

<template>
  <GlassCard hoverable class="group h-full">
    <div class="flex h-full flex-col gap-3">
      <RouterLink :to="`/shop/${props.item.item_code}`" class="relative overflow-hidden rounded-[1rem]">
        <img
          :src="props.item.image_url"
          :alt="props.item.item_name"
          class="h-32 w-full object-cover transition-transform duration-500 group-hover:scale-[1.03] sm:h-36"
        />
        <div class="absolute left-2.5 top-2.5 flex flex-wrap gap-1.5">
          <span
            v-for="badge in props.item.badges.slice(0, 2)"
            :key="badge"
            class="rounded-full bg-slate-950/60 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.14em] text-white backdrop-blur-md"
          >
            {{ badge }}
          </span>
        </div>
      </RouterLink>

      <div class="flex flex-1 flex-col gap-2">
        <div class="space-y-1.5">
          <div class="flex items-center justify-between gap-4">
            <span class="text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-500">
              {{ props.item.category_name }}
            </span>
            <span class="text-[10px] text-slate-500">{{ props.item.review_count }} reviews</span>
          </div>

          <RouterLink :to="`/shop/${props.item.item_code}`" class="block">
            <h3 class="trail-card-title text-[0.96rem] font-semibold leading-5 text-slate-950 sm:text-[1rem]">
              {{ props.item.item_name }}
            </h3>
          </RouterLink>

          <p class="text-[13px] leading-5 text-slate-600 [display:-webkit-box] [-webkit-box-orient:vertical] [-webkit-line-clamp:2] overflow-hidden">
            {{ props.item.short_description }}
          </p>
        </div>

        <ul class="space-y-1 text-[12px] text-slate-700">
          <li v-for="highlight in props.item.highlights.slice(0, 1)" :key="highlight" class="flex items-start gap-1.5">
            <span class="mt-[0.3rem] h-2 w-2 rounded-full bg-[color:var(--color-primary-light)]" aria-hidden="true" />
            <span>{{ highlight }}</span>
          </li>
        </ul>

        <div class="mt-auto flex items-end justify-between gap-3">
          <div>
            <p class="text-[10px] uppercase tracking-[0.16em] text-slate-500">From</p>
            <div class="flex items-center gap-1.5">
            <span class="text-[1rem] font-semibold text-slate-950">KES {{ publicPrice }}</span>
              <span
                v-if="props.item.discount_price"
                class="text-[11px] text-slate-400 line-through"
              >
                KES {{ props.item.selling_price.toLocaleString() }}
              </span>
            </div>
          </div>

          <GlassButton size="sm" @click="emit('add-to-cart', props.item)">
            Add
          </GlassButton>
        </div>
      </div>
    </div>
  </GlassCard>
</template>
