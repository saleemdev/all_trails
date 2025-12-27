<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Trail } from '../../../types'

const props = defineProps<{
  trail: Trail
}>()

const emit = defineEmits<{
  bookingComplete: [data: any]
}>()

// Form state
const numPeople = ref(1)
const userPhone = ref('')
const userEmail = ref('')
const userFullName = ref('')
const agreeToTerms = ref(false)
const paymentMethod = ref<'mpesa' | 'card'>('mpesa')

// Payment state
const paymentProcessing = ref(false)
const paymentStatus = ref<'idle' | 'processing' | 'success' | 'failed'>('idle')
const paymentMessage = ref('')

// Computed
const totalPrice = computed(() => numPeople.value * (props.trail?.price_kshs || 0))

const isFormValid = computed(() => {
  return (
    numPeople.value > 0 &&
    userPhone.value.trim() !== '' &&
    userEmail.value.trim() !== '' &&
    userFullName.value.trim() !== '' &&
    agreeToTerms.value &&
    totalPrice.value > 0
  )
})

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(price)
}

const initiateMpesaPayment = async () => {
  if (!isFormValid.value) return

  paymentProcessing.value = true
  paymentStatus.value = 'processing'
  paymentMessage.value = 'Initiating M-Pesa STK push...'

  try {
    // Call backend API to initiate M-Pesa STK push
    const response = await fetch('/api/method/all_trails.api.initiate_mpesa_stk_push', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': (window as any).csrf_token,
      },
      body: JSON.stringify({
        phone_number: userPhone.value,
        amount: totalPrice.value,
        trail_id: props.trail.id,
        user_name: userFullName.value,
        user_email: userEmail.value,
        spots_booked: numPeople.value,
      }),
    })

    const result = await response.json()

    if (result.message?.success) {
      paymentStatus.value = 'processing'
      paymentMessage.value = 'Check your phone for the M-Pesa prompt. Enter your PIN to complete payment.'

      // Poll for payment status
      await pollPaymentStatus(result.message.checkout_request_id)
    } else {
      paymentStatus.value = 'failed'
      paymentMessage.value = result.message?.error || 'Failed to initiate payment. Please try again.'
    }
  } catch (error) {
    paymentStatus.value = 'failed'
    paymentMessage.value = 'An error occurred. Please try again.'
    console.error('Payment error:', error)
  } finally {
    paymentProcessing.value = false
  }
}

const pollPaymentStatus = async (checkoutRequestId: string) => {
  // Poll for payment status (every 2 seconds for up to 2 minutes)
  const maxAttempts = 60
  let attempts = 0

  const pollInterval = setInterval(async () => {
    attempts++

    try {
      const response = await fetch(
        `/api/method/all_trails.api.check_mpesa_payment_status?checkout_request_id=${checkoutRequestId}`,
        {
          headers: {
            'X-Frappe-CSRF-Token': (window as any).csrf_token,
          },
        }
      )

      const result = await response.json()

      if (result.message?.paid) {
        clearInterval(pollInterval)
        paymentStatus.value = 'success'
        paymentMessage.value = 'Payment successful! Your booking is confirmed.'

        // Emit booking complete event
        emit('bookingComplete', {
          trail_id: props.trail.id,
          user_name: userFullName.value,
          user_email: userEmail.value,
          phone_number: userPhone.value,
          spots_booked: numPeople.value,
          total_price: totalPrice.value,
          payment_method: 'mpesa',
          checkout_request_id: checkoutRequestId,
        })
      } else if (result.message?.failed) {
        clearInterval(pollInterval)
        paymentStatus.value = 'failed'
        paymentMessage.value = result.message?.error || 'Payment failed. Please try again.'
      }

      if (attempts >= maxAttempts) {
        clearInterval(pollInterval)
        paymentStatus.value = 'processing'
        paymentMessage.value = 'Payment is taking longer than expected. Please check your M-Pesa messages.'
      }
    } catch (error) {
      console.error('Error checking payment status:', error)
    }
  }, 2000)
}

const resetForm = () => {
  numPeople.value = 1
  userPhone.value = ''
  userEmail.value = ''
  userFullName.value = ''
  agreeToTerms.value = false
  paymentStatus.value = 'idle'
  paymentMessage.value = ''
}
</script>

