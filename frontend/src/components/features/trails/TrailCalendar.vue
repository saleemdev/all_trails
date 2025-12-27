<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Trail } from '../../../types/index'

const props = defineProps<{
  trails: Trail[]
}>()

const emit = defineEmits<{
  trailClick: [trail: Trail]
}>()

const currentDate = ref(new Date())
const selectedDate = ref<Date | null>(null)

const currentMonth = computed(() => currentDate.value.getMonth())
const currentYear = computed(() => currentDate.value.getFullYear())

const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

const daysInMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
})

const firstDayOfMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value, 1).getDay()
})

const calendarDays = computed(() => {
  const days: Array<{ day: number; date: Date; trails: Trail[] }> = []
  
  // Add empty cells for days before the first day of the month
  for (let i = 0; i < firstDayOfMonth.value; i++) {
    days.push({ day: 0, date: new Date(), trails: [] })
  }
  
  // Add days of the month
  for (let day = 1; day <= daysInMonth.value; day++) {
    const date = new Date(currentYear.value, currentMonth.value, day)
    const trailsOnDate = props.trails.filter(trail => {
      const trailDate = new Date(trail.scheduled_date)
      return trailDate.getDate() === day &&
             trailDate.getMonth() === currentMonth.value &&
             trailDate.getFullYear() === currentYear.value
    })
    days.push({ day, date, trails: trailsOnDate })
  }
  
  return days
})

const trailsByDate = computed(() => {
  const map = new Map<string, Trail[]>()
  props.trails.forEach(trail => {
    const date = new Date(trail.scheduled_date)
    const dateKey = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
    if (!map.has(dateKey)) {
      map.set(dateKey, [])
    }
    map.get(dateKey)!.push(trail)
  })
  return map
})

const getTrailsForDate = (day: number) => {
  if (day === 0) return []
  const date = new Date(currentYear.value, currentMonth.value, day)
  const dateKey = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
  return trailsByDate.value.get(dateKey) || []
}

const previousMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
}

const goToToday = () => {
  currentDate.value = new Date()
  selectedDate.value = null
}

const selectDate = (day: number) => {
  if (day === 0) return
  selectedDate.value = new Date(currentYear.value, currentMonth.value, day)
}

const isToday = (day: number) => {
  if (day === 0) return false
  const today = new Date()
  return day === today.getDate() &&
         currentMonth.value === today.getMonth() &&
         currentYear.value === today.getFullYear()
}

const isSelected = (day: number) => {
  if (day === 0 || !selectedDate.value) return false
  return day === selectedDate.value.getDate() &&
         currentMonth.value === selectedDate.value.getMonth() &&
         currentYear.value === selectedDate.value.getFullYear()
}

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const getDifficultyColor = (difficulty: string) => {
  const colors: Record<string, string> = {
    'Easy': 'bg-green-100 text-green-800 border-green-300',
    'Moderate': 'bg-yellow-100 text-yellow-800 border-yellow-300',
    'Hard': 'bg-orange-100 text-orange-800 border-orange-300',
    'Expert': 'bg-red-100 text-red-800 border-red-300'
  }
  return colors[difficulty] || 'bg-gray-100 text-gray-800 border-gray-300'
}
</script>

