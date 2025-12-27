<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useBlogStore } from '../../stores/blogStore'

const router = useRouter()
const blogStore = useBlogStore()

const activeTab = ref<'posts' | 'galleries'>('posts')
const searchQuery = ref('')

const blogPosts = computed(() => blogStore.filteredBlogPosts)
const galleries = computed(() => blogStore.filteredGalleries)
const categories = computed(() => blogStore.blogCategories)
const galleryCategories = computed(() => blogStore.galleryCategories)
const isLoading = computed(() => blogStore.isLoading)

onMounted(async () => {
  await Promise.all([
    blogStore.fetchBlogPosts(),
    blogStore.fetchGalleries(),
  ])
})

const updateSearch = () => {
  blogStore.setFilters({ search: searchQuery.value })
}

const filterByCategory = (category: string) => {
  blogStore.setFilters({ category })
}

const clearFilters = () => {
  searchQuery.value = ''
  blogStore.clearFilters()
}

const viewBlogPost = (slug: string) => {
  router.push({ name: 'BlogDetail', params: { slug } })
}

const viewGallery = (id: string) => {
  router.push({ name: 'GalleryDetail', params: { id } })
}

const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
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
  <div class="w-full min-h-screen bg-gray-50">
    <!-- Hero Header -->
    <div class="bg-gradient-to-r from-emerald-900 via-teal-800 to-cyan-900 relative overflow-hidden">
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-0 left-0 w-full h-full"
             style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative z-10">
        <h1 class="text-5xl md:text-6xl font-black text-white mb-4 leading-tight">
          Trails & Tales
        </h1>
        <p class="text-xl text-white/90 max-w-2xl leading-relaxed">
          Explore hiking stories, guides, and stunning photo galleries from Kenya's most beautiful trails.
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Tabs and Search -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 mb-8">
        <div class="flex flex-col lg:flex-row gap-4 items-center justify-between">
          <!-- Tabs -->
          <div class="flex bg-gray-100 rounded-xl p-1">
            <button
              @click="activeTab = 'posts'"
              :class="[
                'px-6 py-3 rounded-lg font-bold transition-all',
                activeTab === 'posts'
                  ? 'bg-white text-emerald-900 shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              📝 Blog Posts
            </button>
            <button
              @click="activeTab = 'galleries'"
              :class="[
                'px-6 py-3 rounded-lg font-bold transition-all',
                activeTab === 'galleries'
                  ? 'bg-white text-emerald-900 shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              📸 Photo Galleries
            </button>
          </div>

          <!-- Search -->
          <div class="flex-1 max-w-md">
            <div class="relative">
              <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                v-model="searchQuery"
                @input="updateSearch"
                placeholder="Search..."
                class="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
              />
            </div>
          </div>
        </div>

        <!-- Category Filters -->
        <div v-if="activeTab === 'posts' && categories.length > 0" class="mt-4 flex flex-wrap gap-2">
          <button
            v-for="category in categories"
            :key="category"
            @click="filterByCategory(category)"
            class="px-4 py-2 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 rounded-lg font-medium transition-all"
          >
            {{ category }}
          </button>
          <button
            v-if="blogStore.filters.category"
            @click="clearFilters"
            class="px-4 py-2 bg-red-50 text-red-700 hover:bg-red-100 rounded-lg font-medium transition-all"
          >
            ✗ Clear
          </button>
        </div>

        <div v-if="activeTab === 'galleries' && galleryCategories.length > 0" class="mt-4 flex flex-wrap gap-2">
          <button
            v-for="category in galleryCategories"
            :key="category"
            @click="filterByCategory(category)"
            class="px-4 py-2 bg-cyan-50 text-cyan-700 hover:bg-cyan-100 rounded-lg font-medium transition-all"
          >
            {{ category }}
          </button>
          <button
            v-if="blogStore.filters.category"
            @click="clearFilters"
            class="px-4 py-2 bg-red-50 text-red-700 hover:bg-red-100 rounded-lg font-medium transition-all"
          >
            ✗ Clear
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="w-16 h-16 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mb-4"></div>
        <p class="text-lg text-gray-600 font-medium">Loading...</p>
      </div>

      <!-- Blog Posts Grid -->
      <div v-else-if="activeTab === 'posts'">
        <div v-if="blogPosts.length === 0" class="bg-white rounded-2xl shadow-lg border border-gray-100 p-16 text-center">
          <div class="text-8xl mb-6">📝</div>
          <h3 class="text-3xl font-black text-gray-900 mb-4">No Blog Posts Found</h3>
          <p class="text-xl text-gray-600 mb-8">
            Try adjusting your search or filters.
          </p>
          <button
            @click="clearFilters"
            class="px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg"
          >
            Clear Filters
          </button>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="post in blogPosts"
            :key="post.id"
            @click="viewBlogPost(post.slug)"
            class="group bg-white rounded-2xl shadow-lg hover:shadow-2xl border border-gray-100 overflow-hidden cursor-pointer transition-all hover:-translate-y-2"
          >
            <!-- Featured Image -->
            <div class="h-56 bg-gradient-to-br from-emerald-600 to-teal-600 relative overflow-hidden">
              <img
                :src="post.featured_image"
                :alt="post.title"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                @error="handleImageError"
              />
              <div class="absolute top-4 left-4">
                <span class="px-3 py-1.5 bg-white/90 backdrop-blur-sm text-emerald-900 rounded-full font-bold text-xs">
                  {{ post.category }}
                </span>
              </div>
            </div>

            <!-- Content -->
            <div class="p-6">
              <h3 class="text-2xl font-black text-gray-900 mb-3 group-hover:text-emerald-700 transition-colors line-clamp-2">
                {{ post.title }}
              </h3>
              <p class="text-gray-600 mb-4 line-clamp-3">
                {{ post.excerpt }}
              </p>

              <!-- Meta -->
              <div class="flex items-center justify-between text-sm text-gray-500">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500 to-teal-500"></div>
                  <span class="font-medium">{{ post.author }}</span>
                </div>
                <div class="flex items-center gap-4">
                  <span>{{ post.read_time }} min read</span>
                  <span>{{ formatDate(post.published_date) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Photo Galleries Grid -->
      <div v-else-if="activeTab === 'galleries'">
        <div v-if="galleries.length === 0" class="bg-white rounded-2xl shadow-lg border border-gray-100 p-16 text-center">
          <div class="text-8xl mb-6">📸</div>
          <h3 class="text-3xl font-black text-gray-900 mb-4">No Galleries Found</h3>
          <p class="text-xl text-gray-600 mb-8">
            Try adjusting your search or filters.
          </p>
          <button
            @click="clearFilters"
            class="px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg"
          >
            Clear Filters
          </button>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div
            v-for="gallery in galleries"
            :key="gallery.id"
            @click="viewGallery(gallery.id)"
            class="group bg-white rounded-2xl shadow-lg hover:shadow-2xl border border-gray-100 overflow-hidden cursor-pointer transition-all"
          >
            <!-- Image Grid Preview -->
            <div class="grid grid-cols-2 gap-2 p-4">
              <div
                v-for="(image, index) in gallery.images.slice(0, 4)"
                :key="image.id"
                :class="[
                  'relative overflow-hidden rounded-xl',
                  index === 0 && gallery.images.length > 1 ? 'col-span-2 h-64' : 'h-32'
                ]"
              >
                <img
                  :src="image.url"
                  :alt="image.caption"
                  class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  @error="handleImageError"
                />
                <div v-if="index === 3 && gallery.images.length > 4" class="absolute inset-0 bg-black/60 flex items-center justify-center">
                  <span class="text-white text-3xl font-black">+{{ gallery.images.length - 4 }}</span>
                </div>
              </div>
            </div>

            <!-- Content -->
            <div class="p-6 pt-0">
              <div class="mb-3">
                <span class="px-3 py-1 bg-cyan-100 text-cyan-800 rounded-full font-bold text-xs">
                  {{ gallery.category }}
                </span>
              </div>
              <h3 class="text-2xl font-black text-gray-900 mb-2 group-hover:text-cyan-700 transition-colors">
                {{ gallery.title }}
              </h3>
              <p class="text-gray-600 mb-4">
                {{ gallery.description }}
              </p>
              <div class="flex items-center justify-between text-sm text-gray-500">
                <span>{{ gallery.images.length }} photos</span>
                <span>{{ formatDate(gallery.created_date) }}</span>
              </div>
            </div>
          </div>
        </div>
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
