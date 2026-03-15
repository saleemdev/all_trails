<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../../services/api'

const router = useRouter()

const title = ref('')
const slug = ref('')
const excerpt = ref('')
const featuredImage = ref('')
const content = ref('')
const isSubmitting = ref(false)
const error = ref('')

const autoSlugify = () => {
  if (slug.value.trim()) {
    return
  }

  slug.value = title.value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
}

const submitPost = async () => {
  if (!title.value.trim() || !content.value.trim()) {
    error.value = 'Title and content are required.'
    return
  }

  isSubmitting.value = true
  error.value = ''

  try {
    const post = await apiService.createBlogPost({
      title: title.value.trim(),
      slug: slug.value.trim() || undefined,
      excerpt: excerpt.value.trim() || undefined,
      featured_image: featuredImage.value.trim() || undefined,
      content: content.value,
      published: 1,
    })

    router.push({ name: 'BlogDetail', params: { slug: post.slug } })
  } catch (reason: any) {
    const status = Number(reason?.status || 0)
    if (status === 403) {
      error.value = 'You need both Trail Member and Blogger roles to create blog posts.'
      return
    }

    error.value = reason?.message || 'Unable to publish blog post.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="page-shell w-full min-h-screen">
    <div class="layout-shell-narrow page-block-tight space-y-6">
      <button @click="router.back()" class="soft-button-secondary px-5 py-3">
        ← Back
      </button>

      <section class="surface-card-lg">
        <p class="page-kicker mb-2">Creator mode</p>
        <h1 class="text-[clamp(2rem,4vw,3rem)] font-semibold text-slate-900 leading-[1.02] tracking-[-0.04em] mb-3">Create Blog Post</h1>
        <p class="text-slate-600 mb-0">Publish image-led trail content to the public blog feed.</p>
      </section>

      <section class="surface-card-lg space-y-4">
        <div>
          <label class="tone-kicker mb-2 block">Title</label>
          <input v-model="title" class="soft-input w-full" type="text" @blur="autoSlugify" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="tone-kicker mb-2 block">Slug</label>
            <input v-model="slug" class="soft-input w-full" type="text" placeholder="auto-generated-from-title" />
          </div>
          <div>
            <label class="tone-kicker mb-2 block">Featured Image URL</label>
            <input v-model="featuredImage" class="soft-input w-full" type="url" placeholder="https://..." />
          </div>
        </div>

        <div>
          <label class="tone-kicker mb-2 block">Excerpt</label>
          <textarea v-model="excerpt" rows="3" class="soft-input w-full" placeholder="Short summary shown on the blog listing"></textarea>
        </div>

        <div>
          <label class="tone-kicker mb-2 block">Content (HTML supported)</label>
          <textarea
            v-model="content"
            rows="14"
            class="soft-input w-full"
            placeholder="Write your story here. You can include HTML markup."
          ></textarea>
        </div>

        <div v-if="error" class="surface-danger-subtle rounded-[1rem] px-4 py-3 text-sm">
          {{ error }}
        </div>

        <div class="flex flex-wrap gap-3">
          <button class="soft-button-secondary px-6 py-3" @click="router.back()">Cancel</button>
          <button class="brand-button px-6 py-3 disabled:opacity-60" :disabled="isSubmitting" @click="submitPost">
            <span v-if="!isSubmitting">Publish Post</span>
            <span v-else>Publishing...</span>
          </button>
        </div>
      </section>
    </div>
  </div>
</template>
