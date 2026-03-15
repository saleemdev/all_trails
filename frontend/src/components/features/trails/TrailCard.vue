<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Trail } from '../../../types/index'

const props = defineProps<{
  trail: Trail
}>()

defineEmits<{
  click: []
}>()

const imageLoadFailed = ref(false)

const featuredImageSrc = computed(() => {
  const raw = (props.trail.featured_image || '').trim()
  if (!raw) {
    return ''
  }

  if (/^https?:\/\//i.test(raw) || raw.startsWith('/')) {
    return raw
  }

  return `/${raw.replace(/^\.?\//, '')}`
})

const shouldRenderImage = computed(() => !!featuredImageSrc.value && !imageLoadFailed.value)

watch(
  () => props.trail.featured_image,
  () => {
    imageLoadFailed.value = false
  }
)

const handleImageError = () => {
  imageLoadFailed.value = true
}

const getDifficultyTone = (level: string) => {
  const colors: Record<string, string> = {
    Easy: 'trail-overlay-chip--easy',
    Moderate: 'trail-overlay-chip--moderate',
    Hard: 'trail-overlay-chip--hard',
    Expert: 'trail-overlay-chip--expert',
  }
  return colors[level] || 'trail-overlay-chip--neutral'
}

const getAvailabilityTone = (spots: number) => {
  if (spots > 0) {
    return 'trail-overlay-chip--available'
  }

  return 'trail-overlay-chip--soldout'
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(price)
}

const formatTrailDate = (value: string) => {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return ''
  }

  return date.toLocaleDateString('en-KE', { month: 'short', day: 'numeric' })
}
</script>

<template>
  <div
    class="group glass-panel-strong soft-card-hover h-full overflow-hidden rounded-[1.05rem] border border-white/60 focus-within:ring-2 focus-within:ring-white/70 focus-within:ring-offset-2"
    @click="$emit('click')"
    role="article"
    :aria-label="`Trail: ${props.trail.title} in ${props.trail.location}`"
    tabindex="0"
    @keydown.enter="$emit('click')"
    @keydown.space.prevent="$emit('click')"
  >
    <div class="relative h-32 overflow-hidden bg-slate-900 sm:h-[8.7rem]">
      <div class="absolute inset-0 hero-overlay"></div>
      <div class="absolute inset-0 hero-grid opacity-35"></div>

      <img
        v-if="shouldRenderImage"
        :src="featuredImageSrc"
        :alt="props.trail.title"
        class="h-full w-full object-cover opacity-90 transition-transform duration-500 group-hover:scale-[1.03]"
        loading="lazy"
        decoding="async"
        @error="handleImageError"
      />
      <div v-else class="absolute inset-0 flex items-center justify-center text-white/70">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 19h18M5 19l5-8 3 4 3-6 3 10" />
        </svg>
      </div>

      <div class="absolute right-2 top-2">
        <div
          class="trail-overlay-chip"
          :class="getDifficultyTone(props.trail.difficulty_level)"
        >
          <span class="trail-overlay-dot" aria-hidden="true" />
          {{ props.trail.difficulty_level }}
        </div>
      </div>

      <div class="absolute bottom-2 left-2">
        <div
          class="trail-overlay-chip"
          :class="getAvailabilityTone(props.trail.available_spots)"
        >
          {{ props.trail.available_spots > 0 ? `${props.trail.available_spots} spots` : 'Booked out' }}
        </div>
      </div>
    </div>

    <div class="flex h-full flex-col p-3">
      <h3 class="trail-card-title text-[14px] font-semibold leading-5 text-slate-900 [display:-webkit-box] [-webkit-box-orient:vertical] [-webkit-line-clamp:2] overflow-hidden">
        {{ props.trail.title }}
      </h3>

      <div class="mt-1.5 flex items-center justify-between gap-2 text-[11px] text-slate-500">
        <div class="inline-flex min-w-0 items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 shrink-0 brand-text" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          </svg>
          <span class="truncate text-[11px] font-medium text-slate-600">{{ props.trail.location }}</span>
        </div>
        <span v-if="formatTrailDate(props.trail.scheduled_date)" class="shrink-0 text-[10px]">{{ formatTrailDate(props.trail.scheduled_date) }}</span>
      </div>

      <ul class="mt-2 grid grid-cols-3 gap-1">
        <li class="trail-metric-chip">
          <div class="trail-metric-value">
            <span class="trail-metric-icon" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7" />
              </svg>
            </span>
            <span>{{ props.trail.distance_km }}km</span>
          </div>
          <p class="trail-metric-label">Distance</p>
        </li>
        <li class="trail-metric-chip">
          <div class="trail-metric-value">
            <span class="trail-metric-icon" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </span>
            <span>{{ props.trail.duration_hours }}h</span>
          </div>
          <p class="trail-metric-label">Duration</p>
        </li>
        <li class="trail-metric-chip">
          <div class="trail-metric-value">
            <span class="trail-metric-icon" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8" />
              </svg>
            </span>
            <span>{{ props.trail.elevation_gain_m }}m</span>
          </div>
          <p class="trail-metric-label">Elevation</p>
        </li>
      </ul>

      <div class="mt-2.5 flex items-end justify-between gap-2">
        <div>
          <p class="text-[9px] uppercase tracking-[0.08em] text-slate-500">From</p>
          <p class="brand-text text-[1rem] font-semibold leading-tight">{{ formatPrice(props.trail.price_kshs) }}</p>
        </div>

        <button
          class="inline-flex items-center gap-1 rounded-[0.68rem] bg-[color:var(--color-primary)] px-2.5 py-1.5 text-[11px] font-medium text-white transition-all hover:brightness-[1.04] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--color-primary-ring)]"
          :aria-label="`View details for ${props.trail.title}`"
          @click.stop="$emit('click')"
        >
          <span>View</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Styling is handled through global design tokens */
</style>
