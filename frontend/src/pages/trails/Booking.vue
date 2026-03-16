<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookingsStore } from '../../stores/bookingsStore'
import { useUiStore } from '../../stores/uiStore'
import { useTrailsStore } from '../../stores/trailsStore'
import { useAuthStore } from '../../stores/authStore'
import { apiService } from '../../services/api'
import type { TrailWeather } from '../../types'

const route = useRoute()
const router = useRouter()
const bookingsStore = useBookingsStore()
const uiStore = useUiStore()
const trailsStore = useTrailsStore()
const authStore = useAuthStore()

const trail = computed(() => trailsStore.selectedTrail)
const isLoading = computed(() => trailsStore.isLoading)

const spotsBooked = ref(1)
const selectedActivities = ref<Record<string, number>>({})
const isSubmitting = ref(false)
const weather = ref<TrailWeather | null>(null)
const weatherLoading = ref(false)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'Login', query: { 'redirect-to': route.fullPath } })
    return
  }

  const trailId = route.params.id as string
  if (!trail.value || trail.value.id !== trailId) {
    await trailsStore.fetchTrailById(trailId)
  }
  void loadWeather(trailId)

  if (!trail.value) {
    uiStore.showError('Trail not found')
    router.push({ name: 'TrailBrowse' })
  }
})

const loadWeather = async (trailId: string) => {
  weatherLoading.value = true
  try {
    weather.value = await apiService.getTrailWeather(trailId)
  } catch {
    weather.value = null
  } finally {
    weatherLoading.value = false
  }
}

const basePrice = computed(() => {
  if (!trail.value) return 0
  return trail.value.price_kshs * spotsBooked.value
})

const activitiesPrice = computed(() => {
  if (!trail.value?.extra_activities) return 0
  return trail.value.extra_activities.reduce((total, activity) => {
    const quantity = selectedActivities.value[activity.id] || 0
    return total + activity.price_kshs * quantity
  }, 0)
})

const totalPrice = computed(() => basePrice.value + activitiesPrice.value)

const maxSpots = computed(() => {
  if (!trail.value) return 0
  return Math.min(trail.value.available_spots, 10)
})

const handleBookingSubmit = async () => {
  if (!trail.value) {
    return
  }

  isSubmitting.value = true
  try {
    const activities = (trail.value.extra_activities || [])
      .filter((activity) => selectedActivities.value[activity.id] && selectedActivities.value[activity.id] > 0)
      .map((activity) => ({
        activity_id: activity.id,
        activity_name: activity.name,
        quantity: selectedActivities.value[activity.id],
        price: activity.price_kshs,
      }))

    const booking = await bookingsStore.createBooking(trail.value.id, spotsBooked.value, activities)
    uiStore.showSuccess('Booking created successfully. Complete payment on the booking page.')
    router.push({ name: 'BookingDetail', params: { id: booking.id } })
  } catch (error: any) {
    uiStore.showError(error?.message || 'Failed to create booking')
  } finally {
    isSubmitting.value = false
  }
}

const toggleActivity = (activityId: string) => {
  if (selectedActivities.value[activityId]) {
    delete selectedActivities.value[activityId]
  } else {
    selectedActivities.value[activityId] = 1
  }
}

const updateActivityQuantity = (activityId: string, quantity: number) => {
  if (quantity <= 0) {
    delete selectedActivities.value[activityId]
  } else {
    selectedActivities.value[activityId] = quantity
  }
}

const isActivitySelected = (activityId: string) => {
  return !!selectedActivities.value[activityId] && selectedActivities.value[activityId] > 0
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(price)
}

const weatherRiskPillClass = computed(() => {
  const risk = weather.value?.risk_level
  if (risk === 'good') return 'info-pill info-pill--risk-good'
  if (risk === 'caution') return 'info-pill info-pill--risk-caution'
  if (risk === 'risky') return 'info-pill info-pill--risk-risky'
  return 'soft-badge soft-badge--neutral'
})
</script>

