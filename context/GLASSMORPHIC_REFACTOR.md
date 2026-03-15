# Glassmorphic UI Refactoring Guide

## Overview
This guide provides step-by-step implementation instructions for refactoring the All Trails UI to use glassmorphic design patterns with backdrop blur, layered depth, and minimalist styling.

## Phase 1: CSS Foundation

### Step 1.1: Update Global Design Tokens

**File**: `frontend/src/styles/globals.css`

Add these CSS variables after existing color definitions:

```css
/* Glassmorphic Effect Variables */
:root {
  /* Glass Base Properties */
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
  --glass-backdrop-blur: 30px;
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  --glass-inner-glow: rgba(255, 255, 255, 0.2);

  /* Glass Variants - Primary Forest Dark */
  --glass-primary-bg: rgba(27, 58, 45, 0.15);
  --glass-primary-border: rgba(27, 58, 45, 0.3);
  --glass-primary-shadow: 0 12px 48px rgba(27, 58, 45, 0.15);

  /* Glass Variants - Accent Warm Orange */
  --glass-accent-bg: rgba(232, 93, 31, 0.15);
  --glass-accent-border: rgba(232, 93, 31, 0.3);
  --glass-accent-shadow: 0 12px 48px rgba(232, 93, 31, 0.15);

  /* Glass Variants - Semantic Colors */
  --glass-success-bg: rgba(76, 175, 80, 0.15);
  --glass-success-border: rgba(76, 175, 80, 0.3);

  --glass-warning-bg: rgba(255, 167, 38, 0.15);
  --glass-warning-border: rgba(255, 167, 38, 0.3);

  --glass-error-bg: rgba(239, 83, 80, 0.15);
  --glass-error-border: rgba(239, 83, 80, 0.3);

  --glass-info-bg: rgba(41, 182, 246, 0.15);
  --glass-info-border: rgba(41, 182, 246, 0.3);
}

/* Dark Mode Adjustments */
[data-theme='dark'] {
  --glass-bg: rgba(255, 255, 255, 0.08);
  --glass-border: rgba(255, 255, 255, 0.15);
  --glass-primary-bg: rgba(27, 58, 45, 0.2);
  --glass-primary-border: rgba(255, 255, 255, 0.15);
  --glass-accent-bg: rgba(232, 93, 31, 0.2);
  --glass-accent-border: rgba(255, 255, 255, 0.15);
}

/* Reduced blur on small screens for performance */
@media (max-width: 640px) {
  :root {
    --glass-backdrop-blur: 20px;
  }
}

/* Enhanced effects on large screens */
@media (min-width: 1024px) {
  :root {
    --glass-inner-glow: rgba(255, 255, 255, 0.25);
  }
}
```

### Step 1.2: Create Glass Utility Classes

Add to `frontend/src/styles/globals.css`:

```css
/* Base Glass Class */
.glass {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(var(--glass-backdrop-blur));
  -webkit-backdrop-filter: blur(var(--glass-backdrop-blur)); /* Safari */
  box-shadow: var(--glass-shadow);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

/* Glass Interactive States */
.glass:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.glass:active {
  transform: translateY(0);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

/* Glass Variants */
.glass-primary {
  background: var(--glass-primary-bg);
  border-color: var(--glass-primary-border);
  box-shadow: var(--glass-primary-shadow);
}

.glass-primary:hover {
  background: rgba(27, 58, 45, 0.25);
  border-color: rgba(27, 58, 45, 0.4);
}

.glass-accent {
  background: var(--glass-accent-bg);
  border-color: var(--glass-accent-border);
  box-shadow: var(--glass-accent-shadow);
}

.glass-accent:hover {
  background: rgba(232, 93, 31, 0.25);
  border-color: rgba(232, 93, 31, 0.4);
}

.glass-success {
  background: var(--glass-success-bg);
  border-color: var(--glass-success-border);
}

.glass-warning {
  background: var(--glass-warning-bg);
  border-color: var(--glass-warning-border);
}

.glass-error {
  background: var(--glass-error-bg);
  border-color: var(--glass-error-border);
}

.glass-info {
  background: var(--glass-info-bg);
  border-color: var(--glass-info-border);
}

/* Glass with elevated depth */
.glass-elevated {
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 0 20px var(--glass-inner-glow);
}

.glass-elevated:hover {
  box-shadow:
    0 12px 48px rgba(0, 0, 0, 0.15),
    inset 0 0 20px var(--glass-inner-glow);
}

/* Glass with strong border definition */
.glass-outlined {
  border-width: 2px;
  background: rgba(255, 255, 255, 0.08);
}

/* Glass gradient overlay (for images) */
.glass-gradient-overlay {
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.05),
    rgba(0, 0, 0, 0.3)
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* Glass divider */
.glass-divider {
  height: 1px;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0),
    rgba(255, 255, 255, 0.3),
    rgba(255, 255, 255, 0)
  );
}

/* Responsive sizing */
@media (max-width: 640px) {
  .glass {
    border-radius: var(--radius-md);
  }
}

@media (min-width: 1024px) {
  .glass {
    border-radius: var(--radius-xl);
  }
}
```

## Phase 2: Vue Component Library

### Step 2.1: Create GlassCard Component

**File**: `frontend/src/components/ui/GlassCard.vue`

```vue
<template>
  <div
    class="glass"
    :class="[variantClass, sizeClass, elevatoinClass, customClasses]"
    :style="customStyle"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'primary' | 'accent' | 'success' | 'warning' | 'error' | 'info'
  size?: 'sm' | 'md' | 'lg'
  elevated?: boolean
  outlined?: boolean
  blur?: number
  interactive?: boolean
  customClasses?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'md',
  elevated: false,
  outlined: false,
  blur: 30,
  interactive: true,
  customClasses: ''
})

const variantClass = computed(() => {
  const variants = {
    default: '',
    primary: 'glass-primary',
    accent: 'glass-accent',
    success: 'glass-success',
    warning: 'glass-warning',
    error: 'glass-error',
    info: 'glass-info'
  }
  return variants[props.variant]
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'p-3 gap-2',
    md: 'p-6 gap-4',
    lg: 'p-8 gap-6'
  }
  return sizes[props.size]
})

const elevatoinClass = computed(() => {
  return props.elevated ? 'glass-elevated' : ''
})

const customStyle = computed(() => ({
  '--glass-backdrop-blur': `${props.blur}px`
} as any))
</script>

<style scoped>
:deep(.glass) {
  display: flex;
  flex-direction: column;
}
</style>
```

### Step 2.2: Create GlassButton Component

**File**: `frontend/src/components/ui/GlassButton.vue`

```vue
<template>
  <button
    class="glass-button glass"
    :class="[variantClass, sizeClass, { 'opacity-50 cursor-not-allowed': disabled }]"
    :disabled="disabled"
    :style="customStyle"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'primary' | 'accent' | 'success' | 'warning' | 'error'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  blur?: number
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'accent',
  size: 'md',
  disabled: false,
  blur: 25
})

const variantClass = computed(() => {
  const variants = {
    default: '',
    primary: 'glass-primary',
    accent: 'glass-accent',
    success: 'glass-success',
    warning: 'glass-warning',
    error: 'glass-error'
  }
  return variants[props.variant]
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  }
  return sizes[props.size]
})

const customStyle = computed(() => ({
  '--glass-backdrop-blur': `${props.blur}px`
} as any))
</script>

<style scoped>
.glass-button {
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  outline: none;
  transition: all var(--transition-base);
}

.glass-button:not(:disabled):hover {
  transform: translateY(-1px);
}

.glass-button:not(:disabled):active {
  transform: translateY(0);
}
</style>
```

### Step 2.3: Create GlassModal Component

**File**: `frontend/src/components/ui/GlassModal.vue`

