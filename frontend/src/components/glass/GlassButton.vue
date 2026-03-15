<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
    size?: 'sm' | 'md' | 'lg'
    loading?: boolean
    disabled?: boolean
    type?: 'button' | 'submit' | 'reset'
    block?: boolean
  }>(),
  {
    variant: 'primary',
    size: 'md',
    loading: false,
    disabled: false,
    type: 'button',
    block: false,
  }
)

const variantClasses: Record<string, string> = {
  primary: 'border border-white/20 bg-[linear-gradient(135deg,var(--color-primary),#7a998d)] text-white shadow-md hover:shadow-lg hover:-translate-y-px',
  secondary: 'bg-[color:var(--color-surface-control)] text-[color:var(--color-text-primary)] border border-[color:var(--color-border-soft)] shadow-sm hover:bg-[color:var(--color-surface-control-hover)]',
  ghost: 'bg-transparent text-[color:var(--color-text-secondary)] border border-[color:var(--color-border-soft)] hover:bg-[color:var(--color-surface-control)] hover:text-[color:var(--color-text-primary)]',
  danger: 'bg-red-600 text-white shadow-lg hover:bg-red-700',
}

const sizeClasses: Record<string, string> = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-3.5 py-2 text-sm',
  lg: 'px-4 py-2.5 text-sm sm:text-[15px]',
}
</script>

<template>
  <button
    :type="props.type"
    :disabled="props.disabled || props.loading"
    :class="[
      'inline-flex items-center justify-center gap-1.5 rounded-[0.9rem] font-medium transition-all focus:outline-2 focus:outline-[color:var(--color-primary-light)] focus:outline-offset-2 disabled:opacity-60 disabled:transform-none',
      variantClasses[props.variant],
      sizeClasses[props.size],
      props.block ? 'w-full' : '',
    ]"
  >
    <span
      v-if="props.loading"
      class="inline-flex h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white"
      aria-hidden="true"
    />
    <slot />
  </button>
</template>
