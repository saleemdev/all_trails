<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTrailsStore } from '../../stores/trailsStore'
import { useAuthStore } from '../../stores/authStore'

const route = useRoute()
const router = useRouter()
const trailsStore = useTrailsStore()
const authStore = useAuthStore()

const trail = computed(() => trailsStore.selectedTrail)
const isLoading = computed(() => trailsStore.isLoading)
const error = computed(() => trailsStore.error)

onMounted(() => {
  const trailId = route.params.id as string
  trailsStore.fetchTrailById(trailId)
})

const goToBooking = () => {
  if (!authStore.isAuthenticated) {
    router.push({
      name: 'Login',
      query: { 'redirect-to': `/all-trails/trails/${route.params.id}/book` }
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
</script>

<template>
  <div class="page-shell layout-shell-wide page-block-tight">
    <button @click="$router.back()" class="soft-button-secondary mb-6 px-5 py-3">
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
        <button @click="trailsStore.fetchTrailById(route.params.id as string)" class="soft-button-secondary px-5 py-3 text-red-700 border-red-200 bg-red-50 hover:bg-red-100">
          Retry
        </button>
      </div>
    </div>

    <div v-else-if="trail" class="space-y-6">
      <section class="page-header rounded-[2rem] text-white overflow-hidden">
        <div class="absolute inset-0 hero-grid opacity-25"></div>
        <div class="relative z-10 p-6 sm:p-8 lg:p-10">
          <div class="grid grid-cols-1 lg:grid-cols-[auto_1fr] gap-8 items-center">
            <div class="flex items-center justify-center lg:justify-start">
              <div class="text-9xl opacity-90">🏔️</div>
            </div>
            <div class="space-y-4">
              <span class="soft-kicker">Trail overview</span>
              <h1 class="text-[clamp(2rem,4vw,3.25rem)] font-semibold font-display leading-[1.02] tracking-[-0.04em]">{{ trail.title }}</h1>
              <p class="flex items-center gap-2 text-base text-white/80 sm:text-lg mb-0">
                <span>📍</span>
                <span>{{ trail.location }}</span>
              </p>
              <p class="text-base lg:text-lg text-white/75 leading-relaxed mb-0">
                {{ trail.description }}
              </p>
            </div>
          </div>
        </div>
      </section>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          <div class="surface-card-lg">
            <h2 class="text-2xl brand-text-strong font-display mb-4 font-semibold">Trail Information</h2>

            <div class="grid grid-cols-2 gap-4">
              <div class="surface-muted rounded-[1.25rem] p-4">
                <div class="text-sm text-slate-500">Difficulty</div>
                <div class="text-2xl brand-text-strong font-semibold">{{ trail.difficulty_level }}</div>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4">
                <div class="text-sm text-slate-500">Distance</div>
                <div class="text-2xl brand-text-strong font-semibold">{{ trail.distance_km }} km</div>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4">
                <div class="text-sm text-slate-500">Duration</div>
                <div class="text-2xl brand-text-strong font-semibold">{{ trail.duration_hours }}h</div>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4">
                <div class="text-sm text-slate-500">Elevation</div>
                <div class="text-2xl brand-text-strong font-semibold">{{ trail.elevation_gain_m }}m</div>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4">
                <div class="text-sm text-slate-500">Date</div>
                <div class="text-lg brand-text-strong font-bold">
                  {{ trail ? new Date(trail.scheduled_date).toLocaleDateString() : '' }}
                </div>
              </div>
              <div class="surface-muted rounded-[1.25rem] p-4">
                <div class="text-sm text-slate-500">Time</div>
                <div class="text-lg brand-text-strong font-bold">
                  {{ trail.start_time }} - {{ trail.end_time }}
                </div>
              </div>
            </div>

            <div v-if="trail.extra_activities && trail.extra_activities.length > 0" class="mt-6">
              <div class="flex items-center gap-2 mb-2">
                <h3 class="text-xl font-bold text-slate-900">Extra Activities</h3>
                <span class="soft-badge soft-badge--neutral">Optional</span>
              </div>
              <p class="text-sm text-slate-600 mb-4">
                <span class="font-semibold">Optional activities</span> available during booking.
                <span class="font-semibold brand-text">Each adds extra cost.</span>
              </p>
              <div class="space-y-3">
                <div
                  v-for="activity in trail.extra_activities"
                  :key="activity.id"
                  class="rounded-[1.25rem] p-4 border"
                  :class="activity.available ? 'surface-muted border-[color:var(--color-border-soft)]' : 'bg-slate-50 border-slate-200 opacity-60'"
                >
                  <div class="flex items-start justify-between gap-4">
                    <div class="flex-1">
                      <div class="flex items-center gap-2 mb-2 flex-wrap">
                        <span v-if="activity.icon" class="text-2xl">{{ activity.icon }}</span>
                        <h4 class="font-bold text-slate-900">{{ activity.name }}</h4>
                        <span v-if="!activity.available" class="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full font-bold">
                          Unavailable
                        </span>
                      </div>
                      <p class="text-sm text-slate-600 mb-2">{{ activity.description }}</p>
                      <div class="flex items-center gap-4 text-xs flex-wrap">
                        <span class="font-bold brand-text">+{{ formatPrice(activity.price_kshs) }} <span class="text-slate-500 font-normal">extra</span></span>
                        <span v-if="activity.max_participants" class="text-slate-500">Max: {{ activity.max_participants }} people</span>
                        <span v-if="activity.available_spots !== undefined" class="text-slate-500">Available: {{ activity.available_spots }} spots</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="trail.is_long_weekend" class="mt-6 bg-blue-50 border border-blue-200 rounded-[1.25rem] p-4 flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <div>
                <p class="font-bold text-blue-900 mb-0">Long Weekend Available</p>
                <p class="text-sm text-blue-700 mb-0">Perfect for an extended adventure!</p>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-1">
          <div class="surface-card-lg space-y-5">
            <h2 class="text-2xl brand-text-strong font-display font-semibold">Booking</h2>

            <div class="surface-muted rounded-[1.25rem] p-4">
              <div class="text-sm text-slate-500">Price per person</div>
              <div class="text-3xl brand-text font-semibold">
                {{ trail ? formatPrice(trail.price_kshs) : '' }}
              </div>
            </div>

            <div class="surface-muted rounded-[1.25rem] p-4">
              <div class="text-sm text-slate-500">Available Spots</div>
              <div class="text-2xl font-semibold" :class="trail.available_spots > 0 ? 'text-green-600' : 'text-red-600'">
                {{ trail.available_spots }} / {{ trail.max_capacity }}
              </div>
            </div>

            <button
              :disabled="!trail || trail.available_spots === 0"
              @click="goToBooking"
              class="brand-button w-full px-6 py-4 disabled:opacity-60 disabled:transform-none"
              :aria-label="trail.available_spots > 0 ? `Book ${trail.title}` : 'Trail is fully booked'"
            >
              <span v-if="trail.available_spots > 0">📅</span>
              <span v-else>🚫</span>
              {{ trail.available_spots > 0 ? 'Book Now' : 'Fully Booked' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Styling is handled through global design tokens */
</style>
