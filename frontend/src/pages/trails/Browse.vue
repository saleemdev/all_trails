<script setup lang="ts">
import { onMounted, onUnmounted, computed, ref, defineAsyncComponent } from 'vue'
import { useRouter } from 'vue-router'
import { useTrailsStore } from '../../stores/trailsStore'
import TrailCard from '../../components/features/trails/TrailCard.vue'
import type { Trail } from '../../types/index'

const TrailCalendar = defineAsyncComponent(() => import('../../components/features/trails/TrailCalendar.vue'))
const TrailTable = defineAsyncComponent(() => import('../../components/features/trails/TrailTable.vue'))
const TrailMap = defineAsyncComponent(() => import('../../components/features/trails/TrailMap.vue'))

const router = useRouter()
const trailsStore = useTrailsStore()

const trails = computed(() => trailsStore.trails)
const isLoading = computed(() => trailsStore.isLoading)
const error = computed(() => trailsStore.error)
const filters = computed(() => trailsStore.filters)

const viewMode = ref<'grid' | 'calendar' | 'table' | 'map'>('grid')
const searchQuery = ref(filters.value.search || '')
let searchDebounceTimer: ReturnType<typeof setTimeout> | null = null

const queueTrailFetch = (delay = 0) => {
  if (searchDebounceTimer) {
    clearTimeout(searchDebounceTimer)
    searchDebounceTimer = null
  }

  if (delay <= 0) {
    trailsStore.fetchTrails()
    return
  }

  searchDebounceTimer = setTimeout(() => {
    trailsStore.fetchTrails()
    searchDebounceTimer = null
  }, delay)
}

onMounted(() => {
  trailsStore.fetchTrails()
})

onUnmounted(() => {
  if (searchDebounceTimer) {
    clearTimeout(searchDebounceTimer)
    searchDebounceTimer = null
  }
})

const updateSearch = () => {
  trailsStore.setFilters({ search: searchQuery.value })
  queueTrailFetch(300)
}

const updateDifficulty = (difficulty: string) => {
  trailsStore.setFilters({ difficulty_level: difficulty || undefined })
  queueTrailFetch()
}

const viewTrailDetail = (trailId: string) => {
  router.push({ name: 'TrailDetail', params: { id: trailId } })
}

const clearFilters = () => {
  searchQuery.value = ''
  trailsStore.clearFilters()
  queueTrailFetch()
}

const difficultyLevels = [
  { value: '', label: 'All Levels' },
  { value: 'Easy', label: 'Easy' },
  { value: 'Moderate', label: 'Moderate' },
  { value: 'Hard', label: 'Hard' },
  { value: 'Expert', label: 'Expert' },
]

const isDifficultyActive = (value: string) => filters.value.difficulty_level === value || (!filters.value.difficulty_level && value === '')
const getDifficultyToneClass = (value: string) => {
  const key = value.toLowerCase()
  if (['easy', 'moderate', 'hard', 'expert'].includes(key)) {
    return `difficulty-filter difficulty-filter--${key}`
  }
  return ''
}
const isViewActive = (mode: 'grid' | 'calendar' | 'table' | 'map') => viewMode.value === mode
</script>

