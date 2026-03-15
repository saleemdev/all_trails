<script setup lang="ts">
import { ref, computed, watch, onUnmounted } from 'vue'
import { Dialog, Button, FormControl } from 'frappe-ui'
import type { Trail, TrailBooking, ExtraActivity } from '../../../types/index'
import { useBookingsStore } from '../../../stores/bookingsStore'
import { useUiStore } from '../../../stores/uiStore'
import { apiService } from '../../../services/api'
import { isValidKenyanMpesaPhone, maskKenyanPhone, normalizeKenyanMpesaPhone } from '../../../utils/payments'

const props = defineProps<{
  trail: Trail | null
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const bookingsStore = useBookingsStore()
const uiStore = useUiStore()

// Create a local computed for v-model binding
const isOpen = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value)
})

const spotsBooked = ref(1)
const selectedActivities = ref<Record<string, number>>({}) // activity_id -> quantity
const isSubmitting = ref(false)
const currentStep = ref<'booking' | 'payment' | 'confirm'>('booking')
const createdBooking = ref<TrailBooking | null>(null)
const mpesaPhoneNumber = ref('')
const isProcessingPayment = ref(false)
const paymentStep = ref<'initiate' | 'processing' | 'failed'>('initiate')
const activePaymentId = ref('')
const paymentStatusMessage = ref('')
const paymentReceiptNumber = ref('')

let paymentPollHandle: ReturnType<typeof setInterval> | null = null
let paymentPollAttempts = 0
const maxPaymentPollAttempts = 30

// Reset form function
const resetForm = () => {
  clearPaymentPolling()
  spotsBooked.value = 1
  selectedActivities.value = {}
  isSubmitting.value = false
  currentStep.value = 'booking'
  createdBooking.value = null
  mpesaPhoneNumber.value = ''
  isProcessingPayment.value = false
  paymentStep.value = 'initiate'
  activePaymentId.value = ''
  paymentStatusMessage.value = ''
  paymentReceiptNumber.value = ''
}

// Watch for modal close to reset form
watch(() => props.modelValue, (isOpen, wasOpen) => {
  console.log('BookingModal modelValue changed:', { isOpen, wasOpen, trail: props.trail })
  
  // Only reset when modal closes (was open, now closed)
  // Don't reset when opening to avoid clearing user input
  if (wasOpen && !isOpen) {
    resetForm()
  }
  // Reset when opening if there's leftover state from a previous booking
  if (isOpen && !wasOpen && (createdBooking.value || currentStep.value !== 'booking')) {
    resetForm()
  }
  
  // When opening, ensure form is reset
  if (isOpen && !wasOpen) {
    resetForm()
  }
})

// Calculate base trail price
const basePrice = computed(() => {
  if (!props.trail) return 0
  return props.trail.price_kshs * spotsBooked.value
})

// Calculate activities price
const activitiesPrice = computed(() => {
  if (!props.trail?.extra_activities) return 0
  let total = 0
  props.trail.extra_activities.forEach(activity => {
    const quantity = selectedActivities.value[activity.id] || 0
    total += activity.price_kshs * quantity
  })
  return total
})

// Total price including activities
const totalPrice = computed(() => {
  return basePrice.value + activitiesPrice.value
})

const maskedMpesaPhoneNumber = computed(() => maskKenyanPhone(mpesaPhoneNumber.value))

const maxSpots = computed(() => {
  if (!props.trail) return 0
  return Math.min(props.trail.available_spots, 10)
})

