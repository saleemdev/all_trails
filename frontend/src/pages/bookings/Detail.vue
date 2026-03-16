<script setup lang="ts">
import { onMounted, onUnmounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookingsStore } from '../../stores/bookingsStore'
import { useUiStore } from '../../stores/uiStore'
import type { MpesaPaymentState } from '../../types/index'
import { apiService } from '../../services/api'
import { getMpesaProgressModel } from '../../utils/mpesaStatus'
import { isValidKenyanMpesaPhone, normalizeKenyanMpesaPhone } from '../../utils/payments'
import type { TrailWeather } from '../../types'

const route = useRoute()
const router = useRouter()
const bookingsStore = useBookingsStore()
const uiStore = useUiStore()

const booking = computed(() => bookingsStore.selectedBooking)
const isLoading = computed(() => bookingsStore.isLoading)

const paymentState = ref<MpesaPaymentState | null>(null)
const mpesaPhone = ref('')
const isInitiatingPayment = ref(false)
const isRefreshingPayment = ref(false)
const isCancellingBooking = ref(false)
const pollingStatus = ref(false)
const weather = ref<TrailWeather | null>(null)
const weatherLoading = ref(false)

let pollingHandle: ReturnType<typeof setInterval> | null = null
let pollAttemptCount = 0
const maxPollAttempts = 60

const isPaymentComplete = computed(() => {
  const status = booking.value?.payment_status || ''
  return status === 'Paid' || status === 'Completed'
})

const isBookingClosed = computed(() => {
  const status = booking.value?.status || ''
  return status === 'Cancelled' || status === 'Completed'
})

const canCancelBooking = computed(() => {
  const status = booking.value?.status || ''
  return status === 'Pending' || status === 'Confirmed'
})

const canInitiatePayment = computed(() => {
  if (!booking.value || isBookingClosed.value || isPaymentComplete.value) {
    return false
  }
  return !isInitiatingPayment.value && !isRefreshingPayment.value
})

const paymentProgress = computed(() =>
  getMpesaProgressModel({
    paymentStatus: paymentState.value?.status || booking.value?.payment_status,
    ticketStatus: paymentState.value?.ticket_status,
    fallbackStatus: 'Pending',
    message: paymentState.value?.message,
  })
)

const hasPaymentFailure = computed(() => {
  const status = booking.value?.payment_status || ''
  return status === 'Failed' || status === 'Cancelled' || status === 'Timeout'
})

const paymentLabel = computed(() => {
  if (hasPaymentFailure.value) {
    return 'Retry Payment'
  }
  return 'Pay Now'
})

const latestAttempt = computed(() => {
  const history = paymentState.value?.attempt_history || []
  if (!history.length) {
    return null
  }
  return history[history.length - 1]
})

const selectedActivities = computed(() => booking.value?.selected_activities || [])
const hasSelectedActivities = computed(() => selectedActivities.value.length > 0)

const formatDate = (date: string | undefined) => {
  if (!date) {
    return '—'
  }
  return new Date(date).toLocaleDateString('en-KE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(price)
}

const paymentTimeline = computed(() => {
  const events: Array<{ label: string; detail: string }> = [
    {
      label: 'Booking created',
      detail: formatDate(booking.value?.created_at || booking.value?.booking_date),
    },
    {
      label: 'Payment status',
      detail: booking.value?.payment_status || 'Pending',
    },
  ]

  if (latestAttempt.value?.checkout_request_id) {
    events.push({
      label: 'Latest checkout request',
      detail: latestAttempt.value.checkout_request_id,
    })
  }

  if (booking.value?.mpesa_receipt_number) {
    events.push({
      label: 'Receipt captured',
      detail: booking.value.mpesa_receipt_number,
    })
  }

  return events
})

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    Confirmed: 'info-pill info-pill--status-confirmed',
    Pending: 'info-pill info-pill--status-pending',
    Cancelled: 'info-pill info-pill--status-cancelled',
    Completed: 'info-pill info-pill--status-completed',
  }
  return colors[status] || 'soft-badge soft-badge--neutral'
}

const getPaymentStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    Completed: 'text-green-700',
    Paid: 'text-green-700',
    Pending: 'text-yellow-700',
    'Prompt Sent': 'text-blue-700',
    'Callback Received': 'text-blue-700',
    Failed: 'text-red-700',
    Cancelled: 'text-red-700',
    Timeout: 'text-red-700',
  }
  return colors[status] || 'text-gray-700'
}

const weatherRiskPillClass = computed(() => {
  const risk = weather.value?.risk_level
  if (risk === 'good') return 'info-pill info-pill--risk-good'
  if (risk === 'caution') return 'info-pill info-pill--risk-caution'
  if (risk === 'risky') return 'info-pill info-pill--risk-risky'
  return 'soft-badge soft-badge--neutral'
})

