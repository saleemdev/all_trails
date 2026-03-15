<script setup lang="ts">
import type { CheckoutStep } from '../../types/shop'

const props = defineProps<{
  steps: CheckoutStep[]
  currentStep: CheckoutStep['id']
}>()
</script>

<template>
  <div class="grid gap-2 md:grid-cols-3">
    <article
      v-for="(step, index) in props.steps"
      :key="step.id"
      :class="[
        'rounded-[1rem] border px-3.5 py-3 transition-colors',
        props.currentStep === step.id
          ? 'border-[color:var(--color-border-strong)] bg-[color:var(--color-surface-overlay)] text-[color:var(--color-primary-dark)]'
          : 'border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)] tone-body',
      ]"
    >
      <div class="mb-2 flex items-center gap-2.5">
        <div
          :class="[
            'flex h-8 w-8 items-center justify-center rounded-full text-xs font-medium',
            props.currentStep === step.id
              ? 'bg-[color:var(--color-primary)] text-white'
              : 'bg-[color:var(--color-surface-muted)] tone-body',
          ]"
        >
          {{ index + 1 }}
        </div>
        <div>
          <p class="text-sm font-medium">{{ step.title }}</p>
          <p class="text-[10px] uppercase tracking-[0.14em]">{{ step.id }}</p>
        </div>
      </div>
      <p class="text-[13px] leading-5">{{ step.description }}</p>
    </article>
  </div>
</template>
