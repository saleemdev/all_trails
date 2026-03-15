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
    <div class="page-header relative overflow-hidden">
      <div class="absolute inset-0 hero-grid opacity-30"></div>
      <div class="layout-shell-wide page-hero-block relative z-10">
        <p class="page-kicker-light mb-3">Stories and insight</p>
        <h1 class="page-title-light">Trail Blog</h1>
        <p class="page-copy-light mb-0">Image-led trail stories, guides, and updates sourced live from All Trails content APIs.</p>
      </div>
    </div>

    <div class="layout-shell-wide page-block">
      <div class="surface-card-lg mb-8">
        <div class="flex flex-col lg:flex-row gap-4 items-center justify-between">
          <div class="flex-1 max-w-xl w-full">
            <div class="relative">
              <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                v-model="searchQuery"
                @keyup.enter="updateSearch"
                placeholder="Search stories..."
                class="soft-input w-full pl-12 pr-4 py-3"
              />
            </div>
          </div>

          <div class="flex items-center gap-2 w-full lg:w-auto">
            <button class="soft-button-secondary px-5 py-3" @click="updateSearch">Search</button>
            <button v-if="authStore.isAuthenticated" class="brand-button px-5 py-3" @click="openCreatePost">Create Post</button>
          </div>
        </div>

        <div class="mt-5 flex flex-wrap gap-2">
          <button
            class="soft-filter px-4 py-2"
            :class="!blogStore.filters.category ? 'soft-filter-active' : 'soft-filter-idle'"
            @click="filterByCategory()"
          >
            All
          </button>
          <button
            v-for="category in categories"
            :key="category"
            @click="filterByCategory(category)"
            class="soft-filter px-4 py-2"
            :class="blogStore.filters.category === category ? 'soft-filter-active' : 'soft-filter-idle'"
          >
            {{ category }}
          </button>
          <button
            v-if="blogStore.filters.search || blogStore.filters.category"
            @click="clearFilters"
            class="soft-button-secondary px-4 py-2 text-red-700 border-red-200 bg-red-50 hover:bg-red-100"
          >
            Clear
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div v-for="index in 6" :key="index" class="glass-panel-strong rounded-[1.75rem] overflow-hidden">
          <div class="h-56 bg-slate-200/80 animate-pulse"></div>
          <div class="p-6 space-y-3">
            <div class="h-4 bg-slate-200/80 rounded animate-pulse"></div>
            <div class="h-4 bg-slate-200/70 rounded w-5/6 animate-pulse"></div>
            <div class="h-3 bg-slate-200/60 rounded w-2/3 animate-pulse"></div>
          </div>
        </div>
      </div>

      <div v-else-if="blogPosts.length === 0" class="surface-card-lg text-center">
        <h3 class="text-3xl font-semibold text-slate-900 mb-3">No Blog Posts Found</h3>
        <p class="mb-7 text-base text-slate-600">Try adjusting search or category filters.</p>
        <button @click="clearFilters" class="brand-button px-8 py-4">Clear Filters</button>
      </div>

      <div v-else class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="post in blogPosts"
          :key="post.id"
          @click="viewBlogPost(post.slug)"
          class="group glass-panel-strong rounded-[1.75rem] soft-card-hover overflow-hidden cursor-pointer"
        >
          <div class="h-56 bg-slate-900 relative overflow-hidden">
            <img
              v-if="post.featured_image"
              :src="post.featured_image"
              :alt="post.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              @error="handleImageError"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/65 via-slate-900/10 to-transparent"></div>
            <div class="absolute top-4 left-4">
              <span class="soft-badge soft-badge--neutral">{{ post.category }}</span>
            </div>
          </div>

          <div class="p-6">
            <h3 class="trail-card-title text-xl font-semibold text-slate-900 mb-3 line-clamp-2 sm:text-2xl">{{ post.title }}</h3>
            <p class="text-slate-600 mb-4 line-clamp-3">{{ post.excerpt }}</p>
            <div class="flex items-center justify-between gap-4 text-sm text-slate-500 flex-wrap">
              <div class="flex items-center gap-2 min-w-0">
                <div class="brand-mark w-8 h-8 rounded-full text-[10px] text-white">{{ post.author?.charAt(0) || 'A' }}</div>
                <span class="font-medium truncate">{{ post.author }}</span>
              </div>
              <div class="flex items-center gap-4">
                <span>{{ post.read_time }} min read</span>
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
