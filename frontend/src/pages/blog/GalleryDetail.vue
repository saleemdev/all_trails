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
  <div class="page-shell w-full min-h-screen">
    <div class="layout-shell-wide page-block-tight">
      <button @click="router.back()" class="soft-button-secondary px-5 py-3 mb-6">
        ← Back to Galleries
      </button>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="soft-spinner mb-4"></div>
        <p class="text-lg text-slate-600 font-medium mb-0">Loading gallery...</p>
      </div>

      <div v-else-if="gallery" class="space-y-8">
        <section class="surface-card-lg">
          <span class="soft-badge soft-badge--neutral mb-4 inline-flex">{{ gallery.category }}</span>
          <h1 class="text-[clamp(2rem,4vw,3.1rem)] font-semibold text-slate-900 mb-4 leading-[1.02] tracking-[-0.04em]">{{ gallery.title }}</h1>
          <p class="text-base text-slate-600 sm:text-lg mb-4">{{ gallery.description }}</p>
          <div class="flex items-center gap-4 text-slate-500 flex-wrap">
            <span v-if="gallery.photographer">📷 {{ gallery.photographer }}</span>
            <span>{{ formatDate(gallery.created_date) }}</span>
            <span>{{ gallery.images.length }} photos</span>
          </div>
        </section>

        <section class="glass-panel-strong rounded-[1.5rem] overflow-hidden">
          <div class="relative h-[600px] bg-slate-950">
            <img
              v-if="gallery.images[selectedImageIndex]"
              :src="gallery.images[selectedImageIndex]?.url || ''"
              :alt="gallery.images[selectedImageIndex]?.caption || ''"
              class="w-full h-full object-contain"
              @error="handleImageError"
            />

            <button
              @click="prevImage"
              class="absolute left-4 top-1/2 transform -translate-y-1/2 w-12 h-12 bg-white/85 hover:bg-white rounded-full flex items-center justify-center shadow-lg transition-all"
              aria-label="Previous image"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              @click="nextImage"
              class="absolute right-4 top-1/2 transform -translate-y-1/2 w-12 h-12 bg-white/85 hover:bg-white rounded-full flex items-center justify-center shadow-lg transition-all"
              aria-label="Next image"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 px-4 py-2 bg-slate-950/70 backdrop-blur-sm text-white rounded-full font-bold">
              {{ selectedImageIndex + 1 }} / {{ gallery.images.length }}
            </div>
          </div>

          <div v-if="gallery.images[selectedImageIndex]" class="p-6 surface-muted border-t border-slate-200/80">
            <p class="text-slate-900 font-medium text-center mb-0">{{ gallery.images[selectedImageIndex]?.caption || '' }}</p>
          </div>
        </section>

        <section class="surface-card-lg">
          <h2 class="text-2xl font-semibold text-slate-900 mb-4">All Photos</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            <button
              v-for="(image, index) in gallery.images"
              :key="image.id"
              @click="selectImage(index)"
              :class="[
                'relative h-32 rounded-[1rem] overflow-hidden cursor-pointer transition-all border',
                selectedImageIndex === index
                  ? 'border-[color:var(--color-primary)] ring-2 ring-[color:var(--color-primary-ring)] scale-[1.02]'
                  : 'border-slate-200 hover:scale-[1.02]'
              ]"
            >
              <img
                :src="image.url"
                :alt="image.caption"
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
              <div v-if="selectedImageIndex === index" class="absolute inset-0 bg-[rgba(49,83,72,0.18)]"></div>
            </button>
          </div>
        </section>
      </div>

      <div v-else class="surface-card-lg text-center">
        <div class="mb-5 text-6xl">📸</div>
        <h2 class="text-2xl font-semibold text-slate-900 mb-2">Gallery not found</h2>
        <p class="mb-7 text-base text-slate-600">We couldn't find the gallery you're looking for.</p>
        <button @click="router.push('/blog')" class="brand-button px-8 py-4">
          Back to Galleries
        </button>
      </div>
    </div>
  </div>
</template>
