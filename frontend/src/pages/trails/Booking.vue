<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, FormControl, Card, Spinner, Alert } from 'frappe-ui'
import type { Trail, TrailBooking, ExtraActivity } from '../../types/index'
import { useBookingsStore } from '../../stores/bookingsStore'
import { useUiStore } from '../../stores/uiStore'
import { useTrailsStore } from '../../stores/trailsStore'
import { useAuthStore } from '../../stores/authStore'
import { apiService } from '../../services/api'

const route = useRoute()
const router = useRouter()
const bookingsStore = useBookingsStore()
const uiStore = useUiStore()
const trailsStore = useTrailsStore()
const authStore = useAuthStore()

const trail = computed(() => trailsStore.selectedTrail)
const isLoading = computed(() => trailsStore.isLoading)

const spotsBooked = ref(1)
const selectedActivities = ref<Record<string, number>>({}) // activity_id -> quantity
const isSubmitting = ref(false)
const currentStep = ref<'booking' | 'payment' | 'confirm'>('booking')
const createdBooking = ref<TrailBooking | null>(null)
const mpesaPhoneNumber = ref('')
const mpesaReceiptNumber = ref('')
const mpesaTransactionId = ref('')
const isProcessingPayment = ref(false)
const paymentStep = ref<'initiate' | 'confirm'>('initiate')

onMounted(async () => {
  // Check authentication
  if (!authStore.isAuthenticated) {
    router.push({ name: 'Login', query: { 'redirect-to': route.fullPath } })
    return
  }

  // Fetch trail data
  const trailId = route.params.id as string
  if (!trail.value || trail.value.id !== trailId) {
    await trailsStore.fetchTrailById(trailId)
  }

  if (!trail.value) {
    uiStore.showError('Trail not found')
    router.push({ name: 'TrailBrowse' })
  }
})

// Calculate base trail price
const basePrice = computed(() => {
  if (!trail.value) return 0
  return trail.value.price_kshs * spotsBooked.value
})

// Calculate activities price
const activitiesPrice = computed(() => {
  if (!trail.value?.extra_activities) return 0
  let total = 0
  trail.value.extra_activities.forEach(activity => {
    const quantity = selectedActivities.value[activity.id] || 0
    total += activity.price_kshs * quantity
  })
  return total
})

// Total price including activities
const totalPrice = computed(() => {
  return basePrice.value + activitiesPrice.value
})

const maxSpots = computed(() => {
  if (!trail.value) return 0
  return Math.min(trail.value.available_spots, 10)
})

const handleBookingSubmit = async () => {
  if (!trail.value) return

  isSubmitting.value = true
  try {
    // Prepare selected activities for booking
    const activities = trail.value.extra_activities
      ?.filter(activity => selectedActivities.value[activity.id] && selectedActivities.value[activity.id] > 0)
      .map(activity => ({
        activity_id: activity.id,
        activity_name: activity.name,
        quantity: selectedActivities.value[activity.id],
        price: activity.price_kshs
      })) || []

    const booking = await bookingsStore.createBooking(
      trail.value.id,
      spotsBooked.value,
      activities
    )
    createdBooking.value = booking
    currentStep.value = 'payment'
    paymentStep.value = 'initiate'
  } catch (error) {
    uiStore.showError(error instanceof Error ? error.message : 'Failed to create booking')
  } finally {
    isSubmitting.value = false
  }
}

