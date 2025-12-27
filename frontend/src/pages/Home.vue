<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const exploreTrails = () => {
  router.push('/trails')
}

const heroImageUrl = "/api/method/frappe.utils.file_manager.get_file?file_url=/files/landing-image.jpeg"
const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
}
</script>

<template>
  <div class="w-full">
    <!-- Hero Section - Full Viewport with Image -->
    <div class="hero min-h-screen relative overflow-hidden">
      <!-- Hero Background Image -->
      <div class="absolute inset-0">
        <img
          :src="heroImageUrl"
          alt="Hiking Adventure"
          class="w-full h-full object-cover"
          @error="handleImageError"
        />
        <!-- Overlay for better text readability -->
        <div class="absolute inset-0 bg-gradient-to-br from-emerald-900/90 via-teal-900/85 to-cyan-900/90"></div>
      </div>

      <!-- Animated Pattern Overlay -->
      <div class="absolute inset-0 opacity-10 z-10">
        <div class="absolute top-0 left-0 w-full h-full"
             style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>

      <div class="hero-content text-center relative z-20">
        <div class="max-w-5xl">
          <div class="mb-6">
            <span class="inline-block px-6 py-2 bg-white/20 backdrop-blur-md text-white rounded-full font-bold text-sm tracking-wider border-2 border-white/30">
              KENYA'S #1 HIKING PLATFORM
            </span>
          </div>
          <h1 class="text-6xl md:text-8xl font-black mb-8 text-white drop-shadow-2xl leading-tight">
            Discover Your Next<br>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-amber-400 to-orange-400 drop-shadow-none">
              Adventure
            </span>
          </h1>
          <p class="text-xl md:text-3xl mb-12 text-white font-light max-w-3xl mx-auto leading-relaxed drop-shadow-lg">
            Explore breathtaking hiking trails across Kenya. Book guided experiences with expert trail leaders and create unforgettable memories.
          </p>
          <div class="flex flex-col sm:flex-row gap-6 justify-center">
            <button @click="exploreTrails" class="group px-12 py-5 bg-white text-emerald-900 hover:bg-amber-400 hover:text-white border-0 rounded-2xl text-xl font-black shadow-2xl transform hover:scale-105 transition-all flex items-center justify-center gap-3">
              Explore Trails
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
            <button class="px-12 py-5 bg-transparent text-white border-white border-4 hover:bg-white hover:text-emerald-900 rounded-2xl text-xl font-black shadow-2xl transform hover:scale-105 transition-all">
              Learn More
            </button>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-3 gap-8 mt-20 max-w-3xl mx-auto">
            <div class="text-center">
              <div class="text-5xl font-black text-amber-400 mb-2">50+</div>
              <div class="text-white/80 text-sm uppercase tracking-wider">Trails</div>
            </div>
            <div class="text-center">
              <div class="text-5xl font-black text-amber-400 mb-2">1000+</div>
              <div class="text-white/80 text-sm uppercase tracking-wider">Hikers</div>
            </div>
            <div class="text-center">
              <div class="text-5xl font-black text-amber-400 mb-2">25+</div>
              <div class="text-white/80 text-sm uppercase tracking-wider">Guides</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white/50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </div>

    <!-- Features Section -->
    <div class="bg-white py-24">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center mb-16">
          <h2 class="text-5xl font-black text-gray-900 mb-4">Why Choose Step Up Adventures</h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">Experience the best hiking adventures with our professional guides and carefully curated trails</p>
        </div>

        <div class="grid md:grid-cols-3 gap-12">
          <!-- Feature 1 -->
          <div class="text-center group hover:scale-105 transition-transform cursor-pointer">
            <div class="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-3xl flex items-center justify-center transform group-hover:rotate-6 transition-transform shadow-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-3">Curated Trails</h3>
            <p class="text-gray-600 leading-relaxed">Hand-picked routes ranging from easy walks to challenging climbs, perfect for every skill level</p>
          </div>

          <!-- Feature 2 -->
          <div class="text-center group hover:scale-105 transition-transform cursor-pointer">
            <div class="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-amber-500 to-orange-600 rounded-3xl flex items-center justify-center transform group-hover:rotate-6 transition-transform shadow-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-3">Expert Guides</h3>
            <p class="text-gray-600 leading-relaxed">Professional trail leaders with years of experience ensuring your safety and enjoyment</p>
          </div>

          <!-- Feature 3 -->
          <div class="text-center group hover:scale-105 transition-transform cursor-pointer">
            <div class="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-3xl flex items-center justify-center transform group-hover:rotate-6 transition-transform shadow-xl">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-3">Easy Booking</h3>
            <p class="text-gray-600 leading-relaxed">Simple, secure booking process with instant confirmation and flexible cancellation</p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-gradient-to-r from-emerald-900 to-teal-800 py-20">
      <div class="max-w-4xl mx-auto text-center px-6">
        <h2 class="text-5xl font-black text-white mb-6">Ready for Adventure?</h2>
        <p class="text-xl text-white/90 mb-10">Join thousands of hikers exploring Kenya's most beautiful trails</p>
        <button @click="exploreTrails" class="btn btn-lg bg-white text-emerald-900 hover:bg-amber-400 hover:text-white border-0 px-12 text-lg font-bold shadow-2xl transform hover:scale-105 transition-all">
          Start Exploring
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}
</style>
