<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const currentRoute = computed(() => router.currentRoute.value.name)
const mobileMenuOpen = ref(false)

const logout = () => {
  authStore.logout()
  mobileMenuOpen.value = false
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const navItems = computed(() => {
  const items = [
    { to: '/', label: 'Home', route: 'Home' },
    { to: '/trails', label: 'Trails', route: 'TrailBrowse' },
    { to: '/blog', label: 'Blog', route: 'BlogList' }
  ]

  if (authStore.isAuthenticated) {
    items.push(
      { to: '/bookings', label: 'Bookings', route: 'BookingsList' },
      { to: '/profile', label: 'Profile', route: 'Profile' }
    )
  }

  return items
})
</script>

<template>
  <div class="w-full">
    <!-- Modern minimal navbar -->
    <nav class="bg-white/95 backdrop-blur-md shadow-sm sticky top-0 z-50 border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <RouterLink to="/" class="flex items-center gap-3 group">
            <div class="w-10 h-10 bg-gradient-to-br from-emerald-600 to-teal-500 rounded-xl flex items-center justify-center transform group-hover:scale-105 transition-transform shadow-md">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <span class="text-2xl font-black bg-gradient-to-r from-emerald-900 to-teal-800 bg-clip-text text-transparent">
              Step Up Adventures
            </span>
          </RouterLink>

          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center gap-1">
            <RouterLink
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              class="px-4 py-2 rounded-lg text-gray-700 font-medium hover:bg-emerald-50 hover:text-emerald-900 transition-all"
              :class="{
                'bg-emerald-100 text-emerald-900 font-bold': currentRoute === item.route
              }"
            >
              {{ item.label }}
            </RouterLink>
          </div>

          <!-- Desktop User Section -->
          <div class="hidden md:flex items-center gap-4">
            <div v-if="authStore.isAuthenticated" class="dropdown dropdown-end">
              <div tabindex="0" role="button" class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                <div class="w-9 h-9 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-white font-bold shadow-md">
                  {{ authStore.user?.full_name?.charAt(0) || 'U' }}
                </div>
                <span class="font-medium text-gray-900">{{ authStore.user?.full_name }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
              <ul tabindex="0" class="menu dropdown-content mt-3 z-[1] p-2 shadow-xl bg-white rounded-xl w-56 border border-gray-100">
                <li class="px-4 py-2 text-xs text-gray-500 font-medium border-b border-gray-100">
                  {{ authStore.user?.email }}
                </li>
                <li>
                  <RouterLink to="/profile" class="flex items-center gap-2 py-2 hover:bg-emerald-50 hover:text-emerald-900">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    My Profile
                  </RouterLink>
                </li>
                <li>
                  <a @click="logout" class="flex items-center gap-2 py-2 text-red-600 hover:bg-red-50">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Logout
                  </a>
                </li>
              </ul>
            </div>
            <RouterLink v-else to="/app/login" class="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-lg hover:from-emerald-700 hover:to-teal-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105">
              Login
            </RouterLink>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <svg v-if="!mobileMenuOpen" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mobile Menu -->
        <div
          v-if="mobileMenuOpen"
          class="md:hidden border-t border-gray-100 py-4 animate-in slide-in-from-top"
        >
          <!-- Mobile User Info -->
          <div v-if="authStore.isAuthenticated" class="flex items-center gap-3 px-4 py-3 mb-4 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-lg">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-white font-bold shadow-md">
              {{ authStore.user?.full_name?.charAt(0) || 'U' }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="font-bold text-gray-900 truncate">{{ authStore.user?.full_name }}</div>
              <div class="text-sm text-gray-600 truncate">{{ authStore.user?.email }}</div>
            </div>
          </div>

          <!-- Mobile Nav Items -->
          <div class="space-y-1 px-2">
            <RouterLink
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              @click="closeMobileMenu"
              class="block px-4 py-3 rounded-lg text-gray-700 font-medium hover:bg-emerald-50 hover:text-emerald-900 transition-all"
              :class="{
                'bg-emerald-100 text-emerald-900 font-bold': currentRoute === item.route
              }"
            >
              {{ item.label }}
            </RouterLink>
          </div>

          <!-- Mobile Auth Button -->
          <div class="px-2 mt-4 pt-4 border-t border-gray-100">
            <button
              v-if="authStore.isAuthenticated"
              @click="logout"
              class="w-full px-4 py-3 bg-red-50 text-red-600 font-bold rounded-lg hover:bg-red-100 transition-all flex items-center justify-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
            <RouterLink
              v-else
              to="/app/login"
              @click="closeMobileMenu"
              class="block w-full px-4 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-lg hover:from-emerald-700 hover:to-teal-700 transition-all text-center shadow-md"
            >
              Login
            </RouterLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- Page content slot -->
    <slot />
  </div>
</template>

<style scoped>
@keyframes slide-in-from-top {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: slide-in-from-top 200ms ease-out;
}
</style>
