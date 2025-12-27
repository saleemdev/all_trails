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
</script>

<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>My Profile</h1>
      <p>View and manage your account information</p>
    </div>

    <div v-if="user" class="profile-container">
      <!-- Profile Header Card -->
      <div class="profile-card profile-header-card">
        <div class="profile-header">
          <div class="profile-avatar">
            <img v-if="user.user_image" :src="user.user_image" :alt="user.full_name" />
            <span v-else>{{ user.full_name?.charAt(0)?.toUpperCase() || '👤' }}</span>
          </div>
          <div class="profile-info">
            <h2>{{ user.full_name || user.name }}</h2>
            <p class="email">{{ user.email }}</p>
            <p class="username">@{{ user.name }}</p>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div v-if="userStats" class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📅</div>
          <div class="stat-content">
            <div class="stat-value">{{ userStats.total_bookings || 0 }}</div>
            <div class="stat-label">Total Bookings</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <div class="stat-value">{{ userStats.confirmed_bookings || 0 }}</div>
            <div class="stat-label">Confirmed</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🏁</div>
          <div class="stat-content">
            <div class="stat-value">{{ userStats.completed_bookings || 0 }}</div>
            <div class="stat-label">Completed</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-content">
            <div class="stat-value">{{ formatCurrency(userStats.total_spent || 0) }}</div>
            <div class="stat-label">Total Spent</div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs-container">
        <div class="tabs">
          <button
            @click="activeTab = 'overview'"
            :class="['tab', { active: activeTab === 'overview' }]"
          >
            Overview
          </button>
          <button
            @click="activeTab = 'bookings'"
            :class="['tab', { active: activeTab === 'bookings' }]"
          >
            My Bookings ({{ bookingsStore.bookings.length }})
          </button>
          <button
            @click="activeTab = 'settings'"
            :class="['tab', { active: activeTab === 'settings' }]"
          >
            Settings
          </button>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'" class="profile-card">
          <h3>Account Information</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Full Name</span>
              <span class="value">{{ user.full_name || user.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">Email</span>
              <span class="value">{{ user.email }}</span>
            </div>
            <div class="info-item">
              <span class="label">Username</span>
              <span class="value">{{ user.name }}</span>
            </div>
          </div>

          <h3 style="margin-top: 2rem;">Recent Activity</h3>
          <div v-if="bookingsStore.upcomingBookings.length > 0" class="activity-list">
            <div
              v-for="booking in bookingsStore.upcomingBookings.slice(0, 5)"
              :key="booking.id"
              class="activity-item"
              @click="viewBooking(booking.id)"
            >
              <div class="activity-icon">🎒</div>
              <div class="activity-content">
                <div class="activity-title">{{ booking.trail_title || 'Trail' }}</div>
                <div class="activity-meta">
                  {{ new Date(booking.trail_scheduled_date || booking.booking_date).toLocaleDateString() }} • 
                  {{ booking.spots_booked }} {{ booking.spots_booked === 1 ? 'spot' : 'spots' }}
                </div>
              </div>
              <div class="activity-status" :class="booking.status.toLowerCase()">
                {{ booking.status }}
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <p>No upcoming bookings</p>
          </div>
        </div>

        <!-- Bookings Tab -->
        <div v-if="activeTab === 'bookings'" class="profile-card">
          <div v-if="bookingsStore.isLoading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading bookings...</p>
          </div>
          <div v-else-if="bookingsStore.bookings.length === 0" class="empty-state">
            <div class="empty-icon">📋</div>
            <p>No bookings yet</p>
            <button @click="router.push({ name: 'TrailsBrowse' })" class="btn-primary">
              Browse Trails
            </button>
          </div>
          <div v-else class="bookings-list">
            <div
              v-for="booking in bookingsStore.bookings"
              :key="booking.id"
              class="booking-item"
              @click="viewBooking(booking.id)"
            >
              <div class="booking-header">
                <div class="booking-title">{{ booking.trail_title || 'Trail' }}</div>
                <div class="booking-status" :class="booking.status.toLowerCase()">
                  {{ booking.status }}
                </div>
              </div>
              <div class="booking-details">
                <div class="booking-detail">
                  <span class="detail-label">Date:</span>
                  <span class="detail-value">
                    {{ new Date(booking.trail_scheduled_date || booking.booking_date).toLocaleDateString() }}
                  </span>
                </div>
                <div class="booking-detail">
                  <span class="detail-label">Spots:</span>
                  <span class="detail-value">{{ booking.spots_booked }}</span>
                </div>
                <div class="booking-detail">
                  <span class="detail-label">Total:</span>
                  <span class="detail-value">{{ formatCurrency(booking.total_price) }}</span>
                </div>
                <div class="booking-detail">
                  <span class="detail-label">Confirmation:</span>
                  <span class="detail-value code">{{ booking.confirmation_code }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Settings Tab -->
        <div v-if="activeTab === 'settings'" class="profile-card">
          <h3>Account Settings</h3>
          <div class="settings-list">
            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-label">Email Notifications</span>
                <span class="setting-description">Receive email updates about your bookings</span>
              </div>
              <input type="checkbox" checked disabled />
            </div>
            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-label">Marketing Emails</span>
                <span class="setting-description">Receive updates about new trails and offers</span>
              </div>
              <input type="checkbox" disabled />
            </div>
          </div>

          <h3 style="margin-top: 2rem;">Preferences</h3>
          <div class="preferences-list">
            <div class="preference-item">
              <span class="preference-label">Preferred Difficulty Level</span>
              <select disabled>
                <option>Any</option>
                <option>Easy</option>
                <option>Moderate</option>
                <option>Hard</option>
                <option>Expert</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.page-header {
  margin-bottom: var(--spacing-2xl);
}

.page-header h1 {
  margin-bottom: var(--spacing-sm);
  font-size: 2.5rem;
  color: var(--color-primary);
}

.page-header p {
  color: var(--color-text-secondary);
  margin-bottom: 0;
}

.profile-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.profile-card {
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-2xl);
}

.profile-header-card {
  background: linear-gradient(135deg, var(--color-primary) 0%, #2d5a47 100%);
  color: white;
  padding: var(--spacing-2xl);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: bold;
  overflow: hidden;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info h2 {
  margin: 0 0 var(--spacing-xs) 0;
  color: white;
  font-size: 1.75rem;
}

.profile-info .email {
  margin: 0 0 var(--spacing-xs) 0;
  opacity: 0.9;
  color: white;
}

.profile-info .username {
  margin: 0;
  opacity: 0.7;
  color: white;
  font-size: 0.9rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
}

.stat-card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-xl);
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--color-primary);
  margin-bottom: var(--spacing-xs);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.tabs-container {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-md);
}

.tabs {
  display: flex;
  gap: var(--spacing-sm);
}

.tab {
  padding: var(--spacing-md) var(--spacing-xl);
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  font-weight: 500;
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.tab:hover {
  background: var(--color-neutral-lighter);
}

.tab.active {
  background: var(--color-primary);
  color: white;
}

.tab-content {
  min-height: 400px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-lg);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-md);
  background: var(--color-neutral-lighter);
  border-radius: var(--radius-md);
}

