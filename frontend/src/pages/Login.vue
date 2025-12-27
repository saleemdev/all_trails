<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo and Title -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gradient-to-br from-emerald-600 to-teal-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
        </div>
        <h1 class="text-3xl font-black bg-gradient-to-r from-emerald-900 to-teal-800 bg-clip-text text-transparent mb-2">
          Step Up Adventures
        </h1>
        <p class="text-gray-600 font-medium">Sign in to your account</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
        <!-- Error Message -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border-2 border-red-200 rounded-xl">
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-sm font-medium text-red-800">{{ error }}</p>
          </div>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Email/Username Input -->
          <div>
            <label for="login_email" class="block text-sm font-bold text-gray-700 mb-2">
              Email or Username
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <input
                id="login_email"
                v-model="email"
                type="text"
                autocomplete="username"
                required
                class="w-full pl-12 pr-4 py-3.5 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none text-gray-900 placeholder-gray-400"
                placeholder="jane@example.com"
              />
            </div>
          </div>

          <!-- Password Input -->
          <div>
            <label for="login_password" class="block text-sm font-bold text-gray-700 mb-2">
              Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                id="login_password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                required
                class="w-full pl-12 pr-12 py-3.5 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none text-gray-900 placeholder-gray-400"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
              >
                <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Forgot Password Link -->
          <div class="flex items-center justify-between">
            <label class="flex items-center">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500"
              />
              <span class="ml-2 text-sm text-gray-600">Remember me</span>
            </label>
            <a
              href="/app/forgot-password"
              class="text-sm font-medium text-emerald-600 hover:text-emerald-700 transition-colors"
            >
              Forgot password?
            </a>
          </div>

          <!-- Login Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg hover:shadow-xl transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
          >
            <svg v-if="isLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span v-if="!isLoading">Sign in</span>
            <span v-else>Signing in...</span>
          </button>
        </form>

        <!-- Divider -->
        <div v-if="socialProviders.length > 0" class="my-6 flex items-center">
          <div class="flex-1 border-t border-gray-200"></div>
          <span class="px-4 text-sm text-gray-500 font-medium">or continue with</span>
          <div class="flex-1 border-t border-gray-200"></div>
        </div>

        <!-- Social Login Buttons -->
        <div v-if="socialProviders.length > 0" class="space-y-3">
          <!-- Gmail/Google SSO -->
          <button
            v-for="provider in socialProviders"
            :key="provider.name"
            @click="handleSocialLogin(provider)"
            class="w-full py-3.5 px-4 bg-white border-2 border-gray-200 rounded-xl hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center justify-center gap-3 font-medium text-gray-700 shadow-sm hover:shadow-md"
          >
            <img
              v-if="provider.icon"
              :src="provider.icon"
              :alt="provider.provider_name"
              class="h-5 w-5"
            />
            <svg
              v-else-if="provider.provider_name === 'Google' || provider.provider_name === 'Gmail'"
              class="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
            </svg>
            <span>Continue with {{ provider.provider_name }}</span>
          </button>
        </div>

        <!-- Sign Up Link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Don't have an account?
            <RouterLink to="/signup" class="font-medium text-emerald-600 hover:text-emerald-700 transition-colors">
              Sign up
            </RouterLink>
          </p>
        </div>
      </div>

      <!-- Footer -->
      <p class="mt-8 text-center text-xs text-gray-500">
        By signing in, you agree to our Terms of Service and Privacy Policy
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const isLoading = ref(false)
const error = ref<string | null>(null)
const socialProviders = ref<Array<{
  name: string
  provider_name: string
  auth_url: string
  icon?: string
}>>([])

onMounted(async () => {
  // If already authenticated, redirect
  if (authStore.isAuthenticated) {
    redirectAfterLogin()
    return
  }

  // Fetch social login providers
  await fetchSocialProviders()
})

