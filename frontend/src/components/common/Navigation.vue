<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
import { useMerchandiseStore } from '../../stores/merchandiseStore'
import { useUiStore } from '../../stores/uiStore'
import { Avatar, toast } from 'frappe-ui'

const router = useRouter()
const authStore = useAuthStore()
const merchandiseStore = useMerchandiseStore()
const uiStore = useUiStore()

const currentRoute = computed(() => router.currentRoute.value.name)
const mobileMenuOpen = ref(false)
const userMenuOpen = ref(false)
const userMenuRef = ref<HTMLElement | null>(null)
const cartCount = computed(() => merchandiseStore.cartCount)
const unreadNotifications = computed(() => uiStore.notifications.length)
const themeMode = ref<'light' | 'dark'>('light')

const THEME_STORAGE_KEY = 'alltrails.theme-mode'

const applyThemeMode = (mode: 'light' | 'dark', persist = true) => {
  themeMode.value = mode

  if (typeof document !== 'undefined') {
    document.documentElement.setAttribute('data-theme-mode', mode)
  }

  if (persist && typeof window !== 'undefined') {
    window.localStorage.setItem(THEME_STORAGE_KEY, mode)
  }
}

const toggleThemeMode = () => {
  const nextMode = themeMode.value === 'dark' ? 'light' : 'dark'
  applyThemeMode(nextMode)
}

const openNotifications = () => {
  if (unreadNotifications.value > 0) {
    uiStore.clearAllNotifications()
    toast.info('Notifications cleared')
    return
  }

  toast.info('No new notifications right now')
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

const handleClickOutside = (event: MouseEvent) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target as Node)) {
    closeUserMenu()
  }
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    const savedTheme = window.localStorage.getItem(THEME_STORAGE_KEY)
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const initialTheme = savedTheme === 'dark' || savedTheme === 'light'
      ? savedTheme
      : (systemPrefersDark ? 'dark' : 'light')

    applyThemeMode(initialTheme, false)
  }

  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const navItems = computed(() => {
  const items = [
    { to: '/', label: 'Home', route: 'Home' },
    { to: '/trails', label: 'Trails', route: 'TrailBrowse' },
    { to: '/shop', label: 'Shop', route: 'ShopBrowse' },
    { to: '/blog', label: 'Blog', route: 'BlogList' },
  ]

  if (authStore.isAuthenticated) {
    items.push({ to: '/bookings', label: 'Bookings', route: 'BookingsList' })
  }

  return items
})

const isActiveRoute = (routeName: string) => {
  if (routeName === 'ShopBrowse') {
    return String(currentRoute.value || '').startsWith('Shop')
  }

  return currentRoute.value === routeName
}

const isCartRoute = computed(() =>
  ['ShopCart', 'ShopCheckout', 'ShopPaymentProcessing', 'ShopConfirmation', 'ShopTracking'].includes(
    String(currentRoute.value || '')
  )
)
</script>

