<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMerchandiseStore } from '../../stores/merchandiseStore'
import {
  GlassAlert,
  GlassButton,
  GlassCard,
  GlassProductCard,
  GlassSpinner,
} from '../../components/glass'

const route = useRoute()
const router = useRouter()
const store = useMerchandiseStore()
const quantity = ref(1)
const selectedColor = ref('')
const selectedSize = ref('')
const selectedImage = ref('')

const item = computed(() => store.selectedItem)
const relatedItems = computed(() =>
  store.items
    .filter((entry) => entry.category_slug === item.value?.category_slug && entry.item_code !== item.value?.item_code)
    .slice(0, 3)
)

const loadItem = async () => {
  const current = await store.fetchItem(String(route.params.itemCode || ''))
  if (!current) {
    return
  }

  quantity.value = 1
  selectedColor.value = current.available_colors[0] || ''
  selectedSize.value = current.available_sizes[0] || ''
  selectedImage.value = current.gallery_urls[0] || current.image_url

  if (!store.items.length) {
    await store.fetchCatalog()
  }
}

const addCurrentItemToCart = () => {
  if (!item.value) {
    return
  }

  store.addToCart(item.value, quantity.value, {
    selected_color: selectedColor.value || undefined,
    selected_size: selectedSize.value || undefined,
  })

  router.push('/shop/cart')
}

onMounted(loadItem)

watch(
  () => route.params.itemCode,
  () => {
    loadItem()
  }
)
</script>

