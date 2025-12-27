<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookingsStore } from '../../stores/bookingsStore'

const route = useRoute()
const router = useRouter()
const bookingsStore = useBookingsStore()

const booking = computed(() => bookingsStore.selectedBooking)
const isLoading = computed(() => bookingsStore.isLoading)

onMounted(() => {
  const bookingId = route.params.id as string
  bookingsStore.fetchBookingById(bookingId)
})

const formatDate = (date: string) => {
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

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    Confirmed: 'bg-green-100 text-green-800 border-green-300',
    Pending: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    Cancelled: 'bg-red-100 text-red-800 border-red-300',
    Completed: 'bg-blue-100 text-blue-800 border-blue-300',
  }
  return colors[status] || 'bg-gray-100 text-gray-800 border-gray-300'
}

const getPaymentStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    Paid: 'text-green-700',
    Pending: 'text-yellow-700',
    Failed: 'text-red-700',
  }
  return colors[status] || 'text-gray-700'
}
</script>

<template>
  <div class="w-full min-h-screen bg-gray-50">
    <!-- Back Button Bar -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <button
          @click="router.back()"
          class="flex items-center gap-2 px-4 py-2 text-emerald-700 hover:bg-emerald-50 rounded-lg transition-all font-medium"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Bookings
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="w-16 h-16 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mb-4"></div>
        <p class="text-lg text-gray-600 font-medium">Loading booking details...</p>
      </div>

      <!-- Booking Details -->
      <div v-else-if="booking" class="space-y-6">
        <!-- Header Card -->
        <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
          <div class="h-48 bg-gradient-to-br from-emerald-900 via-teal-800 to-cyan-900 relative">
            <div class="absolute inset-0 opacity-20">
              <div class="absolute top-0 left-0 w-full h-full"
                   style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
            </div>

            <div class="absolute inset-0 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-white opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>

            <!-- Status Badge -->
            <div class="absolute top-6 right-6">
              <div :class="['px-4 py-2 rounded-full font-bold text-base shadow-lg border-2 backdrop-blur-sm', getStatusColor(booking.status)]">
                {{ booking.status }}
              </div>
            </div>
          </div>

          <div class="p-8">
            <div class="flex items-center justify-between mb-6">
              <div>
                <h1 class="text-4xl font-black text-gray-900 mb-2">Booking Confirmation</h1>
                <p class="text-gray-600">Your trail adventure details</p>
              </div>
              <div class="text-right">
                <div class="text-sm text-gray-500 font-medium mb-1">Confirmation Code</div>
                <div class="text-3xl font-black text-emerald-700">{{ booking.confirmation_code }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Details Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Booking Information Card -->
          <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center shadow-md">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h2 class="text-2xl font-black text-gray-900">Booking Information</h2>
                <p class="text-sm text-gray-600">Reservation details</p>
              </div>
            </div>

            <div class="space-y-4">
              <div class="flex justify-between items-center py-3 border-b border-gray-100">
                <span class="text-sm text-gray-600 font-medium">Booking Date</span>
                <span class="text-sm font-bold text-gray-900">{{ formatDate(booking.booking_date) }}</span>
              </div>

              <div class="flex justify-between items-center py-3 border-b border-gray-100">
                <span class="text-sm text-gray-600 font-medium">Spots Booked</span>
                <span class="text-sm font-bold text-gray-900">{{ booking.spots_booked }} {{ booking.spots_booked === 1 ? 'person' : 'people' }}</span>
              </div>

              <div class="flex justify-between items-center py-3 border-b border-gray-100">
                <span class="text-sm text-gray-600 font-medium">Status</span>
                <span :class="['px-3 py-1 rounded-full font-bold text-xs border-2', getStatusColor(booking.status)]">
                  {{ booking.status }}
                </span>
              </div>

              <div class="flex justify-between items-center py-3">
                <span class="text-sm text-gray-600 font-medium">Confirmation</span>
                <span class="text-sm font-black text-emerald-700">{{ booking.confirmation_code }}</span>
              </div>
            </div>
          </div>

          <!-- Payment Information Card -->
          <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center shadow-md">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div>
                <h2 class="text-2xl font-black text-gray-900">Payment Information</h2>
                <p class="text-sm text-gray-600">Transaction details</p>
              </div>
            </div>

            <div class="space-y-4">
              <div class="flex justify-between items-center py-3 border-b border-gray-100">
                <span class="text-sm text-gray-600 font-medium">Payment Status</span>
                <span :class="['font-bold text-sm', getPaymentStatusColor(booking.payment_status)]">
                  {{ booking.payment_status }}
                </span>
              </div>

              <div class="flex justify-between items-center py-3 border-b border-gray-100">
                <span class="text-sm text-gray-600 font-medium">Spots Booked</span>
                <span class="text-sm font-bold text-gray-900">{{ booking.spots_booked }} × {{ formatPrice(booking.total_price / booking.spots_booked) }}</span>
              </div>

              <div class="bg-emerald-50 rounded-xl p-4 mt-4">
                <div class="flex justify-between items-center">
                  <span class="text-base text-emerald-900 font-bold">Total Amount</span>
                  <span class="text-3xl font-black text-emerald-700">{{ formatPrice(booking.total_price) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              v-if="booking.status === 'Confirmed'"
              class="px-8 py-4 bg-red-50 text-red-700 font-bold rounded-xl hover:bg-red-100 transition-all border-2 border-red-200"
            >
              Cancel Booking
            </button>
            <button
              class="px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-md hover:shadow-lg"
              @click="router.push('/trails')"
            >
              Book Another Trail
            </button>
          </div>
        </div>
      </div>

      <!-- Not Found State -->
      <div v-else class="bg-white rounded-2xl shadow-lg border border-gray-100 p-16 text-center">
        <div class="text-8xl mb-6">❓</div>
        <h3 class="text-3xl font-black text-gray-900 mb-4">Booking Not Found</h3>
        <p class="text-xl text-gray-600 mb-8">
          We couldn't find the booking you're looking for.
        </p>
        <button
          @click="router.push('/bookings')"
          class="px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg"
        >
          View All Bookings
        </button>
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