```vue
<template>
  <div v-if="isOpen" class="glass-modal-overlay" @click.self="close">
    <div class="glass-modal glass" :class="[variantClass, sizeClass]">
      <!-- Close button -->
      <button class="glass-modal-close" @click="close">
        <Icon name="x" class="w-5 h-5" />
      </button>

      <!-- Content -->
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import Icon from '@/components/Icon.vue'

interface Props {
  isOpen: boolean
  variant?: 'default' | 'primary' | 'accent'
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'md'
})

const emit = defineEmits<{
  close: []
}>()

const variantClass = computed(() => {
  const variants = {
    default: '',
    primary: 'glass-primary',
    accent: 'glass-accent'
  }
  return variants[props.variant]
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg'
  }
  return sizes[props.size]
})

function close() {
  emit('close')
}

// Close on escape key
watch(
  () => props.isOpen,
  (isOpen) => {
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown)
    } else {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }
)

function handleKeyDown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    close()
  }
}
</script>

<style scoped>
.glass-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  animation: fadeIn 0.2s ease-in-out;
}

.glass-modal {
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
  animation: slideUp 0.3s ease-in-out;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.2),
    inset 0 0 30px rgba(255, 255, 255, 0.15);
}

.glass-modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 150ms;
  color: currentColor;
}

.glass-modal-close:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 640px) {
  .glass-modal {
    max-width: 95vw;
    max-height: 95vh;
    border-radius: var(--radius-md);
  }
}
</style>
```

## Phase 3: Component Refactoring

### Step 3.1: Refactor TrailCard Component

**File**: `frontend/src/components/features/trails/TrailCard.vue`

Replace existing implementation:

```vue
<template>
  <GlassCard variant="primary" class="overflow-hidden group h-full flex flex-col">
    <!-- Image with glass overlay -->
    <div class="relative h-48 overflow-hidden rounded-lg flex-shrink-0">
      <img
        :src="trail.featured_image || 'https://via.placeholder.com/400x300'"
        :alt="trail.title"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
      />

      <!-- Glassmorphic overlay with difficulty badge -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent
                   glass-gradient-overlay group-hover:opacity-100 opacity-0
                   flex flex-col justify-between p-3 transition-opacity">
        <div class="flex justify-end">
          <GlassChip
            :difficulty="trail.difficulty_level"
            size="sm"
          />
        </div>

        <!-- Location at bottom -->
        <div class="text-white text-sm font-medium drop-shadow">
          📍 {{ trail.location }}
        </div>
      </div>
    </div>

    <!-- Content section -->
    <div class="flex-1 flex flex-col p-4 gap-3">
      <!-- Title -->
      <h3 class="text-lg font-bold leading-tight">
        {{ trail.title }}
      </h3>

      <!-- Glass divider -->
      <div class="glass-divider" />

      <!-- Trail metrics grid -->
      <div class="grid grid-cols-2 gap-2">
        <div class="glass glass-accent text-center p-2 rounded-lg">
          <div class="text-xs text-gray-600">Distance</div>
          <div class="font-semibold text-sm">{{ trail.distance_km }}km</div>
        </div>
        <div class="glass glass-accent text-center p-2 rounded-lg">
          <div class="text-xs text-gray-600">Duration</div>
          <div class="font-semibold text-sm">{{ trail.duration_hours }}h</div>
        </div>
        <div class="glass glass-accent text-center p-2 rounded-lg">
          <div class="text-xs text-gray-600">Elevation</div>
          <div class="font-semibold text-sm">{{ trail.elevation_gain_m }}m</div>
        </div>
        <div class="glass glass-accent text-center p-2 rounded-lg">
          <div class="text-xs text-gray-600">Spots</div>
          <div class="font-semibold text-sm">{{ trail.available_spots }}/{{ trail.max_capacity }}</div>
        </div>
      </div>

      <!-- Glass divider -->
      <div class="glass-divider" />

      <!-- Price & CTA section -->
      <div class="flex items-center justify-between gap-2 mt-auto pt-2">
        <div>
          <p class="text-xs text-gray-600">Price per person</p>
          <p class="text-xl font-bold text-orange-600">
            KES {{ trail.price_kshs.toLocaleString() }}
          </p>
        </div>
        <GlassButton
          variant="accent"
          size="sm"
          @click="$emit('book')"
          class="flex-1"
        >
          Book Now
        </GlassButton>
      </div>
    </div>
  </GlassCard>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import type { Trail } from '@/types'
import GlassCard from '@/components/ui/GlassCard.vue'
import GlassButton from '@/components/ui/GlassButton.vue'
import GlassChip from '@/components/ui/GlassChip.vue'

defineProps<{
  trail: Trail
}>()

defineEmits<{
  book: []
}>()
</script>
```