<template>
  <div class="page-shell min-h-screen py-6 sm:py-8">
    <div class="layout-shell-narrow">
      <button @click="router.back()" class="soft-button-secondary px-4 py-2.5 mb-5 text-sm">
        ← Back to Trail
      </button>

      <div v-if="isLoading" class="surface-card-lg py-16 text-center">
        <div class="soft-spinner mx-auto mb-4"></div>
        <p class="text-lg text-slate-600 mb-0">Loading trail details...</p>
      </div>

      <div v-else-if="!trail" class="glass-panel rounded-[1.5rem] p-5 border border-red-200/80 text-red-900">
        Trail not found. Please go back and try again.
      </div>

      <div v-else class="space-y-6">
        <section class="page-header rounded-[1.5rem] overflow-hidden text-white relative">
          <div class="absolute inset-0 hero-grid opacity-25"></div>
          <div class="relative z-10 p-6 sm:p-8 lg:p-9">
            <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6">
              <div>
                <span class="soft-kicker mb-4">Trail booking</span>
                <h1 class="text-[clamp(1.9rem,4vw,2.7rem)] font-semibold leading-[1.04] tracking-[-0.03em] mb-3">Reserve your place</h1>
                <p class="text-white/80 text-base mb-0">Create your booking now, then complete MPESA payment on your booking page.</p>
              </div>
              <div class="glass-panel hero-side-panel rounded-[1.2rem] px-5 py-4 min-w-[17rem]">
                <div class="text-xs uppercase tracking-[0.14em] text-white/80 mb-2">Your Trail</div>
                <div class="mb-1.5 text-xl font-semibold text-white">{{ trail.title }}</div>
                <div class="text-white/90 text-sm">🗓 {{ new Date(trail.scheduled_date).toLocaleDateString() }} • {{ trail.start_time }}</div>
              </div>
            </div>
          </div>
        </section>

        <section class="surface-card-lg">
          <div class="mb-5 rounded-[1rem] surface-muted p-3.5">
            <div class="flex items-center justify-between gap-3 flex-wrap mb-2">
              <p class="text-sm font-semibold tone-heading mb-0">Trail Day Weather</p>
              <span v-if="weather?.available" :class="weatherRiskPillClass">{{ weather.risk_label }}</span>
            </div>
            <p v-if="weatherLoading" class="text-sm tone-body mb-0">Checking weather forecast...</p>
            <p v-else-if="!weather?.available" class="text-sm tone-body mb-0">
              {{ weather?.message || 'Weather forecast is unavailable right now.' }}
            </p>
            <div v-else class="flex flex-wrap gap-1.5 text-xs">
              <span class="soft-badge soft-badge--neutral">{{ weather.summary }}</span>
              <span class="soft-badge soft-badge--neutral">{{ weather.temperature_min_c }}°-{{ weather.temperature_max_c }}°C</span>
              <span class="soft-badge soft-badge--neutral">Rain {{ weather.precipitation_probability_max }}%</span>
              <span class="soft-badge soft-badge--neutral">Gust {{ weather.wind_gusts_10m_max_kmh }} km/h</span>
            </div>
          </div>

          <div class="grid grid-cols-1 xl:grid-cols-[1.5fr_0.9fr] gap-8">
            <div class="space-y-6">
              <div>
                <label class="block text-sm font-semibold text-slate-700 mb-2">Number of Spots</label>
                <input v-model.number="spotsBooked" type="number" min="1" :max="maxSpots" class="soft-input w-full" />
                <p class="text-sm tone-body mt-2 mb-0">Available: {{ trail.available_spots }} spots</p>
              </div>

              <div v-if="trail.is_long_weekend" class="surface-muted rounded-[1rem] p-3.5 flex items-center gap-2.5 border border-blue-200/70">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="text-sm font-semibold text-blue-900 mb-0">Long-weekend friendly schedule.</span>
              </div>

              <div v-if="trail.extra_activities && trail.extra_activities.length > 0" class="space-y-4">
                <div class="flex items-center gap-2">
                  <h3 class="text-lg font-semibold text-slate-900">Extra Activities</h3>
                  <span class="soft-badge soft-badge--neutral">Optional</span>
                </div>

                <div class="space-y-3">
                  <div
                    v-for="activity in trail.extra_activities"
                    :key="activity.id"
                    class="rounded-[1.25rem] p-4 border transition-all"
                    :class="isActivitySelected(activity.id)
                      ? 'bg-[rgba(49,83,72,0.08)] border-[color:var(--color-border-strong)]'
                      : activity.available
                        ? 'glass-panel border-white/70'
                        : 'bg-slate-50 border-slate-200 opacity-60'"
                  >
                    <div class="flex items-start justify-between gap-4 flex-wrap">
                      <div class="flex-1 min-w-[16rem]">
                        <div class="flex items-center gap-2 mb-2 flex-wrap">
                          <span v-if="activity.icon" class="text-2xl">{{ activity.icon }}</span>
                          <h4 class="font-semibold text-slate-900">{{ activity.name }}</h4>
                          <span v-if="!activity.available" class="soft-badge soft-badge--accent">Unavailable</span>
                        </div>
                        <p class="text-sm text-slate-600 mb-2">{{ activity.description }}</p>
                        <div class="flex items-center gap-4 text-xs flex-wrap">
                          <span class="font-semibold brand-text">+{{ formatPrice(activity.price_kshs) }}</span>
                          <span v-if="activity.available_spots !== undefined" class="text-slate-500">{{ activity.available_spots }} spots left</span>
                        </div>
                      </div>

                      <div v-if="activity.available" class="flex items-center gap-2 flex-wrap justify-end">
                        <button
                          v-if="!isActivitySelected(activity.id)"
                          @click="toggleActivity(activity.id)"
                          class="brand-button px-4 py-2 text-sm"
                          :aria-label="`Add ${activity.name} for ${formatPrice(activity.price_kshs)} extra`"
                        >
                          Add (+{{ formatPrice(activity.price_kshs) }})
                        </button>
                        <div v-else class="flex items-center gap-2 flex-wrap justify-end">
                          <button @click="updateActivityQuantity(activity.id, (selectedActivities[activity.id] || 1) - 1)" class="soft-button-secondary w-8 h-8 p-0">−</button>
                          <input
                            type="number"
                            :value="selectedActivities[activity.id] || 1"
                            @input="updateActivityQuantity(activity.id, parseInt(($event.target as HTMLInputElement).value) || 0)"
                            :min="1"
                            :max="activity.max_participants || activity.available_spots || 10"
                            class="soft-input w-16 text-center py-2"
                          />
                          <button
                            @click="updateActivityQuantity(activity.id, (selectedActivities[activity.id] || 1) + 1)"
                            :disabled="(selectedActivities[activity.id] || 1) >= (activity.max_participants || activity.available_spots || 10)"
                            class="soft-button-secondary w-8 h-8 p-0 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            +
                          </button>
                          <button @click="toggleActivity(activity.id)" class="soft-button-secondary px-3 py-2 text-red-700 border-red-200 bg-red-50 hover:bg-red-100">
                            Remove
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <aside class="space-y-4">
              <div class="surface-muted rounded-[1.2rem] p-5 space-y-3">
                <p class="text-xs uppercase tracking-[0.1em] tone-muted mb-2">Booking Summary</p>
                <div class="flex justify-between text-slate-700"><span>Price per person</span><span class="font-semibold">{{ formatPrice(trail.price_kshs) }}</span></div>
                <div class="flex justify-between text-slate-700"><span>Spots</span><span class="font-semibold">{{ spotsBooked }}</span></div>
                <div class="flex justify-between text-slate-700"><span>Base total</span><span class="font-semibold">{{ formatPrice(basePrice) }}</span></div>
                <div v-if="activitiesPrice > 0" class="flex justify-between brand-text font-semibold"><span>Extra activities</span><span>+{{ formatPrice(activitiesPrice) }}</span></div>
                <div class="flex justify-between font-semibold text-base pt-3 border-t border-slate-200/80"><span>Total</span><span class="brand-text">{{ formatPrice(totalPrice) }}</span></div>
              </div>

              <div class="glass-panel rounded-[1.2rem] p-4">
                <h3 class="font-semibold text-slate-900 mb-2">What happens next</h3>
                <p class="text-sm tone-body mb-0">You’ll be redirected to booking details to pay, refresh payment status, and track progress.</p>
              </div>
            </aside>
          </div>

          <div class="flex gap-4 pt-8 flex-col sm:flex-row">
            <button @click="router.back()" class="soft-button-secondary px-6 py-4 flex-1">Cancel</button>
            <button
              @click="handleBookingSubmit"
              :disabled="isSubmitting"
              class="brand-button px-6 py-4 flex-1 disabled:opacity-60 disabled:transform-none"
            >
              <span v-if="!isSubmitting">Create Booking</span>
              <span v-else class="flex items-center justify-center gap-2"><span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>Creating Booking...</span>
            </button>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
