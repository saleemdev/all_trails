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
const authorImageFailed = ref(false)
const coverImageFailed = ref(false)

const loadPost = async () => {
  const slug = route.params.slug as string
  authorImageFailed.value = false
  coverImageFailed.value = false
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
      <button @click="router.back()" class="soft-button-secondary px-4 py-2.5 text-sm mb-5">
        ← Back to Blog
      </button>

      <div v-if="isLoading" class="flex flex-col items-center justify-center py-32">
        <div class="soft-spinner mb-4"></div>
        <p class="text-lg text-slate-600 font-medium mb-0">Loading article...</p>
      </div>

      <article v-else-if="post" class="surface-card-lg rounded-[1.1rem]">
        <header class="mb-5 border-b border-[color:var(--color-border-soft)] pb-5">
          <div class="mb-3 flex items-center gap-3">
            <img
              v-if="post.author_image && !authorImageFailed"
              :src="post.author_image"
              :alt="post.author"
              class="h-11 w-11 rounded-full object-cover border border-[color:var(--color-border-soft)]"
              @error="authorImageFailed = true"
            />
            <div v-else class="brand-mark h-11 w-11 rounded-full text-[13px] text-white">
              {{ post.author?.charAt(0) || 'A' }}
            </div>
            <div class="min-w-0">
              <p class="mb-0 text-[15px] font-semibold text-[color:var(--color-text-primary)] truncate">{{ post.author }}</p>
              <p class="mb-0 text-[12px] text-[color:var(--color-text-secondary)]">{{ formatDate(post.published_date) }} · {{ post.read_time }} min read</p>
            </div>
          </div>

          <h1 class="text-[clamp(1.55rem,3.1vw,2.3rem)] font-semibold leading-[1.1] tracking-[-0.03em] text-[color:var(--color-text-primary)] mb-0">
            {{ post.title }}
          </h1>

          <div class="mt-3 flex flex-wrap items-center gap-2">
            <span class="soft-badge soft-badge--neutral">{{ post.category }}</span>
          </div>
        </header>

        <figure
          v-if="post.featured_image && !coverImageFailed"
          class="mb-5 overflow-hidden rounded-[1rem] border border-[color:var(--color-border-soft)] bg-slate-900"
        >
          <img
            :src="post.featured_image"
            :alt="post.title"
            class="h-[210px] w-full object-cover sm:h-[280px]"
            @error="coverImageFailed = true"
          />
        </figure>

        <p v-if="post.excerpt" class="mb-5 text-[14px] leading-7 text-[color:var(--color-text-secondary)]">
          {{ post.excerpt }}
        </p>

        <div class="prose prose-lg max-w-none text-slate-700" v-html="post.content"></div>

        <div v-if="post.tags.length" class="mt-8 pt-6 border-t border-[color:var(--color-border-soft)]">
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
      </article>

      <div v-else class="surface-card-lg text-center">
        <h2 class="text-2xl font-semibold text-slate-900 mb-2">Article not found</h2>
        <p class="mb-7 text-base text-slate-600">We couldn't find the article you're looking for.</p>
        <button @click="router.push('/blog')" class="brand-button px-8 py-4">
          Back to Blog
        </button>
      </div>

      <section v-if="post" class="surface-card-lg mt-6 space-y-5">
        <div>
          <h2 class="text-xl font-semibold text-slate-900 mb-2">Comments</h2>
          <p class="text-sm tone-body mb-0">Published comments appear below. New comments are moderated.</p>
        </div>

        <div class="space-y-3">
          <div v-if="commentsLoading" class="text-sm text-slate-500">Loading comments...</div>
          <div v-else-if="comments.length === 0" class="text-sm text-slate-500">No published comments yet.</div>
          <article v-else v-for="comment in comments" :key="comment.id" class="surface-muted rounded-[1rem] p-3.5">
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
