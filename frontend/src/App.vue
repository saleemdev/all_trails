<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'
import Navigation from './components/common/Navigation.vue'
import Notifications from './components/common/Notifications.vue'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  await authStore.initializeAuth()
})

// Re-check authentication when route changes (e.g., after login redirect)
watch(() => router.currentRoute.value.path, async (newPath, oldPath) => {
  // If we just navigated from login page, re-check auth
  if (oldPath && oldPath.includes('/login') && !newPath.includes('/login')) {
    await authStore.checkAuthentication()
  }
})
</script>

<template>
  <div id="app" class="min-h-screen bg-base-100">
    <Navigation>
      <main class="w-full">
        <RouterView />
      </main>
    </Navigation>
    <Notifications />
  </div>
</template>

<style>
/* Global styles - no scoped styles needed since we're using Tailwind */
</style>
