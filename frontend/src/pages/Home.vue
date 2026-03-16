<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const exploreTrails = () => {
  router.push('/trails')
}

const kenyaHeroClips = [
  'https://upload.wikimedia.org/wikipedia/commons/transcoded/2/24/Safari_at_Nairobi_National_Park%2C_Aug_2025.webm/Safari_at_Nairobi_National_Park%2C_Aug_2025.webm.720p.vp9.webm',
  'https://upload.wikimedia.org/wikipedia/commons/transcoded/9/92/Nairobi_National_Park_%28August_2025%29_road_driving_slowly.webm/Nairobi_National_Park_%28August_2025%29_road_driving_slowly.webm.720p.vp9.webm',
  'https://upload.wikimedia.org/wikipedia/commons/transcoded/9/9e/Mount_Kenya_bog_stream.webm/Mount_Kenya_bog_stream.webm.720p.vp9.webm',
]
const gearVideoUrl = 'https://upload.wikimedia.org/wikipedia/commons/transcoded/4/40/Airbag_backpack%2C_IAA_2021%2C_Munich_%28IAA10362%29.webm/Airbag_backpack%2C_IAA_2021%2C_Munich_%28IAA10362%29.webm.480p.vp9.webm'
const heroImageUrl = '/api/method/frappe.utils.file_manager.get_file?file_url=/files/landing-image.jpeg'
const imageFailed = ref(false)
const isVideoReady = ref(false)
const videoFailed = ref(false)
const gearVideoFailed = ref(false)
const prefersReducedMotion = ref(false)
const currentKenyaClipIndex = ref(0)
const failedKenyaClipCount = ref(0)
const heroVideoElement = ref<HTMLVideoElement | null>(null)
let motionQuery: MediaQueryList | null = null

const heroStaticVisible = computed(() => prefersReducedMotion.value || videoFailed.value || !isVideoReady.value)
const activeKenyaClip = computed(() => kenyaHeroClips[currentKenyaClipIndex.value] || '')

const updateMotionPreference = () => {
  prefersReducedMotion.value = motionQuery?.matches ?? false
}

onMounted(() => {
  if (typeof window === 'undefined') {
    return
  }

  motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
  updateMotionPreference()
  motionQuery.addEventListener('change', updateMotionPreference)
})

onBeforeUnmount(() => {
  motionQuery?.removeEventListener('change', updateMotionPreference)
})

const handleVideoReady = () => {
  isVideoReady.value = true
  failedKenyaClipCount.value = 0
}

const loadActiveKenyaClip = () => {
  const video = heroVideoElement.value
  if (!video) {
    return
  }

  video.load()
  void video.play().catch(() => {
    // Ignore autoplay rejection; fallback image remains visible.
  })
}

const advanceKenyaClip = () => {
  if (kenyaHeroClips.length < 2) {
    return
  }

  currentKenyaClipIndex.value = (currentKenyaClipIndex.value + 1) % kenyaHeroClips.length
  isVideoReady.value = false
  failedKenyaClipCount.value = 0
  requestAnimationFrame(loadActiveKenyaClip)
}

const handleVideoError = () => {
  failedKenyaClipCount.value += 1

  if (failedKenyaClipCount.value >= kenyaHeroClips.length) {
    videoFailed.value = true
    isVideoReady.value = false
    return
  }

  currentKenyaClipIndex.value = (currentKenyaClipIndex.value + 1) % kenyaHeroClips.length
  isVideoReady.value = false
  requestAnimationFrame(loadActiveKenyaClip)
}

const handleGearVideoError = () => {
  gearVideoFailed.value = true
}

const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement | null
  if (img) {
    img.style.display = 'none'
  }
  imageFailed.value = true
}
</script>

