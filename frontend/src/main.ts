import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { FrappeUI } from 'frappe-ui'
import './styles/globals.css'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/authStore'

// Normalize the current path to handle trailing slash issues
if (typeof window !== 'undefined') {
  const currentPath = window.location.pathname;
  const routerBase = '/all-trails/';
  const routerBaseNoSlash = routerBase.replace(/\/$/, '');
  
  // If we're at /all-trails (without trailing slash), ensure we're at the base path
  if (currentPath === routerBaseNoSlash && !currentPath.endsWith('/')) {
    // Replace state to add trailing slash
    const newPath = routerBaseNoSlash + '/';
    window.history.replaceState(null, '', newPath);
  }
}

// Initialize CSRF token from window object (injected by Frappe)
if (typeof window !== 'undefined') {
  // SECURITY: Validate CSRF token is available
  if (!(window as any).csrf_token) {
    console.error('[SECURITY] CSRF token is not available. Frappe may not have injected it properly.');
  } else {
    console.log('[SECURITY] CSRF token initialized successfully');
    // Set up axios defaults for CSRF token
    import('axios').then((axiosModule) => {
      axiosModule.default.defaults.headers.common['X-Frappe-CSRF-Token'] = (window as any).csrf_token;
    });
  }
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(FrappeUI)

// Listen for session expiry events from API interceptor
if (typeof window !== 'undefined') {
  const handleSessionExpired = () => {
    console.warn('[SECURITY] Session expired event received. Triggering re-authentication.');
    const authStore = useAuthStore();
    authStore.handleSessionExpiry();
    // Redirect to login if on a protected route
    if (router.currentRoute.value.meta?.requiresAuth) {
      window.location.href = '/app/login?redirect-to=' + encodeURIComponent(window.location.href);
    }
  };

  const handlePermissionDenied = () => {
    console.warn('[SECURITY] Permission denied event received.');
    // Could show a toast notification here
  };

  window.addEventListener('session-expired', handleSessionExpired);
  window.addEventListener('permission-denied', handlePermissionDenied);
}

// Ensure router is ready before mounting
router.isReady().then(() => {
  app.mount('#app')
}).catch((err) => {
  console.error('Router initialization error:', err)
  // Mount anyway to show error
  app.mount('#app')
})
