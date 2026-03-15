import { defineStore } from 'pinia'
import { apiService } from '../services/api'
import type { BlogFilters, BlogPost, BlogPostInput, PhotoGallery } from '../types'

interface BlogState {
  blogPosts: BlogPost[]
  galleries: PhotoGallery[]
  selectedPost: BlogPost | null
  selectedGallery: PhotoGallery | null
  filters: BlogFilters
  isLoading: boolean
  error: string | null
  page: number
  pageSize: number
  total: number
}

export const useBlogStore = defineStore('blog', {
  state: (): BlogState => ({
    blogPosts: [],
    galleries: [],
    selectedPost: null,
    selectedGallery: null,
    filters: {},
    isLoading: false,
    error: null,
    page: 1,
    pageSize: 12,
    total: 0,
  }),

  getters: {
    filteredBlogPosts: (state): BlogPost[] => {
      const search = String(state.filters.search || '').trim().toLowerCase()
      const category = String(state.filters.category || '').trim().toLowerCase()
      const tag = String(state.filters.tag || '').trim().toLowerCase()

      return state.blogPosts.filter((post) => {
        const inSearch =
          !search ||
          post.title.toLowerCase().includes(search) ||
          post.excerpt.toLowerCase().includes(search) ||
          post.author.toLowerCase().includes(search)

        const inCategory = !category || post.category.toLowerCase() === category
        const inTag = !tag || post.tags.some((postTag) => postTag.toLowerCase() === tag)

        return inSearch && inCategory && inTag
      })
    },

    filteredGalleries: (state): PhotoGallery[] => state.galleries,

    blogCategories: (state): string[] => {
      const categories = new Set(state.blogPosts.map((post) => post.category).filter(Boolean))
      return Array.from(categories).sort()
    },

    galleryCategories: () => [] as string[],

    allTags: (state): string[] => {
      const tags = new Set<string>()
      state.blogPosts.forEach((post) => {
        post.tags.forEach((tag) => tags.add(tag))
      })
      return Array.from(tags).sort()
    },
  },

  actions: {
    async fetchBlogPosts(page = 1) {
      this.isLoading = true
      this.error = null

      try {
        const response = await apiService.getBlogPosts(this.filters.search, page, this.pageSize)
        this.blogPosts = response.data
        this.total = response.total
        this.page = response.page
      } catch (error: any) {
        this.error = error?.message || 'Failed to load blog posts'
      } finally {
        this.isLoading = false
      }
    },

    async fetchBlogPostBySlug(slug: string) {
      this.isLoading = true
      this.error = null

      try {
        this.selectedPost = await apiService.getBlogPost(slug)
      } catch (error: any) {
        this.error = error?.message || 'Failed to load blog post'
        this.selectedPost = null
      } finally {
        this.isLoading = false
      }
    },

    async createBlogPost(payload: BlogPostInput) {
      this.isLoading = true
      this.error = null

      try {
        const post = await apiService.createBlogPost(payload)
        this.blogPosts.unshift(post)
        this.total += 1
        return post
      } catch (error: any) {
        this.error = error?.message || 'Failed to create blog post'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchGalleries() {
      this.galleries = []
      this.selectedGallery = null
    },

    async fetchGalleryById(_id: string) {
      this.selectedGallery = null
    },

    setFilters(filters: Partial<BlogFilters>) {
      this.filters = { ...this.filters, ...filters }
      this.page = 1
    },

    clearFilters() {
      this.filters = {}
      this.page = 1
    },
  },
})
