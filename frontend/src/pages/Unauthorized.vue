<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <section class="dense-ui page-shell page-block">
    <div class="layout-shell-narrow">
      <div class="surface-card-lg text-center">
        <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full surface-muted">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 tone-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 9v2m0 4h.01M5.07 19h13.86c1.54 0 2.5-1.67 1.73-3L13.73 4c-.77-1.33-2.69-1.33-3.46 0L3.34 16c-.77 1.33.19 3 1.73 3z" />
          </svg>
        </div>
        <p class="page-kicker mb-2">Access notice</p>
        <h1 class="page-title">This page is not available for your role.</h1>
        <p class="page-copy mx-auto mb-0 max-w-xl">
          You are signed in, but this section needs a different permission level. Continue from a page you can access.
        </p>

        <div class="mt-5 flex flex-wrap items-center justify-center gap-2.5">
          <button class="brand-button px-4 py-2 text-[13px]" @click="router.push('/')">Go home</button>
          <button class="soft-button-secondary px-4 py-2 text-[13px]" @click="router.push('/trails')">Browse Trails</button>
        </div>
      </div>
    </div>
  </section>
</template>
