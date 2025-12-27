<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useBookingsStore } from '../../stores/bookingsStore'

const router = useRouter()
const bookingsStore = useBookingsStore()

const upcomingBookings = computed(() => bookingsStore.upcomingBookings)
const pastBookings = computed(() => bookingsStore.pastBookings)
const isLoading = computed(() => bookingsStore.isLoading)

onMounted(() => {
  bookingsStore.fetchUserBookings()
})

const viewBookingDetail = (bookingId: string) => {
  router.push({ name: 'BookingDetail', params: { id: bookingId } })
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-KE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
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

const getStatusIcon = (status: string) => {
  const icons: Record<string, string> = {
    Confirmed: '✓',
    Pending: '⏳',
    Cancelled: '✗',
    Completed: '✓',
  }
  return icons[status] || '•'
}
</script>

<template>
  <div class="w-full min-h-screen bg-gray-50">
    <!-- Hero Header -->
    <div class="bg-gradient-to-r from-emerald-900 via-teal-800 to-cyan-900 relative overflow-hidden">
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-0 left-0 w-full h-full"
             style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative z-10">
        <h1 class="text-5xl md:text-6xl font-black text-white mb-4 leading-tight">
          My Bookings
        </h1>
        <p class="text-xl text-white/90 max-w-2xl leading-relaxed">
          View and manage your trail bookings and adventure history.
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="w-16 h-16 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mb-4"></div>
        <p class="text-lg text-gray-600 font-medium">Loading your bookings...</p>
      </div>

      <!-- Loaded State -->
      <div v-else class="space-y-12">
        <!-- Upcoming Bookings -->
        <div>
          <div class="flex items-center gap-3 mb-6">
            <div class="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h2 class="text-3xl font-black text-gray-900">Upcoming Adventures</h2>
              <p class="text-gray-600">Your scheduled trail bookings</p>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="upcomingBookings.length === 0" class="bg-white rounded-2xl shadow-lg border border-gray-100 p-16 text-center">
            <div class="text-8xl mb-6">📅</div>
            <h3 class="text-3xl font-black text-gray-900 mb-4">No Upcoming Bookings</h3>
            <p class="text-xl text-gray-600 mb-8 max-w-md mx-auto">
              Ready for your next adventure?
            </p>
            <RouterLink
              to="/trails"
              class="inline-block px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Browse Trails
            </RouterLink>
          </div>

          <!-- Bookings Grid -->
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="booking in upcomingBookings"
              :key="booking.id"
              @click="viewBookingDetail(booking.id)"
              class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden cursor-pointer hover:shadow-2xl transition-all hover:-translate-y-1"
            >
              <!-- Card Header with Gradient -->
              <div class="h-32 bg-gradient-to-br from-emerald-600 to-teal-600 relative">
                <div class="absolute inset-0 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                </div>
                <!-- Status Badge -->
                <div class="absolute top-4 right-4">
                  <div :class="['px-3 py-1.5 rounded-full font-bold text-sm shadow-lg border-2 backdrop-blur-sm', getStatusColor(booking.status)]">
                    {{ getStatusIcon(booking.status) }} {{ booking.status }}
                  </div>
                </div>
              </div>

              <!-- Card Body -->
              <div class="p-6">
                <h3 class="text-xl font-black text-gray-900 mb-4">Trail Booking</h3>

                <div class="space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-600 font-medium">Confirmation</span>
                    <span class="text-sm font-bold text-emerald-700">{{ booking.confirmation_code }}</span>
                  </div>

                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-600 font-medium">Spots</span>
                    <span class="text-sm font-bold text-gray-900">{{ booking.spots_booked }} {{ booking.spots_booked === 1 ? 'person' : 'people' }}</span>
                  </div>

                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-600 font-medium">Total Price</span>
                    <span class="text-lg font-black text-emerald-700">{{ formatPrice(booking.total_price) }}</span>
                  </div>

                  <div class="pt-3 border-t-2 border-gray-100">
                    <div class="flex items-center gap-2 text-gray-600">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span class="text-sm font-medium">{{ formatDate(booking.booking_date) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Past Bookings -->
        <div>
          <div class="flex items-center gap-3 mb-6">
            <div class="w-12 h-12 bg-gradient-to-br from-gray-500 to-gray-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h2 class="text-3xl font-black text-gray-900">Past Adventures</h2>
              <p class="text-gray-600">Your completed trail experiences</p>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="pastBookings.length === 0" class="bg-white rounded-2xl shadow-lg border border-gray-100 p-12 text-center">
            <div class="text-6xl mb-4">🏔️</div>
            <p class="text-lg text-gray-600">No past bookings yet.</p>
          </div>

          <!-- Bookings Grid -->
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="booking in pastBookings"
              :key="booking.id"
              @click="viewBookingDetail(booking.id)"
              class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden cursor-pointer hover:shadow-xl transition-all"
            >
              <!-- Card Header with Gray Gradient -->
              <div class="h-24 bg-gradient-to-br from-gray-400 to-gray-500 relative">
                <div class="absolute inset-0 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <!-- Status Badge -->
                <div class="absolute top-3 right-3">
                  <div :class="['px-2 py-1 rounded-full font-bold text-xs shadow-md border backdrop-blur-sm', getStatusColor(booking.status)]">
                    {{ booking.status }}
                  </div>
                </div>
              </div>

              <!-- Card Body -->
              <div class="p-5">
                <h3 class="text-lg font-bold text-gray-700 mb-3">Trail Booking</h3>

                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-xs text-gray-500 font-medium">Confirmation</span>
                    <span class="text-xs font-bold text-gray-700">{{ booking.confirmation_code }}</span>
                  </div>

                  <div class="flex justify-between items-center">
                    <span class="text-xs text-gray-500 font-medium">Total Price</span>
                    <span class="text-base font-black text-gray-900">{{ formatPrice(booking.total_price) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
