import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
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
    console.warn('[SECURITY] CSRF token is not available. Frappe may not have injected it properly.');
  } else {
    // Set up axios defaults for CSRF token
    axios.defaults.headers.common['X-Frappe-CSRF-Token'] = (window as any).csrf_token;
  }
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Listen for session expiry events from API interceptor
if (typeof window !== 'undefined') {
  const handleSessionExpired = () => {
    console.warn('[SECURITY] Session expired event received. Triggering re-authentication.');
    const authStore = useAuthStore();
    authStore.handleSessionExpiry();
    // Redirect to login if on a protected route
    if (router.currentRoute.value.meta?.requiresAuth) {
      const redirectTarget = `${window.location.pathname}${window.location.search}${window.location.hash}`;
      window.location.href = '/app/login?redirect-to=' + encodeURIComponent(redirectTarget);
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
