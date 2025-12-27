<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Trail, TrailBooking } from '../../../types/index'
import { useBookingsStore } from '../../../stores/bookingsStore'
import { useUiStore } from '../../../stores/uiStore'
import { apiService } from '../../../services/api'

const props = defineProps<{
  trail: Trail | null
}>()

const emit = defineEmits<{
  close: []
  success: []
}>()

const bookingsStore = useBookingsStore()
const uiStore = useUiStore()

const spotsBooked = ref(1)
const isSubmitting = ref(false)
const currentStep = ref<'booking' | 'payment' | 'confirm'>('booking')
const createdBooking = ref<TrailBooking | null>(null)
const mpesaPhoneNumber = ref('')
const mpesaReceiptNumber = ref('')
const mpesaTransactionId = ref('')
const isProcessingPayment = ref(false)
const paymentStep = ref<'initiate' | 'confirm'>('initiate')

const totalPrice = computed(() => {
  if (!props.trail) return 0
  return props.trail.price_kshs * spotsBooked.value
})

const maxSpots = computed(() => {
  if (!props.trail) return 0
  return Math.min(props.trail.available_spots, 10)
})

const handleBookingSubmit = async () => {
  if (!props.trail) return

  isSubmitting.value = true
  try {
    const booking = await bookingsStore.createBooking(props.trail.id, spotsBooked.value)
    createdBooking.value = booking
    currentStep.value = 'payment'
    paymentStep.value = 'initiate'
  } catch (error) {
    uiStore.showError(error instanceof Error ? error.message : 'Failed to create booking')
  } finally {
    isSubmitting.value = false
  }
}

const handleMpesaPayment = async () => {
  if (!createdBooking.value || !mpesaPhoneNumber.value) return

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
  emit('success')
  emit('close')
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
  <div class="modal-overlay" @click="emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Book Trail</h2>
        <button class="close-btn" @click="emit('close')">×</button>
      </div>

      <div class="modal-body">
        <!-- Booking Step -->
        <div v-if="currentStep === 'booking' && trail" class="booking-form">
          <div class="form-group">
            <label for="spots">Number of Spots</label>
            <div class="spots-selector">
              <button
                @click="spotsBooked = Math.max(1, spotsBooked - 1)"
                :disabled="spotsBooked <= 1"
                class="spot-btn"
              >
                −
              </button>
              <input
                id="spots"
                v-model.number="spotsBooked"
                type="number"
                :min="1"
                :max="maxSpots"
                class="spot-input"
              />
              <button
                @click="spotsBooked = Math.min(maxSpots, spotsBooked + 1)"
                :disabled="spotsBooked >= maxSpots"
                class="spot-btn"
              >
                +
              </button>
            </div>
            <p class="help-text">Available: {{ trail.available_spots }} spots</p>
          </div>

          <div class="price-summary">
            <div class="summary-row">
              <span>Price per person</span>
              <span>{{ formatPrice(trail.price_kshs) }}</span>
            </div>
            <div class="summary-row">
              <span>Number of spots</span>
              <span>{{ spotsBooked }}</span>
            </div>
            <div class="summary-row total">
              <span>Total Price</span>
              <span>{{ formatPrice(totalPrice) }}</span>
            </div>
          </div>

          <div class="trail-info">
            <h3>{{ trail.title }}</h3>
            <p>{{ new Date(trail.scheduled_date).toLocaleDateString() }} at {{ trail.start_time }}</p>
          </div>
        </div>

        <!-- Payment Step -->
        <div v-else-if="currentStep === 'payment' && createdBooking" class="payment-form">
          <div class="payment-header">
            <h3>Complete Payment</h3>
            <p class="payment-amount">Total: {{ formatPrice(createdBooking.total_price) }}</p>
          </div>

          <!-- Initiate Payment -->
          <div v-if="paymentStep === 'initiate'" class="payment-section">
            <div class="form-group">
              <label for="mpesa-phone">MPESA Phone Number</label>
              <input
                id="mpesa-phone"
                v-model="mpesaPhoneNumber"
                type="tel"
                placeholder="254712345678"
                class="form-input"
              />
              <p class="help-text">Enter your MPESA phone number (format: 254712345678)</p>
            </div>
            <div class="payment-info">
              <p>📱 You will receive an MPESA prompt on your phone</p>
              <p>💰 Amount: {{ formatPrice(createdBooking.total_price) }}</p>
            </div>
          </div>

          <!-- Confirm Payment -->
          <div v-else-if="paymentStep === 'confirm'" class="payment-section">
            <div class="form-group">
              <label for="receipt-number">MPESA Receipt Number</label>
              <input
                id="receipt-number"
                v-model="mpesaReceiptNumber"
                type="text"
                placeholder="Enter receipt number"
                class="form-input"
              />
            </div>
            <div class="form-group">
              <label for="transaction-id">MPESA Transaction ID</label>
              <input
                id="transaction-id"
                v-model="mpesaTransactionId"
                type="text"
                placeholder="Enter transaction ID"
                class="form-input"
              />
            </div>
            <div class="payment-info">
              <p>✅ Enter the details from your MPESA confirmation message</p>
            </div>
          </div>
        </div>

        <!-- Confirmation Step -->
        <div v-else-if="currentStep === 'confirm' && createdBooking" class="confirmation-form">
          <div class="confirmation-icon">✅</div>
          <h3>Booking Confirmed!</h3>
          <div class="confirmation-details">
            <div class="confirmation-item">
              <span class="label">Confirmation Code:</span>
              <span class="value code">{{ createdBooking.confirmation_code }}</span>
            </div>
            <div class="confirmation-item">
              <span class="label">Trail:</span>
              <span class="value">{{ trail?.title }}</span>
            </div>
            <div class="confirmation-item">
              <span class="label">Date:</span>
              <span class="value">{{ new Date(trail?.scheduled_date || '').toLocaleDateString() }}</span>
            </div>
            <div class="confirmation-item">
              <span class="label">Spots:</span>
              <span class="value">{{ createdBooking.spots_booked }}</span>
            </div>
            <div class="confirmation-item">
              <span class="label">Total:</span>
              <span class="value">{{ formatPrice(createdBooking.total_price) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <!-- Booking Step Footer -->
        <template v-if="currentStep === 'booking'">
          <button @click="emit('close')" class="btn-secondary">Cancel</button>
          <button
            @click="handleBookingSubmit"
            :disabled="isSubmitting"
            class="btn-primary"
          >
            {{ isSubmitting ? 'Creating...' : 'Continue to Payment' }}
          </button>
        </template>

        <!-- Payment Step Footer -->
        <template v-else-if="currentStep === 'payment'">
          <button @click="currentStep = 'booking'" class="btn-secondary">Back</button>
          <button
            v-if="paymentStep === 'initiate'"
            @click="handleMpesaPayment"
            :disabled="isProcessingPayment || !mpesaPhoneNumber"
            class="btn-primary"
          >
            {{ isProcessingPayment ? 'Processing...' : 'Initiate Payment' }}
          </button>
          <button
            v-else
            @click="handleConfirmPayment"
            :disabled="isProcessingPayment || !mpesaReceiptNumber || !mpesaTransactionId"
            class="btn-primary"
          >
            {{ isProcessingPayment ? 'Confirming...' : 'Confirm Payment' }}
          </button>
          <button
            v-if="paymentStep === 'initiate'"
            @click="handleSkipPayment"
            class="btn-secondary"
          >
            Pay Later
          </button>
        </template>

        <!-- Confirmation Step Footer -->
        <template v-else-if="currentStep === 'confirm'">
          <button @click="handleComplete" class="btn-primary">Done</button>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-neutral-light);
}

.modal-header h2 {
  margin: 0;
  color: var(--color-primary);
}

.close-btn {
  background: none;
  border: none;
  font-size: var(--font-size-2xl);
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color var(--transition-base);
}

.close-btn:hover {
  color: var(--color-text-primary);
}

.modal-body {
  padding: var(--spacing-lg);
}

.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 500;
  color: var(--color-text-primary);
}

