<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useMerchandiseStore } from '../../stores/merchandiseStore'
import {
  GlassAlert,
  GlassButton,
  GlassCard,
  GlassProductCard,
  GlassSpinner,
} from '../../components/glass'
import type { MerchandiseItem } from '../../types/shop'

const route = useRoute()
const store = useMerchandiseStore()
const searchQuery = ref(store.filters.search || '')
let searchTimer: ReturnType<typeof setTimeout> | null = null

const categoryOptions = computed(() =>
  store.categories.map((category) => ({
    label: category.name,
    value: category.slug,
  }))
)

const refreshCatalog = async () => {
  await store.fetchCatalog()
}

const updateSearch = () => {
  store.setFilters({ search: searchQuery.value })

  if (searchTimer) {
    clearTimeout(searchTimer)
  }

  searchTimer = setTimeout(() => {
    refreshCatalog()
    searchTimer = null
  }, 220)
}

const updateCategory = async (value: string) => {
  store.setFilters({ category: value })
  await refreshCatalog()
}

const updateSort = async (value: string) => {
  store.setFilters({ sort_by: value as 'featured' | 'price-asc' | 'price-desc' | 'rating' | 'newest' })
  await refreshCatalog()
}

const quickAdd = (item: MerchandiseItem) => {
  store.addToCart(item, 1, {
    selected_color: item.available_colors[0],
    selected_size: item.available_sizes[0],
  })
}

onMounted(async () => {
  const initialCategory = typeof route.query.category === 'string' ? route.query.category : ''
  if (initialCategory) {
    store.setFilters({ category: initialCategory })
  }

  if (!store.items.length) {
    await refreshCatalog()
  } else if (!store.categories.length) {
    await store.fetchCategories()
  }
})

watch(
  () => route.query.category,
  async (value) => {
    if (!value && store.filters.category) {
      store.setFilters({ category: '' })
      await refreshCatalog()
      return
    }

    if (typeof value === 'string' && value !== store.filters.category) {
      store.setFilters({ category: value })
      await refreshCatalog()
    }
  }
)

onUnmounted(() => {
  if (searchTimer) {
    clearTimeout(searchTimer)
  }
})
</script>

