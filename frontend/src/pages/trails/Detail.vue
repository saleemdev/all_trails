<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTrailsStore } from '../../stores/trailsStore'
import { useUiStore } from '../../stores/uiStore'
import { useAuthStore } from '../../stores/authStore'
import BookingForm from '../../components/features/trails/BookingForm.vue'

const route = useRoute()
const router = useRouter()
const trailsStore = useTrailsStore()
const uiStore = useUiStore()
const authStore = useAuthStore()

const trail = computed(() => trailsStore.selectedTrail)
const isLoading = computed(() => trailsStore.isLoading)
const error = computed(() => trailsStore.error)

const showBookingForm = ref(false)

onMounted(() => {
  const trailId = route.params.id as string
  trailsStore.fetchTrailById(trailId)
})

const toggleBookingForm = () => {
  if (!authStore.isAuthenticated) {
    window.location.href = '/app/login'
    return
  }
  showBookingForm.value = !showBookingForm.value
}

const handleBookingComplete = () => {
  // Handle successful booking completion
  showBookingForm.value = false
  uiStore.showSuccess('Booking created successfully!')
  // Optionally redirect to bookings list
  setTimeout(() => {
    router.push({ name: 'BookingsList' })
  }, 1500)
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
  <div class="max-w-7xl mx-auto">
    <button @click="$router.back()" class="btn btn-ghost gap-2 mb-6">
      <span>←</span> Back
    </button>

    <!-- Loading State -->
    <div v-if="isLoading" class="card bg-base-100 shadow-md">
      <div class="card-body items-center text-center py-16">
        <span class="loading loading-spinner loading-lg text-primary"></span>
        <p class="text-lg text-neutral mt-4">Loading trail details...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-error shadow-lg">
      <div class="flex flex-col sm:flex-row items-center gap-4 w-full">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="flex-1">{{ error }}</span>
        <button @click="trailsStore.fetchTrailById(route.params.id as string)" class="btn btn-sm btn-ghost">
          Retry
        </button>
      </div>
    </div>

    <!-- Trail Detail -->
    <div v-else-if="trail" class="space-y-6">
      <!-- Header Card -->
      <div class="card bg-gradient-to-br from-primary to-primary-light text-primary-content shadow-xl">
        <div class="card-body p-8 lg:p-12">
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
      </div>

      <!-- Main Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Trail Information -->
        <div class="lg:col-span-2">
          <div class="card bg-base-100 shadow-md">
            <div class="card-body p-6">
              <h2 class="card-title text-2xl text-primary font-display mb-4">
                Trail Information
              </h2>

              <div class="grid grid-cols-2 gap-6">
                <div class="stat bg-base-200 rounded-lg p-4">
                  <div class="stat-title text-sm">Difficulty</div>
                  <div class="stat-value text-2xl text-primary">{{ trail.difficulty_level }}</div>
                </div>

                <div class="stat bg-base-200 rounded-lg p-4">
                  <div class="stat-title text-sm">Distance</div>
                  <div class="stat-value text-2xl text-primary">{{ trail.distance_km }} km</div>
                </div>

                <div class="stat bg-base-200 rounded-lg p-4">
                  <div class="stat-title text-sm">Duration</div>
                  <div class="stat-value text-2xl text-primary">{{ trail.duration_hours }}h</div>
                </div>

                <div class="stat bg-base-200 rounded-lg p-4">
                  <div class="stat-title text-sm">Elevation</div>
                  <div class="stat-value text-2xl text-primary">{{ trail.elevation_gain_m }}m</div>
                </div>

                <div class="stat bg-base-200 rounded-lg p-4">
                  <div class="stat-title text-sm">Date</div>
                  <div class="stat-value text-lg text-primary">
                    {{ new Date(trail.scheduled_date).toLocaleDateString() }}
                  </div>
                </div>

                <div class="stat bg-base-200 rounded-lg p-4">
                  <div class="stat-title text-sm">Time</div>
                  <div class="stat-value text-lg text-primary">
                    {{ trail.start_time }} - {{ trail.end_time }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Booking Section -->
        <div class="lg:col-span-1">
          <div v-if="!showBookingForm" class="card bg-base-100 shadow-md border-2 border-base-300">
            <div class="card-body p-6 space-y-6">
              <h2 class="card-title text-2xl text-primary font-display">
                Booking
              </h2>

              <!-- Price Display -->
              <div class="stat bg-base-200 rounded-lg p-4">
                <div class="stat-title text-sm">Price per person</div>
                <div class="stat-value text-3xl text-secondary">
                  {{ formatPrice(trail.price_kshs) }}
                </div>
              </div>

              <!-- Availability -->
              <div class="stat bg-base-200 rounded-lg p-4">
                <div class="stat-title text-sm">Available Spots</div>
                <div class="stat-value text-2xl" :class="trail.available_spots > 0 ? 'text-success' : 'text-error'">
                  {{ trail.available_spots }} / {{ trail.max_capacity }}
                </div>
              </div>

              <!-- Book Now Button -->
              <button
                @click="toggleBookingForm"
                :disabled="trail.available_spots === 0"
                class="btn btn-secondary btn-block btn-lg gap-2"
              >
                <span v-if="trail.available_spots > 0">📅</span>
                <span v-else>🚫</span>
                {{ trail.available_spots > 0 ? 'Book Now' : 'Fully Booked' }}
              </button>
            </div>
          </div>

          <!-- Booking Form Component -->
          <div v-else>
            <BookingForm :trail="trail" @bookingComplete="handleBookingComplete" />
            <button
              @click="toggleBookingForm"
              class="btn btn-ghost btn-block mt-4"
            >
              Back to Trail Info
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Minimal custom styles - most styling via Tailwind/DaisyUI */
</style>