<template>
  <div class="w-full">
    <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
      <h2 class="text-3xl font-black text-gray-900 mb-2">Book This Trail</h2>
      <p class="text-gray-600 mb-8">Complete your booking and secure your spot now</p>

      <!-- Booking Form -->
      <form v-if="paymentStatus === 'idle' || paymentStatus === 'processing' || paymentStatus === 'failed'" @submit.prevent="initiateMpesaPayment" class="space-y-6">
        <!-- Participant Info -->
        <div class="bg-gray-50 rounded-xl p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">Participant Information</h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Full Name -->
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-2">Full Name</label>
              <input
                v-model="userFullName"
                type="text"
                placeholder="John Doe"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
                required
              />
            </div>

            <!-- Email -->
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-2">Email Address</label>
              <input
                v-model="userEmail"
                type="email"
                placeholder="john@example.com"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
                required
              />
            </div>

            <!-- Phone Number -->
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-2">Phone Number (M-Pesa)</label>
              <input
                v-model="userPhone"
                type="tel"
                placeholder="254712345678"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
                required
              />
              <p class="text-xs text-gray-500 mt-1">Include country code (e.g., 254...)</p>
            </div>

            <!-- Number of People -->
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-2">Number of People</label>
              <div class="flex items-center gap-2">
                <button
                  type="button"
                  @click="numPeople = Math.max(1, numPeople - 1)"
                  :disabled="numPeople <= 1"
                  class="px-4 py-3 bg-gray-100 hover:bg-gray-200 disabled:opacity-50 rounded-lg font-bold transition-all"
                >
                  −
                </button>
                <input
                  v-model.number="numPeople"
                  type="number"
                  min="1"
                  :max="trail.available_spots"
                  class="flex-1 px-4 py-3 text-center border-2 border-gray-200 rounded-xl font-bold focus:border-emerald-500 outline-none"
                  required
                />
                <button
                  type="button"
                  @click="numPeople = Math.min(trail.available_spots, numPeople + 1)"
                  :disabled="numPeople >= trail.available_spots"
                  class="px-4 py-3 bg-gray-100 hover:bg-gray-200 disabled:opacity-50 rounded-lg font-bold transition-all"
                >
                  +
                </button>
              </div>
              <p class="text-xs text-gray-500 mt-1">{{ trail.available_spots - numPeople }} spots remaining</p>
            </div>
          </div>
        </div>

        <!-- Price Breakdown -->
        <div class="bg-emerald-50 rounded-xl p-6 border-2 border-emerald-200">
          <div class="space-y-2 mb-4">
            <div class="flex justify-between items-center">
              <span class="text-gray-700">Price per person</span>
              <span class="font-bold text-gray-900">{{ formatPrice(trail.price_kshs) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-700">Number of people</span>
              <span class="font-bold text-gray-900">{{ numPeople }}</span>
            </div>
            <div class="border-t-2 border-emerald-200 pt-2 flex justify-between items-center">
              <span class="text-lg font-bold text-emerald-900">Total Amount</span>
              <span class="text-3xl font-black text-emerald-700">{{ formatPrice(totalPrice) }}</span>
            </div>
          </div>
        </div>

        <!-- Payment Method -->
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-3">Payment Method</label>
          <div class="flex gap-4">
            <label class="flex items-center gap-3 px-4 py-3 border-2 border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-all"
                   :class="paymentMethod === 'mpesa' ? 'border-emerald-500 bg-emerald-50' : ''">
              <input
                v-model="paymentMethod"
                type="radio"
                value="mpesa"
                class="w-4 h-4"
              />
              <span class="font-bold text-gray-900">📱 M-Pesa (STK Push)</span>
            </label>
          </div>
          <p class="text-sm text-gray-600 mt-2">We support M-Pesa payment via STK Push. A prompt will appear on your phone to complete the payment.</p>
        </div>

        <!-- Terms & Conditions -->
        <div class="flex items-start gap-3 p-4 bg-blue-50 rounded-xl border-2 border-blue-200">
          <input
            v-model="agreeToTerms"
            type="checkbox"
            class="w-5 h-5 mt-0.5 cursor-pointer"
            required
          />
          <div>
            <label class="text-sm font-medium text-gray-900 cursor-pointer">
              I agree to the Terms & Conditions and Booking Policy
            </label>
            <p class="text-xs text-gray-600 mt-1">
              By booking, you confirm that you have read and agree to our cancellation policy and safety guidelines.
            </p>
          </div>
        </div>

        <!-- Payment Processing Status -->
        <div v-if="paymentStatus !== 'idle'" :class="[
          'p-4 rounded-xl border-2 font-medium',
          paymentStatus === 'processing' ? 'bg-blue-50 border-blue-200 text-blue-900' :
          'bg-red-50 border-red-200 text-red-900'
        ]">
          <div class="flex items-center gap-2">
            <span v-if="paymentStatus === 'processing'" class="inline-block w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></span>
            <span v-else>✗</span>
            {{ paymentMessage }}
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="!isFormValid || paymentProcessing"
          class="w-full px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-black rounded-xl hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:scale-105"
        >
          <span v-if="!paymentProcessing">Complete Booking - {{ formatPrice(totalPrice) }}</span>
          <span v-else class="flex items-center justify-center gap-2">
            <span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            Processing Payment...
          </span>
        </button>
      </form>

      <!-- Success State -->
      <div v-else class="text-center py-12">
        <div class="text-6xl mb-4">✓</div>
        <h3 class="text-3xl font-black text-emerald-700 mb-2">Booking Confirmed!</h3>
        <p class="text-gray-600 mb-6 max-w-md mx-auto">
          Your booking has been confirmed. A confirmation email has been sent to {{ userEmail }}. You can view your booking in your dashboard.
        </p>
        <div class="flex gap-4 justify-center">
          <button
            @click="resetForm"
            class="px-8 py-3 bg-gray-100 text-gray-900 font-bold rounded-xl hover:bg-gray-200 transition-all"
          >
            Book Another Trail
          </button>
          <RouterLink
            to="/bookings"
            class="px-8 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all"
          >
            View My Bookings
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
