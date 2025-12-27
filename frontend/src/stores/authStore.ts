import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '../types/index';
import { apiService } from '../services/api';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const isCheckingAuth = ref(false);

  const isAuthenticated = computed(() => !!user.value);

  /**
   * Check current authentication status
   */
  const checkAuthentication = async () => {
    isCheckingAuth.value = true;
    isLoading.value = true;
    error.value = null;

    try {
      // SECURITY: Validate CSRF token exists before checking auth
      if (!(window as any).csrf_token) {
        console.warn('[SECURITY] CSRF token not available during authentication check');
      }

      // Get current user info from API service
      const currentUser = await apiService.getCurrentUser();

      if (currentUser) {
        // User is authenticated
        user.value = currentUser;
        isLoading.value = false;
        isCheckingAuth.value = false;
        return true;
      } else {
        // User is not authenticated (Guest or no session)
        user.value = null;
        isLoading.value = false;
        isCheckingAuth.value = false;
        error.value = null;
        return false;
      }
    } catch (err) {
      // Don't redirect on error, just set state to unauthenticated
      // This allows the app to show appropriate UI
      user.value = null;
      error.value = err instanceof Error ? err.message : 'Authentication failed';
      isLoading.value = false;
      isCheckingAuth.value = false;
      return false;
    }
  };

  /**
   * Initialize authentication (alias for checkAuthentication for backward compatibility)
   */
  const initializeAuth = async () => {
    return await checkAuthentication();
  };

  /**
   * Handle session expiry (called when 401 error is detected)
   */
  const handleSessionExpiry = () => {
    console.warn('[SECURITY] Session has expired. Clearing authentication state.');
    user.value = null;
    error.value = 'Your session has expired. Please log in again.';
    isLoading.value = false;
    isCheckingAuth.value = false;
  };

  /**
   * Logout user
   */
  const logout = async () => {
    isLoading.value = true;
    
    try {
      // Call Frappe's logout API endpoint to properly invalidate the session
      await fetch('/api/method/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Frappe-CSRF-Token': (window as any).csrf_token || ''
        }
      });
    } catch (error) {
      // Continue with logout even if API call fails
      console.warn('[AuthStore] Logout API call failed, proceeding with redirect:', error);
    } finally {
      // Clear state regardless of API call result
      user.value = null;
      isLoading.value = false;
      error.value = null;
      
      // Redirect to home page after logout
      window.location.href = '/all-trails/';
    }
  };

  return {
    user,
    isLoading,
    error,
    isCheckingAuth,
    isAuthenticated,
    checkAuthentication,
    initializeAuth,
    handleSessionExpiry,
    logout,
  };
});

