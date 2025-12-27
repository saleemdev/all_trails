<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from './stores/authStore'
import Navigation from './components/common/Navigation.vue'
import Notifications from './components/common/Notifications.vue'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.initializeAuth()
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