const handleBookingSubmit = async () => {
  if (!props.trail) return

  isSubmitting.value = true
  try {
    // Prepare selected activities for booking
    const activities = props.trail.extra_activities
      ?.filter(activity => selectedActivities.value[activity.id] && selectedActivities.value[activity.id] > 0)
      .map(activity => ({
        activity_id: activity.id,
        activity_name: activity.name,
        quantity: selectedActivities.value[activity.id],
        price: activity.price_kshs
      })) || []

    const booking = await bookingsStore.createBooking(
      props.trail.id,
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

const clearPaymentPolling = () => {
  if (paymentPollHandle) {
    clearInterval(paymentPollHandle)
    paymentPollHandle = null
  }
  paymentPollAttempts = 0
}

const updateBookingPaymentState = (receiptNumber?: string, transactionId?: string) => {
  if (!createdBooking.value) {
    return
  }

  createdBooking.value.payment_status = 'Completed'
  createdBooking.value.status = 'Confirmed'
  createdBooking.value.payment_method = 'MPESA'
  createdBooking.value.mpesa_phone_number = normalizeKenyanMpesaPhone(mpesaPhoneNumber.value)
  createdBooking.value.mpesa_receipt_number = receiptNumber
  createdBooking.value.mpesa_transaction_id = transactionId
}

const finishSuccessfulPayment = async (paymentState: any) => {
  clearPaymentPolling()
  paymentReceiptNumber.value = paymentState.receipt_number || ''
  updateBookingPaymentState(paymentState.receipt_number, paymentState.provider_transaction_id)
  uiStore.showSuccess(paymentState.message || 'Payment confirmed successfully!')
  currentStep.value = 'confirm'
  await bookingsStore.fetchUserBookings()
  emit('success')
}

const checkPaymentStatus = async (paymentId: string) => {
  const paymentState = await apiService.getMpesaPaymentStatus(paymentId)
  paymentStatusMessage.value = paymentState.message || paymentState.status

  if (paymentState.paid) {
    await finishSuccessfulPayment(paymentState)
    return
  }

  if (paymentState.failed) {
    clearPaymentPolling()
    paymentStep.value = 'failed'
    uiStore.showError(paymentState.message || 'MPESA payment did not complete successfully.')
    return
  }

  paymentStep.value = 'processing'
}

const startPaymentPolling = async (paymentId: string) => {
  clearPaymentPolling()
  paymentPollAttempts = 0

  const poll = async () => {
    paymentPollAttempts += 1
    try {
      await checkPaymentStatus(paymentId)
    } catch (error) {
      if (paymentPollAttempts >= maxPaymentPollAttempts) {
        clearPaymentPolling()
        paymentStatusMessage.value = 'Still waiting for confirmation. You can keep this modal open and check again shortly.'
      }
      if (error instanceof Error) {
        console.error('Payment status polling failed:', error)
      }
    }

    if (paymentPollAttempts >= maxPaymentPollAttempts) {
      clearPaymentPolling()
    }
  }

  await poll()
  if (currentStep.value === 'payment' && paymentStep.value === 'processing') {
    paymentPollHandle = setInterval(() => {
      void poll()
    }, 3000)
  }
}

const resetPaymentState = () => {
  clearPaymentPolling()
  activePaymentId.value = ''
  paymentStatusMessage.value = ''
  paymentReceiptNumber.value = ''
  paymentStep.value = 'initiate'
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

  const normalizedPhone = normalizeKenyanMpesaPhone(mpesaPhoneNumber.value)
  if (!isValidKenyanMpesaPhone(normalizedPhone)) {
    uiStore.showError('Please enter a valid MPESA phone number (format: 254712345678)')
    return
  }

  isProcessingPayment.value = true
  try {
    mpesaPhoneNumber.value = normalizedPhone
    const paymentResponse = await apiService.initiateMpesaPayment({
      journey_type: 'Trail Booking',
      reference_name: createdBooking.value.id,
      reference_doctype: 'Trail Booking',
      phone_number: normalizedPhone,
      amount: createdBooking.value.total_price,
      metadata: {
        trail_id: props.trail?.id || '',
        trail_title: props.trail?.title || '',
        confirmation_code: createdBooking.value.confirmation_code,
      },
    })

    activePaymentId.value = paymentResponse.payment_id
    paymentStatusMessage.value = paymentResponse.message

    if (!paymentResponse.success) {
      paymentStep.value = 'failed'
      uiStore.showError(paymentResponse.message || 'Failed to initiate payment')
      return
    }

    paymentStep.value = 'processing'
    uiStore.showSuccess('Payment prompt sent. Complete the MPESA prompt on your phone.')
    await startPaymentPolling(paymentResponse.payment_id)
  } catch (error) {
    uiStore.showError(error instanceof Error ? error.message : 'Failed to initiate payment')
  } finally {
    isProcessingPayment.value = false
  }
}

const handleRefreshPaymentStatus = async () => {
  if (!activePaymentId.value) {
    uiStore.showError('Payment session not found. Please retry the payment.')
    return
  }

  isProcessingPayment.value = true
  try {
    await checkPaymentStatus(activePaymentId.value)
  } catch (error) {
    uiStore.showError(error instanceof Error ? error.message : 'Failed to refresh payment status')
  } finally {
    isProcessingPayment.value = false
  }
}

const handleSkipPayment = () => {
  clearPaymentPolling()
  currentStep.value = 'confirm'
  uiStore.showSuccess('Booking created! You can complete payment later.')
}

const handleComplete = () => {
  resetForm()
  emit('success')
  emit('update:modelValue', false)
}

const handleCancel = () => {
  resetForm()
  emit('update:modelValue', false)
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(price)
}

const dialogTitle = computed(() => {
  if (currentStep.value === 'booking') return 'Book Trail'
  if (currentStep.value === 'payment') return 'Complete Payment'
  return 'Booking Confirmed!'
})

onUnmounted(() => {
  clearPaymentPolling()
})
</script>

<template>
  <Dialog
    v-model="isOpen"
    :title="dialogTitle"
  >
    <!-- Booking Step -->
    <div v-if="currentStep === 'booking' && trail" class="space-y-6">
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
            <span class="font-semibold brand-text">Each activity adds extra cost.</span>
          </p>
          
          <div class="space-y-3">
            <div
              v-for="activity in trail.extra_activities"
              :key="activity.id"
              class="border-2 rounded-xl p-4 transition-all"
              :class="isActivitySelected(activity.id)
                ? 'border-[color:var(--color-border-strong)] bg-[rgba(49,83,72,0.08)]'
                : activity.available
                  ? 'border-gray-200 hover:border-[color:var(--color-border-strong)] bg-white'
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
                    <span class="font-bold brand-text">+{{ formatPrice(activity.price_kshs) }} <span class="text-gray-500 font-normal">extra</span></span>
                    <span v-if="activity.max_participants" class="text-gray-500">Max: {{ activity.max_participants }} people</span>
                    <span v-if="activity.available_spots !== undefined" class="text-gray-500">Available: {{ activity.available_spots }} spots</span>
                  </div>
                </div>
                
                <div v-if="activity.available" class="flex items-center gap-2">
                  <button
                    v-if="!isActivitySelected(activity.id)"
                    @click="toggleActivity(activity.id)"
                    class="brand-button px-4 py-2 text-sm"
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
          <div v-if="activitiesPrice > 0" class="flex justify-between brand-text font-semibold">
            <span>Extra activities (optional)</span>
            <span>+{{ formatPrice(activitiesPrice) }}</span>
          </div>
          <div v-else-if="trail.extra_activities && trail.extra_activities.length > 0" class="flex justify-between text-xs text-gray-500 italic">
            <span>No extra activities selected</span>
            <span>+{{ formatPrice(0) }}</span>
          </div>
          <div class="flex justify-between font-bold text-lg pt-2 border-t border-gray-200">
            <span>Total Price</span>
            <span class="brand-text">{{ formatPrice(totalPrice) }}</span>
          </div>
        </div>

        <div class="page-header text-white rounded-lg p-4">
          <h3 class="font-bold mb-1">{{ trail.title }}</h3>
          <p class="text-sm opacity-90">
            {{ new Date(trail.scheduled_date).toLocaleDateString() }} at {{ trail.start_time }}
          </p>
        </div>
      </div>

      <!-- Payment Step -->
      <div v-else-if="currentStep === 'payment' && createdBooking" class="space-y-6">
        <div class="text-center mb-6">
          <h3 class="text-xl font-bold mb-2">Complete Payment</h3>
          <p class="text-2xl font-bold brand-text">Total: {{ formatPrice(createdBooking.total_price) }}</p>
        </div>

        <!-- Initiate Payment -->
        <div v-if="paymentStep === 'initiate'">
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

        <!-- Awaiting Callback -->
        <div v-else-if="paymentStep === 'processing'" class="space-y-4">
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-2">
            <p class="font-semibold text-blue-900">Waiting for MPESA confirmation</p>
            <p class="text-sm text-blue-900">
              Complete the prompt on {{ maskedMpesaPhoneNumber }}. This modal checks your payment automatically.
            </p>
            <p class="text-sm text-blue-800">
              {{ paymentStatusMessage || 'Prompt sent. Enter your PIN on your phone to finish payment.' }}
            </p>
            <p v-if="activePaymentId" class="text-xs text-blue-700">
              Payment reference: {{ activePaymentId }}
            </p>
          </div>
        </div>

        <!-- Failed / Retry -->
        <div v-else-if="paymentStep === 'failed'" class="space-y-4">
          <div class="bg-red-50 border border-red-200 rounded-lg p-4 space-y-2">
            <p class="font-semibold text-red-900">Payment did not complete</p>
            <p class="text-sm text-red-800">
              {{ paymentStatusMessage || 'The MPESA prompt was not completed successfully. You can retry or pay later.' }}
            </p>
            <p v-if="paymentReceiptNumber" class="text-xs text-red-700">
              Last receipt: {{ paymentReceiptNumber }}
            </p>
          </div>
        </div>
      </div>

      <!-- Confirmation Step -->
      <div v-else-if="currentStep === 'confirm' && createdBooking" class="text-center space-y-6">
        <div class="text-6xl mb-4">✅</div>
        <h3 class="text-2xl font-bold">Booking Confirmed!</h3>
        <div class="bg-gray-50 rounded-lg p-4 space-y-3 text-left">
          <div class="flex justify-between">
            <span class="font-medium text-gray-600">Confirmation Code:</span>
            <span class="font-mono font-bold brand-text">{{ createdBooking.confirmation_code }}</span>
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
            <span class="brand-text">{{ formatPrice(createdBooking.total_price) }}</span>
          </div>
        </div>
      </div>

    <template #footer>
      <!-- Booking Step Actions -->
      <div v-if="currentStep === 'booking'" class="flex gap-2">
        <Button variant="outline" @click="handleCancel">Cancel</Button>
        <Button
          variant="solid"
          theme="gray"
          :loading="isSubmitting"
          @click="handleBookingSubmit"
        >
          {{ isSubmitting ? 'Creating...' : 'Continue to Payment' }}
        </Button>
      </div>

      <!-- Payment Step Actions -->
      <div v-else-if="currentStep === 'payment'" class="flex gap-2">
        <Button variant="outline" @click="resetPaymentState(); currentStep = 'booking'">Back</Button>
        <Button
          v-if="paymentStep !== 'processing'"
          variant="outline"
          @click="handleSkipPayment"
        >
          Pay Later
        </Button>
        <Button
          v-if="paymentStep === 'initiate'"
          variant="solid"
          theme="gray"
          :loading="isProcessingPayment"
          :disabled="!mpesaPhoneNumber"
          @click="handleMpesaPayment"
        >
          {{ isProcessingPayment ? 'Sending Prompt...' : 'Pay via MPESA' }}
        </Button>
        <Button
          v-else-if="paymentStep === 'processing'"
          variant="solid"
          theme="gray"
          :loading="isProcessingPayment"
          :disabled="!activePaymentId"
          @click="handleRefreshPaymentStatus"
        >
          {{ isProcessingPayment ? 'Checking...' : 'Check Again' }}
        </Button>
        <Button
          v-else
          variant="solid"
          theme="gray"
          :loading="isProcessingPayment"
          @click="resetPaymentState"
        >
          Retry Payment
        </Button>
      </div>

      <!-- Confirmation Step Actions -->
      <div v-else-if="currentStep === 'confirm'">
        <Button variant="solid" theme="gray" @click="handleComplete">Done</Button>
      </div>
    </template>
  </Dialog>
</template>

<style scoped>
/* Additional styling if needed */
</style>
