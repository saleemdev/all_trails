import { defineStore } from 'pinia'
import type { BlogPost, PhotoGallery, BlogFilters } from '../types'

const USE_MOCK_DATA = true

// Mock blog posts
const mockBlogPosts: BlogPost[] = [
  {
    id: '1',
    title: 'Conquering Mount Kenya: A Beginner\'s Guide',
    slug: 'conquering-mount-kenya-beginners-guide',
    excerpt: 'Everything you need to know before attempting Kenya\'s highest peak. From preparation to summit day, we\'ve got you covered.',
    content: 'Full article content...',
    featured_image: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/blog-1.jpeg',
    author: 'Sarah Kamau',
    author_image: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/author-1.jpeg',
    category: 'Mountain Hiking',
    tags: ['Mount Kenya', 'Beginner', 'High Altitude'],
    published_date: '2025-01-15',
    read_time: 8,
    status: 'Published',
    created_at: '2025-01-15T10:00:00',
    updated_at: '2025-01-15T10:00:00',
  },
  {
    id: '2',
    title: 'Hidden Gems: 5 Unexplored Trails in the Rift Valley',
    slug: 'hidden-gems-unexplored-trails-rift-valley',
    excerpt: 'Discover secret hiking spots that most tourists miss. These trails offer stunning views without the crowds.',
    content: 'Full article content...',
    featured_image: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/blog-2.jpeg',
    author: 'John Mwangi',
    author_image: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/author-2.jpeg',
    category: 'Trail Discovery',
    tags: ['Rift Valley', 'Hidden Trails', 'Off the Beaten Path'],
    published_date: '2025-01-10',
    read_time: 6,
    status: 'Published',
    created_at: '2025-01-10T10:00:00',
    updated_at: '2025-01-10T10:00:00',
  },
  {
    id: '3',
    title: 'Essential Hiking Gear for East African Climates',
    slug: 'essential-hiking-gear-east-africa',
    excerpt: 'A comprehensive guide to packing for hiking in Kenya. Don\'t hit the trail without these essentials!',
    content: 'Full article content...',
    featured_image: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/blog-3.jpeg',
    author: 'Grace Wanjiru',
    author_image: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/author-3.jpeg',
    category: 'Gear & Equipment',
    tags: ['Hiking Gear', 'Preparation', 'Equipment'],
    published_date: '2025-01-05',
    read_time: 10,
    status: 'Published',
    created_at: '2025-01-05T10:00:00',
    updated_at: '2025-01-05T10:00:00',
  },
  {
    id: '4',
    title: 'Best Time to Hike in Kenya: A Seasonal Guide',
    slug: 'best-time-to-hike-kenya-seasonal-guide',
    excerpt: 'Plan your hiking adventures around Kenya\'s seasons for the best experience. Weather, wildlife, and crowd insights.',
    content: 'Full article content...',
    featured_image: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/blog-4.jpeg',
    author: 'David Omondi',
    author_image: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/author-4.jpeg',
    category: 'Travel Tips',
    tags: ['Seasons', 'Weather', 'Planning'],
    published_date: '2024-12-20',
    read_time: 7,
    status: 'Published',
    created_at: '2024-12-20T10:00:00',
    updated_at: '2024-12-20T10:00:00',
  },
]

// Mock photo galleries
const mockGalleries: PhotoGallery[] = [
  {
    id: '1',
    title: 'Mount Longonot Crater',
    description: 'Stunning views from the rim of Mount Longonot volcano',
    category: 'Mountain Views',
    photographer: 'Sarah Kamau',
    created_date: '2025-01-10',
    images: [
      {
        id: '1-1',
        url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-longonot-1.jpeg',
        caption: 'Sunrise at the crater rim',
        thumbnail_url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-longonot-1-thumb.jpeg',
      },
      {
        id: '1-2',
        url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-longonot-2.jpeg',
        caption: 'Panoramic crater view',
        thumbnail_url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-longonot-2-thumb.jpeg',
      },
      {
        id: '1-3',
        url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-longonot-3.jpeg',
        caption: 'Hikers descending into the crater',
        thumbnail_url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-longonot-3-thumb.jpeg',
      },
    ],
  },
  {
    id: '2',
    title: 'Karura Forest Trails',
    description: 'Urban jungle escape in the heart of Nairobi',
    category: 'Forest Trails',
    photographer: 'John Mwangi',
    created_date: '2025-01-08',
    images: [
      {
        id: '2-1',
        url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-karura-1.jpeg',
        caption: 'Waterfall along the trail',
        thumbnail_url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-karura-1-thumb.jpeg',
      },
      {
        id: '2-2',
        url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-karura-2.jpeg',
        caption: 'Bamboo forest section',
        thumbnail_url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-karura-2-thumb.jpeg',
      },
    ],
  },
  {
    id: '3',
    title: 'Ngong Hills Adventure',
    description: 'Rolling green hills with panoramic valley views',
    category: 'Hill Hiking',
    photographer: 'Grace Wanjiru',
    created_date: '2025-01-05',
    images: [
      {
        id: '3-1',
        url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-ngong-1.jpeg',
        caption: 'Wind turbines on the ridge',
        thumbnail_url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-ngong-1-thumb.jpeg',
      },
      {
        id: '3-2',
        url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-ngong-2.jpeg',
        caption: 'Sunset over the Rift Valley',
        thumbnail_url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-ngong-2-thumb.jpeg',
      },
      {
        id: '3-3',
        url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-ngong-3.jpeg',
        caption: 'Hikers on the ridge trail',
        thumbnail_url: '/api/method/frappe.utils.file_manager.get_file?file_url=/files/gallery-ngong-3-thumb.jpeg',
      },
    ],
  },
]

