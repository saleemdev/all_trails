<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTrailsStore } from '../../stores/trailsStore'
import TrailCard from '../../components/features/trails/TrailCard.vue'
import TrailCalendar from '../../components/features/trails/TrailCalendar.vue'
import type { Trail } from '../../types/index'

const router = useRouter()
const trailsStore = useTrailsStore()

const trails = computed(() => trailsStore.trails)
const isLoading = computed(() => trailsStore.isLoading)
const error = computed(() => trailsStore.error)
const filters = computed(() => trailsStore.filters)

const viewMode = ref<'grid' | 'calendar'>('grid')
const searchQuery = ref(filters.value.search || '')

onMounted(() => {
  trailsStore.fetchTrails()
})

const updateSearch = () => {
  trailsStore.setFilters({ search: searchQuery.value })
  trailsStore.fetchTrails()
}

const updateDifficulty = (difficulty: string) => {
  trailsStore.setFilters({ difficulty_level: difficulty || undefined })
  trailsStore.fetchTrails()
}

const viewTrailDetail = (trailId: string) => {
  router.push({ name: 'TrailDetail', params: { id: trailId } })
}

const clearFilters = () => {
  searchQuery.value = ''
  trailsStore.clearFilters()
  trailsStore.fetchTrails()
}

const difficultyLevels = [
  { value: '', label: 'All Levels', emoji: '🌟', color: 'text-gray-700' },
  { value: 'Easy', label: 'Easy', emoji: '🟢', color: 'text-green-600' },
  { value: 'Moderate', label: 'Moderate', emoji: '🟡', color: 'text-yellow-600' },
  { value: 'Hard', label: 'Hard', emoji: '🟠', color: 'text-orange-600' },
  { value: 'Expert', label: 'Expert', emoji: '🔴', color: 'text-red-600' }
]
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
          Explore Amazing Trails
        </h1>
        <p class="text-xl text-white/90 max-w-2xl leading-relaxed">
          Discover breathtaking hiking adventures across Kenya. Find your perfect trail and book your next outdoor experience.
        </p>
      </div>
    </div>

    <!-- Search and Filters Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8 relative z-20">
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-end">
          <!-- Search Input -->
          <div class="lg:col-span-5">
            <label class="block text-sm font-bold text-gray-700 mb-2">Search Trails</label>
            <div class="relative">
              <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                v-model="searchQuery"
                @input="updateSearch"
                placeholder="Search by name or location..."
                class="w-full pl-12 pr-4 py-3.5 text-base border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
              />
            </div>
          </div>

          <!-- Difficulty Filter -->
          <div class="lg:col-span-4">
            <label class="block text-sm font-bold text-gray-700 mb-2">Difficulty Level</label>
            <div class="flex gap-2">
              <button
                v-for="level in difficultyLevels"
                :key="level.value"
                @click="updateDifficulty(level.value)"
                :class="[
                  'flex-1 px-3 py-3.5 rounded-xl font-bold text-sm transition-all border-2',
                  filters.difficulty_level === level.value || (!filters.difficulty_level && level.value === '')
                    ? 'bg-emerald-100 border-emerald-500 text-emerald-900'
                    : 'bg-white border-gray-200 text-gray-600 hover:border-emerald-300 hover:bg-emerald-50'
                ]"
              >
                <span class="block text-lg mb-0.5">{{ level.emoji }}</span>
                <span class="hidden sm:block text-xs">{{ level.label }}</span>
              </button>
            </div>
          </div>

          <!-- View Toggle & Actions -->
          <div class="lg:col-span-3 flex gap-2">
            <!-- View Mode Toggle -->
            <div class="flex-1 bg-gray-100 rounded-xl p-1 flex">
              <button
                @click="viewMode = 'grid'"
                :class="[
                  'flex-1 py-2.5 rounded-lg font-bold text-sm transition-all',
                  viewMode === 'grid'
                    ? 'bg-white text-emerald-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                ]"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
              </button>
              <button
                @click="viewMode = 'calendar'"
                :class="[
                  'flex-1 py-2.5 rounded-lg font-bold text-sm transition-all',
                  viewMode === 'calendar'
                    ? 'bg-white text-emerald-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                ]"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </button>
            </div>

            <!-- Clear Filters -->
            <button
              v-if="filters.search || filters.difficulty_level"
              @click="clearFilters"
              class="px-4 py-2.5 bg-red-50 text-red-600 rounded-xl font-bold hover:bg-red-100 transition-all border-2 border-red-200"
              title="Clear all filters"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="w-16 h-16 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mb-4"></div>
        <p class="text-lg text-gray-600 font-medium">Discovering amazing trails...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border-2 border-red-200 rounded-2xl p-8 text-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-red-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-2xl font-bold text-red-900 mb-2">Error Loading Trails</h3>
        <p class="text-red-700 mb-6">{{ error }}</p>
        <button @click="trailsStore.fetchTrails()" class="px-6 py-3 bg-red-600 text-white font-bold rounded-xl hover:bg-red-700 transition-all">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="trails.length === 0" class="text-center py-32">
        <div class="text-8xl mb-6">🏔️</div>
        <h3 class="text-4xl font-black text-gray-900 mb-4">No Trails Found</h3>
        <p class="text-xl text-gray-600 mb-8 max-w-md mx-auto">
          Try adjusting your search or filters to discover more trails.
        </p>
        <button
          v-if="filters.search || filters.difficulty_level"
          @click="clearFilters"
          class="px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg hover:shadow-xl transform hover:scale-105"
        >
          Clear All Filters
        </button>
      </div>

      <!-- Grid View -->
      <div v-else-if="viewMode === 'grid'">
        <!-- Results Count -->
        <div class="mb-8">
          <h2 class="text-2xl font-black text-gray-900">
            <span class="text-emerald-600">{{ trails.length }}</span>
            {{ trails.length === 1 ? 'Trail' : 'Trails' }} Available
          </h2>
          <p class="text-gray-600 mt-1">Find your next adventure below</p>
        </div>

        <!-- Trail Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <TrailCard
            v-for="trail in trails"
            :key="trail.id"
            :trail="trail"
            @click="viewTrailDetail(trail.id)"
            class="transform hover:scale-105 transition-transform cursor-pointer"
          />
        </div>
      </div>

      <!-- Calendar View -->
      <div v-else-if="viewMode === 'calendar'">
        <TrailCalendar
          :trails="trails"
          @trail-click="(trail: Trail) => viewTrailDetail(trail.id)"
        />
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