<template>
  <div class="trail-calendar">
    <!-- Calendar Header -->
    <div class="calendar-header">
      <div class="month-navigation">
        <button @click="previousMonth" class="nav-button" aria-label="Previous month">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <h2 class="month-year">{{ monthNames[currentMonth] }} {{ currentYear }}</h2>
        <button @click="nextMonth" class="nav-button" aria-label="Next month">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      <button @click="goToToday" class="today-button">Today</button>
    </div>

    <!-- Calendar Grid -->
    <div class="calendar-grid">
      <!-- Day Headers -->
      <div class="day-header" v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day">
        {{ day }}
      </div>

      <!-- Calendar Days -->
      <div
        v-for="(calendarDay, index) in calendarDays"
        :key="index"
        :class="[
          'calendar-day',
          { 'empty': calendarDay.day === 0 },
          { 'today': isToday(calendarDay.day) },
          { 'selected': isSelected(calendarDay.day) },
          { 'has-trails': calendarDay.trails.length > 0 }
        ]"
        @click="selectDate(calendarDay.day)"
      >
        <div v-if="calendarDay.day > 0" class="day-number">{{ calendarDay.day }}</div>
        <div v-if="calendarDay.trails.length > 0" class="trails-indicator">
          <div class="trail-dots">
            <span
              v-for="(trail) in calendarDay.trails.slice(0, 3)"
              :key="trail.id"
              :class="['trail-dot', getDifficultyColor(trail.difficulty_level)]"
              :title="trail.title"
            ></span>
            <span v-if="calendarDay.trails.length > 3" class="more-trails">+{{ calendarDay.trails.length - 3 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected Date Trails -->
    <div v-if="selectedDate" class="selected-date-trails">
      <div class="selected-date-header">
        <h3>{{ formatDate(selectedDate) }}</h3>
        <button @click="selectedDate = null" class="close-button">×</button>
      </div>
      <div v-if="getTrailsForDate(selectedDate.getDate()).length === 0" class="no-trails">
        <p>No trails scheduled for this date</p>
      </div>
      <div v-else class="trails-list">
        <div
          v-for="trail in getTrailsForDate(selectedDate.getDate())"
          :key="trail.id"
          class="trail-item"
          @click="emit('trailClick', trail)"
        >
          <div class="trail-item-header">
            <h4>{{ trail.title }}</h4>
            <span :class="['difficulty-badge', getDifficultyColor(trail.difficulty_level)]">
              {{ trail.difficulty_level }}
            </span>
          </div>
          <div class="trail-item-details">
            <span class="detail">📍 {{ trail.location }}</span>
            <span class="detail">⏰ {{ trail.start_time }}</span>
            <span class="detail">💰 {{ new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES' }).format(trail.price_kshs) }}</span>
            <span class="detail">👥 {{ trail.available_spots }} spots</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trail-calendar {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-xl);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 2px solid var(--color-neutral-light);
}

.month-navigation {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.nav-button {
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-neutral-lighter);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--color-text-primary);
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-button:hover {
  background: var(--color-neutral-light);
  transform: scale(1.05);
}

.month-year {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-primary);
  margin: 0;
  min-width: 200px;
  text-align: center;
}

.today-button {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-accent);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.today-button:hover {
  background: var(--color-accent-light);
  transform: translateY(-2px);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
}

.day-header {
  text-align: center;
  font-weight: 600;
  color: var(--color-text-secondary);
  padding: var(--spacing-md);
  font-size: 0.875rem;
  text-transform: uppercase;
}

.calendar-day {
  aspect-ratio: 1;
  border: 2px solid var(--color-neutral-light);
  border-radius: var(--radius-md);
  padding: var(--spacing-sm);
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  position: relative;
  background: white;
}

.calendar-day.empty {
  border: none;
  cursor: default;
  background: transparent;
}

.calendar-day:hover:not(.empty) {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
  transform: scale(1.05);
}

.calendar-day.today {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
  font-weight: bold;
}

.calendar-day.selected {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: white;
}

.calendar-day.has-trails {
  border-color: var(--color-primary);
}

.day-number {
  font-weight: 600;
  font-size: 1rem;
}

.trails-indicator {
  margin-top: auto;
  width: 100%;
}

.trail-dots {
  display: flex;
  gap: 2px;
  flex-wrap: wrap;
  align-items: center;
}

.trail-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1px solid;
}

.more-trails {
  font-size: 0.7rem;
  font-weight: bold;
  color: var(--color-text-secondary);
  margin-left: 4px;
}

.selected-date-trails {
  border-top: 2px solid var(--color-neutral-light);
  padding-top: var(--spacing-xl);
}

.selected-date-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.selected-date-header h3 {
  margin: 0;
  color: var(--color-primary);
  font-size: 1.25rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all var(--transition-base);
}

.close-button:hover {
  background: var(--color-neutral-lighter);
  color: var(--color-text-primary);
}

.no-trails {
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--color-text-secondary);
}

.trails-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.trail-item {
  padding: var(--spacing-lg);
  background: var(--color-neutral-lighter);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  border: 2px solid transparent;
}

.trail-item:hover {
  background: var(--color-neutral-light);
  border-color: var(--color-primary);
  transform: translateX(4px);
}

.trail-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.trail-item-header h4 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: 1.1rem;
}

.difficulty-badge {
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid;
}

.trail-item-details {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.detail {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

@media (max-width: 768px) {
  .calendar-header {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .month-year {
    min-width: auto;
  }

  .trail-item-details {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
}
</style>