const fetchSocialProviders = async () => {
  try {
    // Get social login providers from our API
    const response = await axios.get('/api/method/all_trails.api.get_social_login_providers', {
      headers: {
        'X-Frappe-CSRF-Token': (window as any).csrf_token || ''
      }
    })

    if (response.data?.message?.providers) {
      socialProviders.value = response.data.message.providers
    }
  } catch (err) {
    console.warn('Failed to fetch social providers:', err)
    // Add a placeholder Gmail SSO button even if API fails (incomplete as requested)
    socialProviders.value = [
      {
        name: 'google',
        provider_name: 'Gmail',
        auth_url: '#',
        icon: undefined
      }
    ]
  }
}

const handleLogin = async () => {
  isLoading.value = true
  error.value = null

  try {
    // Frappe login expects form-encoded data, not JSON
    // Use URLSearchParams for proper encoding
    const formData = new URLSearchParams()
    formData.append('usr', email.value)
    formData.append('pwd', password.value)

    // Use direct axios call (not the apiService instance) to avoid interceptors interfering
    const response = await axios.post(
      '/api/method/login',
      formData.toString(),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-Frappe-CSRF-Token': (window as any).csrf_token || ''
        },
        withCredentials: true // Critical for cookie-based session management
      }
    )

    // Frappe login returns "Logged In" or "No App" on success
    const message = response.data?.message
    if (message === 'Logged In' || message === 'No App') {
      // Login successful - immediately check authentication
      // Cookies should be set by the login response
      try {
        const authenticated = await authStore.checkAuthentication()
        if (authenticated) {
          redirectAfterLogin()
        } else {
          // If not authenticated yet, wait a bit for cookies to propagate
          setTimeout(async () => {
            await authStore.checkAuthentication()
            redirectAfterLogin()
          }, 200)
        }
      } catch (err) {
        console.error('Error checking auth after login:', err)
        // Even if check fails, try redirecting - cookies might be set
        setTimeout(() => {
          redirectAfterLogin()
        }, 200)
      }
    } else if (message && typeof message === 'object' && message.full_name) {
      // Sometimes returns user object directly - set user immediately
      authStore.user = {
        name: message.name || email.value,
        email: message.email || email.value,
        full_name: message.full_name || email.value,
        user_image: message.user_image || null
      }
      redirectAfterLogin()
    } else {
      error.value = 'Invalid email or password'
      isLoading.value = false
    }
  } catch (err: any) {
    console.error('Login error:', err)
    
    // Handle different error formats from Frappe
    if (err.response?.data) {
      let errorMsg = err.response.data.message
      
      // Check for _server_messages (Frappe's error format)
      if (err.response.data._server_messages) {
        try {
          const messages = JSON.parse(err.response.data._server_messages)
          if (Array.isArray(messages) && messages.length > 0) {
            errorMsg = messages[0].message || messages[0]
          }
        } catch {
          // If parsing fails, use the raw value
          errorMsg = err.response.data._server_messages
        }
      }
      
      // Check for exc (exception message)
      if (!errorMsg && err.response.data.exc) {
        errorMsg = err.response.data.exc
      }
      
      error.value = errorMsg || 'Invalid email or password. Please try again.'
    } else if (err.message) {
      error.value = err.message
    } else {
      error.value = 'Login failed. Please check your credentials and try again.'
    }
    isLoading.value = false
  }
}

const handleSocialLogin = (provider: any) => {
  // Get redirect URL
  const redirectTo = route.query['redirect-to'] as string || '/all-trails/'
  
  // Build auth URL with redirect
  const authUrl = provider.auth_url.includes('?')
    ? `${provider.auth_url}&redirect-to=${encodeURIComponent(redirectTo)}`
    : `${provider.auth_url}?redirect-to=${encodeURIComponent(redirectTo)}`
  
  // Redirect to OAuth provider
  window.location.href = authUrl
}

const redirectAfterLogin = () => {
  const redirectTo = route.query['redirect-to'] as string
  if (redirectTo) {
    // Decode and navigate to the redirect URL
    try {
      const decoded = decodeURIComponent(redirectTo)
      if (decoded.startsWith('/all-trails')) {
        router.push(decoded.replace('/all-trails', ''))
      } else {
        window.location.href = decoded
      }
    } catch {
      router.push('/')
    }
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>