<template>
  <div class="page-shell">
    <section class="page-header overflow-hidden">
      <div class="hero-grid absolute inset-0 opacity-70" />
      <div class="layout-shell-wide relative py-14 sm:py-16 lg:py-20">
        <div class="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] lg:items-end">
          <div class="text-white">
            <span class="soft-kicker">Phase 2 Merchandise</span>
            <h1 class="mt-5 max-w-3xl text-[clamp(2.3rem,5vw,4.3rem)] font-semibold leading-[0.98] tracking-[-0.05em]">
              Field-tested gear for the way Stepup Adventures members actually hike.
            </h1>
            <p class="mt-5 max-w-2xl text-base leading-7 text-white/80 sm:text-lg sm:leading-8">
              Packs, layers, and trail accessories designed around early starts, long descents, and the little
              details that decide whether a hike feels smooth or annoying.
            </p>

            <div class="mt-8 flex flex-wrap gap-3">
              <GlassButton @click="store.setFilters({ featured_only: true }); refreshCatalog()">
                Shop featured kit
              </GlassButton>
              <GlassButton variant="secondary" @click="store.clearFilters(); searchQuery = ''; refreshCatalog()">
                Reset filters
              </GlassButton>
            </div>
          </div>

          <GlassCard tone="hero" class="relative">
            <p class="text-xs uppercase tracking-[0.22em] text-white/55">Launch capsule</p>
            <p class="mt-3 text-2xl font-semibold">Merch that feels aligned with the premium trip experience.</p>
            <div class="mt-8 grid gap-4 sm:grid-cols-3">
              <div class="rounded-[1.15rem] bg-white/10 px-4 py-4">
                <p class="text-3xl font-semibold">{{ store.categories.length || 4 }}</p>
                <p class="mt-1 text-sm text-white/65">Shop departments</p>
              </div>
              <div class="rounded-[1.15rem] bg-white/10 px-4 py-4">
                <p class="text-3xl font-semibold">{{ store.items.length || 8 }}</p>
                <p class="mt-1 text-sm text-white/65">Launch products</p>
              </div>
              <div class="rounded-[1.15rem] bg-white/10 px-4 py-4">
                <p class="text-3xl font-semibold">2-step</p>
                <p class="mt-1 text-sm text-white/65">BNPL supported</p>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </section>

    <section class="layout-shell-wide -mt-6 pb-12 sm:-mt-8 sm:pb-14">
      <GlassCard tone="strong">
        <div class="grid gap-4 lg:grid-cols-[1.6fr_1fr_1fr_auto] lg:items-end">
          <label class="flex flex-col gap-2 text-sm">
            <span class="font-semibold text-slate-800">Search products</span>
            <input
              v-model="searchQuery"
              type="text"
              class="soft-input rounded-[1.1rem] bg-white/85"
              placeholder="Search by product, category, or feature"
              @input="updateSearch"
            />
          </label>

          <label class="flex flex-col gap-2 text-sm">
            <span class="font-semibold text-slate-800">Category</span>
            <select
              :value="store.filters.category"
              class="soft-input rounded-[1.1rem] bg-white/85"
              @change="updateCategory(($event.target as HTMLSelectElement).value)"
            >
              <option value="">All categories</option>
              <option v-for="option in categoryOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </label>

          <label class="flex flex-col gap-2 text-sm">
            <span class="font-semibold text-slate-800">Sort</span>
            <select
              :value="store.filters.sort_by"
              class="soft-input rounded-[1.1rem] bg-white/85"
              @change="updateSort(($event.target as HTMLSelectElement).value)"
            >
              <option value="featured">Featured first</option>
              <option value="price-asc">Price: low to high</option>
              <option value="price-desc">Price: high to low</option>
              <option value="rating">Highest rated</option>
              <option value="newest">Newest</option>
            </select>
          </label>

          <div class="flex gap-2">
            <button
              class="soft-filter px-4 py-3 text-sm"
              :class="store.filters.featured_only ? 'soft-filter-active' : 'soft-filter-idle'"
              @click="store.setFilters({ featured_only: !store.filters.featured_only }); refreshCatalog()"
            >
              Featured only
            </button>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="layout-shell-wide pb-8 sm:pb-10">
      <div class="mb-6 flex items-center justify-between gap-4">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Curated categories</p>
          <h2 class="app-section-title">Start with a department</h2>
        </div>
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <RouterLink
          v-for="category in store.categories"
          :key="category.slug"
          :to="{ path: '/shop', query: { category: category.slug } }"
          class="group"
          @click="store.setFilters({ category: category.slug })"
        >
          <GlassCard hoverable :padded="false" class="h-full overflow-hidden">
            <img :src="category.image_url" :alt="category.name" class="h-48 w-full object-cover" />
            <div class="p-5">
              <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">{{ category.hero_copy }}</p>
              <h3 class="mt-2 text-2xl font-semibold text-slate-950">{{ category.name }}</h3>
              <p class="mt-3 text-sm leading-6 text-slate-600">{{ category.description }}</p>
            </div>
          </GlassCard>
        </RouterLink>
      </div>
    </section>

    <section class="layout-shell-wide pb-16 sm:pb-20">
      <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">Featured drop</p>
          <h2 class="app-section-title">Signature trail pieces</h2>
        </div>
        <p class="text-sm text-slate-500">{{ store.items.length }} products currently live</p>
      </div>

      <div v-if="store.error" class="mb-6">
        <GlassAlert tone="error" title="Catalog error">
          {{ store.error }}
        </GlassAlert>
      </div>

      <div v-if="store.isLoading" class="py-16">
        <GlassSpinner label="Loading merchandise catalog" size="lg" />
      </div>

      <template v-else>
        <div v-if="store.items.length" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
          <GlassProductCard
            v-for="item in store.items"
            :key="item.item_code"
            :item="item"
            @add-to-cart="quickAdd"
          />
        </div>

        <GlassCard v-else tone="strong" class="text-center">
          <p class="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">No products matched</p>
          <h3 class="mt-3 text-3xl font-semibold text-slate-950">Broaden the search window</h3>
          <p class="mt-4 text-sm leading-6 text-slate-600">
            Try clearing the category filter or searching with a broader term. The catalog is currently scoped to a
            tight launch collection.
          </p>
          <div class="mt-6">
            <GlassButton @click="store.clearFilters(); searchQuery = ''; refreshCatalog()">
              Clear filters
            </GlassButton>
          </div>
        </GlassCard>
      </template>
    </section>
  </div>
</template>