.info-item .label {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.info-item .value {
  font-size: 1rem;
  color: var(--color-text-primary);
  font-weight: 600;
}

.activity-list {
  margin-top: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.activity-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-neutral-lighter);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.activity-item:hover {
  background: var(--color-neutral-light);
  transform: translateX(4px);
}

.activity-icon {
  font-size: 1.5rem;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.activity-meta {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.activity-status {
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.activity-status.confirmed {
  background: #d1fae5;
  color: #065f46;
}

.activity-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.booking-item {
  padding: var(--spacing-lg);
  background: var(--color-neutral-lighter);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.booking-item:hover {
  background: var(--color-neutral-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.booking-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.booking-status {
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.booking-status.confirmed {
  background: #d1fae5;
  color: #065f46;
}

.booking-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.booking-status.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.booking-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
}

.booking-detail {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.detail-label {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.detail-value {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.detail-value.code {
  font-family: monospace;
  background: white;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
}

.settings-list,
.preferences-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-top: var(--spacing-lg);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  background: var(--color-neutral-lighter);
  border-radius: var(--radius-md);
}

.setting-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.setting-label {
  font-weight: 600;
  color: var(--color-text-primary);
}

.setting-description {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  background: var(--color-neutral-lighter);
  border-radius: var(--radius-md);
}

.preference-label {
  font-weight: 600;
  color: var(--color-text-primary);
}

.preference-item select {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-neutral-light);
  border-radius: var(--radius-md);
  background: white;
}

.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--color-text-secondary);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-md);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl);
  gap: var(--spacing-md);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-neutral-light);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn-primary {
  padding: var(--spacing-md) var(--spacing-xl);
  background: var(--color-accent);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  margin-top: var(--spacing-md);
}

.btn-primary:hover {
  background: var(--color-accent-light);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .tabs {
    flex-direction: column;
  }

  .booking-details {
    grid-template-columns: 1fr;
  }
}
</style>