<template>
  <div class="page-shell w-full">
    <section class="relative min-h-screen overflow-hidden flex items-center">
      <div class="absolute inset-0 hero-media-shell">
        <img
          v-if="!imageFailed"
          :src="heroImageUrl"
          alt=""
          class="hero-fallback-image w-full h-full object-cover transition-opacity duration-700"
          :class="heroStaticVisible ? 'opacity-100' : 'opacity-0'"
          aria-hidden="true"
          @error="handleImageError"
        />
        <video
          v-if="!prefersReducedMotion && !videoFailed"
          ref="heroVideoElement"
          class="hero-video-layer absolute inset-0 w-full h-full object-cover transition-opacity duration-700"
          :class="isVideoReady ? 'opacity-100' : 'opacity-0'"
          :src="activeKenyaClip"
          :poster="heroImageUrl"
          autoplay
          muted
          playsinline
          preload="metadata"
          aria-hidden="true"
          @loadeddata="handleVideoReady"
          @ended="advanceKenyaClip"
          @error="handleVideoError"
        />
        <video
          v-if="!prefersReducedMotion && !gearVideoFailed"
          class="hero-gear-layer"
          autoplay
          muted
          loop
          playsinline
          preload="metadata"
          aria-hidden="true"
          @error="handleGearVideoError"
        >
          <source :src="gearVideoUrl" type="video/webm" />
        </video>
        <div class="absolute inset-0 hero-vignette"></div>
        <div class="absolute inset-0 hero-film-grain"></div>
        <div class="absolute inset-0 hero-overlay"></div>
      </div>

      <div class="absolute inset-0 hero-grid opacity-60"></div>
      <div class="absolute -top-24 -left-20 w-80 h-80 rounded-full blur-3xl opacity-60" style="background: radial-gradient(circle, rgba(219, 233, 225, 0.18) 0%, transparent 70%)"></div>
      <div class="absolute bottom-0 right-0 w-[28rem] h-[28rem] rounded-full blur-3xl opacity-70" style="background: radial-gradient(circle, rgba(221, 200, 177, 0.18) 0%, transparent 70%)"></div>

      <div class="layout-shell-wide relative z-10 w-full py-16 sm:py-20 lg:py-24">
        <div class="max-w-4xl">
          <span class="soft-kicker mb-5">Fresh air. Better routes. Zero noise.</span>
          <h1 class="text-[clamp(2.45rem,6.2vw,5rem)] font-medium mb-5 text-white leading-[0.95] tracking-[-0.04em]">
            Discover your next
            <span class="block soft-count">adventure in motion</span>
          </h1>
          <p class="max-w-2xl text-[15px] leading-6 text-white/80 sm:text-lg sm:leading-7 mb-7">
            Stepup Adventures helps hikers find, compare, and book Kenya's most compelling trail experiences through a calmer, more considered interface.
          </p>

          <div class="flex flex-col sm:flex-row gap-3.5 sm:gap-4.5">
            <button
              @click="exploreTrails"
              class="brand-button px-5 py-2.5 text-sm sm:text-[15px]"
              aria-label="Explore available trails"
            >
              Explore Trails
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
            <button
              class="brand-button-secondary px-5 py-2.5 text-sm sm:text-[15px]"
              aria-label="Learn more about Stepup Adventures"
            >
              Learn More
            </button>
          </div>

          <div class="mt-9 flex flex-wrap items-center gap-2.5">
            <span class="hero-info-pill">🌿 Curated local trails</span>
            <span class="hero-info-pill">🧭 Guide-led experiences</span>
            <span class="hero-info-pill">💳 Simple MPESA checkout</span>
          </div>
        </div>
      </div>

      <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce z-10">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </section>

    <section class="page-block px-4 sm:px-6">
      <div class="layout-shell-wide">
        <div class="mb-10 text-center">
          <p class="app-section-kicker mb-2.5">Design direction</p>
          <h2 class="app-section-title mx-auto max-w-3xl">A fresher way to plan the outdoors</h2>
          <p class="app-section-copy mx-auto max-w-2xl">
            The product now leans into quieter depth: softer glass, gentler green, and a more premium sense of space.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4.5 md:gap-5">
          <article class="surface-card soft-card-hover text-center">
            <div class="soft-icon-tile soft-icon-tile--sage mx-auto mb-5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
            </div>
            <h3 class="tone-heading mb-2 text-lg font-medium sm:text-[1.3rem]">Curated Trails</h3>
            <p class="tone-body leading-relaxed mb-0">A cleaner discovery flow for routes that feel thoughtfully selected, not dumped into a catalog.</p>
          </article>

          <article class="surface-card soft-card-hover text-center">
            <div class="soft-icon-tile soft-icon-tile--brass mx-auto mb-5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="tone-heading mb-2 text-lg font-medium sm:text-[1.3rem]">Expert Guides</h3>
            <p class="tone-body leading-relaxed mb-0">Guide-led experiences presented with more confidence, less marketing noise, and better hierarchy.</p>
          </article>

          <article class="surface-card soft-card-hover text-center">
            <div class="soft-icon-tile soft-icon-tile--mist mx-auto mb-5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="tone-heading mb-2 text-lg font-medium sm:text-[1.3rem]">Clear Booking</h3>
            <p class="tone-body leading-relaxed mb-0">Transactions and scheduling now sit inside a calmer interface that feels more credible for payments.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="px-4 pb-12 sm:px-6 sm:pb-14">
      <div class="layout-shell glass-panel-strong rounded-[1.65rem] px-5 py-7 sm:px-7 sm:py-9 md:px-9 md:py-10 relative overflow-hidden">
        <div class="absolute inset-y-0 right-0 w-64 opacity-80" style="background: radial-gradient(circle at center, rgba(184, 140, 98, 0.12) 0%, transparent 70%)"></div>
        <div class="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-7">
          <div class="max-w-2xl">
            <p class="app-section-kicker mb-2.5">Ready when you are</p>
            <h2 class="app-section-title">Start with the trails, carry the same calm through the app</h2>
            <p class="app-section-copy mb-0">The new token system keeps the experience fresh and futuristic without losing the outdoor identity.</p>
          </div>
          <div>
            <button
              @click="exploreTrails"
              class="brand-button px-5 py-2.5 text-sm sm:text-[15px]"
              aria-label="Start exploring trails"
            >
              Start Exploring
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero-media-shell {
  isolation: isolate;
  background: linear-gradient(135deg, #16251f 0%, #21382f 48%, #3d6355 100%);
}

.hero-fallback-image {
  object-position: center 58%;
  filter: saturate(0.9) contrast(1.05) brightness(0.78);
}

.hero-video-layer {
  filter: saturate(1.05) contrast(1.05) brightness(0.74);
  transform: scale(1.08);
  animation: heroFloat 22s ease-in-out infinite alternate;
}

.hero-gear-layer {
  position: absolute;
  inset: -7%;
  width: 114%;
  height: 114%;
  object-fit: cover;
  opacity: 0.18;
  mix-blend-mode: soft-light;
  pointer-events: none;
  filter: sepia(0.66) saturate(1.22) contrast(1.08) brightness(0.95);
  animation: heroGearSweep 34s linear infinite alternate;
}

.hero-vignette {
  background:
    radial-gradient(circle at 12% 14%, rgba(219, 233, 225, 0.22) 0%, transparent 34%),
    radial-gradient(circle at 88% 82%, rgba(221, 200, 177, 0.2) 0%, transparent 42%),
    linear-gradient(180deg, rgba(6, 14, 11, 0.08) 0%, rgba(6, 14, 11, 0.36) 100%);
}

.hero-film-grain {
  opacity: 0.2;
  mix-blend-mode: soft-light;
  background-image:
    radial-gradient(circle, rgba(255, 255, 255, 0.16) 0.5px, transparent 0.5px),
    radial-gradient(circle, rgba(255, 255, 255, 0.08) 0.5px, transparent 0.5px);
  background-size: 3px 3px, 5px 5px;
  background-position: 0 0, 1px 1px;
}

@keyframes heroFloat {
  from {
    transform: scale(1.08) translate3d(-1%, 0, 0);
  }
  to {
    transform: scale(1.12) translate3d(1.5%, -1.5%, 0);
  }
}

@keyframes heroGearSweep {
  from {
    transform: translate3d(-1.2%, 1.2%, 0) scale(1.02);
  }
  to {
    transform: translate3d(1.4%, -1.4%, 0) scale(1.08);
  }
}

@media (max-width: 640px) {
  .hero-video-layer {
    transform: scale(1.14);
    animation-duration: 18s;
  }

  .hero-gear-layer {
    opacity: 0.16;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-video-layer,
  .hero-gear-layer {
    animation: none;
    transform: none;
  }
}
</style>