<template>
  <div class="dense-ui page-shell w-full min-h-screen">
    <div class="page-header relative overflow-hidden">
      <div class="absolute inset-0 hero-grid opacity-30"></div>
      <div class="layout-shell-wide page-hero-block relative z-10">
        <p class="page-kicker-light mb-3">Trail discovery</p>
        <h1 class="page-title-light max-w-3xl">
          Explore amazing trails
        </h1>
        <p class="page-copy-light mb-0">
          Browse Kenya's hikes through a calmer interface designed to make route comparison feel effortless.
        </p>
      </div>
    </div>

    <div class="layout-shell-wide -mt-6 relative z-20 sm:-mt-8">
      <div class="surface-card">
        <div class="grid grid-cols-1 gap-3 lg:grid-cols-[minmax(0,1.25fr)_minmax(0,1fr)_minmax(9.5rem,auto)] lg:items-end">
          <div class="min-w-0">
            <label class="tone-kicker mb-1.5 block">Search trails</label>
            <div class="relative">
              <svg xmlns="http://www.w3.org/2000/svg" class="tone-muted absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                v-model="searchQuery"
                @input="updateSearch"
                placeholder="Search by name or location..."
                class="soft-input h-9 w-full !pl-9 !pr-3 text-[13px]"
                aria-label="Search trails by name or location"
                autocomplete="off"
              />
            </div>
          </div>

          <div class="min-w-0">
            <label class="tone-kicker mb-1.5 block">Difficulty level</label>
            <div class="flex flex-wrap gap-1.5 pt-0.5">
              <button
                v-for="level in difficultyLevels"
                :key="level.value"
                @click="updateDifficulty(level.value)"
                class="soft-filter inline-flex items-center gap-1.5 whitespace-nowrap rounded-[0.72rem] px-2.5 py-1.5 text-[12px] leading-none"
                :class="[
                  level.value
                    ? getDifficultyToneClass(level.value)
                    : (isDifficultyActive(level.value) ? 'soft-filter-active' : 'soft-filter-idle'),
                  level.value && isDifficultyActive(level.value) ? 'difficulty-filter-active' : '',
                ]"
                :aria-label="`Filter by ${level.label || 'all'} difficulty`"
                :aria-pressed="isDifficultyActive(level.value)"
              >
                <span
                  v-if="level.value"
                  class="difficulty-dot"
                  :class="`difficulty-dot--${level.value.toLowerCase()}`"
                  aria-hidden="true"
                />
                <span>{{ level.label }}</span>
              </button>
            </div>
          </div>

          <div class="flex items-end gap-2 lg:justify-end">
            <div class="min-w-0">
              <p class="tone-kicker mb-1.5">View</p>
              <div class="soft-toggle-strip inline-flex p-1">
                <button
                  @click="viewMode = 'grid'"
                  class="soft-toggle-button flex h-8 w-8 items-center justify-center"
                  :class="{ 'soft-toggle-active': isViewActive('grid') }"
                  aria-label="Grid view"
                  :aria-pressed="isViewActive('grid')"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                </button>
                <button
                  @click="viewMode = 'calendar'"
                  class="soft-toggle-button flex h-8 w-8 items-center justify-center"
                  :class="{ 'soft-toggle-active': isViewActive('calendar') }"
                  aria-label="Calendar view"
                  :aria-pressed="isViewActive('calendar')"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </button>
                <button
                  @click="viewMode = 'table'"
                  class="soft-toggle-button flex h-8 w-8 items-center justify-center"
                  :class="{ 'soft-toggle-active': isViewActive('table') }"
                  aria-label="Table view"
                  :aria-pressed="isViewActive('table')"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </button>
                <button
                  @click="viewMode = 'map'"
                  class="soft-toggle-button flex h-8 w-8 items-center justify-center"
                  :class="{ 'soft-toggle-active': isViewActive('map') }"
                  aria-label="Map view"
                  :aria-pressed="isViewActive('map')"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                  </svg>
                </button>
              </div>
            </div>

            <button
              v-if="filters.search || filters.difficulty_level"
              @click="clearFilters"
              class="surface-danger-subtle inline-flex h-8 w-8 items-center justify-center rounded-[0.72rem] transition-all hover:brightness-[1.04]"
              title="Clear all filters"
              aria-label="Clear all filters"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="layout-shell-wide page-block">
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="soft-spinner mb-4"></div>
        <p class="text-lg text-slate-600 font-medium mb-0">Discovering amazing trails...</p>
      </div>

      <div v-else-if="error" class="surface-card-lg text-center border border-red-200/80">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-red-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-2xl font-semibold text-red-900 mb-2">Error Loading Trails</h3>
        <p class="text-red-700 mb-6">{{ error }}</p>
        <button @click="trailsStore.fetchTrails()" class="soft-button-secondary px-6 py-3">
          Try Again
        </button>
      </div>

      <div v-else-if="trails.length === 0" class="text-center py-32">
        <div class="mb-5 text-6xl">🏔️</div>
        <h3 class="text-3xl font-semibold text-slate-900 mb-3">No Trails Found</h3>
        <p class="mx-auto mb-7 max-w-md text-base text-slate-600">
          Try adjusting your search or filters to discover more trails.
        </p>
        <button
          v-if="filters.search || filters.difficulty_level"
          @click="clearFilters"
          class="brand-button px-8 py-4"
        >
          Clear All Filters
        </button>
      </div>

      <div v-else-if="viewMode === 'grid'">
        <div class="mb-8">
          <h2 class="text-2xl font-semibold text-slate-900">
            <span class="brand-text">{{ trails.length }}</span>
            {{ trails.length === 1 ? 'Trail' : 'Trails' }} Available
          </h2>
          <p class="text-slate-600 mt-1 mb-0">Find your next adventure below</p>
        </div>

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
          <TrailCard
            v-for="trail in trails"
            :key="trail.id"
            :trail="trail"
            @click="viewTrailDetail(trail.id)"
            class="cursor-pointer"
            :aria-label="`View details for ${trail.title}`"
            tabindex="0"
            @keydown.enter="viewTrailDetail(trail.id)"
            @keydown.space.prevent="viewTrailDetail(trail.id)"
          />
        </div>
      </div>

      <div v-else-if="viewMode === 'calendar'">
        <div class="mb-8">
          <h2 class="text-2xl font-semibold text-slate-900">
            <span class="brand-text">{{ trails.length }}</span>
            {{ trails.length === 1 ? 'Trail' : 'Trails' }} Available
          </h2>
          <p class="text-slate-600 mt-1 mb-0">Browse your trail schedule in calendar format</p>
        </div>
        <TrailCalendar
          :trails="trails"
          @trail-click="(trail: Trail) => viewTrailDetail(trail.id)"
        />
      </div>

      <div v-else-if="viewMode === 'table'">
        <div class="mb-8">
          <h2 class="text-2xl font-semibold text-slate-900">
            <span class="brand-text">{{ trails.length }}</span>
            {{ trails.length === 1 ? 'Trail' : 'Trails' }} Available
          </h2>
          <p class="text-slate-600 mt-1 mb-0">Browse trails in table format</p>
        </div>
        <TrailTable
          :trails="trails"
          @trail-click="(trail: Trail) => viewTrailDetail(trail.id)"
        />
      </div>

      <div v-else-if="viewMode === 'map'">
        <div class="mb-8">
          <h2 class="text-2xl font-semibold text-slate-900">
            <span class="brand-text">{{ trails.length }}</span>
            {{ trails.length === 1 ? 'Trail' : 'Trails' }} Available
          </h2>
          <p class="text-slate-600 mt-1 mb-0">Explore trails on the map</p>
        </div>
        <TrailMap
          :trails="trails"
          @trail-click="(trail: Trail) => viewTrailDetail(trail.id)"
        />
      </div>
    </div>
  </div>
</template>
