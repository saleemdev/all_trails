<script setup lang="ts">
import { onMounted, computed, watch, ref, defineAsyncComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTrailsStore } from '../../stores/trailsStore'
import { useAuthStore } from '../../stores/authStore'
import { apiService } from '../../services/api'
import TrailWeatherHighlight from '../../components/features/trails/TrailWeatherHighlight.vue'
import type { TrailWeather } from '../../types'

const route = useRoute()
const router = useRouter()
const trailsStore = useTrailsStore()
const authStore = useAuthStore()
const TrailMap = defineAsyncComponent(() => import('../../components/features/trails/TrailMap.vue'))

const trail = computed(() => trailsStore.selectedTrail)
const isLoading = computed(() => trailsStore.isLoading)
const error = computed(() => trailsStore.error)
const trailId = computed(() => String(route.params.id ?? ''))
const weather = ref<TrailWeather | null>(null)
const weatherLoading = ref(false)

onMounted(() => {
  if (trailId.value) {
    trailsStore.fetchTrailById(trailId.value)
    void loadWeather(trailId.value)
  }
})

watch(
  () => route.params.id,
  (nextId, prevId) => {
    if (!nextId || nextId === prevId) {
      return
    }
    trailsStore.fetchTrailById(String(nextId))
    void loadWeather(String(nextId))
  }
)

const goToBooking = () => {
  if (!authStore.isAuthenticated) {
    router.push({
      name: 'Login',
      query: { 'redirect-to': `/all-trails/trails/${trailId.value}/book` }
    })
    return
  }

  if (!trail.value) {
    return
  }

  router.push({ name: 'TrailBooking', params: { id: trail.value.id } })
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(price)
}