export const useBlogStore = defineStore('blog', {
  state: () => ({
    blogPosts: [] as BlogPost[],
    galleries: [] as PhotoGallery[],
    selectedPost: null as BlogPost | null,
    selectedGallery: null as PhotoGallery | null,
    filters: {} as BlogFilters,
    isLoading: false,
    error: null as string | null,
  }),

  getters: {
    filteredBlogPosts: (state) => {
      let posts = [...state.blogPosts]

      if (state.filters.search) {
        const search = state.filters.search.toLowerCase()
        posts = posts.filter(
          (post) =>
            post.title.toLowerCase().includes(search) ||
            post.excerpt.toLowerCase().includes(search) ||
            post.category.toLowerCase().includes(search)
        )
      }

      if (state.filters.category) {
        posts = posts.filter((post) => post.category === state.filters.category)
      }

      if (state.filters.tag) {
        posts = posts.filter((post) => post.tags.includes(state.filters.tag!))
      }

      return posts.sort(
        (a, b) =>
          new Date(b.published_date).getTime() - new Date(a.published_date).getTime()
      )
    },

    filteredGalleries: (state) => {
      let galleries = [...state.galleries]

      if (state.filters.category) {
        galleries = galleries.filter((g) => g.category === state.filters.category)
      }

      if (state.filters.search) {
        const search = state.filters.search.toLowerCase()
        galleries = galleries.filter(
          (g) =>
            g.title.toLowerCase().includes(search) ||
            g.description.toLowerCase().includes(search)
        )
      }

      return galleries.sort(
        (a, b) =>
          new Date(b.created_date).getTime() - new Date(a.created_date).getTime()
      )
    },

    blogCategories: (state) => {
      const categories = new Set(state.blogPosts.map((post) => post.category))
      return Array.from(categories).sort()
    },

    galleryCategories: (state) => {
      const categories = new Set(state.galleries.map((g) => g.category))
      return Array.from(categories).sort()
    },

    allTags: (state) => {
      const tags = new Set<string>()
      state.blogPosts.forEach((post) => {
        post.tags.forEach((tag) => tags.add(tag))
      })
      return Array.from(tags).sort()
    },
  },

  actions: {
    async fetchBlogPosts() {
      this.isLoading = true
      this.error = null

      try {
        if (USE_MOCK_DATA) {
          await new Promise((resolve) => setTimeout(resolve, 500))
          this.blogPosts = mockBlogPosts
        } else {
          // TODO: Implement real API call
          // const response = await fetch('/api/method/all_trails.api.get_blog_posts')
          // this.blogPosts = response.data
        }
      } catch (error) {
        this.error = 'Failed to load blog posts'
        console.error('Error fetching blog posts:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchGalleries() {
      this.isLoading = true
      this.error = null

      try {
        if (USE_MOCK_DATA) {
          await new Promise((resolve) => setTimeout(resolve, 500))
          this.galleries = mockGalleries
        } else {
          // TODO: Implement real API call
          // const response = await fetch('/api/method/all_trails.api.get_galleries')
          // this.galleries = response.data
        }
      } catch (error) {
        this.error = 'Failed to load galleries'
        console.error('Error fetching galleries:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchBlogPostBySlug(slug: string) {
      this.isLoading = true
      this.error = null

      try {
        if (USE_MOCK_DATA) {
          await new Promise((resolve) => setTimeout(resolve, 300))
          this.selectedPost =
            mockBlogPosts.find((post) => post.slug === slug) || null
        } else {
          // TODO: Implement real API call
        }
      } catch (error) {
        this.error = 'Failed to load blog post'
        console.error('Error fetching blog post:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchGalleryById(id: string) {
      this.isLoading = true
      this.error = null

      try {
        if (USE_MOCK_DATA) {
          await new Promise((resolve) => setTimeout(resolve, 300))
          this.selectedGallery = mockGalleries.find((g) => g.id === id) || null
        } else {
          // TODO: Implement real API call
        }
      } catch (error) {
        this.error = 'Failed to load gallery'
        console.error('Error fetching gallery:', error)
      } finally {
        this.isLoading = false
      }
    },

    setFilters(filters: Partial<BlogFilters>) {
      this.filters = { ...this.filters, ...filters }
    },

    clearFilters() {
      this.filters = {}
    },
  },
})