### Step 3.2: Create GlassChip Component

**File**: `frontend/src/components/ui/GlassChip.vue`

```vue
<template>
  <span
    class="glass-chip glass"
    :class="[variantClass, sizeClass]"
  >
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  difficulty?: 'Easy' | 'Moderate' | 'Hard' | 'Expert'
  label?: string
  size?: 'sm' | 'md'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'sm'
})

const variantClass = computed(() => {
  const variants = {
    'Easy': 'glass-success',
    'Moderate': 'glass-info',
    'Hard': 'glass-warning',
    'Expert': 'glass-error'
  }
  return variants[props.difficulty] || ''
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'px-3 py-1 text-xs',
    md: 'px-4 py-2 text-sm'
  }
  return sizes[props.size]
})

const label = computed(() => {
  if (props.label) return props.label
  return props.difficulty || 'Unknown'
})
</script>

<style scoped>
.glass-chip {
  display: inline-block;
  font-weight: 600;
  border-radius: 999px;
  white-space: nowrap;
}
</style>
```

## Phase 4: Testing & Validation

### Checklist for Glassmorphic Implementation

- [ ] Glass CSS variables load in browser DevTools
- [ ] Blur effect renders on Chrome, Firefox, Safari (desktop & mobile)
- [ ] Hover states trigger smoothly without lag
- [ ] Dark mode CSS variables apply correctly
- [ ] Mobile blur reduced to 20px (check performance)
- [ ] Components render without layout shifts
- [ ] Accessibility: focus states visible with keyboard navigation
- [ ] Print styles hide blur effects
- [ ] All color variants visually distinct

### Performance Testing

```bash
# Check frame rate during hover interactions
# DevTools → Performance → Record → Hover on glass elements
# Target: 60fps (16ms frame budget)

# Check CSS file size increase
du -h frontend/src/styles/globals.css

# Measure paint/composite time
# DevTools → Performance → Record → Analyze
```

## Migration Path

1. **Week 1**: Implement CSS tokens + utility classes
2. **Week 1-2**: Create 4-5 core UI components (Card, Button, Modal, Chip, Panel)
3. **Week 2-3**: Refactor existing components (TrailCard, TrailFilters, Modals)
4. **Week 3-4**: Full page refactoring (detail views, booking flows)
5. **Week 4**: Testing, performance optimization, browser compatibility

## Browser Support

| Browser | Version | Support | Notes |
|---------|---------|---------|-------|
| Chrome | 76+ | Full | backdrop-filter supported |
| Firefox | 103+ | Full | Recent versions |
| Safari | 14.1+ | Full | -webkit-backdrop-filter needed |
| Edge | 79+ | Full | Chromium-based |
| Mobile Safari | 14.5+ | Full | iOS performance optimized |
| Mobile Chrome | 99+ | Full | Android support |

---

## Resources

- [MDN: backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)
- [Can I Use: backdrop-filter](https://caniuse.com/backdrop-filter)
- [Glassmorphism UI Design](https://glassmorphism.com/)
- Context7: Glass UI Library Documentation

