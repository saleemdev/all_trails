<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useBlogStore } from '../../stores/blogStore'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const blogStore = useBlogStore()
const authStore = useAuthStore()

const searchQuery = ref('')

const blogPosts = computed(() => blogStore.filteredBlogPosts)
const categories = computed(() => blogStore.blogCategories)
const isLoading = computed(() => blogStore.isLoading)

onMounted(async () => {
  await blogStore.fetchBlogPosts()
})

const updateSearch = async () => {
  blogStore.setFilters({ search: searchQuery.value || undefined })
  await blogStore.fetchBlogPosts(1)
}

const filterByCategory = async (category?: string) => {
  blogStore.setFilters({ category: category || undefined })
}

const clearFilters = async () => {
  searchQuery.value = ''
  blogStore.clearFilters()
  await blogStore.fetchBlogPosts(1)
}

const viewBlogPost = (slug: string) => {
  router.push({ name: 'BlogDetail', params: { slug } })
}

const openCreatePost = () => {
  router.push({ name: 'BlogCreate' })
}

const handleImageError = (event: Event) => {
  const image = event.target as HTMLImageElement
  image.style.display = 'none'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-KE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<template>
  <div class="page-shell w-full min-h-screen">
    <div class="layout-shell-wide page-block">
      <div class="surface-card mb-4 sm:mb-5">
        <div class="flex flex-wrap items-end justify-between gap-3">
          <div>
            <p class="tone-kicker mb-1">Stories and insight</p>
            <h1 class="text-[clamp(1.35rem,2.2vw,1.9rem)] font-semibold leading-tight tracking-[-0.02em] text-[color:var(--color-text-primary)] mb-0">
              Trail Blog
            </h1>
          </div>
          <button v-if="authStore.isAuthenticated" class="brand-button px-4 py-2.5 text-[13px]" @click="openCreatePost">
            Create Post
          </button>
        </div>
      </div>

      <div class="surface-card mb-5 sm:mb-6">
        <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <div class="w-full max-w-xl">
            <div class="relative">
              <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                v-model="searchQuery"
                @keyup.enter="updateSearch"
                placeholder="Search stories..."
                class="soft-input h-10 w-full pl-12 pr-3.5 text-[14px]"
              />
            </div>
          </div>

          <div class="flex items-center gap-2">
            <button class="soft-button-secondary px-4 py-2.5 text-[13px]" @click="updateSearch">Apply</button>
          </div>
        </div>

        <div class="mt-3 flex flex-wrap gap-2">
          <button
            class="soft-filter px-3 py-1.5 text-[12px]"
            :class="!blogStore.filters.category ? 'soft-filter-active' : 'soft-filter-idle'"
            @click="filterByCategory()"
          >
            All
          </button>
          <button
            v-for="category in categories"
            :key="category"
            @click="filterByCategory(category)"
            class="soft-filter px-3 py-1.5 text-[12px]"
            :class="blogStore.filters.category === category ? 'soft-filter-active' : 'soft-filter-idle'"
          >
            {{ category }}
          </button>
          <button
            v-if="blogStore.filters.search || blogStore.filters.category"
            @click="clearFilters"
            class="soft-button-secondary px-3 py-1.5 text-[12px] text-red-700 border-red-200 bg-red-50 hover:bg-red-100"
          >
            Clear
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="grid grid-cols-1 gap-3.5 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        <div v-for="index in 8" :key="index" class="glass-panel-strong rounded-[1rem] overflow-hidden">
          <div class="h-32 bg-slate-200/80 animate-pulse"></div>
          <div class="p-3.5 space-y-2.5">
            <div class="h-3.5 bg-slate-200/80 rounded animate-pulse"></div>
            <div class="h-3.5 bg-slate-200/70 rounded w-5/6 animate-pulse"></div>
            <div class="h-3 bg-slate-200/60 rounded w-2/3 animate-pulse"></div>
          </div>
        </div>
      </div>

      <div v-else-if="blogPosts.length === 0" class="surface-card-lg text-center">
        <h3 class="text-2xl font-semibold text-slate-900 mb-3">No stories found</h3>
        <p class="mb-6 text-sm tone-body">Try a broader keyword or clear category filters.</p>
        <button @click="clearFilters" class="brand-button px-6 py-3">Clear filters</button>
      </div>

      <div v-else class="grid grid-cols-1 gap-3.5 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        <article
          v-for="post in blogPosts"
          :key="post.id"
          @click="viewBlogPost(post.slug)"
          class="group glass-panel-strong rounded-[1rem] soft-card-hover overflow-hidden cursor-pointer"
        >
          <div class="h-32 bg-slate-900 relative overflow-hidden">
            <img
              v-if="post.featured_image"
              :src="post.featured_image"
              :alt="post.title"
              class="w-full h-full object-cover group-hover:scale-[1.04] transition-transform duration-500"
              @error="handleImageError"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/65 via-slate-900/10 to-transparent"></div>
            <div class="absolute top-3 left-3">
              <span class="soft-badge soft-badge--neutral text-[10px] px-2 py-1">{{ post.category }}</span>
            </div>
          </div>

          <div class="p-3.5">
            <h3 class="trail-card-title text-[0.98rem] font-semibold text-slate-900 mb-2 leading-[1.25] line-clamp-2">{{ post.title }}</h3>
            <p class="text-slate-600 mb-3 text-[13px] leading-[1.4] line-clamp-2">{{ post.excerpt }}</p>
            <div class="flex items-center justify-between gap-2 text-[11px] text-slate-500">
              <div class="flex items-center gap-2 min-w-0">
                <img
                  v-if="post.author_image"
                  :src="post.author_image"
                  :alt="post.author"
                  class="w-7 h-7 rounded-full object-cover border border-[color:var(--color-border-soft)]"
                  @error="handleImageError"
                />
                <div v-else class="brand-mark w-7 h-7 rounded-full text-[10px] text-white">{{ post.author?.charAt(0) || 'A' }}</div>
                <span class="font-medium truncate max-w-[8rem]">{{ post.author }}</span>
              </div>
              <div class="flex items-center gap-2 whitespace-nowrap">
                <span>{{ post.read_time }} min</span>
                <span>·</span>
                <span>{{ formatDate(post.published_date) }}</span>
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
