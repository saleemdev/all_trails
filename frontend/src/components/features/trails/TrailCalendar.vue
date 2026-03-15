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

const normalizeDate = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const calendarDays = computed(() => {
  const days: Array<{ day: number; date: Date; trails: Trail[]; dateKey: string }> = []

  for (let i = 0; i < firstDayOfMonth.value; i++) {
    days.push({ day: 0, date: new Date(), trails: [], dateKey: '' })
  }

  for (let day = 1; day <= daysInMonth.value; day++) {
    const date = new Date(currentYear.value, currentMonth.value, day)
    const dateKey = normalizeDate(date)
    const trailsOnDate = props.trails.filter(trail => normalizeDate(trail.scheduled_date) === dateKey)
    days.push({ day, date, trails: trailsOnDate, dateKey })
  }

  return days
})

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

const getTrailsForSelectedDate = computed(() => {
  if (!selectedDate.value) return []
  const dateKey = normalizeDate(selectedDate.value)
  return props.trails.filter(trail => normalizeDate(trail.scheduled_date) === dateKey)
})

const getDifficultyColor = (difficulty: string) => {
  const colors: Record<string, string> = {
    Easy: 'bg-green-500',
    Moderate: 'bg-yellow-500',
    Hard: 'bg-orange-500',
    Expert: 'bg-red-500'
  }
  return colors[difficulty] || 'bg-gray-500'
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
  <div class="glass-panel-strong rounded-[2rem] p-6 lg:p-8">
    <div class="flex flex-col sm:flex-row justify-between items-center gap-4 mb-8 pb-6 border-b border-slate-200/80">
      <div class="flex items-center gap-4">
        <button @click="previousMonth" class="soft-button-secondary w-11 h-11 p-0" aria-label="Previous month">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <h2 class="text-2xl font-bold text-slate-900 min-w-[200px] text-center">{{ monthNames[currentMonth] }} {{ currentYear }}</h2>
        <button @click="nextMonth" class="soft-button-secondary w-11 h-11 p-0" aria-label="Next month">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      <button @click="goToToday" class="brand-button px-4 py-2">Today</button>
    </div>

    <div class="grid grid-cols-7 gap-2 mb-8">
      <div
        v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']"
        :key="day"
        class="text-center font-semibold text-slate-500 py-2 text-sm uppercase"
      >
        {{ day }}
      </div>

      <div
        v-for="(calendarDay, index) in calendarDays"
        :key="index"
        :class="[
          'aspect-square rounded-[1rem] p-2 cursor-pointer transition-all flex flex-col items-start justify-start relative border',
          calendarDay.day === 0 ? 'border-transparent' : 'border-slate-200 hover:border-[color:var(--color-border-strong)] hover:bg-white/70',
          isToday(calendarDay.day) ? 'border-[color:var(--color-primary)] bg-[rgba(49,83,72,0.08)] font-bold' : '',
          isSelected(calendarDay.day) ? 'border-[color:var(--color-primary)] bg-[var(--color-primary)] text-white' : '',
          calendarDay.trails.length > 0 ? 'shadow-sm' : ''
        ]"
        @click="selectDate(calendarDay.day)"
      >
        <div v-if="calendarDay.day > 0" class="text-sm font-semibold mb-1">{{ calendarDay.day }}</div>
        <div v-if="calendarDay.trails.length > 0" class="mt-auto w-full">
          <div class="flex gap-1 flex-wrap">
            <span
              v-for="trail in calendarDay.trails.slice(0, 3)"
              :key="trail.id"
              :class="['w-2 h-2 rounded-full', getDifficultyColor(trail.difficulty_level)]"
              :title="trail.title"
            ></span>
            <span v-if="calendarDay.trails.length > 3" class="text-xs font-bold" :class="isSelected(calendarDay.day) ? 'text-white/80' : 'text-slate-600'">
              +{{ calendarDay.trails.length - 3 }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedDate" class="border-t border-slate-200/80 pt-6">
      <div class="flex justify-between items-center mb-4 gap-4">
        <h3 class="text-xl font-bold text-slate-900">{{ formatDate(selectedDate) }}</h3>
        <button @click="selectedDate = null" class="soft-button-secondary w-11 h-11 p-0" aria-label="Close">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div v-if="getTrailsForSelectedDate.length === 0" class="text-center py-12 text-slate-500">
        <p class="mb-0">No trails scheduled for this date</p>
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="trail in getTrailsForSelectedDate"
          :key="trail.id"
          class="surface-muted rounded-[1.25rem] p-4 cursor-pointer hover:bg-white/90 border border-transparent hover:border-[color:var(--color-border-strong)] transition-all"
          @click="emit('trailClick', trail)"
        >
          <div class="flex justify-between items-center mb-2 gap-4 flex-wrap">
            <h4 class="font-bold text-slate-900 mb-0">{{ trail.title }}</h4>
            <span :class="['px-3 py-1 rounded-full text-xs font-semibold', getDifficultyColor(trail.difficulty_level) + ' text-white']">
              {{ trail.difficulty_level }}
            </span>
          </div>
          <div class="flex flex-wrap gap-4 text-sm text-slate-600">
            <span>📍 {{ trail.location }}</span>
            <span>⏰ {{ trail.start_time }}</span>
            <span>💰 {{ formatPrice(trail.price_kshs) }}</span>
            <span>👥 {{ trail.available_spots }} spots</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
