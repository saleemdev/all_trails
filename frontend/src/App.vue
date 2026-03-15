<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'
import Navigation from './components/common/Navigation.vue'
import Notifications from './components/common/Notifications.vue'
import ShopMaintenanceOverlay from './components/common/ShopMaintenanceOverlay.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const showNavigation = computed(() => !route.meta.hideNavigation)
const isShopComingSoon = computed(() => route.path === '/shop' || route.path.startsWith('/shop/'))

onMounted(async () => {
  await authStore.initializeAuth()
})

watch(() => router.currentRoute.value.path, async (newPath, oldPath) => {
  if (oldPath && oldPath.includes('/login') && !newPath.includes('/login')) {
    await authStore.checkAuthentication()
  }
})
</script>

<template>
  <div id="app" class="app-shell">
    <Navigation v-if="showNavigation">
      <main class="w-full relative z-10">
        <div :class="isShopComingSoon ? 'pointer-events-none select-none blur-[4px] saturate-50' : ''">
          <RouterView />
        </div>
      </main>
    </Navigation>
    <main v-else class="w-full relative z-10">
      <div :class="isShopComingSoon ? 'pointer-events-none select-none blur-[4px] saturate-50' : ''">
        <RouterView />
      </div>
    </main>
    <ShopMaintenanceOverlay v-if="isShopComingSoon" />
    <Notifications />
  </div>
</template>

<style>
/* Global styles are provided through globals.css */
</style>