const toggleActivity = (activityId: string) => {
  if (selectedActivities.value[activityId]) {
    // Remove activity
    delete selectedActivities.value[activityId]
  } else {
    // Add activity with quantity 1
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

const handleMpesaPayment = async () => {
  if (!createdBooking.value) {
    uiStore.showError('Booking not found. Please try again.')
    return
  }
  
  if (!mpesaPhoneNumber.value) {
    uiStore.showError('Please enter your MPESA phone number')
    return
  }

  // Validate phone number format (should be 254XXXXXXXXX)
  const phoneRegex = /^254\d{9}$/
  if (!phoneRegex.test(mpesaPhoneNumber.value)) {
    uiStore.showError('Please enter a valid MPESA phone number (format: 254712345678)')
    return
  }

  isProcessingPayment.value = true
  try {
    await apiService.initiateMpesaPayment(createdBooking.value.id, mpesaPhoneNumber.value)
    uiStore.showSuccess('Payment request initiated. Please complete the MPESA payment on your phone.')
    paymentStep.value = 'confirm'
  } catch (error) {
    uiStore.showError(error instanceof Error ? error.message : 'Failed to initiate payment')
  } finally {
    isProcessingPayment.value = false
  }
}

const handleConfirmPayment = async () => {
  if (!createdBooking.value || !mpesaReceiptNumber.value || !mpesaTransactionId.value) {
    uiStore.showError('Please enter both receipt number and transaction ID')
    return
  }

  isProcessingPayment.value = true
  try {
    await apiService.confirmMpesaPayment(
      createdBooking.value.id,
      mpesaReceiptNumber.value,
      mpesaTransactionId.value
    )
    uiStore.showSuccess('Payment confirmed successfully!')
    currentStep.value = 'confirm'
    // Refresh bookings
    await bookingsStore.fetchUserBookings()
  } catch (error) {
    uiStore.showError(error instanceof Error ? error.message : 'Failed to confirm payment')
  } finally {
    isProcessingPayment.value = false
  }
}

const handleSkipPayment = () => {
  currentStep.value = 'confirm'
  uiStore.showSuccess('Booking created! You can complete payment later.')
}

const handleComplete = () => {
  router.push({ name: 'BookingsList' })
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
  <div class="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Back Button -->
      <Button
        variant="ghost"
        @click="router.back()"
        class="mb-6"
      >
        ← Back to Trail
      </Button>

      <!-- Loading State -->
      <Card v-if="isLoading" class="text-center py-16">
        <Spinner class="mx-auto mb-4" />
        <p class="text-lg text-gray-600">Loading trail details...</p>
      </Card>

      <!-- Error State -->
      <Alert v-else-if="!trail" variant="danger" class="mb-6">
        Trail not found. Please go back and try again.
      </Alert>

      <!-- Booking Step -->
      <div v-else-if="currentStep === 'booking' && trail" class="space-y-6">
        <Card>
          <div class="p-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Book Trail</h1>
            <h2 class="text-xl text-emerald-700 mb-6">{{ trail.title }}</h2>

            <div class="space-y-6">
              <FormControl
                label="Number of Spots"
                type="number"
                v-model="spotsBooked"
                :min="1"
                :max="maxSpots"
                class="mb-4"
              />
              <p class="text-sm text-gray-600 mb-4">Available: {{ trail.available_spots }} spots</p>

              <!-- Long Weekend Badge -->
              <div v-if="trail.is_long_weekend" class="bg-blue-50 border-2 border-blue-200 rounded-lg p-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="text-sm font-bold text-blue-900">Long Weekend Available</span>
              </div>

              <!-- Extra Activities Section -->
              <div v-if="trail.extra_activities && trail.extra_activities.length > 0" class="space-y-4">
                <div class="flex items-center gap-2">
                  <h3 class="text-lg font-bold text-gray-900">Extra Activities</h3>
                  <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-bold">
                    Optional
                  </span>
                </div>
                <p class="text-sm text-gray-600">
                  <span class="font-semibold text-gray-700">Optional:</span> Enhance your trail experience with additional activities. 
                  <span class="font-semibold text-emerald-700">Each activity adds extra cost.</span>
                </p>
                
                <div class="space-y-3">
                  <div
                    v-for="activity in trail.extra_activities"
                    :key="activity.id"
                    class="border-2 rounded-xl p-4 transition-all"
                    :class="isActivitySelected(activity.id)
                      ? 'border-emerald-500 bg-emerald-50'
                      : activity.available
                        ? 'border-gray-200 hover:border-emerald-300 bg-white'
                        : 'border-gray-100 bg-gray-50 opacity-60'"
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
                      
                      <div v-if="activity.available" class="flex items-center gap-2">
                        <button
                          v-if="!isActivitySelected(activity.id)"
                          @click="toggleActivity(activity.id)"
                          class="px-4 py-2 bg-emerald-600 text-white font-bold rounded-lg hover:bg-emerald-700 transition-colors text-sm shadow-md hover:shadow-lg"
                          :aria-label="`Add ${activity.name} for ${formatPrice(activity.price_kshs)} extra`"
                        >
                          Add (+{{ formatPrice(activity.price_kshs) }})
                        </button>
                        <div v-else class="flex items-center gap-2">
                          <button
                            @click="updateActivityQuantity(activity.id, (selectedActivities[activity.id] || 1) - 1)"
                            class="w-8 h-8 rounded-lg bg-gray-200 hover:bg-gray-300 font-bold flex items-center justify-center transition-colors"
                          >
                            −
                          </button>
                          <input
                            type="number"
                            :value="selectedActivities[activity.id] || 1"
                            @input="updateActivityQuantity(activity.id, parseInt(($event.target as HTMLInputElement).value) || 0)"
                            :min="1"
                            :max="activity.max_participants || activity.available_spots || 10"
                            class="w-16 text-center border-2 border-gray-200 rounded-lg py-1 font-bold"
                          />
                          <button
                            @click="updateActivityQuantity(activity.id, (selectedActivities[activity.id] || 1) + 1)"
                            :disabled="(selectedActivities[activity.id] || 1) >= (activity.max_participants || activity.available_spots || 10)"
                            class="w-8 h-8 rounded-lg bg-gray-200 hover:bg-gray-300 font-bold flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            +
                          </button>
                          <button
                            @click="toggleActivity(activity.id)"
                            class="ml-2 px-3 py-1 text-red-600 hover:bg-red-50 rounded-lg font-bold text-sm transition-colors"
                          >
                            Remove
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Price Summary -->
              <div class="bg-gray-50 rounded-lg p-4 space-y-2">
                <div class="flex justify-between">
                  <span>Price per person</span>
                  <span>{{ formatPrice(trail.price_kshs) }}</span>
                </div>
                <div class="flex justify-between">
                  <span>Number of spots</span>
                  <span>{{ spotsBooked }}</span>
                </div>
                <div class="flex justify-between">
                  <span>Base total</span>
                  <span>{{ formatPrice(basePrice) }}</span>
                </div>
                <div v-if="activitiesPrice > 0" class="flex justify-between text-emerald-700 font-semibold">
                  <span>Extra activities (optional)</span>
                  <span>+{{ formatPrice(activitiesPrice) }}</span>
                </div>
                <div v-else-if="trail.extra_activities && trail.extra_activities.length > 0" class="flex justify-between text-xs text-gray-500 italic">
                  <span>No extra activities selected</span>
                  <span>+{{ formatPrice(0) }}</span>
                </div>
                <div class="flex justify-between font-bold text-lg pt-2 border-t border-gray-200">
                  <span>Total Price</span>
                  <span class="text-emerald-700">{{ formatPrice(totalPrice) }}</span>
                </div>
              </div>

              <div class="flex gap-4 pt-4">
                <Button variant="outline" @click="router.back()" class="flex-1">
                  Cancel
                </Button>
                <Button
                  variant="solid"
                  theme="green"
                  :loading="isSubmitting"
                  @click="handleBookingSubmit"
                  class="flex-1"
                >
                  {{ isSubmitting ? 'Creating...' : 'Continue to Payment' }}
                </Button>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Payment Step -->
      <div v-else-if="currentStep === 'payment' && createdBooking" class="space-y-6">
        <Card>
          <div class="p-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-6">Complete Payment</h1>
            <div class="text-center mb-6">
              <p class="text-2xl font-bold text-emerald-700">Total: {{ formatPrice(createdBooking.total_price) }}</p>
            </div>

            <!-- Initiate Payment -->
            <div v-if="paymentStep === 'initiate'" class="space-y-6">
              <FormControl
                label="MPESA Phone Number"
                type="tel"
                v-model="mpesaPhoneNumber"
                placeholder="254712345678"
                class="mb-4"
              />
              <p class="text-sm text-gray-600 mb-4">
                Enter your MPESA phone number (format: 254712345678)
              </p>
              <div class="bg-blue-50 rounded-lg p-4 space-y-2">
                <p>📱 You will receive an MPESA prompt on your phone</p>
                <p>💰 Amount: {{ formatPrice(createdBooking.total_price) }}</p>
              </div>
            </div>

            <!-- Confirm Payment -->
            <div v-else-if="paymentStep === 'confirm'" class="space-y-6">
              <FormControl
                label="MPESA Receipt Number"
                type="text"
                v-model="mpesaReceiptNumber"
                placeholder="Enter receipt number"
                class="mb-4"
              />
              <FormControl
                label="MPESA Transaction ID"
                type="text"
                v-model="mpesaTransactionId"
                placeholder="Enter transaction ID"
                class="mb-4"
              />
              <div class="bg-green-50 rounded-lg p-4">
                <p>✅ Enter the details from your MPESA confirmation message</p>
              </div>
            </div>

            <div class="flex gap-4 pt-6">
              <Button variant="outline" @click="currentStep = 'booking'" class="flex-1">
                Back
              </Button>
              <Button
                v-if="paymentStep === 'initiate'"
                variant="outline"
                @click="handleSkipPayment"
                class="flex-1"
              >
                Pay Later
              </Button>
              <Button
                v-if="paymentStep === 'initiate'"
                variant="solid"
                theme="green"
                :loading="isProcessingPayment"
                :disabled="!mpesaPhoneNumber"
                @click="handleMpesaPayment"
                class="flex-1"
              >
                {{ isProcessingPayment ? 'Processing...' : 'Initiate Payment' }}
              </Button>
              <Button
                v-else
                variant="solid"
                theme="green"
                :loading="isProcessingPayment"
                :disabled="!mpesaReceiptNumber || !mpesaTransactionId"
                @click="handleConfirmPayment"
                class="flex-1"
              >
                {{ isProcessingPayment ? 'Confirming...' : 'Confirm Payment' }}
              </Button>
            </div>
          </div>
        </Card>
      </div>

      <!-- Confirmation Step -->
      <div v-else-if="currentStep === 'confirm' && createdBooking" class="space-y-6">
        <Card>
          <div class="p-8 text-center">
            <div class="text-6xl mb-4">✅</div>
            <h1 class="text-3xl font-bold mb-4">Booking Confirmed!</h1>
            <div class="bg-gray-50 rounded-lg p-6 space-y-3 text-left max-w-md mx-auto">
              <div class="flex justify-between">
                <span class="font-medium text-gray-600">Confirmation Code:</span>
                <span class="font-mono font-bold text-emerald-700">{{ createdBooking.confirmation_code }}</span>
              </div>
              <div class="flex justify-between">
                <span class="font-medium text-gray-600">Trail:</span>
                <span class="font-semibold">{{ trail?.title }}</span>
              </div>
              <div class="flex justify-between">
                <span class="font-medium text-gray-600">Date:</span>
                <span>{{ new Date(trail?.scheduled_date || '').toLocaleDateString() }}</span>
              </div>
              <div class="flex justify-between">
                <span class="font-medium text-gray-600">Spots:</span>
                <span>{{ createdBooking.spots_booked }}</span>
              </div>
              <div v-if="createdBooking.selected_activities && createdBooking.selected_activities.length > 0" class="space-y-1 pt-2 border-t border-gray-200">
                <div class="text-xs font-bold text-gray-500 mb-1">Extra Activities:</div>
                <div
                  v-for="activity in createdBooking.selected_activities"
                  :key="activity.activity_id"
                  class="flex justify-between text-sm"
                >
                  <span class="text-gray-600">{{ activity.activity_name }} (×{{ activity.quantity }})</span>
                  <span class="font-medium">{{ formatPrice(activity.price * activity.quantity) }}</span>
                </div>
              </div>
              <div class="flex justify-between font-bold pt-2 border-t-2 border-gray-300">
                <span>Total:</span>
                <span class="text-emerald-700">{{ formatPrice(createdBooking.total_price) }}</span>
              </div>
            </div>
            <div class="mt-6">
              <Button variant="solid" theme="green" @click="handleComplete" size="lg">
                View My Bookings
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