const clearPolling = () => {
  if (pollingHandle) {
    clearInterval(pollingHandle)
    pollingHandle = null
  }
  pollAttemptCount = 0
  pollingStatus.value = false
}

const shouldPoll = () => {
  const status = paymentState.value?.status || booking.value?.payment_status || ''
  return ['Pending', 'Prompt Sent', 'Callback Received'].includes(status)
}

const refreshPaymentStatus = async (silent = false) => {
  if (!booking.value) {
    return
  }

  if (!silent) {
    isRefreshingPayment.value = true
  }

  try {
    const payload = await apiService.getBookingPaymentStatus(booking.value.id)
    paymentState.value = payload.payment
    bookingsStore.selectedBooking = payload.booking

    if (isPaymentComplete.value) {
      clearPolling()
    }
  } catch (error: any) {
    if (!silent) {
      uiStore.showError(error?.message || 'Unable to refresh payment status')
    }
  } finally {
    if (!silent) {
      isRefreshingPayment.value = false
    }
  }
}

const startPolling = async () => {
  if (!shouldPoll()) {
    clearPolling()
    return
  }

  clearPolling()
  pollingStatus.value = true

  const poll = async () => {
    pollAttemptCount += 1
    await refreshPaymentStatus(true)

    if (!shouldPoll() || pollAttemptCount >= maxPollAttempts) {
      clearPolling()
    }
  }

  await poll()

  if (shouldPoll()) {
    pollingHandle = setInterval(() => {
      void poll()
    }, 3000)
  }
}

const loadBooking = async () => {
  const bookingId = route.params.id as string
  await bookingsStore.fetchBookingById(bookingId)

  if (!booking.value) {
    return
  }

  if (booking.value.mpesa_phone_number) {
    mpesaPhone.value = booking.value.mpesa_phone_number
  }

  await refreshPaymentStatus(true)
  void loadBookingWeather(bookingId)
  if (shouldPoll()) {
    await startPolling()
  }
}

const loadBookingWeather = async (bookingId: string) => {
  weatherLoading.value = true
  try {
    weather.value = await apiService.getBookingWeather(bookingId)
  } catch {
    weather.value = null
  } finally {
    weatherLoading.value = false
  }
}

const handleInitiatePayment = async () => {
  if (!booking.value) {
    return
  }

  if (!mpesaPhone.value) {
    uiStore.showError('Enter your MPESA phone number to continue')
    return
  }

  const normalizedPhone = normalizeKenyanMpesaPhone(mpesaPhone.value)
  if (!isValidKenyanMpesaPhone(normalizedPhone)) {
    uiStore.showError('Use a valid MPESA number (2547XXXXXXXX)')
    return
  }

  isInitiatingPayment.value = true
  try {
    const payload = await apiService.initiateBookingPayment(booking.value.id, normalizedPhone)
    mpesaPhone.value = normalizedPhone
    bookingsStore.selectedBooking = payload.booking
    if (payload.payment) {
      paymentState.value = payload.payment
    }

    uiStore.showSuccess(payload.message || 'Payment prompt sent. Confirm on your phone.')
    await startPolling()
  } catch (error: any) {
    uiStore.showError(error?.message || 'Unable to initiate payment')
  } finally {
    isInitiatingPayment.value = false
  }
}

const handleCancelBooking = async () => {
  if (!booking.value) {
    return
  }

  const reason = window.prompt('Provide a short cancellation reason (optional):') || ''

  isCancellingBooking.value = true
  try {
    await bookingsStore.cancelBooking(booking.value.id, reason)
    await bookingsStore.fetchBookingById(booking.value.id)
    uiStore.showSuccess('Booking cancelled successfully')
    clearPolling()
  } catch (error: any) {
    uiStore.showError(error?.message || 'Unable to cancel booking')
  } finally {
    isCancellingBooking.value = false
  }
}

onMounted(() => {
  void loadBooking()
})

onUnmounted(() => {
  clearPolling()
})
</script>