.spots-selector {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.spot-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--color-neutral-light);
  background-color: white;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--font-size-lg);
  transition: all var(--transition-base);
}

.spot-btn:hover:not(:disabled) {
  background-color: var(--color-accent);
  color: white;
  border-color: var(--color-accent);
}

.spot-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spot-input {
  flex: 1;
  text-align: center;
  font-size: var(--font-size-lg);
  font-weight: 600;
  border: 1px solid var(--color-neutral-light);
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
}

.form-input {
  width: 100%;
  padding: var(--spacing-md);
  border: 1px solid var(--color-neutral-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  transition: all var(--transition-base);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(27, 58, 45, 0.1);
}

.payment-form {
  padding: var(--spacing-md);
}

.payment-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.payment-header h3 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--color-primary);
}

.payment-amount {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-accent);
  margin: 0;
}

.payment-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.payment-info {
  background: var(--color-neutral-lighter);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  text-align: center;
}

.payment-info p {
  margin: var(--spacing-xs) 0;
  color: var(--color-text-secondary);
}

.confirmation-form {
  text-align: center;
  padding: var(--spacing-lg);
}

.confirmation-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-lg);
}

.confirmation-form h3 {
  margin: 0 0 var(--spacing-xl) 0;
  color: var(--color-primary);
}

.confirmation-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  text-align: left;
  background: var(--color-neutral-lighter);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
}

.confirmation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.confirmation-item .label {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.confirmation-item .value {
  font-weight: 600;
  color: var(--color-text-primary);
}

.confirmation-item .value.code {
  font-family: monospace;
  background: white;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
}

.help-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-top: var(--spacing-sm);
  margin-bottom: 0;
}

.price-summary {
  background-color: var(--color-neutral-lighter);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-lg);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-base);
}

.summary-row.total {
  border-top: 2px solid var(--color-neutral-light);
  padding-top: var(--spacing-md);
  margin-top: var(--spacing-md);
  font-weight: 600;
  color: var(--color-accent);
  font-size: var(--font-size-lg);
}

.trail-info {
  padding: var(--spacing-lg);
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-lg);
}

.trail-info h3 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--color-text-light);
}

.trail-info p {
  margin: 0;
  opacity: 0.9;
}

.modal-footer {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-top: 1px solid var(--color-neutral-light);
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: var(--spacing-md);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-primary {
  background-color: var(--color-accent);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-accent-light);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: var(--color-neutral-light);
  color: var(--color-text-primary);
}

.btn-secondary:hover {
  background-color: var(--color-neutral);
}
</style>

