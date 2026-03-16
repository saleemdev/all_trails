<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useBookingsStore } from '../stores/bookingsStore'
import { apiService } from '../services/api'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const bookingsStore = useBookingsStore()
const router = useRouter()

const user = computed(() => authStore.user)
const userStats = ref<any>(null)
const isLoadingStats = ref(false)
const activeTab = ref<'overview' | 'bookings' | 'settings'>('overview')

onMounted(async () => {
  await loadUserStats()
  await bookingsStore.fetchUserBookings()
})

const loadUserStats = async () => {
  isLoadingStats.value = true
  try {
    userStats.value = await apiService.getUserStats()
  } catch (error) {
    console.error('Failed to load user stats:', error)
  } finally {
    isLoadingStats.value = false
  }
}

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(amount)
}

const viewBooking = (bookingId: string) => {
  router.push({ name: 'BookingDetail', params: { id: bookingId } })
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-KE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const bookingStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    Confirmed: 'info-pill info-pill--status-confirmed',
    Pending: 'info-pill info-pill--status-pending',
    Completed: 'info-pill info-pill--status-completed',
    Cancelled: 'info-pill info-pill--status-cancelled',
  }

  return classes[status] || 'soft-badge soft-badge--neutral'
}
</script>

<template>
  <div class="page-shell w-full min-h-screen">
    <section class="page-header overflow-hidden">
      <div class="absolute inset-0 hero-grid opacity-30"></div>
      <div class="layout-shell-wide page-hero-block relative z-10">
        <div class="grid gap-6 lg:grid-cols-[auto_1fr_auto] lg:items-end">
          <div class="flex justify-center lg:justify-start">
            <div class="flex h-24 w-24 items-center justify-center overflow-hidden rounded-[2rem] border border-white/20 bg-white/15 shadow-[0_18px_50px_rgba(17,31,26,0.16)] backdrop-blur-xl sm:h-28 sm:w-28">
              <img v-if="user?.user_image" :src="user.user_image" :alt="user.full_name" class="h-full w-full object-cover" />
              <span v-else class="text-4xl font-semibold text-white">
                {{ user?.full_name?.charAt(0)?.toUpperCase() || 'A' }}
              </span>
            </div>
          </div>

          <div>
            <p class="page-kicker-light">Account hub</p>
            <h1 class="page-title-light">{{ user?.full_name || user?.name || 'User' }}</h1>
            <p class="page-copy-light max-w-3xl">{{ user?.email }}<span v-if="user?.name"> · @{{ user?.name }}</span></p>
          </div>

          <div class="flex lg:justify-end">
            <button class="brand-button w-full sm:w-auto" @click="router.push({ name: 'TrailBrowse' })">
              Browse trails
            </button>
          </div>
        </div>
      </div>
    </section>

    <div class="layout-shell-wide page-block -mt-6 relative z-20 sm:-mt-8">
      <div v-if="isLoadingStats" class="surface-card mb-8 text-center">
        <div class="soft-spinner mx-auto mb-4"></div>
        <p class="text-sm text-slate-600 mb-0">Loading account metrics...</p>
      </div>

      <div v-else-if="userStats" class="mb-8">
        <div class="glass-panel-strong rounded-[1.25rem] p-4 sm:p-5">
          <p class="app-section-kicker mb-3">Quick snapshot</p>
          <div class="flex flex-wrap gap-2.5">
            <span class="hero-info-pill">Bookings {{ userStats.total_bookings || 0 }}</span>
            <span class="hero-info-pill">Confirmed {{ userStats.confirmed_bookings || 0 }}</span>
            <span class="hero-info-pill">Completed {{ userStats.completed_bookings || 0 }}</span>
            <span class="hero-info-pill">Spend {{ formatCurrency(userStats.total_spent || 0) }}</span>
          </div>
        </div>
      </div>

      <div class="glass-panel-strong mb-8 rounded-[1.5rem] p-2">
        <div class="flex flex-wrap gap-2" role="tablist" aria-label="Profile sections">
          <button
            class="soft-toggle-button rounded-[1rem] px-4 py-3 text-sm"
            :class="{ 'soft-toggle-active': activeTab === 'overview' }"
            @click="activeTab = 'overview'"
            role="tab"
            :aria-selected="activeTab === 'overview'"
            aria-controls="overview-panel"
            id="overview-tab"
          >
            Overview
          </button>
          <button
            class="soft-toggle-button rounded-[1rem] px-4 py-3 text-sm"
            :class="{ 'soft-toggle-active': activeTab === 'bookings' }"
            @click="activeTab = 'bookings'"
            role="tab"
            :aria-selected="activeTab === 'bookings'"
            aria-controls="bookings-panel"
            id="bookings-tab"
          >
            My bookings
            <span v-if="bookingsStore.bookings.length" class="ml-2 rounded-full bg-slate-900 px-2 py-0.5 text-[11px] font-semibold text-white">
              {{ bookingsStore.bookings.length }}
            </span>
          </button>
          <button
            class="soft-toggle-button rounded-[1rem] px-4 py-3 text-sm"
            :class="{ 'soft-toggle-active': activeTab === 'settings' }"
            @click="activeTab = 'settings'"
            role="tab"
            :aria-selected="activeTab === 'settings'"
            aria-controls="settings-panel"
            id="settings-tab"
          >
            Settings
          </button>
        </div>
      </div>

      <div
        v-if="activeTab === 'overview'"
        id="overview-panel"
        role="tabpanel"
        aria-labelledby="overview-tab"
        class="grid gap-6 lg:grid-cols-[0.92fr_1.08fr]"
      >
        <section class="surface-card-lg">
          <p class="app-section-kicker">Profile</p>
          <h2 class="app-section-title">Account information</h2>
          <div class="mt-6 grid gap-4 sm:grid-cols-2">
            <div class="surface-card-muted">
              <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Full name</p>
              <p class="mt-3 mb-0 text-base font-semibold text-slate-950">{{ user?.full_name || user?.name }}</p>
            </div>
            <div class="surface-card-muted">
              <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Email</p>
              <p class="mt-3 mb-0 text-base font-semibold text-slate-950 break-all">{{ user?.email }}</p>
            </div>
            <div class="surface-card-muted sm:col-span-2">
              <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Username</p>
              <p class="mt-3 mb-0 text-base font-semibold text-slate-950">{{ user?.name }}</p>
            </div>
          </div>
        </section>

        <section class="surface-card-lg">
          <p class="app-section-kicker">Recent activity</p>
          <h2 class="app-section-title">Upcoming bookings</h2>

          <div v-if="bookingsStore.upcomingBookings.length > 0" class="mt-6 space-y-4">
            <button
              v-for="booking in bookingsStore.upcomingBookings.slice(0, 5)"
              :key="booking.id"
              @click="viewBooking(booking.id)"
              class="w-full rounded-[1.2rem] bg-white/82 px-4 py-4 text-left transition-all hover:-translate-y-0.5 hover:shadow-md"
              :aria-label="`View booking for ${booking.trail_title || 'Trail'}`"
            >
              <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <p class="font-semibold text-slate-950">{{ booking.trail_title || 'Trail' }}</p>
                  <p class="mt-2 text-sm text-slate-600">
                    {{ formatDate(booking.trail_scheduled_date || booking.booking_date) }} ·
                    {{ booking.spots_booked }} {{ booking.spots_booked === 1 ? 'spot' : 'spots' }}
                  </p>
                </div>
                <span :class="bookingStatusClass(booking.status)">
                  {{ booking.status }}
                </span>
              </div>
            </button>
          </div>

          <div v-else class="mt-6 rounded-[1.25rem] border border-dashed border-slate-300 bg-white/55 px-5 py-8 text-center">
            <p class="mb-2 text-base font-semibold text-slate-900">No upcoming bookings</p>
            <p class="text-sm text-slate-600">Start with a trail and the next reservation will land here.</p>
            <button @click="router.push({ name: 'TrailBrowse' })" class="brand-button mt-5">Browse trails</button>
          </div>
        </section>
      </div>

      <section
        v-else-if="activeTab === 'bookings'"
        id="bookings-panel"
        role="tabpanel"
        aria-labelledby="bookings-tab"
        class="surface-card-lg"
      >
        <p class="app-section-kicker">Reservation history</p>
        <h2 class="app-section-title">All bookings</h2>

        <div v-if="bookingsStore.isLoading" class="py-16 text-center">
          <div class="soft-spinner mx-auto mb-4"></div>
          <p class="mb-0 text-sm text-slate-600">Loading bookings...</p>
        </div>

        <div v-else-if="bookingsStore.bookings.length === 0" class="mt-6 rounded-[1.25rem] border border-dashed border-slate-300 bg-white/55 px-5 py-10 text-center">
          <p class="mb-2 text-lg font-semibold text-slate-900">No bookings yet</p>
          <p class="text-sm text-slate-600">Start with your first trail and your reservation history will appear here.</p>
          <button @click="router.push({ name: 'TrailBrowse' })" class="brand-button mt-5">Browse trails</button>
        </div>

        <div v-else class="mt-6 space-y-4">
          <button
            v-for="booking in bookingsStore.bookings"
            :key="booking.id"
            @click="viewBooking(booking.id)"
            class="w-full rounded-[1.35rem] bg-white/82 px-4 py-4 text-left transition-all hover:-translate-y-0.5 hover:shadow-md sm:px-5"
            :aria-label="`View booking ${booking.confirmation_code}`"
          >
            <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
              <div>
                <div class="flex flex-wrap items-center gap-3">
                  <p class="text-base font-semibold text-slate-950">{{ booking.trail_title || 'Trail' }}</p>
                  <span :class="bookingStatusClass(booking.status)">
                    {{ booking.status }}
                  </span>
                </div>
                <div class="mt-3 grid gap-2 text-sm text-slate-600 sm:grid-cols-2 xl:grid-cols-4 xl:gap-4">
                  <span>Date: {{ formatDate(booking.trail_scheduled_date || booking.booking_date) }}</span>
                  <span>Spots: {{ booking.spots_booked }}</span>
                  <span>Total: {{ formatCurrency(booking.total_price) }}</span>
                  <span class="font-semibold text-[color:var(--color-primary-dark)]">Ref: {{ booking.confirmation_code }}</span>
                </div>
              </div>
            </div>
          </button>
        </div>
      </section>

      <div
        v-else
        id="settings-panel"
        role="tabpanel"
        aria-labelledby="settings-tab"
        class="grid gap-6 lg:grid-cols-2"
      >
        <section class="surface-card-lg">
          <p class="app-section-kicker">Notifications</p>
          <h2 class="app-section-title">Account settings</h2>
          <div class="mt-6 space-y-4">
            <div class="surface-card-muted flex items-center justify-between gap-4">
              <div>
                <p class="font-semibold text-slate-950">Email notifications</p>
                <p class="mt-1 mb-0 text-sm text-slate-600">Receive booking updates and reminders.</p>
              </div>
              <input type="checkbox" checked disabled aria-label="Email notifications enabled" />
            </div>
            <div class="surface-card-muted flex items-center justify-between gap-4">
              <div>
                <p class="font-semibold text-slate-950">Marketing emails</p>
                <p class="mt-1 mb-0 text-sm text-slate-600">Receive updates about new trails and offers.</p>
              </div>
              <input type="checkbox" disabled aria-label="Marketing emails disabled" />
            </div>
          </div>
        </section>

        <section class="surface-card-lg">
          <p class="app-section-kicker">Preferences</p>
          <h2 class="app-section-title">Trip defaults</h2>
          <div class="mt-6 space-y-4">
            <div class="surface-card-muted">
              <label for="difficulty-preference" class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                Preferred difficulty
              </label>
              <select id="difficulty-preference" class="soft-input mt-3 w-full bg-white/85" disabled aria-label="Preferred difficulty level">
                <option>Any</option>
                <option>Easy</option>
                <option>Moderate</option>
                <option>Hard</option>
                <option>Expert</option>
              </select>
            </div>
            <p class="mb-0 text-sm leading-6 text-slate-600">
              Preference editing is staged for a later phase, but the page now follows the same shared layout and token system as the rest of the app.
            </p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
