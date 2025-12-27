<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, Card, Spinner } from 'frappe-ui'
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
  
  // Navigate to booking page
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
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <Button
      variant="ghost"
      @click="$router.back()"
      class="mb-6"
    >
      ← Back
    </Button>

    <!-- Loading State -->
    <Card v-if="isLoading" class="text-center py-16">
      <Spinner class="mx-auto mb-4" />
      <p class="text-lg text-gray-600">Loading trail details...</p>
    </Card>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border-2 border-red-200 rounded-lg p-4 mb-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-red-900 font-medium">{{ error }}</span>
        </div>
        <Button
          variant="ghost"
          size="sm"
          @click="trailsStore.fetchTrailById(route.params.id as string)"
        >
          Retry
        </Button>
      </div>
    </div>

    <!-- Trail Detail -->
    <div v-else-if="trail" class="space-y-6">
      <!-- Header Card -->
      <Card class="bg-gradient-to-br from-emerald-900 to-teal-800 text-white">
        <div class="p-8 lg:p-12">
          <div class="grid grid-cols-1 lg:grid-cols-[auto_1fr] gap-8">
            <!-- Icon -->
            <div class="flex items-center justify-center lg:justify-start">
              <div class="text-9xl opacity-90">🏔️</div>
            </div>

            <!-- Content -->
            <div class="space-y-4">
              <h1 class="text-4xl lg:text-5xl font-bold font-display">{{ trail.title }}</h1>
              <p class="text-xl flex items-center gap-2 opacity-90">
                <span>📍</span>
                <span>{{ trail.location }}</span>
              </p>
              <p class="text-base lg:text-lg opacity-85 leading-relaxed">
                {{ trail.description }}
              </p>
            </div>
          </div>
        </div>
      </Card>

      <!-- Main Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Trail Information -->
        <div class="lg:col-span-2">
          <Card>
            <div class="p-6">
              <h2 class="card-title text-2xl text-primary font-display mb-4">
                Trail Information
              </h2>

              <div class="grid grid-cols-2 gap-6">
                <div class="stat bg-gray-100 rounded-lg p-4">
                  <div class="stat-title text-sm">Difficulty</div>
                  <div class="stat-value text-2xl text-emerald-900">{{ trail?.difficulty_level }}</div>
                </div>

                <div class="stat bg-gray-100 rounded-lg p-4">
                  <div class="stat-title text-sm">Distance</div>
                  <div class="stat-value text-2xl text-emerald-900">{{ trail?.distance_km }} km</div>
                </div>

                <div class="stat bg-gray-100 rounded-lg p-4">
                  <div class="stat-title text-sm">Duration</div>
                  <div class="stat-value text-2xl text-emerald-900">{{ trail?.duration_hours }}h</div>
                </div>

                <div class="stat bg-gray-100 rounded-lg p-4">
                  <div class="stat-title text-sm">Elevation</div>
                  <div class="stat-value text-2xl text-emerald-900">{{ trail?.elevation_gain_m }}m</div>
                </div>

                <div class="stat bg-gray-100 rounded-lg p-4">
                  <div class="stat-title text-sm">Date</div>
                  <div class="stat-value text-lg text-emerald-900">
                    {{ trail ? new Date(trail.scheduled_date).toLocaleDateString() : '' }}
                  </div>
                </div>

                <div class="stat bg-gray-100 rounded-lg p-4">
                  <div class="stat-title text-sm">Time</div>
                  <div class="stat-value text-lg text-emerald-900">
                    {{ trail?.start_time }} - {{ trail?.end_time }}
                  </div>
                </div>
              </div>

              <!-- Extra Activities Section -->
              <div v-if="trail?.extra_activities && trail.extra_activities.length > 0" class="mt-6">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="text-xl font-bold text-gray-900">Extra Activities</h3>
                  <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-bold">
                    Optional
                  </span>
                </div>
                <p class="text-sm text-gray-600 mb-4">
                  <span class="font-semibold">Optional activities</span> available during booking. 
                  <span class="font-semibold text-emerald-700">Each adds extra cost.</span>
                </p>
                <div class="space-y-3">
                  <div
                    v-for="activity in trail.extra_activities"
                    :key="activity.id"
                    class="border-2 rounded-xl p-4"
                    :class="activity.available
                      ? 'border-emerald-200 bg-emerald-50'
                      : 'border-gray-200 bg-gray-50 opacity-60'"
                  >
                    <div class="flex items-start justify-between gap-4">
                      <div class="flex-1">
                        <div class="flex items-center gap-2 mb-2">
                          <span v-if="activity.icon" class="text-2xl">{{ activity.icon }}</span>
                          <h4 class="font-bold text-gray-900">{{ activity.name }}</h4>
                          <span v-if="!activity.available" class="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full font-bold">
                            Unavailable
                          </span>
                        </div>
                        <p class="text-sm text-gray-600 mb-2">{{ activity.description }}</p>
                        <div class="flex items-center gap-4 text-xs">
                          <span class="font-bold text-emerald-700">+{{ formatPrice(activity.price_kshs) }} <span class="text-gray-500 font-normal">extra</span></span>
                          <span v-if="activity.max_participants" class="text-gray-500">Max: {{ activity.max_participants }} people</span>
                          <span v-if="activity.available_spots !== undefined" class="text-gray-500">Available: {{ activity.available_spots }} spots</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Long Weekend Badge -->
              <div v-if="trail?.is_long_weekend" class="mt-6 bg-blue-50 border-2 border-blue-200 rounded-xl p-4 flex items-center gap-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <div>
                  <p class="font-bold text-blue-900">Long Weekend Available</p>
                  <p class="text-sm text-blue-700">Perfect for an extended adventure!</p>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <!-- Booking Section -->
        <div class="lg:col-span-1">
          <Card v-if="!showBookingForm" class="border-2 border-gray-200">
            <div class="p-6 space-y-6">
              <h2 class="card-title text-2xl text-primary font-display">
                Booking
              </h2>

              <!-- Price Display -->
              <div class="stat bg-gray-100 rounded-lg p-4">
                <div class="stat-title text-sm">Price per person</div>
                <div class="stat-value text-3xl text-emerald-700">
                  {{ trail ? formatPrice(trail.price_kshs) : '' }}
                </div>
              </div>

              <!-- Availability -->
              <div class="stat bg-gray-100 rounded-lg p-4">
                <div class="stat-title text-sm">Available Spots</div>
                <div class="stat-value text-2xl" :class="trail && trail.available_spots > 0 ? 'text-green-600' : 'text-red-600'">
                  {{ trail?.available_spots }} / {{ trail?.max_capacity }}
                </div>
              </div>

              <!-- Book Now Button -->
              <Button
                variant="solid"
                theme="green"
                size="lg"
                :disabled="!trail || trail.available_spots === 0"
                @click="goToBooking"
                class="w-full"
                :aria-label="trail && trail.available_spots > 0 ? `Book ${trail.title}` : 'Trail is fully booked'"
              >
                <span v-if="trail && trail.available_spots > 0">📅</span>
                <span v-else>🚫</span>
                {{ trail && trail.available_spots > 0 ? 'Book Now' : 'Fully Booked' }}
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Minimal custom styles - most styling via Tailwind/DaisyUI */
</style>
