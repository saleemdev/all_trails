<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    tone?: 'info' | 'success' | 'warning' | 'error'
    title?: string
  }>(),
  {
    tone: 'info',
    title: '',
  }
)

const toneClasses: Record<string, string> = {
  info: 'surface-active text-[color:var(--color-text-primary)]',
  success: 'bg-[rgba(49,83,72,0.1)] border-[color:var(--color-border-soft)] text-[color:var(--color-primary-dark)]',
  warning: 'bg-[rgba(217,149,76,0.16)] border-[rgba(217,149,76,0.34)] text-[color:var(--color-text-primary)]',
  error: 'surface-danger-subtle',
}
</script>

<template>
  <div :class="['rounded-[1rem] border px-3.5 py-3', toneClasses[props.tone]]">
    <p v-if="props.title" class="mb-0.5 text-sm font-medium">{{ props.title }}</p>
    <div class="text-[13px] leading-5">
      <slot />
    </div>
  </div>
</template>
