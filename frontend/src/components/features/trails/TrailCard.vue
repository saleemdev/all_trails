<script setup lang="ts">
import type { Trail } from '../../../types/index'

defineProps<{
  trail: Trail
}>()

defineEmits<{
  click: []
}>()

const getDifficultyEmoji = (level: string) => {
  const emojis: Record<string, string> = {
    Easy: '🟢',
    Moderate: '🟡',
    Hard: '🟠',
    Expert: '🔴',
  }
  return emojis[level] || '⚪'
}

const getDifficultyColor = (level: string) => {
  const colors: Record<string, string> = {
    Easy: 'bg-green-100 text-green-800 border-green-300',
    Moderate: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    Hard: 'bg-orange-100 text-orange-800 border-orange-300',
    Expert: 'bg-red-100 text-red-800 border-red-300',
  }
  return colors[level] || 'bg-gray-100 text-gray-800 border-gray-300'
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
  <div
    class="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100 h-full flex flex-col cursor-pointer"
    @click="$emit('click')"
  >
    <!-- Card Image -->
    <div class="relative h-56 bg-gradient-to-br from-emerald-900 via-teal-800 to-cyan-900 overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-20">
        <div class="absolute top-0 left-0 w-full h-full"
             style="background-image: url('data:image/svg+xml,%3Csvg width=\'40\' height=\'40\' viewBox=\'0 0 40 40\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.4\' fill-rule=\'evenodd\'%3E%3Cpath d=\'M0 40L40 0H20L0 20M40 40V20L20 40\'/%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>

      <!-- Icon -->
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="text-9xl opacity-60 transform group-hover:scale-110 transition-transform duration-500">
          🏔️
        </div>
      </div>

      <!-- Difficulty Badge -->
      <div class="absolute top-4 right-4">
        <div
          class="px-3 py-1.5 rounded-full font-bold text-sm shadow-lg border-2 backdrop-blur-sm"
          :class="getDifficultyColor(trail.difficulty_level)"
        >
          {{ getDifficultyEmoji(trail.difficulty_level) }} {{ trail.difficulty_level }}
        </div>
      </div>

      <!-- Availability Badge -->
      <div class="absolute bottom-4 left-4">
        <div
          v-if="trail.available_spots > 0"
          class="px-3 py-1.5 bg-emerald-500 text-white rounded-full font-bold text-sm shadow-lg backdrop-blur-sm"
        >
          {{ trail.available_spots }} spots left
        </div>
        <div
          v-else
          class="px-3 py-1.5 bg-red-500 text-white rounded-full font-bold text-sm shadow-lg backdrop-blur-sm"
        >
          Fully Booked
        </div>
      </div>
    </div>

    <!-- Card Content -->
    <div class="p-6 flex flex-col flex-1">
      <!-- Title -->
      <h3 class="text-2xl font-black text-gray-900 mb-2 group-hover:text-emerald-700 transition-colors">
        {{ trail.title }}
      </h3>

      <!-- Location -->
      <div class="flex items-center gap-2 text-gray-600 mb-6">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <span class="font-medium">{{ trail.location }}</span>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-3 gap-4 pb-6 mb-6 border-b-2 border-gray-100">
        <!-- Distance -->
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mb-2 shadow-md">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
          </div>
          <span class="text-sm font-bold text-gray-900">{{ trail.distance_km }} km</span>
          <span class="text-xs text-gray-500">Distance</span>
        </div>

        <!-- Duration -->
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mb-2 shadow-md">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <span class="text-sm font-bold text-gray-900">{{ trail.duration_hours }}h</span>
          <span class="text-xs text-gray-500">Duration</span>
        </div>

        <!-- Elevation -->
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl flex items-center justify-center mb-2 shadow-md">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <span class="text-sm font-bold text-gray-900">{{ trail.elevation_gain_m }}m</span>
          <span class="text-xs text-gray-500">Elevation</span>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-between items-center mt-auto">
        <!-- Price -->
        <div class="flex flex-col">
          <span class="text-xs text-gray-500 font-medium">From</span>
          <span class="text-2xl font-black text-emerald-700">
            {{ formatPrice(trail.price_kshs) }}
          </span>
        </div>

        <!-- View Button -->
        <button class="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-md group-hover:shadow-lg transform group-hover:scale-105">
          View Trail
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Minimal custom styles - leveraging Tailwind utilities */
</style>
