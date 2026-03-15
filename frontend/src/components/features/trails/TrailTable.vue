<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Trail } from '../../../types/index'

const props = defineProps<{
  trails: Trail[]
}>()

const emit = defineEmits<{
  trailClick: [trail: Trail]
}>()

const sortKey = ref<keyof Trail | ''>('')
const sortOrder = ref<'asc' | 'desc'>('asc')

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
  }).format(price)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getDifficultyBadge = (difficulty: string) => {
  const colors: Record<string, string> = {
    Easy: 'bg-green-100 text-green-800 border-green-300',
    Moderate: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    Hard: 'bg-orange-100 text-orange-800 border-orange-300',
    Expert: 'bg-red-100 text-red-800 border-red-300'
  }
  return colors[difficulty] || 'bg-gray-100 text-gray-800 border-gray-300'
}

const sortedTrails = computed(() => {
  if (!sortKey.value) return props.trails

  const sorted = [...props.trails].sort((a, b) => {
    const aVal = a[sortKey.value as keyof Trail]
    const bVal = b[sortKey.value as keyof Trail]

    if (aVal === undefined || aVal === null) return 1
    if (bVal === undefined || bVal === null) return -1

    if (typeof aVal === 'string' && typeof bVal === 'string') {
      return sortOrder.value === 'asc'
        ? aVal.localeCompare(bVal)
        : bVal.localeCompare(aVal)
    }

    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal
    }

    return 0
  })

  return sorted
})

const handleSort = (key: keyof Trail) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const getSortIcon = (key: keyof Trail) => {
  if (sortKey.value !== key) {
    return '↕️'
  }
  return sortOrder.value === 'asc' ? '↑' : '↓'
}
</script>

<template>
  <div class="glass-panel-strong rounded-[2rem] overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="surface-control border-b border-[color:var(--color-border-soft)]">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider cursor-pointer hover:bg-[color:var(--color-surface-control-hover)] transition-colors" @click="handleSort('title')">
              <div class="flex items-center gap-2">Trail <span class="tone-muted">{{ getSortIcon('title') }}</span></div>
            </th>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider cursor-pointer hover:bg-[color:var(--color-surface-control-hover)] transition-colors" @click="handleSort('location')">
              <div class="flex items-center gap-2">Location <span class="tone-muted">{{ getSortIcon('location') }}</span></div>
            </th>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider cursor-pointer hover:bg-[color:var(--color-surface-control-hover)] transition-colors" @click="handleSort('difficulty_level')">
              <div class="flex items-center gap-2">Difficulty <span class="tone-muted">{{ getSortIcon('difficulty_level') }}</span></div>
            </th>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider cursor-pointer hover:bg-[color:var(--color-surface-control-hover)] transition-colors" @click="handleSort('scheduled_date')">
              <div class="flex items-center gap-2">Date <span class="tone-muted">{{ getSortIcon('scheduled_date') }}</span></div>
            </th>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider">Time</th>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider cursor-pointer hover:bg-[color:var(--color-surface-control-hover)] transition-colors" @click="handleSort('distance_km')">
              <div class="flex items-center gap-2">Distance <span class="tone-muted">{{ getSortIcon('distance_km') }}</span></div>
            </th>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider">Duration</th>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider cursor-pointer hover:bg-[color:var(--color-surface-control-hover)] transition-colors" @click="handleSort('price_kshs')">
              <div class="flex items-center gap-2">Price <span class="tone-muted">{{ getSortIcon('price_kshs') }}</span></div>
            </th>
            <th class="px-6 py-4 text-left text-xs font-bold tone-heading uppercase tracking-wider cursor-pointer hover:bg-[color:var(--color-surface-control-hover)] transition-colors" @click="handleSort('available_spots')">
              <div class="flex items-center gap-2">Availability <span class="tone-muted">{{ getSortIcon('available_spots') }}</span></div>
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200/80">
          <tr
            v-for="trail in sortedTrails"
            :key="trail.id"
            class="hover:bg-white/70 cursor-pointer transition-colors"
            @click="emit('trailClick', trail)"
          >
            <td class="px-6 py-4 whitespace-nowrap"><div class="font-semibold text-slate-900 trail-card-title">{{ trail.title }}</div></td>
            <td class="px-6 py-4 whitespace-nowrap"><div class="text-slate-700">📍 {{ trail.location }}</div></td>
            <td class="px-6 py-4 whitespace-nowrap"><span :class="['px-2 py-1 rounded-full text-xs font-semibold border', getDifficultyBadge(trail.difficulty_level)]">{{ trail.difficulty_level }}</span></td>
            <td class="px-6 py-4 whitespace-nowrap"><div class="text-slate-700">{{ formatDate(trail.scheduled_date) }}</div></td>
            <td class="px-6 py-4 whitespace-nowrap"><div class="text-slate-700">{{ trail.start_time }}</div></td>
            <td class="px-6 py-4 whitespace-nowrap"><div class="text-slate-700 font-medium">{{ trail.distance_km }} km</div></td>
            <td class="px-6 py-4 whitespace-nowrap"><div class="text-slate-700">{{ trail.duration_hours }}h</div></td>
            <td class="px-6 py-4 whitespace-nowrap"><div class="font-semibold brand-text">{{ formatPrice(trail.price_kshs) }}</div></td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center gap-2">
                <span :class="trail.available_spots > 0 ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'">{{ trail.available_spots }}</span>
                <span class="text-slate-500 text-sm">/ {{ trail.max_capacity }}</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="sortedTrails.length === 0" class="text-center py-16">
      <p class="text-slate-500 mb-0">No trails to display</p>
    </div>
  </div>
</template>

<style scoped>
table {
  min-width: 1000px;
}
</style>
