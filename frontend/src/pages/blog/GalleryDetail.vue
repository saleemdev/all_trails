<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBlogStore } from '../../stores/blogStore'

const route = useRoute()
const router = useRouter()
const blogStore = useBlogStore()

const gallery = computed(() => blogStore.selectedGallery)
const isLoading = computed(() => blogStore.isLoading)
const selectedImageIndex = ref(0)

onMounted(() => {
  const id = route.params.id as string
  blogStore.fetchGalleryById(id)
})

const selectImage = (index: number) => {
  selectedImageIndex.value = index
}

const nextImage = () => {
  if (gallery.value) {
    selectedImageIndex.value = (selectedImageIndex.value + 1) % gallery.value.images.length
  }
}

const prevImage = () => {
  if (gallery.value) {
    selectedImageIndex.value = (selectedImageIndex.value - 1 + gallery.value.images.length) % gallery.value.images.length
  }
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
    <!-- Back Button Bar -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <button
          @click="router.back()"
          class="flex items-center gap-2 px-4 py-2 text-cyan-700 hover:bg-cyan-50 rounded-lg transition-all font-medium"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Galleries
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
      <div class="w-16 h-16 border-4 border-cyan-200 border-t-cyan-600 rounded-full animate-spin mb-4"></div>
      <p class="text-lg text-gray-600 font-medium">Loading gallery...</p>
    </div>

    <!-- Gallery Content -->
    <div v-else-if="gallery" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 mb-8">
        <div class="flex items-start justify-between">
          <div>
            <span class="px-3 py-1.5 bg-cyan-100 text-cyan-800 rounded-full font-bold text-sm mb-4 inline-block">
              {{ gallery.category }}
            </span>
            <h1 class="text-4xl md:text-5xl font-black text-gray-900 mb-4">
              {{ gallery.title }}
            </h1>
            <p class="text-xl text-gray-600 mb-4">
              {{ gallery.description }}
            </p>
            <div class="flex items-center gap-4 text-gray-500">
              <span v-if="gallery.photographer">📷 {{ gallery.photographer }}</span>
              <span>{{ formatDate(gallery.created_date) }}</span>
              <span>{{ gallery.images.length }} photos</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Image Viewer -->
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden mb-8">
        <div class="relative h-[600px] bg-black">
          <img
            v-if="gallery.images[selectedImageIndex]"
            :src="gallery.images[selectedImageIndex]?.url || ''"
            :alt="gallery.images[selectedImageIndex]?.caption || ''"
            class="w-full h-full object-contain"
            @error="handleImageError"
          />

          <!-- Navigation Arrows -->
          <button
            @click="prevImage"
            class="absolute left-4 top-1/2 transform -translate-y-1/2 w-12 h-12 bg-white/90 hover:bg-white rounded-full flex items-center justify-center shadow-lg transition-all"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            @click="nextImage"
            class="absolute right-4 top-1/2 transform -translate-y-1/2 w-12 h-12 bg-white/90 hover:bg-white rounded-full flex items-center justify-center shadow-lg transition-all"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Image Counter -->
          <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 px-4 py-2 bg-black/70 backdrop-blur-sm text-white rounded-full font-bold">
            {{ selectedImageIndex + 1 }} / {{ gallery.images.length }}
          </div>
        </div>

        <!-- Caption -->
        <div v-if="gallery.images[selectedImageIndex]" class="p-6 bg-gray-50 border-t border-gray-200">
          <p class="text-gray-900 font-medium text-center">
            {{ gallery.images[selectedImageIndex]?.caption || '' }}
          </p>
        </div>
      </div>

      <!-- Thumbnail Grid -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
        <h2 class="text-2xl font-black text-gray-900 mb-4">All Photos</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          <div
            v-for="(image, index) in gallery.images"
            :key="image.id"
            @click="selectImage(index)"
            :class="[
              'relative h-32 rounded-xl overflow-hidden cursor-pointer transition-all',
              selectedImageIndex === index
                ? 'ring-4 ring-cyan-500 scale-105'
                : 'hover:scale-105'
            ]"
          >
            <img
              :src="image.url"
              :alt="image.caption"
              class="w-full h-full object-cover"
              @error="handleImageError"
            />
            <div v-if="selectedImageIndex === index" class="absolute inset-0 bg-cyan-500/20"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-32 text-center">
      <div class="text-8xl mb-6">📸</div>
      <h2 class="text-3xl font-black text-gray-900 mb-4">Gallery Not Found</h2>
      <p class="text-xl text-gray-600 mb-8">
        We couldn't find the gallery you're looking for.
      </p>
      <button
        @click="router.push('/blog')"
        class="px-8 py-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-bold rounded-xl hover:from-cyan-700 hover:to-blue-700 transition-all shadow-lg"
      >
        Back to Galleries
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