<template>
  <div class="w-full">
    <a
      href="#main-content"
      class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[100] brand-button"
    >
      Skip to main content
    </a>

    <nav class="glass-nav sticky top-0 z-50" role="navigation" aria-label="Main navigation">
      <div class="layout-shell-wide">
        <div class="flex min-h-16 items-center justify-between py-2 sm:min-h-[4.5rem]">
          <RouterLink to="/" class="flex items-center gap-3 group" @click="closeMobileMenu">
            <div class="brand-mark h-10 w-10 transform transition-transform group-hover:scale-[1.03] sm:h-11 sm:w-11">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <div>
              <div class="brand-wordmark text-xl font-semibold leading-none sm:text-2xl">Stepup Adventures</div>
              <div class="tone-muted mt-1 hidden text-[10px] uppercase tracking-[0.24em] sm:block">Trails across Kenya</div>
            </div>
          </RouterLink>

          <div class="hidden md:flex items-center gap-0.5">
            <RouterLink
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              class="nav-link"
              :class="{ 'nav-link-active': isActiveRoute(item.route) }"
            >
              {{ item.label }}
            </RouterLink>
          </div>

          <div class="hidden md:flex items-center gap-3">
            <button
              type="button"
              class="icon-control-button relative"
              aria-label="Open notifications"
              title="Notifications"
              @click="openNotifications"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.4-1.4A2 2 0 0118 14.2V11a6 6 0 10-12 0v3.2a2 2 0 01-.6 1.4L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span
                v-if="unreadNotifications"
                class="count-pill absolute -right-1.5 -top-1.5"
              >
                {{ unreadNotifications > 9 ? '9+' : unreadNotifications }}
              </span>
            </button>

            <button
              type="button"
              class="icon-control-button"
              :aria-label="themeMode === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'"
              :title="themeMode === 'dark' ? 'Light mode' : 'Dark mode'"
              @click="toggleThemeMode"
            >
              <svg
                v-if="themeMode === 'dark'"
                xmlns="http://www.w3.org/2000/svg"
                class="h-[18px] w-[18px]"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v2m0 14v2m7-9h2M3 12H1m16.95 6.95l1.4 1.4M4.65 4.65l1.4 1.4m11.9-1.4l-1.4 1.4M6.05 17.95l-1.4 1.4M12 7a5 5 0 100 10 5 5 0 000-10z" />
              </svg>
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                class="h-[18px] w-[18px]"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9 9 0 1020.354 15.354z" />
              </svg>
            </button>

            <RouterLink
              to="/shop/cart"
              class="icon-control-button relative"
              :class="isCartRoute ? 'icon-control-button-active' : ''"
              aria-label="Open cart"
              title="Cart"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h2l.8 2m0 0L7 14h10l2-8H5.8M7 14l-1 2h12M10 20a1 1 0 100 2 1 1 0 000-2zm8 0a1 1 0 100 2 1 1 0 000-2z" />
              </svg>
              <span
                v-if="cartCount"
                class="count-pill absolute -right-1.5 -top-1.5"
              >
                {{ cartCount }}
              </span>
            </RouterLink>
            <div v-if="authStore.isAuthenticated" ref="userMenuRef" class="relative">
              <button
                @click="toggleUserMenu"
                class="flex cursor-pointer items-center gap-3 rounded-2xl px-3 py-2 transition-colors hover:bg-[color:var(--color-surface-control)]"
                aria-label="User menu"
                :aria-expanded="userMenuOpen"
              >
                <Avatar
                  :label="authStore.user?.full_name || authStore.user?.name || 'User'"
                  :image="authStore.user?.user_image"
                  size="md"
                  class="flex-shrink-0"
                />
                <span class="tone-heading font-medium">{{ authStore.user?.full_name || authStore.user?.name }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="tone-muted h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div
                v-if="userMenuOpen"
                class="absolute right-0 mt-2 w-60 glass-panel-strong rounded-2xl z-50 py-2"
                role="menu"
                aria-orientation="vertical"
              >
                <div class="tone-muted border-b border-[color:var(--color-border-soft)] px-4 py-2 text-xs font-medium">
                  {{ authStore.user?.email }}
                </div>
                <RouterLink
                  to="/profile"
                  @click="closeUserMenu"
                  class="soft-menu-item mx-2"
                  :class="{ 'soft-menu-item-active': isActiveRoute('Profile') }"
                  role="menuitem"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  My Profile
                </RouterLink>
                <button
                  @click="logout"
                  class="surface-danger-subtle mx-2 mt-1 flex w-[calc(100%-1rem)] items-center gap-2 rounded-2xl px-4 py-3 text-left transition-colors hover:brightness-[1.04]"
                  role="menuitem"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Logout
                </button>
              </div>
            </div>
            <RouterLink v-else to="/login" class="brand-button px-5 py-2.5 text-sm">
              Login
            </RouterLink>
          </div>

          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="icon-control-button md:hidden"
            :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
            :aria-expanded="mobileMenuOpen"
            aria-controls="mobile-menu"
          >
            <svg v-if="!mobileMenuOpen" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div
          v-if="mobileMenuOpen"
          id="mobile-menu"
          class="md:hidden pb-4 animate-in slide-in-from-top"
          role="menu"
        >
          <div class="glass-panel-strong rounded-[1.5rem] p-3">
            <div v-if="authStore.isAuthenticated" class="px-2 py-2 mb-2">
              <div class="flex items-center gap-3 rounded-[1.25rem] surface-muted p-3">
                <Avatar
                  :label="authStore.user?.full_name || authStore.user?.name || 'User'"
                  :image="authStore.user?.user_image"
                  size="lg"
                  class="flex-shrink-0"
                />
                <div class="flex-1 min-w-0">
                  <div class="tone-heading truncate font-medium">{{ authStore.user?.full_name || authStore.user?.name }}</div>
                  <div class="tone-body truncate text-sm">{{ authStore.user?.email }}</div>
                </div>
              </div>
              <RouterLink
                to="/profile"
                @click="closeMobileMenu"
                class="soft-menu-item mt-2"
                :class="{ 'soft-menu-item-active': isActiveRoute('Profile') }"
                role="menuitem"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                My Profile
              </RouterLink>
            </div>

            <div class="space-y-1 px-1">
              <RouterLink
                v-for="item in navItems"
                :key="item.to"
                :to="item.to"
                @click="closeMobileMenu"
                class="soft-menu-item"
                :class="{ 'soft-menu-item-active': isActiveRoute(item.route) }"
                role="menuitem"
                :aria-current="isActiveRoute(item.route) ? 'page' : undefined"
              >
                {{ item.label }}
              </RouterLink>
            </div>

            <RouterLink
              to="/shop/cart"
              @click="closeMobileMenu"
              class="soft-menu-item mt-3"
              :class="{ 'soft-menu-item-active': isCartRoute }"
              role="menuitem"
            >
              Cart
              <span
                v-if="cartCount"
                class="count-pill ml-auto min-w-6 px-2 text-xs"
              >
                {{ cartCount }}
              </span>
            </RouterLink>

            <button
              type="button"
              class="soft-menu-item mt-2 w-full text-left"
              role="menuitem"
              @click="openNotifications"
            >
              Notifications
              <span
                v-if="unreadNotifications"
                class="count-pill ml-auto min-w-6 px-2 text-xs"
              >
                {{ unreadNotifications > 9 ? '9+' : unreadNotifications }}
              </span>
            </button>

            <button
              type="button"
              class="soft-menu-item mt-1 w-full text-left"
              role="menuitem"
              @click="toggleThemeMode"
            >
              {{ themeMode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode' }}
            </button>

            <div class="mt-4 border-t border-[color:var(--color-border-soft)] px-1 pt-4">
              <button
                v-if="authStore.isAuthenticated"
                @click="logout"
                class="surface-danger-subtle flex w-full items-center justify-center gap-2 rounded-2xl px-4 py-3 font-medium transition-all hover:brightness-[1.04]"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Logout
              </button>
              <RouterLink
                v-else
                to="/login"
                @click="closeMobileMenu"
                class="brand-button w-full"
              >
                Login
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </nav>

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
