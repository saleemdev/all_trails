import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import './styles/globals.css'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/authStore'

const CHUNK_RECOVERY_KEY = 'all-trails:chunk-recovery'

const isDynamicImportFetchError = (error: unknown): boolean => {
  if (!(error instanceof Error) || !error.message) {
    return false
  }

  return (
    error.message.includes('Failed to fetch dynamically imported module') ||
    error.message.includes('Importing a module script failed')
  )
}

const recoverFromStaleChunk = (reason: string, error?: unknown): void => {
  if (typeof window === 'undefined') {
    return
  }

  const alreadyRetried = window.sessionStorage.getItem(CHUNK_RECOVERY_KEY) === '1'
  if (alreadyRetried) {
    console.error('[ASSETS] Chunk recovery already attempted once in this session.', { reason, error })
    return
  }

  window.sessionStorage.setItem(CHUNK_RECOVERY_KEY, '1')

  const currentUrl = new URL(window.location.href)
  currentUrl.searchParams.set('v', Date.now().toString())
  console.warn('[ASSETS] Recovering from stale frontend chunks by forcing a fresh page load.', { reason })
  window.location.replace(currentUrl.toString())
}

// Normalize the current path to handle trailing slash issues
if (typeof window !== 'undefined') {
  const currentPath = window.location.pathname
  const routerBase = '/all-trails/'
  const routerBaseNoSlash = routerBase.replace(/\/$/, '')

  // If we're at /all-trails (without trailing slash), ensure we're at the base path
  if (currentPath === routerBaseNoSlash && !currentPath.endsWith('/')) {
    // Replace state to add trailing slash
    const newPath = routerBaseNoSlash + '/'
    window.history.replaceState(null, '', newPath)
  }
}

// Initialize CSRF token from window object (injected by Frappe)
if (typeof window !== 'undefined') {
  // SECURITY: Validate CSRF token is available
  if (!(window as any).csrf_token) {
    console.warn('[SECURITY] CSRF token is not available. Frappe may not have injected it properly.')
  } else {
    // Set up axios defaults for CSRF token
    axios.defaults.headers.common['X-Frappe-CSRF-Token'] = (window as any).csrf_token
  }

  // Official Vite recovery hook for stale-deployment chunk mismatches.
  window.addEventListener('vite:preloadError', (event: Event) => {
    event.preventDefault()
    const viteEvent = event as Event & { payload?: unknown }
    recoverFromStaleChunk('vite:preloadError', viteEvent.payload)
  })

  // Guard for browsers/environments where preloadError is not emitted.
  window.addEventListener('unhandledrejection', (event: PromiseRejectionEvent) => {
    if (!isDynamicImportFetchError(event.reason)) {
      return
    }

    event.preventDefault()
    recoverFromStaleChunk('unhandledrejection:dynamic-import', event.reason)
  })
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Listen for session expiry events from API interceptor
if (typeof window !== 'undefined') {
  const handleSessionExpired = () => {
    console.warn('[SECURITY] Session expired event received. Triggering re-authentication.')
    const authStore = useAuthStore()
    authStore.handleSessionExpiry()
    // Redirect to login if on a protected route
    if (router.currentRoute.value.meta?.requiresAuth) {
      const redirectTarget = `${window.location.pathname}${window.location.search}${window.location.hash}`
      window.location.href = '/app/login?redirect-to=' + encodeURIComponent(redirectTarget)
    }
  }

  const handlePermissionDenied = () => {
    console.warn('[SECURITY] Permission denied event received.')
    // Could show a toast notification here
  }

  window.addEventListener('session-expired', handleSessionExpired)
  window.addEventListener('permission-denied', handlePermissionDenied)
}

// Ensure router is ready before mounting
router.isReady().then(() => {
  if (typeof window !== 'undefined') {
    window.sessionStorage.removeItem(CHUNK_RECOVERY_KEY)
  }

  app.mount('#app')
}).catch((err) => {
  console.error('Router initialization error:', err)
  // Mount anyway to show error
  app.mount('#app')
})
