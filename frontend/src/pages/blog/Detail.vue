<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBlogStore } from '../../stores/blogStore'

const route = useRoute()
const router = useRouter()
const blogStore = useBlogStore()

const post = computed(() => blogStore.selectedPost)
const isLoading = computed(() => blogStore.isLoading)

onMounted(() => {
  const slug = route.params.slug as string
  blogStore.fetchBlogPostBySlug(slug)
})

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
    <!-- Back Button Bar -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <button
          @click="router.back()"
          class="flex items-center gap-2 px-4 py-2 text-emerald-700 hover:bg-emerald-50 rounded-lg transition-all font-medium"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Blog
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
      <div class="w-16 h-16 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mb-4"></div>
      <p class="text-lg text-gray-600 font-medium">Loading article...</p>
    </div>

    <!-- Article Content -->
    <div v-else-if="post" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <article class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
        <!-- Featured Image -->
        <div class="h-96 bg-gradient-to-br from-emerald-600 to-teal-600 relative">
          <img
            :src="post.featured_image"
            :alt="post.title"
            class="w-full h-full object-cover"
            @error="handleImageError"
          />
        </div>

        <!-- Content -->
        <div class="p-8 md:p-12">
          <!-- Category -->
          <div class="mb-4">
            <span class="px-4 py-2 bg-emerald-100 text-emerald-800 rounded-full font-bold text-sm">
              {{ post.category }}
            </span>
          </div>

          <!-- Title -->
          <h1 class="text-4xl md:text-5xl font-black text-gray-900 mb-6 leading-tight">
            {{ post.title }}
          </h1>

          <!-- Author Info -->
          <div class="flex items-center gap-4 mb-8 pb-8 border-b-2 border-gray-100">
            <div class="w-16 h-16 rounded-full bg-gradient-to-br from-emerald-500 to-teal-500"></div>
            <div>
              <div class="font-black text-lg text-gray-900">{{ post.author }}</div>
              <div class="text-gray-600">
                {{ formatDate(post.published_date) }} · {{ post.read_time }} min read
              </div>
            </div>
          </div>

          <!-- Excerpt -->
          <div class="text-xl text-gray-700 mb-8 leading-relaxed font-medium italic border-l-4 border-emerald-500 pl-6">
            {{ post.excerpt }}
          </div>

          <!-- Content Placeholder -->
          <div class="prose prose-lg max-w-none">
            <p class="text-gray-600 leading-relaxed mb-6">
              {{ post.content }}
            </p>
            <p class="text-gray-600 leading-relaxed">
              [Full article content would be displayed here...]
            </p>
          </div>

          <!-- Tags -->
          <div class="mt-12 pt-8 border-t-2 border-gray-100">
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in post.tags"
                :key="tag"
                class="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg font-medium text-sm hover:bg-gray-200 transition-all cursor-pointer"
              >
                #{{ tag }}
              </span>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- Not Found -->
    <div v-else class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-32 text-center">
      <div class="text-8xl mb-6">📝</div>
      <h2 class="text-3xl font-black text-gray-900 mb-4">Article Not Found</h2>
      <p class="text-xl text-gray-600 mb-8">
        We couldn't find the article you're looking for.
      </p>
      <button
        @click="router.push('/blog')"
        class="px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg"
      >
        Back to Blog
      </button>
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
