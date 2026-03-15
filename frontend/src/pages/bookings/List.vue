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
  <div class="page-shell w-full min-h-screen">
    <div class="page-header relative overflow-hidden">
      <div class="absolute inset-0 hero-grid opacity-30"></div>
      <div class="layout-shell-wide page-hero-block relative z-10">
        <p class="page-kicker-light mb-3">Personal dashboard</p>
        <h1 class="page-title-light">My bookings</h1>
        <p class="page-copy-light mb-0">
          Track upcoming hikes and past adventures in the same softer visual system.
        </p>
      </div>
    </div>

    <div class="layout-shell-wide page-block">
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="soft-spinner mb-4"></div>
        <p class="text-lg text-slate-600 font-medium mb-0">Loading your bookings...</p>
      </div>

      <div v-else class="space-y-12">
        <section>
          <div class="flex items-center gap-3 mb-6">
            <div class="soft-icon-tile soft-icon-tile--sage w-12 h-12 rounded-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-semibold text-slate-900 sm:text-3xl">Upcoming adventures</h2>
              <p class="text-slate-600 mb-0">Your scheduled trail bookings</p>
            </div>
          </div>

          <div v-if="upcomingBookings.length === 0" class="surface-card-lg text-center">
            <div class="mb-5 text-6xl">📅</div>
            <h3 class="text-3xl font-semibold text-slate-900 mb-3">No Upcoming Bookings</h3>
            <p class="mx-auto mb-7 max-w-md text-base text-slate-600">Ready for your next adventure?</p>
            <RouterLink to="/trails" class="brand-button px-8 py-4">
              Browse Trails
            </RouterLink>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <article
              v-for="booking in upcomingBookings"
              :key="booking.id"
              @click="viewBookingDetail(booking.id)"
              class="glass-panel-strong rounded-[1.75rem] overflow-hidden cursor-pointer soft-card-hover"
            >
              <div class="h-32 relative bg-slate-900">
                <div class="absolute inset-0 hero-overlay"></div>
                <div class="absolute inset-0 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                </div>
                <div class="absolute top-4 right-4">
                  <div :class="['px-3 py-1.5 rounded-full font-bold text-sm shadow-lg border backdrop-blur-sm', getStatusColor(booking.status)]">
                    {{ getStatusIcon(booking.status) }} {{ booking.status }}
                  </div>
                </div>
              </div>

              <div class="p-6">
              <h3 class="text-xl font-semibold text-slate-900 mb-4">Trail Booking</h3>

                <div class="space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-slate-600 font-medium">Confirmation</span>
                    <span class="text-sm font-bold brand-text">{{ booking.confirmation_code }}</span>
                  </div>

                  <div class="flex justify-between items-center">
                    <span class="text-sm text-slate-600 font-medium">Spots</span>
                    <span class="text-sm font-bold text-slate-900">{{ booking.spots_booked }} {{ booking.spots_booked === 1 ? 'person' : 'people' }}</span>
                  </div>

                  <div class="flex justify-between items-center">
                    <span class="text-sm text-slate-600 font-medium">Total Price</span>
                    <span class="text-lg font-semibold brand-text">{{ formatPrice(booking.total_price) }}</span>
                  </div>

                  <div class="pt-3 border-t border-slate-200/80">
                    <div class="flex items-center gap-2 text-slate-600">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span class="text-sm font-medium">{{ formatDate(booking.booking_date) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </section>

        <section>
          <div class="flex items-center gap-3 mb-6">
            <div class="soft-icon-tile soft-icon-tile--mist w-12 h-12 rounded-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-semibold text-slate-900 sm:text-3xl">Past adventures</h2>
              <p class="text-slate-600 mb-0">Your completed trail experiences</p>
            </div>
          </div>

          <div v-if="pastBookings.length === 0" class="glass-panel rounded-[1.75rem] p-12 text-center">
            <div class="text-6xl mb-4">🏔️</div>
            <p class="text-lg text-slate-600 mb-0">No past bookings yet.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <article
              v-for="booking in pastBookings"
              :key="booking.id"
              @click="viewBookingDetail(booking.id)"
              class="glass-panel rounded-[1.5rem] overflow-hidden cursor-pointer soft-card-hover"
            >
              <div class="h-24 bg-gradient-to-br from-slate-400 to-slate-500 relative">
                <div class="absolute inset-0 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div class="absolute top-3 right-3">
                  <div :class="['px-2 py-1 rounded-full font-bold text-xs shadow-md border backdrop-blur-sm', getStatusColor(booking.status)]">
                    {{ booking.status }}
                  </div>
                </div>
              </div>

              <div class="p-5">
                <h3 class="text-lg font-bold text-slate-700 mb-3">Trail Booking</h3>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-xs text-slate-500 font-medium">Confirmation</span>
                    <span class="text-xs font-bold text-slate-700">{{ booking.confirmation_code }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-xs text-slate-500 font-medium">Total Price</span>
                    <span class="text-base font-semibold text-slate-900">{{ formatPrice(booking.total_price) }}</span>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