const formatDate = (dateValue?: string) => {
  if (!dateValue) {
    return 'Date to be announced'
  }

  const parsed = new Date(dateValue)
  if (Number.isNaN(parsed.getTime())) {
    return dateValue
  }

  return parsed.toLocaleDateString('en-KE', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

const formatTrailTime = (timeValue?: string) => {
  if (!timeValue) {
    return 'TBA'
  }

  const [hours, minutes] = String(timeValue).split(':').map((part) => Number(part))
  if (!Number.isFinite(hours) || !Number.isFinite(minutes)) {
    return timeValue
  }

  const formattedHours = ((hours + 11) % 12) + 1
  const period = hours >= 12 ? 'PM' : 'AM'
  return `${formattedHours}:${String(minutes).padStart(2, '0')} ${period}`
}

const difficultyPillClass = computed(() => {
  const level = trail.value?.difficulty_level?.toLowerCase()
  if (!level || !['easy', 'moderate', 'hard', 'expert'].includes(level)) {
    return 'soft-badge--neutral'
  }
  return `info-pill info-pill--difficulty-${level}`
})

const availabilityPercent = computed(() => {
  if (!trail.value || trail.value.max_capacity <= 0) {
    return 0
  }

  const ratio = (trail.value.available_spots / trail.value.max_capacity) * 100
  return Math.max(0, Math.min(100, Math.round(ratio)))
})

const availabilityLabel = computed(() => {
  if (!trail.value) {
    return ''
  }
  if (trail.value.available_spots <= 0) {
    return 'Sold out'
  }
  if (trail.value.available_spots <= 5) {
    return 'Selling fast'
  }
  return 'Spots available'
})

const hasExtraActivities = computed(() => (trail.value?.extra_activities?.length ?? 0) > 0)
const trailLocationLabel = computed(() => trail.value?.location || 'Trail location')
const trailMapItems = computed(() => (trail.value ? [trail.value] : []))
const hasMapCoordinates = computed(() => {
  const lat = trail.value?.coordinates?.lat
  const lng = trail.value?.coordinates?.lng
  return typeof lat === 'number' && typeof lng === 'number' && Number.isFinite(lat) && Number.isFinite(lng)
})
const mapQuery = computed(() => {
  if (!hasMapCoordinates.value) {
    return ''
  }

  return `${trail.value?.coordinates?.lat},${trail.value?.coordinates?.lng}`
})
const googleMapsPlaceUrl = computed(() =>
  hasMapCoordinates.value
    ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(mapQuery.value)}`
    : ''
)
const googleMapsDirectionsUrl = computed(() =>
  hasMapCoordinates.value
    ? `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(mapQuery.value)}&travelmode=driving`
    : ''
)
const splitLines = (value?: string) =>
  String(value || '')
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)

const loadWeather = async (id: string) => {
  weatherLoading.value = true
  try {
    weather.value = await apiService.getTrailWeather(id)
  } catch {
    weather.value = null
  } finally {
    weatherLoading.value = false
  }
}
</script>

<template>
  <div class="page-shell layout-shell-wide page-block-tight">
    <button @click="$router.back()" class="soft-button-secondary mb-5 px-4 py-2.5 text-sm">
      ← Back
    </button>

    <div v-if="isLoading" class="surface-card-lg text-center py-14">
      <div class="soft-spinner mx-auto mb-4"></div>
      <p class="text-lg text-slate-600 mb-0">Loading trail details...</p>
    </div>

    <div v-else-if="error" class="glass-panel rounded-[1.5rem] p-5 mb-6 border border-red-200/80">
      <div class="flex items-center justify-between gap-4 flex-wrap">
        <div class="flex items-center gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-red-900 font-medium">{{ error }}</span>
        </div>
        <button @click="trailsStore.fetchTrailById(trailId)" class="soft-button-secondary px-5 py-3 text-red-700 border-red-200 bg-red-50 hover:bg-red-100">
          Retry
        </button>
      </div>
    </div>

    <div v-else-if="trail" class="space-y-6">
      <section class="page-header rounded-[1.5rem] text-white overflow-hidden">
        <div class="absolute inset-0 hero-grid opacity-25"></div>
        <div class="relative z-10 p-6 sm:p-8 lg:p-10">
          <div class="grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,1fr)_20rem] xl:grid-cols-[minmax(0,1fr)_23rem] items-start">
            <div class="space-y-4">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="soft-kicker">Trail detail</span>
                <span :class="difficultyPillClass">
                  {{ trail.difficulty_level }}
                </span>
                <span
                  class="soft-badge"
                  :class="trail.available_spots > 0 ? 'soft-badge--brand' : 'soft-badge--accent'"
                >
                  {{ availabilityLabel }}
                </span>
              </div>

              <h1 class="text-[clamp(2rem,4vw,3.25rem)] font-semibold font-display leading-[1.02] tracking-[-0.04em]">
                {{ trail.title }}
              </h1>

              <p class="flex items-center gap-2 text-base text-white/80 sm:text-lg mb-0">
                <span>📍</span>
                <span>{{ trailLocationLabel }}</span>
              </p>

              <p class="text-base lg:text-lg text-white/80 leading-relaxed mb-0 max-w-3xl">
                {{ trail.description }}
              </p>

              <div class="flex flex-wrap gap-2.5 pt-1">
                <span class="hero-info-pill">🥾 {{ trail.distance_km }} km</span>
                <span class="hero-info-pill">⏱ {{ trail.duration_hours }} hrs</span>
                <span class="hero-info-pill">⛰ {{ trail.elevation_gain_m }} m</span>
                <span class="hero-info-pill">💳 {{ formatPrice(trail.price_kshs) }}</span>
              </div>
            </div>

            <div class="surface-card-lg hero-side-panel">
              <div class="space-y-4">
                <div>
                  <p class="text-[11px] uppercase tracking-[0.12em] text-white/80 mb-1">Scheduled</p>
                  <p class="text-lg font-semibold mb-0">{{ formatDate(trail.scheduled_date) }}</p>
                  <p class="text-sm text-white/90 mb-0">
                    {{ formatTrailTime(trail.start_time) }} - {{ formatTrailTime(trail.end_time) }}
                  </p>
                </div>
                <div class="h-px bg-white/20"></div>
                <div>
                  <p class="text-[11px] uppercase tracking-[0.12em] text-white/80 mb-1">Capacity</p>
                  <p class="text-base font-semibold mb-1">
                    {{ trail.available_spots }} of {{ trail.max_capacity }} spots left
                  </p>
                  <div class="w-full rounded-full h-2 bg-white/20 overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all"
                      :class="trail.available_spots > 0 ? 'bg-emerald-300' : 'bg-red-300'"
                      :style="{ width: `${availabilityPercent}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <TrailWeatherHighlight :weather="weather" :loading="weatherLoading" />

      <div class="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1fr)_21.5rem]">
        <div class="space-y-6">
          <section class="surface-card-lg">
            <p class="app-section-kicker mb-2">Trail flow</p>
            <h2 class="text-2xl brand-text-strong font-display font-semibold mb-2">Your day at a glance</h2>
            <p class="tone-body leading-relaxed mb-5">See the schedule, route profile, and expected pace.</p>

            <div class="space-y-3">
              <article class="surface-muted rounded-[1rem] p-4">
                <div class="flex items-start gap-3">
                  <span class="soft-icon-tile soft-icon-tile--sage !w-9 !h-9 shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </span>
                  <div>
                    <p class="text-sm font-semibold tone-heading mb-1">Meet-up window</p>
                    <p class="text-sm tone-body mb-0">{{ formatDate(trail.scheduled_date) }} · {{ formatTrailTime(trail.start_time) }}</p>
                  </div>
                </div>
              </article>

              <article class="surface-muted rounded-[1rem] p-4">
                <div class="flex items-start gap-3">
                  <span class="soft-icon-tile soft-icon-tile--mist !w-9 !h-9 shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                    </svg>
                  </span>
                  <div>
                    <p class="text-sm font-semibold tone-heading mb-1">Route profile</p>
                    <p class="text-sm tone-body mb-0">{{ trail.distance_km }} km distance · {{ trail.elevation_gain_m }} m gain · {{ trail.duration_hours }} hrs moving time.</p>
                  </div>
                </div>
              </article>

              <article class="surface-muted rounded-[1rem] p-4">
                <div class="flex items-start gap-3">
                  <span class="soft-icon-tile soft-icon-tile--brass !w-9 !h-9 shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </span>
                  <div>
                    <p class="text-sm font-semibold tone-heading mb-1">Difficulty and pace</p>
                    <p class="text-sm tone-body mb-0">{{ trail.difficulty_level }} intensity with a return window by {{ formatTrailTime(trail.end_time) }}.</p>
                  </div>
                </div>
              </article>
            </div>
          </section>

          <section class="surface-card-lg">
            <p class="app-section-kicker mb-2">Trail facts</p>
            <h2 class="text-2xl brand-text-strong font-display font-semibold mb-4">Trail details</h2>
            <div class="flex flex-wrap gap-2.5">
              <span class="soft-badge soft-badge--neutral">Status: {{ trail.status }}</span>
              <span v-if="trail.host" class="soft-badge soft-badge--neutral">Host: {{ trail.host }}</span>
              <span v-if="trail.county" class="soft-badge soft-badge--neutral">County: {{ trail.county }}</span>
              <span v-if="trail.trail_type" class="soft-badge soft-badge--neutral">{{ trail.trail_type }}</span>
              <span class="soft-badge soft-badge--neutral">Capacity {{ trail.available_spots }}/{{ trail.max_capacity }}</span>
              <span v-if="trail.is_long_weekend" class="soft-badge soft-badge--brand">Long-weekend friendly</span>
              <span v-if="trail.fitness_level" class="soft-badge soft-badge--neutral">{{ trail.fitness_level }}</span>
              <span v-if="trail.altitude_max_m" class="soft-badge soft-badge--neutral">Max altitude {{ trail.altitude_max_m }} m</span>
              <span v-if="trail.water_requirement_litres" class="soft-badge soft-badge--neutral">Carry {{ trail.water_requirement_litres }} L water</span>
              <span v-if="trail.best_season" class="soft-badge soft-badge--neutral">Best in {{ trail.best_season }}</span>
              <span v-if="trail.latitude !== undefined && trail.longitude !== undefined" class="soft-badge soft-badge--neutral">
                Coordinates {{ trail.latitude.toFixed(6) }}, {{ trail.longitude.toFixed(6) }}
              </span>
            </div>
          </section>

          <section class="surface-card-lg">
            <div class="flex items-center justify-between gap-3 flex-wrap mb-4">
              <div>
                <p class="app-section-kicker mb-2">Map view</p>
                <h2 class="text-2xl brand-text-strong font-display font-semibold mb-1">Trail location map</h2>
                <p class="tone-body text-sm mb-0">
                  <span v-if="hasMapCoordinates">See where this trail starts and explore its location before you book.</span>
                  <span v-else>Add latitude and longitude on the trail to show the map here.</span>
                </p>
              </div>
              <span v-if="hasMapCoordinates" class="soft-badge soft-badge--neutral">
                {{ trail.coordinates?.lat?.toFixed(6) }}, {{ trail.coordinates?.lng?.toFixed(6) }}
              </span>
            </div>
            <div v-if="hasMapCoordinates" class="flex flex-wrap gap-3 mb-4">
              <a
                :href="googleMapsPlaceUrl"
                target="_blank"
                rel="noreferrer"
                class="brand-button inline-flex items-center justify-center px-5 py-3"
              >
                Open in Google Maps
              </a>
              <a
                :href="googleMapsDirectionsUrl"
                target="_blank"
                rel="noreferrer"
                class="soft-button-secondary inline-flex items-center justify-center px-5 py-3"
              >
                Get directions
              </a>
            </div>
            <TrailMap v-if="hasMapCoordinates" :trails="trailMapItems" @trail-click="view => router.push({ name: 'TrailDetail', params: { id: view.id } })" />
            <div v-else class="surface-muted rounded-[1rem] p-5 text-sm tone-body">
              This trail does not have coordinate fields filled yet, so the map cannot be rendered.
            </div>
          </section>

          <section class="surface-card-lg" v-if="trail.meeting_point || trail.meeting_notes || trail.transport_notes">
            <p class="app-section-kicker mb-2">Meeting and transport</p>
            <h2 class="text-2xl brand-text-strong font-display font-semibold mb-4">Getting there</h2>
            <div class="space-y-3">
              <article v-if="trail.meeting_point || trail.meeting_time" class="surface-muted rounded-[1rem] p-4">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-1">Meeting point</p>
                <p class="text-sm font-semibold tone-heading mb-1">
                  {{ trail.meeting_point || trailLocationLabel }}
                  <span v-if="trail.meeting_time"> · {{ formatTrailTime(trail.meeting_time) }}</span>
                </p>
                <p v-if="trail.meeting_notes" class="text-sm tone-body mb-0">{{ trail.meeting_notes }}</p>
                <a
                  v-if="trail.meeting_point_maps_url"
                  :href="trail.meeting_point_maps_url"
                  target="_blank"
                  rel="noreferrer"
                  class="brand-link inline-block mt-2 text-sm"
                >
                  Open map
                </a>
              </article>

              <article v-if="trail.transport_notes" class="surface-muted rounded-[1rem] p-4">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-1">Transport notes</p>
                <p class="text-sm tone-body mb-0">{{ trail.transport_notes }}</p>
              </article>
            </div>
          </section>

          <section class="surface-card-lg" v-if="trail.terrain_summary || trail.trail_highlights || trail.altitude_start_m || trail.altitude_max_m">
            <p class="app-section-kicker mb-2">Route character</p>
            <h2 class="text-2xl brand-text-strong font-display font-semibold mb-4">Terrain and altitude</h2>
            <div class="grid gap-3 sm:grid-cols-2">
              <article v-if="trail.terrain_summary" class="surface-muted rounded-[1rem] p-4">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-1">Terrain</p>
                <p class="text-sm tone-body mb-0">{{ trail.terrain_summary }}</p>
              </article>
              <article v-if="trail.altitude_start_m || trail.altitude_max_m" class="surface-muted rounded-[1rem] p-4">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-1">Altitude</p>
                <p class="text-sm tone-body mb-0">
                  <span v-if="trail.altitude_start_m">Start {{ trail.altitude_start_m }} m</span>
                  <span v-if="trail.altitude_start_m && trail.altitude_max_m"> · </span>
                  <span v-if="trail.altitude_max_m">High point {{ trail.altitude_max_m }} m</span>
                </p>
              </article>
            </div>
            <div v-if="splitLines(trail.trail_highlights).length" class="mt-4 flex flex-wrap gap-2">
              <span v-for="item in splitLines(trail.trail_highlights)" :key="item" class="soft-badge soft-badge--neutral">{{ item }}</span>
            </div>
          </section>

          <section class="surface-card-lg" v-if="splitLines(trail.packing_list).length || splitLines(trail.safety_notes).length || splitLines(trail.inclusions).length || splitLines(trail.exclusions).length">
            <p class="app-section-kicker mb-2">Before you go</p>
            <h2 class="text-2xl brand-text-strong font-display font-semibold mb-4">Preparation notes</h2>
            <div class="grid gap-4 lg:grid-cols-2">
              <article v-if="splitLines(trail.packing_list).length" class="surface-muted rounded-[1rem] p-4">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-2">Packing list</p>
                <ul class="space-y-2 text-sm tone-body">
                  <li v-for="item in splitLines(trail.packing_list)" :key="item" class="flex gap-2">
                    <span class="mt-[2px]">•</span>
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </article>

              <article v-if="splitLines(trail.safety_notes).length" class="surface-muted rounded-[1rem] p-4">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-2">Safety notes</p>
                <ul class="space-y-2 text-sm tone-body">
                  <li v-for="item in splitLines(trail.safety_notes)" :key="item" class="flex gap-2">
                    <span class="mt-[2px]">•</span>
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </article>

              <article v-if="splitLines(trail.inclusions).length" class="surface-muted rounded-[1rem] p-4">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-2">Included</p>
                <ul class="space-y-2 text-sm tone-body">
                  <li v-for="item in splitLines(trail.inclusions)" :key="item" class="flex gap-2">
                    <span class="mt-[2px]">•</span>
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </article>

              <article v-if="splitLines(trail.exclusions).length" class="surface-muted rounded-[1rem] p-4">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-2">Not included</p>
                <ul class="space-y-2 text-sm tone-body">
                  <li v-for="item in splitLines(trail.exclusions)" :key="item" class="flex gap-2">
                    <span class="mt-[2px]">•</span>
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </article>
            </div>
          </section>

          <section v-if="hasExtraActivities" class="surface-card-lg">
            <div class="flex items-center gap-2 mb-2">
              <h3 class="text-2xl brand-text-strong font-display font-semibold">Extra Activities</h3>
              <span class="soft-badge soft-badge--neutral">Optional add-ons</span>
            </div>
            <p class="tone-body text-sm mb-4">
              Add these during booking to personalize your trail day.
            </p>
            <div class="space-y-3">
              <article
                v-for="activity in trail.extra_activities"
                :key="activity.id"
                class="rounded-[1rem] p-4 border"
                :class="activity.available ? 'surface-muted border-[color:var(--color-border-soft)]' : 'bg-slate-50 border-slate-200 opacity-65'"
              >
                <div class="flex items-start justify-between gap-4">
                  <div>
                    <div class="flex items-center gap-2 mb-1.5 flex-wrap">
                      <span v-if="activity.icon" class="text-xl">{{ activity.icon }}</span>
                      <h4 class="text-base font-semibold tone-heading mb-0">{{ activity.name }}</h4>
                      <span v-if="!activity.available" class="soft-badge soft-badge--accent">Unavailable</span>
                    </div>
                    <p class="text-sm tone-body mb-2">{{ activity.description }}</p>
                    <div class="flex items-center gap-3 text-xs flex-wrap">
                      <span class="font-semibold brand-text">+{{ formatPrice(activity.price_kshs) }}</span>
                      <span v-if="activity.max_participants" class="tone-muted">Max {{ activity.max_participants }}</span>
                      <span v-if="activity.available_spots !== undefined" class="tone-muted">{{ activity.available_spots }} spots left</span>
                    </div>
                  </div>
                </div>
              </article>
            </div>
          </section>
        </div>

        <aside class="xl:sticky xl:top-24 h-fit">
          <div class="surface-card-lg space-y-5">
            <div>
              <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-1">Booking action</p>
              <h2 class="text-2xl brand-text-strong font-display font-semibold mb-0">Reserve your spot</h2>
            </div>

            <div class="surface-muted rounded-[1rem] p-4">
              <div class="text-sm tone-muted">Price per person</div>
              <div class="text-3xl brand-text font-semibold mt-1">
                {{ formatPrice(trail.price_kshs) }}
              </div>
            </div>

            <div class="surface-muted rounded-[1rem] p-4">
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="text-sm tone-muted">Availability</span>
                <span
                  class="text-xs font-semibold"
                  :class="trail.available_spots > 0 ? 'text-emerald-700' : 'text-red-700'"
                >
                  {{ availabilityLabel }}
                </span>
              </div>
              <div class="text-lg font-semibold mb-2" :class="trail.available_spots > 0 ? 'text-emerald-700' : 'text-red-700'">
                {{ trail.available_spots }} / {{ trail.max_capacity }}
              </div>
              <div class="w-full rounded-full h-2 bg-slate-200 overflow-hidden">
                <div
                  class="h-full rounded-full transition-all"
                  :class="trail.available_spots > 0 ? 'bg-emerald-500' : 'bg-red-500'"
                  :style="{ width: `${availabilityPercent}%` }"
                ></div>
              </div>
            </div>

            <button
              :disabled="trail.available_spots === 0"
              @click="goToBooking"
              class="brand-button w-full px-6 py-4 disabled:opacity-60 disabled:transform-none"
              :aria-label="trail.available_spots > 0 ? `Book ${trail.title}` : 'Trail is fully booked'"
            >
              <span v-if="trail.available_spots > 0">📅</span>
              <span v-else>🚫</span>
              {{ trail.available_spots > 0 ? 'Book now' : 'Fully booked' }}
            </button>

            <ul class="text-sm tone-body space-y-2">
              <li class="flex gap-2">
                <span class="mt-[2px]">•</span>
                <span>Secure your place first, then pick optional activities.</span>
              </li>
              <li class="flex gap-2">
                <span class="mt-[2px]">•</span>
                <span>Fast checkout with MPESA-based payment flow.</span>
              </li>
              <li class="flex gap-2">
                <span class="mt-[2px]">•</span>
                <span>Weather and route context stay visible through the booking journey.</span>
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </div>

    <div v-else class="surface-card-lg text-center py-10">
      <p class="text-lg tone-body mb-3">We could not find this trail.</p>
      <button @click="$router.push({ name: 'TrailBrowse' })" class="brand-button px-5 py-3">
        Browse trails
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Styling is handled through global design tokens */
</style>
