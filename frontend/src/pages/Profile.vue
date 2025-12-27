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
</script>

<template>
  <div class="profile-page">
    <!-- Hero Header with Better Visual Hierarchy -->
    <div class="profile-hero">
      <div class="profile-hero-content">
        <div class="profile-avatar-large">
          <img v-if="user?.user_image" :src="user.user_image" :alt="user.full_name" />
          <div v-else class="avatar-initial">
            {{ user?.full_name?.charAt(0)?.toUpperCase() || '👤' }}
          </div>
        </div>
        <div class="profile-hero-info">
          <h1 class="profile-name">{{ user?.full_name || user?.name || 'User' }}</h1>
          <p class="profile-email">{{ user?.email }}</p>
          <p class="profile-username">@{{ user?.name }}</p>
        </div>
      </div>
    </div>

    <!-- Stats Cards with Gestalt Proximity -->
    <div v-if="userStats" class="stats-section">
      <div class="stats-grid">
        <div class="stat-card" role="article" aria-label="Total bookings">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">📅</div>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ userStats.total_bookings || 0 }}</div>
            <div class="stat-label">Total Bookings</div>
          </div>
        </div>
        <div class="stat-card" role="article" aria-label="Confirmed bookings">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">✅</div>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ userStats.confirmed_bookings || 0 }}</div>
            <div class="stat-label">Confirmed</div>
          </div>
        </div>
        <div class="stat-card" role="article" aria-label="Completed bookings">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">🏁</div>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ userStats.completed_bookings || 0 }}</div>
            <div class="stat-label">Completed</div>
          </div>
        </div>
        <div class="stat-card" role="article" aria-label="Total spent">
          <div class="stat-icon-wrapper">
            <div class="stat-icon">💰</div>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatCurrency(userStats.total_spent || 0) }}</div>
            <div class="stat-label">Total Spent</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs with Better Accessibility -->
    <div class="tabs-section" role="tablist" aria-label="Profile sections">
      <button
        @click="activeTab = 'overview'"
        :class="['tab-button', { active: activeTab === 'overview' }]"
        role="tab"
        :aria-selected="activeTab === 'overview'"
        aria-controls="overview-panel"
        id="overview-tab"
      >
        Overview
      </button>
      <button
        @click="activeTab = 'bookings'"
        :class="['tab-button', { active: activeTab === 'bookings' }]"
        role="tab"
        :aria-selected="activeTab === 'bookings'"
        aria-controls="bookings-panel"
        id="bookings-tab"
      >
        My Bookings
        <span v-if="bookingsStore.bookings.length > 0" class="tab-badge">
          {{ bookingsStore.bookings.length }}
        </span>
      </button>
      <button
        @click="activeTab = 'settings'"
        :class="['tab-button', { active: activeTab === 'settings' }]"
        role="tab"
        :aria-selected="activeTab === 'settings'"
        aria-controls="settings-panel"
        id="settings-tab"
      >
        Settings
      </button>
    </div>

    <!-- Tab Content with Proper Containment -->
    <div class="tab-content-wrapper">
      <!-- Overview Tab -->
      <div
        v-if="activeTab === 'overview'"
        id="overview-panel"
        role="tabpanel"
        aria-labelledby="overview-tab"
        class="tab-panel"
      >
        <div class="content-card">
          <h2 class="section-title">Account Information</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Full Name</span>
              <span class="info-value">{{ user?.full_name || user?.name }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Email</span>
              <span class="info-value">{{ user?.email }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Username</span>
              <span class="info-value">{{ user?.name }}</span>
            </div>
          </div>
        </div>

        <div class="content-card">
          <h2 class="section-title">Recent Activity</h2>
          <div v-if="bookingsStore.upcomingBookings.length > 0" class="activity-list">
            <button
              v-for="booking in bookingsStore.upcomingBookings.slice(0, 5)"
              :key="booking.id"
              @click="viewBooking(booking.id)"
              class="activity-item"
              aria-label="View booking for {{ booking.trail_title || 'Trail' }}"
            >
              <div class="activity-icon">🎒</div>
              <div class="activity-content">
                <div class="activity-title">{{ booking.trail_title || 'Trail' }}</div>
                <div class="activity-meta">
                  {{ formatDate(booking.trail_scheduled_date || booking.booking_date) }} • 
                  {{ booking.spots_booked }} {{ booking.spots_booked === 1 ? 'spot' : 'spots' }}
                </div>
              </div>
              <div class="activity-status" :class="booking.status.toLowerCase()">
                {{ booking.status }}
              </div>
            </button>
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">📅</div>
            <p>No upcoming bookings</p>
            <button
              @click="router.push({ name: 'TrailBrowse' })"
              class="btn-primary"
              aria-label="Browse trails"
            >
              Browse Trails
            </button>
          </div>
        </div>
      </div>

      <!-- Bookings Tab -->
      <div
        v-if="activeTab === 'bookings'"
        id="bookings-panel"
        role="tabpanel"
        aria-labelledby="bookings-tab"
        class="tab-panel"
      >
        <div class="content-card">
          <div v-if="bookingsStore.isLoading" class="loading-state">
            <div class="spinner" aria-label="Loading bookings"></div>
            <p>Loading bookings...</p>
          </div>
          <div v-else-if="bookingsStore.bookings.length === 0" class="empty-state">
            <div class="empty-icon">📋</div>
            <h3>No bookings yet</h3>
            <p>Start your adventure by booking your first trail!</p>
            <button
              @click="router.push({ name: 'TrailBrowse' })"
              class="btn-primary"
              aria-label="Browse trails"
            >
              Browse Trails
            </button>
          </div>
          <div v-else class="bookings-list">
            <button
              v-for="booking in bookingsStore.bookings"
              :key="booking.id"
              @click="viewBooking(booking.id)"
              class="booking-item"
              :aria-label="`View booking ${booking.confirmation_code}`"
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
                    {{ formatDate(booking.trail_scheduled_date || booking.booking_date) }}
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
            </button>
          </div>
        </div>
      </div>

      <!-- Settings Tab -->
      <div
        v-if="activeTab === 'settings'"
        id="settings-panel"
        role="tabpanel"
        aria-labelledby="settings-tab"
        class="tab-panel"
      >
        <div class="content-card">
          <h2 class="section-title">Account Settings</h2>
          <div class="settings-list">
            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-label">Email Notifications</span>
                <span class="setting-description">Receive email updates about your bookings</span>
              </div>
              <input
                type="checkbox"
                checked
                disabled
                aria-label="Email notifications enabled"
              />
            </div>
            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-label">Marketing Emails</span>
                <span class="setting-description">Receive updates about new trails and offers</span>
              </div>
              <input
                type="checkbox"
                disabled
                aria-label="Marketing emails disabled"
              />
            </div>
          </div>
        </div>

        <div class="content-card">
          <h2 class="section-title">Preferences</h2>
          <div class="preferences-list">
            <div class="preference-item">
              <label for="difficulty-preference" class="preference-label">
                Preferred Difficulty Level
              </label>
              <select id="difficulty-preference" disabled aria-label="Preferred difficulty level">
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
/* Mobile-First Base Styles */
.profile-page {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
  overflow-x: hidden; /* Prevent horizontal overflow */
  box-sizing: border-box;
}

/* Hero Section with Better Visual Hierarchy */
.profile-hero {
  background: linear-gradient(135deg, #1B3A2D 0%, #2d5a47 100%);
  border-radius: 1rem;
  padding: 2rem 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
}

.profile-avatar-large {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border: 4px solid rgba(255, 255, 255, 0.3);
  flex-shrink: 0;
}

.profile-avatar-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initial {
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
}

.profile-hero-info {
  color: white;
  min-width: 0; /* Prevent overflow */
}

.profile-name {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: white;
  word-wrap: break-word;
}

.profile-email {
  margin: 0 0 0.25rem 0;
  opacity: 0.9;
  color: white;
  font-size: 0.95rem;
  word-wrap: break-word;
}

.profile-username {
  margin: 0;
  opacity: 0.7;
  color: white;
  font-size: 0.875rem;
  word-wrap: break-word;
}

/* Stats Section with Gestalt Proximity */
.stats-section {
  margin-bottom: 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.stat-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.25rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
  min-width: 0; /* Prevent overflow */
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.stat-icon-wrapper {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon {
  font-size: 2rem;
  line-height: 1;
}

.stat-content {
  width: 100%;
  min-width: 0;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1B3A2D;
  margin-bottom: 0.25rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.stat-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

/* Tabs with Better Accessibility */
.tabs-section {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.tabs-section::-webkit-scrollbar {
  display: none;
}

.tab-button {
  padding: 0.75rem 1.25rem;
  border: none;
  background: transparent;
  color: #6B7280;
  font-weight: 500;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  min-width: fit-content;
}

.tab-button:hover {
  background: #F3F4F6;
}

.tab-button:focus {
  outline: 2px solid #1B3A2D;
  outline-offset: 2px;
}

.tab-button.active {
  background: #1B3A2D;
  color: white;
}

.tab-badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.tab-button.active .tab-badge {
  background: rgba(255, 255, 255, 0.3);
}

/* Tab Content with Proper Containment */
.tab-content-wrapper {
  width: 100%;
  box-sizing: border-box;
  min-height: 400px;
}

.tab-panel {
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.content-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden; /* Prevent overflow */
}

.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1B3A2D;
  margin: 0 0 1.25rem 0;
}

/* Info Grid with Gestalt Similarity */
.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
  border: 1px solid #E5E7EB;
}

.info-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.info-value {
  font-size: 1rem;
  color: #111827;
  font-weight: 600;
  word-wrap: break-word;
}

/* Activity List */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
  box-sizing: border-box;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #E5E7EB;
  width: 100%;
  box-sizing: border-box;
  text-align: left;
}

.activity-item:hover {
  background: #F3F4F6;
  transform: translateX(4px);
  border-color: #1B3A2D;
}

.activity-item:focus {
  outline: 2px solid #1B3A2D;
  outline-offset: 2px;
}

.activity-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-title {
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.25rem;
  word-wrap: break-word;
}

.activity-meta {
  font-size: 0.875rem;
  color: #6B7280;
}

.activity-status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
  flex-shrink: 0;
}

.activity-status.confirmed {
  background: #D1FAE5;
  color: #065F46;
}

.activity-status.pending {
  background: #FEF3C7;
  color: #92400E;
}

/* Bookings List */
.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.booking-item {
  padding: 1.25rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #E5E7EB;
  width: 100%;
  box-sizing: border-box;
  text-align: left;
}

.booking-item:hover {
  background: #F3F4F6;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-color: #1B3A2D;
}

.booking-item:focus {
  outline: 2px solid #1B3A2D;
  outline-offset: 2px;
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.booking-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  word-wrap: break-word;
  flex: 1;
  min-width: 0;
}

.booking-status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
  flex-shrink: 0;
}

.booking-status.confirmed {
  background: #D1FAE5;
  color: #065F46;
}

.booking-status.pending {
  background: #FEF3C7;
  color: #92400E;
}

.booking-status.cancelled {
  background: #FEE2E2;
  color: #991B1B;
}

.booking-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.booking-detail {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.detail-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.detail-value {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  word-wrap: break-word;
}

.detail-value.code {
  font-family: 'Courier New', monospace;
  background: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid #E5E7EB;
  display: inline-block;
}

/* Settings */
.settings-list,
.preferences-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
  border: 1px solid #E5E7EB;
  gap: 1rem;
  flex-wrap: wrap;
}

.setting-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
  min-width: 0;
}

.setting-label {
  font-weight: 600;
  color: #111827;
  word-wrap: break-word;
}

.setting-description {
  font-size: 0.875rem;
  color: #6B7280;
}

.preference-item {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.25rem;
  background: #F9FAFB;
  border-radius: 0.5rem;
  border: 1px solid #E5E7EB;
}

.preference-label {
  font-weight: 600;
  color: #111827;
}

.preference-item select {
  padding: 0.5rem 1rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.5rem;
  background: white;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
}

/* Empty States */
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  color: #6B7280;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  margin: 0 0 1.5rem 0;
  color: #6B7280;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #E5E7EB;
  border-top-color: #1B3A2D;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Buttons */
.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #E85D1F;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
}

.btn-primary:hover {
  background: #F07A3F;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn-primary:focus {
  outline: 2px solid #E85D1F;
  outline-offset: 2px;
}

/* Tablet and Desktop Responsive */
@media (min-width: 640px) {
  .profile-page {
    padding: 1.5rem;
  }

  .profile-hero {
    padding: 2.5rem 2rem;
  }

  .profile-hero-content {
    flex-direction: row;
    text-align: left;
    gap: 1.5rem;
  }

  .profile-avatar-large {
    width: 120px;
    height: 120px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .booking-details {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) {
  .profile-page {
    padding: 2rem;
  }

  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .info-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .booking-details {
    grid-template-columns: repeat(4, 1fr);
  }

  .setting-item {
    flex-wrap: nowrap;
  }

  .preference-item {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .preference-item select {
    width: auto;
    min-width: 200px;
  }
}

@media (min-width: 1024px) {
  .profile-page {
    padding: 2.5rem;
  }

  .content-card {
    padding: 2rem;
  }
}
</style>
