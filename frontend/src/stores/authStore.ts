import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '../types/index';
import { apiService } from '../services/api';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => !!user.value);

  const initializeAuth = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      // Check if Frappe session exists
      if (typeof window !== 'undefined' && (window as any).frappe?.session?.user) {
        user.value = {
          name: (window as any).frappe.session.user,
          email: (window as any).frappe.session.user,
          full_name: (window as any).frappe.session.user_fullname || (window as any).frappe.session.user,
        };
      } else {
        // Fallback to mock user for development
        user.value = await apiService.getCurrentUser();
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to initialize auth';
      console.error('Auth initialization error:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    user.value = null;
    // Redirect to Frappe logout
    if (typeof window !== 'undefined') {
      window.location.href = '/app/logout';
    }
  };

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    initializeAuth,
    logout,
  };
});

