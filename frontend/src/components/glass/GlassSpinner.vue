<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    label?: string
    size?: 'sm' | 'md' | 'lg'
  }>(),
  {
    label: 'Loading',
    size: 'md',
  }
)

const sizeClasses: Record<string, string> = {
  sm: 'h-5 w-5 border-2',
  md: 'h-10 w-10 border-[3px]',
  lg: 'h-16 w-16 border-4',
}
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3">
    <div :class="['animate-spin rounded-full border-[rgba(111,143,132,0.2)] border-t-[color:var(--color-primary)]', sizeClasses[props.size]]" />
    <p class="text-sm text-slate-600">{{ props.label }}</p>
  </div>
</template>
