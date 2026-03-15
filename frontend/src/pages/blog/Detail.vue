<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBlogStore } from '../../stores/blogStore'
import { apiService } from '../../services/api'
import { useAuthStore } from '../../stores/authStore'
import type { BlogComment } from '../../types'

const route = useRoute()
const router = useRouter()
const blogStore = useBlogStore()
const authStore = useAuthStore()

const post = computed(() => blogStore.selectedPost)
const isLoading = computed(() => blogStore.isLoading)

const comments = ref<BlogComment[]>([])
const commentsLoading = ref(false)
const submittingComment = ref(false)
const commentContent = ref('')
const guestName = ref('')
const guestEmail = ref('')
const commentFeedback = ref('')

const loadPost = async () => {
  const slug = route.params.slug as string
  await blogStore.fetchBlogPostBySlug(slug)
}

const loadComments = async () => {
  const slug = route.params.slug as string
  commentsLoading.value = true
  try {
    const response = await apiService.getBlogComments(slug, 1, 50)
    comments.value = response.data
  } catch {
    comments.value = []
  } finally {
    commentsLoading.value = false
  }
}

const submitComment = async () => {
  if (!post.value?.slug) {
    return
  }

  const content = commentContent.value.trim()
  if (!content) {
    commentFeedback.value = 'Please enter your comment before submitting.'
    return
  }

  submittingComment.value = true
  commentFeedback.value = ''

  try {
    await apiService.createBlogComment({
      slug: post.value.slug,
      content,
      comment_by: authStore.isAuthenticated ? undefined : guestName.value || undefined,
      comment_email: authStore.isAuthenticated ? undefined : guestEmail.value || undefined,
    })

    commentContent.value = ''
    if (!authStore.isAuthenticated) {
      guestName.value = ''
      guestEmail.value = ''
    }

    commentFeedback.value = 'Comment submitted successfully and is awaiting moderation.'
  } catch (error: any) {
    commentFeedback.value = error?.message || 'Unable to submit comment right now.'
  } finally {
    submittingComment.value = false
  }
}

const handleImageError = (event: Event) => {
  const image = event.target as HTMLImageElement
  image.style.display = 'none'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-KE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

onMounted(async () => {
  await Promise.all([loadPost(), loadComments()])
})
</script>

<template>
  <div class="page-shell w-full min-h-screen">
    <div class="layout-shell-narrow page-block-tight">
      <button @click="router.back()" class="soft-button-secondary px-5 py-3 mb-6">
        ← Back to Blog
      </button>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="soft-spinner mb-4"></div>
        <p class="text-lg text-slate-600 font-medium mb-0">Loading article...</p>
      </div>

      <article v-else-if="post" class="glass-panel-strong rounded-[2rem] overflow-hidden space-y-0">
        <div class="h-96 bg-slate-900 relative overflow-hidden">
          <img
            v-if="post.featured_image"
            :src="post.featured_image"
            :alt="post.title"
            class="w-full h-full object-cover"
            @error="handleImageError"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/78 via-slate-900/18 to-transparent"></div>
          <div class="absolute bottom-8 left-8 right-8">
            <span class="soft-badge soft-badge--neutral mb-4">{{ post.category }}</span>
            <h1 class="text-[clamp(2rem,4vw,3.2rem)] font-semibold text-white leading-[1.02] tracking-[-0.04em] max-w-4xl">{{ post.title }}</h1>
          </div>
        </div>

        <div class="p-5 sm:p-6 md:p-10">
          <div class="flex items-center gap-4 mb-8 pb-8 border-b border-slate-200/80 flex-wrap">
            <div class="brand-mark w-16 h-16 rounded-full text-xl text-white">{{ post.author?.charAt(0) || 'A' }}</div>
            <div>
              <div class="text-lg font-semibold text-slate-900">{{ post.author }}</div>
              <div class="text-slate-600">{{ formatDate(post.published_date) }} · {{ post.read_time }} min read</div>
            </div>
          </div>

          <div class="surface-muted rounded-[1.5rem] p-5 sm:p-6 mb-8 border-l-4 border-[color:var(--color-primary)]">
            <p class="text-lg text-slate-700 leading-8 font-medium italic mb-0">{{ post.excerpt }}</p>
          </div>

          <div class="prose prose-lg max-w-none text-slate-700" v-html="post.content"></div>

          <div v-if="post.tags.length" class="mt-12 pt-8 border-t border-slate-200/80">
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in post.tags"
                :key="tag"
                class="soft-badge soft-badge--neutral"
              >
                #{{ tag }}
              </span>
            </div>
          </div>
        </div>
      </article>

      <div v-else class="surface-card-lg text-center">
        <h2 class="text-3xl font-semibold text-slate-900 mb-3">Article Not Found</h2>
        <p class="mb-7 text-base text-slate-600">We couldn't find the article you're looking for.</p>
        <button @click="router.push('/blog')" class="brand-button px-8 py-4">
          Back to Blog
        </button>
      </div>

      <section v-if="post" class="surface-card-lg mt-6 space-y-6">
        <div>
          <h2 class="text-2xl font-semibold text-slate-900 mb-2">Comments</h2>
          <p class="text-sm text-slate-600 mb-0">Published comments are shown below. New comments are moderated before display.</p>
        </div>

        <div class="space-y-3">
          <div v-if="commentsLoading" class="text-sm text-slate-500">Loading comments...</div>
          <div v-else-if="comments.length === 0" class="text-sm text-slate-500">No published comments yet.</div>
          <article v-else v-for="comment in comments" :key="comment.id" class="surface-muted rounded-[1.2rem] p-4">
            <div class="flex items-center justify-between gap-4 mb-2 flex-wrap">
              <p class="font-semibold text-slate-900 mb-0">{{ comment.author }}</p>
              <p class="text-xs text-slate-500 mb-0">{{ formatDate(comment.created_at) }}</p>
            </div>
            <p class="text-sm text-slate-700 mb-0" v-html="comment.content"></p>
          </article>
        </div>

        <div class="border-t border-slate-200/80 pt-6 space-y-4">
          <h3 class="text-lg font-semibold text-slate-900 mb-0">Leave a Comment</h3>

          <div v-if="!authStore.isAuthenticated" class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <input v-model="guestName" type="text" placeholder="Your name (optional)" class="soft-input" />
            <input v-model="guestEmail" type="email" placeholder="Email (optional)" class="soft-input" />
          </div>

          <textarea
            v-model="commentContent"
            rows="4"
            class="soft-input w-full"
            placeholder="Share your thoughts about this trail story..."
          ></textarea>

          <div class="flex flex-wrap gap-3 items-center">
            <button
              class="brand-button px-6 py-3 disabled:opacity-60"
              :disabled="submittingComment"
              @click="submitComment"
            >
              <span v-if="!submittingComment">Submit Comment</span>
              <span v-else>Submitting...</span>
            </button>
            <p v-if="commentFeedback" class="text-sm text-slate-600 mb-0">{{ commentFeedback }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
