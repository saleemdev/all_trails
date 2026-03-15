<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <section class="dense-ui page-shell page-block">
    <div class="layout-shell-narrow">
      <div class="surface-card-lg text-center">
        <p class="page-kicker mb-2">Access notice</p>
        <h1 class="page-title">You do not have permission to view this page.</h1>
        <p class="page-copy mx-auto mb-0 max-w-xl">
          Your account is signed in, but this section is restricted to a different role. Return to a permitted page
          and continue from there.
        </p>

        <div class="mt-5 flex flex-wrap items-center justify-center gap-2.5">
          <button class="brand-button px-4 py-2 text-[13px]" @click="router.push('/')">Go To Home</button>
          <button class="soft-button-secondary px-4 py-2 text-[13px]" @click="router.push('/trails')">Browse Trails</button>
        </div>
      </div>
    </div>
  </section>
</template>