<template>
  <div class="layout-shell-wide page-block">
    <div v-if="store.isLoading" class="py-24">
      <GlassSpinner size="lg" label="Loading product detail" />
    </div>

    <template v-else-if="item">
      <div class="grid gap-7 lg:grid-cols-[1.02fr_0.98fr]">
        <div class="space-y-5">
          <GlassCard :padded="false" class="overflow-hidden">
            <img :src="selectedImage || item.image_url" :alt="item.item_name" class="h-[320px] w-full object-cover sm:h-[460px]" />
          </GlassCard>

          <div class="grid gap-3 sm:grid-cols-3">
            <button
              v-for="image in item.gallery_urls"
              :key="image"
              class="overflow-hidden rounded-[1.25rem] border-2 transition-all"
              :class="selectedImage === image ? 'border-[color:var(--color-primary)] shadow-lg' : 'border-transparent'"
              @click="selectedImage = image"
            >
              <img :src="image" :alt="item.item_name" class="h-28 w-full object-cover" />
            </button>
          </div>
        </div>

        <div class="space-y-5">
          <GlassCard tone="strong">
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">{{ item.category_name }}</p>
            <div class="mt-3 flex flex-wrap gap-2">
              <span
                v-for="badge in item.badges"
                :key="badge"
                class="soft-badge soft-badge--neutral"
              >
                {{ badge }}
              </span>
            </div>

            <h1 class="mt-4 text-[clamp(1.85rem,4vw,2.7rem)] font-semibold leading-[1.05] tracking-[-0.03em] text-slate-950">{{ item.item_name }}</h1>
            <p class="mt-4 text-sm leading-7 text-slate-600">{{ item.description }}</p>

            <div class="mt-6 flex flex-wrap items-end gap-3">
              <div>
                <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Current price</p>
                <div class="mt-1 flex items-center gap-3">
                  <span class="text-2xl font-semibold text-slate-950 sm:text-3xl">
                    KES {{ (item.discount_price ?? item.selling_price).toLocaleString() }}
                  </span>
                  <span v-if="item.discount_price" class="text-base text-slate-400 line-through">
                    KES {{ item.selling_price.toLocaleString() }}
                  </span>
                </div>
              </div>

              <div class="rounded-[0.95rem] bg-[rgba(49,83,72,0.08)] px-3.5 py-2.5 text-xs text-[color:var(--color-primary-dark)]">
                <p class="font-semibold">{{ item.average_rating.toFixed(1) }} / 5</p>
                <p>{{ item.review_count }} verified reviews</p>
              </div>
            </div>

            <div class="mt-7 grid gap-3.5 sm:grid-cols-2">
              <label class="flex flex-col gap-2 text-sm">
                <span class="font-semibold text-slate-800">Color</span>
                <select v-model="selectedColor" class="soft-input rounded-[1.05rem] bg-white/85">
                  <option v-for="color in item.available_colors" :key="color" :value="color">
                    {{ color }}
                  </option>
                </select>
              </label>

              <label class="flex flex-col gap-2 text-sm">
                <span class="font-semibold text-slate-800">Size</span>
                <select v-model="selectedSize" class="soft-input rounded-[1.05rem] bg-white/85">
                  <option v-for="size in item.available_sizes" :key="size" :value="size">
                    {{ size }}
                  </option>
                </select>
              </label>
            </div>

            <div class="mt-4 flex flex-wrap items-center gap-3">
              <label class="surface-muted flex items-center gap-2.5 rounded-full px-3.5 py-2">
                <span class="text-sm font-semibold text-slate-800">Qty</span>
                <input v-model.number="quantity" type="number" min="1" class="w-16 bg-transparent p-0 text-center text-base" />
              </label>
              <p class="text-sm text-slate-500">{{ item.inventory_qty }} units ready to dispatch</p>
            </div>

            <div class="mt-7 flex flex-wrap gap-3">
              <GlassButton @click="addCurrentItemToCart">Add to cart</GlassButton>
              <GlassButton variant="secondary" @click="router.push('/shop')">Keep browsing</GlassButton>
            </div>
          </GlassCard>

          <GlassCard>
            <div class="grid gap-4 sm:grid-cols-2">
              <div>
                <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Key highlights</p>
                <ul class="mt-3 space-y-3 text-sm leading-6 text-slate-700">
                  <li v-for="highlight in item.highlights" :key="highlight" class="flex items-start gap-2">
                    <span class="mt-1 h-2.5 w-2.5 rounded-full bg-[color:var(--color-primary-light)]" aria-hidden="true" />
                    <span>{{ highlight }}</span>
                  </li>
                </ul>
              </div>

              <div>
                <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Materials & dispatch</p>
                <ul class="mt-3 space-y-3 text-sm leading-6 text-slate-700">
                  <li v-for="material in item.materials" :key="material">{{ material }}</li>
                </ul>
                <p class="mt-4 rounded-[1rem] bg-slate-950 px-4 py-3 text-sm text-white">
                  {{ item.estimated_dispatch }}
                </p>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>

      <section class="mt-12 grid gap-7 lg:grid-cols-[0.95fr_1.05fr]">
        <GlassCard>
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Customer proof</p>
          <h2 class="app-section-title">Recent reviews</h2>

          <div class="mt-6 space-y-4">
            <article
              v-for="review in item.reviews || []"
              :key="review.id"
              class="rounded-[1.2rem] bg-white/80 p-4"
            >
              <div class="flex items-start justify-between gap-4">
                <div>
                  <h3 class="font-semibold text-slate-950">{{ review.title }}</h3>
                  <p class="text-sm text-slate-500">{{ review.customer_name }}</p>
                </div>
                <span class="rounded-full bg-[rgba(49,83,72,0.08)] px-3 py-1 text-sm font-semibold text-[color:var(--color-primary-dark)]">
                  {{ review.rating.toFixed(1) }} / 5
                </span>
              </div>
              <p class="mt-3 text-sm leading-6 text-slate-600">{{ review.review_text }}</p>
            </article>

            <GlassAlert v-if="!(item.reviews || []).length" tone="info" title="No reviews yet">
              This product is in the launch collection and waiting for the first customer notes.
            </GlassAlert>
          </div>
        </GlassCard>

        <div>
          <div class="mb-5 flex items-end justify-between gap-3">
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">More in this category</p>
              <h2 class="app-section-title">Related picks</h2>
            </div>
          </div>

          <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-2">
            <GlassProductCard
              v-for="related in relatedItems"
              :key="related.item_code"
              :item="related"
              @add-to-cart="store.addToCart($event, 1, { selected_color: $event.available_colors[0], selected_size: $event.available_sizes[0] })"
            />
          </div>
        </div>
      </section>
    </template>

    <GlassAlert v-else tone="error" title="Product unavailable">
      We could not find the requested item. Try returning to the shop catalog and selecting another product.
    </GlassAlert>
  </div>
</template>
