<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    tone?: 'default' | 'strong' | 'hero'
    padded?: boolean
    hoverable?: boolean
  }>(),
  {
    tone: 'default',
    padded: true,
    hoverable: false,
  }
)

const toneClasses: Record<string, string> = {
  default: 'glass-panel',
  strong: 'glass-panel-strong',
  hero: 'glass-panel-hero',
}
</script>

<template>
  <section
    :class="[
      'rounded-[1.35rem] overflow-hidden',
      toneClasses[props.tone],
      props.padded ? 'p-4 sm:p-5' : '',
      props.hoverable ? 'soft-card-hover' : '',
    ]"
  >
    <slot />
  </section>
</template>