<template>
  <div class="page-shell w-full min-h-screen">
    <div class="layout-shell-wide page-block-tight">
      <button @click="router.back()" class="soft-button-secondary px-4 py-2.5 mb-5 text-sm">
        ← Back to Bookings
      </button>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="soft-spinner mb-4"></div>
        <p class="text-lg text-slate-600 font-medium mb-0">Loading booking details...</p>
      </div>

      <div v-else-if="booking" class="space-y-6">
        <section class="page-header rounded-[1.5rem] overflow-hidden text-white relative">
          <div class="absolute inset-0 hero-grid opacity-25"></div>
          <div class="relative z-10 p-6 sm:p-8 lg:p-10">
            <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-8">
              <div>
                <span class="soft-kicker mb-4">Booking confirmation</span>
                <h1 class="text-[clamp(1.9rem,4vw,2.8rem)] font-semibold leading-[1.04] tracking-[-0.03em] mb-3">Your trail reservation</h1>
                <p class="text-white/80 text-base mb-0">Status updates here are synced from booking and MPESA callbacks.</p>
                <div class="mt-4 flex flex-wrap gap-2">
                  <span :class="getStatusColor(booking.status)">{{ booking.status }}</span>
                  <span class="hero-info-pill">💳 {{ booking.payment_status }}</span>
                  <span class="hero-info-pill">👥 {{ booking.spots_booked }} {{ booking.spots_booked === 1 ? 'spot' : 'spots' }}</span>
                </div>
              </div>
              <div class="glass-panel hero-side-panel rounded-[1.2rem] px-5 py-4 text-left min-w-[17rem]">
                <div class="text-xs uppercase tracking-[0.14em] text-white/80 mb-2">Confirmation code</div>
                <div class="text-2xl font-semibold text-white mb-3">{{ booking.confirmation_code }}</div>
                <p class="text-white/90 text-sm mb-0">{{ booking.trail_title || booking.trail_id }}</p>
              </div>
            </div>
          </div>
        </section>

        <section class="surface-card-lg">
          <p class="app-section-kicker mb-2">Reservation snapshot</p>
          <h2 class="text-2xl brand-text-strong font-display font-semibold mb-4">All key details in one story</h2>
          <div class="space-y-3">
            <article class="surface-muted rounded-[1rem] p-4 flex items-start gap-3">
              <span class="soft-icon-tile soft-icon-tile--sage !w-9 !h-9 shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </span>
              <div>
                <p class="text-sm font-semibold tone-heading mb-1">Trail day</p>
                <p class="text-sm tone-body mb-0">{{ formatDate(booking.trail_scheduled_date || booking.booking_date) }}</p>
              </div>
            </article>
            <article class="surface-muted rounded-[1rem] p-4 flex items-start gap-3">
              <span class="soft-icon-tile soft-icon-tile--mist !w-9 !h-9 shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0" />
                </svg>
              </span>
              <div>
                <p class="text-sm font-semibold tone-heading mb-1">Trail and spots</p>
                <p class="text-sm tone-body mb-0">{{ booking.trail_title || booking.trail_id }} · {{ booking.spots_booked }} {{ booking.spots_booked === 1 ? 'spot' : 'spots' }}</p>
              </div>
            </article>
            <article class="surface-muted rounded-[1rem] p-4 flex items-start gap-3">
              <span class="soft-icon-tile soft-icon-tile--brass !w-9 !h-9 shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 8c-1.105 0-2 .67-2 1.5S10.895 11 12 11s2 .67 2 1.5-0.895 1.5-2 1.5m0-6v6m0 0v2m0-10V4" />
                </svg>
              </span>
              <div>
                <p class="text-sm font-semibold tone-heading mb-1">Amount and status</p>
                <p class="text-sm tone-body mb-0">{{ formatPrice(booking.total_price) }} · {{ booking.payment_status }}</p>
              </div>
            </article>
          </div>
        </section>

        <section class="surface-card-lg space-y-5">
          <div>
            <p class="app-section-kicker mb-2">Payment journey</p>
            <h2 class="text-2xl brand-text-strong font-display font-semibold mb-2">MPESA progress</h2>
            <p class="text-sm text-slate-600 mb-0">Initiate or retry payment from this booking only. Status is synced from backend callbacks.</p>
          </div>

          <div class="surface-muted rounded-[1rem] p-4 border border-slate-200/80">
            <p class="text-sm text-slate-700 mb-3">{{ paymentProgress.detail }}</p>
            <div class="w-full h-2 rounded-full bg-slate-200/80">
              <div class="h-2 rounded-full bg-[linear-gradient(135deg,var(--color-primary),#7a998d)] transition-all duration-500" :style="{ width: `${paymentProgress.progress}%` }"></div>
            </div>
            <p class="text-xs text-slate-500 mt-2 mb-0">{{ paymentProgress.progress }}% complete</p>
          </div>

          <div class="space-y-2">
            <article v-for="event in paymentTimeline" :key="event.label" class="surface-muted rounded-[0.9rem] p-3">
              <p class="text-xs uppercase tracking-[0.12em] text-slate-500 mb-1">{{ event.label }}</p>
              <p class="text-sm font-semibold text-slate-900 mb-0 break-all">{{ event.detail }}</p>
            </article>
          </div>

          <div v-if="canInitiatePayment" class="grid grid-cols-1 lg:grid-cols-[1fr_auto_auto] gap-3">
            <input
              v-model="mpesaPhone"
              type="tel"
              placeholder="2547XXXXXXXX"
              class="soft-input"
            />
            <button
              class="brand-button px-6 py-3 disabled:opacity-60"
              :disabled="!canInitiatePayment"
              @click="handleInitiatePayment"
            >
              <span v-if="!isInitiatingPayment">{{ paymentLabel }}</span>
              <span v-else class="flex items-center gap-2">
                <span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                Processing
              </span>
            </button>
            <button
              class="soft-button-secondary px-6 py-3"
              :disabled="isRefreshingPayment"
              @click="refreshPaymentStatus()"
            >
              <span v-if="!isRefreshingPayment">Refresh Status</span>
              <span v-else>Refreshing...</span>
            </button>
          </div>

          <div v-else class="flex flex-wrap gap-3">
            <button class="soft-button-secondary px-6 py-3" :disabled="isRefreshingPayment" @click="refreshPaymentStatus()">
              <span v-if="!isRefreshingPayment">Refresh Status</span>
              <span v-else>Refreshing...</span>
            </button>
            <span v-if="isPaymentComplete" class="soft-badge soft-badge--neutral">Payment completed</span>
            <span v-else-if="isBookingClosed" class="soft-badge soft-badge--neutral">Booking is closed</span>
          </div>

          <p v-if="pollingStatus" class="text-xs text-blue-700 mb-0">Auto-refresh is active while payment is pending.</p>
        </section>

        <section class="surface-card-lg">
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              v-if="canCancelBooking"
              class="soft-button-secondary px-8 py-4 text-red-700 border-red-200 bg-red-50 hover:bg-red-100 disabled:opacity-60"
              :disabled="isCancellingBooking"
              @click="handleCancelBooking"
            >
              <span v-if="!isCancellingBooking">Cancel Booking</span>
              <span v-else>Cancelling...</span>
            </button>
            <button class="brand-button px-8 py-4" @click="router.push('/trails')">
              Book Another Trail
            </button>
          </div>
        </section>

        <section v-if="hasSelectedActivities" class="surface-card-lg">
          <div class="flex items-center justify-between gap-3 flex-wrap mb-3">
            <h2 class="text-xl font-semibold text-slate-900 mb-0">Selected add-ons</h2>
            <span class="soft-badge soft-badge--neutral">{{ selectedActivities.length }} item(s)</span>
          </div>
          <div class="space-y-2.5">
            <article v-for="activity in selectedActivities" :key="activity.activity_id" class="surface-muted rounded-[1rem] p-3.5 flex items-center justify-between gap-3">
              <div>
                <p class="text-sm font-semibold text-slate-900 mb-1">{{ activity.activity_name }}</p>
                <p class="text-xs text-slate-600 mb-0">Qty {{ activity.quantity }}</p>
              </div>
              <p class="text-sm font-semibold brand-text mb-0">{{ formatPrice(activity.total_price || (activity.price * activity.quantity)) }}</p>
            </article>
          </div>
        </section>

        <section class="surface-card-lg">
          <div class="flex items-center justify-between gap-3 flex-wrap mb-3">
            <h2 class="text-xl font-semibold text-slate-900 mb-0">Trail Day Weather</h2>
            <span v-if="weather?.available" :class="weatherRiskPillClass">
              {{ weather.risk_label || 'Weather' }}
            </span>
          </div>
          <p v-if="weatherLoading" class="text-sm tone-body mb-0">Checking weather forecast...</p>
          <p v-else-if="!weather?.available" class="text-sm tone-body mb-0">
            {{ weather?.message || 'Weather forecast is unavailable right now.' }}
          </p>
          <div v-else class="flex flex-wrap items-center gap-2 text-sm">
            <span class="soft-badge soft-badge--neutral">{{ weather.summary }}</span>
            <span class="soft-badge soft-badge--neutral">{{ weather.temperature_min_c }}° - {{ weather.temperature_max_c }}°C</span>
            <span class="soft-badge soft-badge--neutral">Rain {{ weather.precipitation_probability_max }}%</span>
            <span class="soft-badge soft-badge--neutral">Wind {{ weather.wind_gusts_10m_max_kmh }} km/h gusts</span>
            <span class="soft-badge soft-badge--neutral">UV {{ weather.uv_index_max }}</span>
          </div>
        </section>
      </div>

      <div v-else class="surface-card-lg text-center">
        <h3 class="text-2xl font-semibold text-slate-900 mb-2">Booking not found</h3>
        <p class="mb-7 text-base text-slate-600">We couldn't find the booking you're looking for.</p>
        <button @click="router.push('/bookings')" class="brand-button px-8 py-4">
          View All Bookings
        </button>
      </div>
    </div>
  </div>
</template>
