<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
import { Avatar } from 'frappe-ui'

const router = useRouter()
const authStore = useAuthStore()

const currentRoute = computed(() => router.currentRoute.value.name)
const mobileMenuOpen = ref(false)
const userMenuOpen = ref(false)
const userMenuRef = ref<HTMLElement | null>(null)

// Watch for auth state changes to ensure UI updates reactively
watch(() => authStore.isAuthenticated, (newVal) => {
  // Force reactivity - Navigation will update when auth state changes
  if (newVal) {
    console.log('User authenticated, updating navigation')
  }
}, { immediate: true })

/**
 * Get user initials (first 2 letters)
 */
const getUserInitials = (fullName?: string, userName?: string): string => {
  let name = fullName || userName || 'U'
  // Handle null/undefined by using 'U'
  if (!name || typeof name !== 'string') {
    return 'U'
  }
  // Remove spaces and get first 2 characters
  const initials = name.replace(/\s+/g, '').substring(0, 2).toUpperCase()
  return initials || 'U'
}

const logout = () => {
  authStore.logout()
  mobileMenuOpen.value = false
  userMenuOpen.value = false
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const toggleUserMenu = () => {
  userMenuOpen.value = !userMenuOpen.value
}

const closeUserMenu = () => {
  userMenuOpen.value = false
}

// Handle click outside to close user menu
const handleClickOutside = (event: MouseEvent) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target as Node)) {
    closeUserMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const navItems = computed(() => {
  const items = [
    { to: '/', label: 'Home', route: 'Home' },
    { to: '/trails', label: 'Trails', route: 'TrailBrowse' },
    { to: '/blog', label: 'Blog', route: 'BlogList' }
  ]

  if (authStore.isAuthenticated) {
    items.push(
      { to: '/bookings', label: 'Bookings', route: 'BookingsList' }
    )
  }

  return items
})
</script>

<template>
  <div class="w-full">
    <!-- Skip to main content link for accessibility -->
    <a
      href="#main-content"
      class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-emerald-600 focus:text-white focus:rounded-lg focus:font-bold"
    >
      Skip to main content
    </a>
    <!-- Modern minimal navbar -->
    <nav class="bg-white/95 backdrop-blur-md shadow-sm sticky top-0 z-50 border-b border-gray-100" role="navigation" aria-label="Main navigation">
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
            <div v-if="authStore.isAuthenticated" ref="userMenuRef" class="relative">
              <button
                @click="toggleUserMenu"
                class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer focus:outline-2 focus:outline-emerald-500 focus:outline-offset-2"
                aria-label="User menu"
                :aria-expanded="userMenuOpen"
              >
                <Avatar
                  :label="authStore.user?.full_name || authStore.user?.name || 'User'"
                  :image="authStore.user?.user_image"
                  size="md"
                  class="flex-shrink-0"
                />
                <span class="font-medium text-gray-900">{{ authStore.user?.full_name || authStore.user?.name }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div
                v-if="userMenuOpen"
                class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-gray-100 z-50 py-2"
                role="menu"
                aria-orientation="vertical"
              >
                <div class="px-4 py-2 text-xs text-gray-500 font-medium border-b border-gray-100">
                  {{ authStore.user?.email }}
                </div>
                <RouterLink
                  to="/profile"
                  @click="closeUserMenu"
                  class="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-emerald-50 hover:text-emerald-900 transition-colors"
                  role="menuitem"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  My Profile
                </RouterLink>
                <button
                  @click="logout"
                  class="w-full flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 transition-colors text-left"
                  role="menuitem"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Logout
                </button>
              </div>
            </div>
            <RouterLink to="/login" class="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-lg hover:from-emerald-700 hover:to-teal-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105">
              Login
            </RouterLink>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors focus:outline-2 focus:outline-emerald-500 focus:outline-offset-2"
            :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
            :aria-expanded="mobileMenuOpen"
            aria-controls="mobile-menu"
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
          id="mobile-menu"
          class="md:hidden border-t border-gray-100 py-4 animate-in slide-in-from-top"
          role="menu"
        >
          <!-- Mobile User Info -->
          <div v-if="authStore.isAuthenticated" class="px-4 py-3 mb-4">
            <div class="flex items-center gap-3 mb-3 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-lg p-3">
              <Avatar
                :label="authStore.user?.full_name || authStore.user?.name || 'User'"
                :image="authStore.user?.user_image"
                size="lg"
                class="flex-shrink-0"
              />
              <div class="flex-1 min-w-0">
                <div class="font-bold text-gray-900 truncate">{{ authStore.user?.full_name || authStore.user?.name }}</div>
                <div class="text-sm text-gray-600 truncate">{{ authStore.user?.email }}</div>
              </div>
            </div>
            <!-- Mobile User Menu Items -->
            <div class="space-y-1">
              <RouterLink
                to="/profile"
                @click="closeMobileMenu"
                class="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-emerald-50 hover:text-emerald-900 transition-colors rounded-lg"
                :class="{
                  'bg-emerald-100 text-emerald-900 font-bold': currentRoute === 'Profile'
                }"
                role="menuitem"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                My Profile
              </RouterLink>
            </div>
          </div>

          <!-- Mobile Nav Items -->
          <div class="space-y-1 px-2">
            <RouterLink
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              @click="closeMobileMenu"
              class="block px-4 py-3 rounded-lg text-gray-700 font-medium hover:bg-emerald-50 hover:text-emerald-900 transition-all focus:outline-2 focus:outline-emerald-500 focus:outline-offset-2"
              :class="{
                'bg-emerald-100 text-emerald-900 font-bold': currentRoute === item.route
              }"
              role="menuitem"
              :aria-current="currentRoute === item.route ? 'page' : undefined"
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
              to="/login"
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
    <main id="main-content" tabindex="-1">
      <slot />
    </main>
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

/* Screen reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.focus\:not-sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
</style>
