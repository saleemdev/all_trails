<template>
  <section class="dense-ui page-shell relative isolate grid min-h-dvh overflow-hidden px-4 py-4 sm:px-6 sm:py-5 lg:px-8">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute left-1/2 top-[-12rem] h-[26rem] w-[26rem] -translate-x-1/2 rounded-full blur-3xl" style="background: radial-gradient(circle, rgba(149, 177, 165, 0.26) 0%, transparent 68%)"></div>
      <div class="absolute left-[-7rem] top-[28%] h-72 w-72 rounded-full blur-3xl" style="background: radial-gradient(circle, rgba(255, 255, 255, 0.5) 0%, transparent 74%)"></div>
      <div class="absolute bottom-[-9rem] right-[-8rem] h-80 w-80 rounded-full blur-3xl" style="background: radial-gradient(circle, rgba(211, 192, 169, 0.22) 0%, transparent 72%)"></div>
      <div class="absolute inset-0" style="background: linear-gradient(180deg, rgba(248, 251, 248, 0.2) 0%, rgba(238, 243, 239, 0.04) 100%)"></div>
    </div>

    <div class="relative z-10 mx-auto grid w-full max-w-[25.5rem] place-items-center self-center">
      <div class="w-full">
        <div class="mb-3 text-center sm:mb-4">
          <div class="surface-control inline-flex items-center gap-2.5 rounded-[0.95rem] px-3 py-1.5 shadow-[0_12px_26px_rgba(17,31,26,0.08)] backdrop-blur-xl">
            <div class="brand-mark h-8 w-8">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <div class="text-left">
              <p class="tone-kicker text-[9px]">Trail account</p>
              <h1 class="brand-wordmark text-[1.45rem] font-medium leading-none tracking-[-0.02em]">Stepup Adventures</h1>
            </div>
          </div>
        </div>

        <div class="glass-panel-strong rounded-[1.2rem] border border-[color:var(--color-border-soft)] p-4 shadow-[0_26px_76px_rgba(17,31,26,0.14)] sm:p-5">
          <div class="mb-4 border-b border-[color:var(--color-border-soft)] pb-3">
            <p class="tone-kicker text-[10px]">Welcome back</p>
            <h2 class="tone-heading mt-1.5 text-[clamp(1.25rem,3.3vw,1.65rem)] font-medium leading-tight tracking-[-0.02em]">Sign in to continue</h2>
            <p class="tone-body mt-1.5 mb-0 text-[13px] leading-5">
              Pick up where your next trail left off.
            </p>
          </div>

          <div v-if="error" class="surface-danger-subtle mb-4 rounded-[0.9rem] px-3.5 py-2.5">
            <div class="flex items-center gap-1.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p class="mb-0 text-[13px] font-medium">{{ error }}</p>
            </div>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-3.5 sm:space-y-4">
            <div>
              <label for="login_email" class="tone-kicker mb-1.5 block text-[10px]">
                Email or Username
              </label>
              <input
                id="login_email"
                v-model="email"
                name="usr"
                type="text"
                autocomplete="username"
                autocapitalize="none"
                spellcheck="false"
                required
                class="soft-input h-10 w-full px-3.5 text-[14px] leading-[1.2]"
                placeholder="jane@example.com"
              />
            </div>

            <div>
              <label for="login_password" class="tone-kicker mb-1.5 block text-[10px]">
                Password
              </label>
              <div class="relative">
                <input
                  id="login_password"
                  v-model="password"
                  name="pwd"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  required
                  class="soft-input h-10 w-full px-3.5 pr-10 text-[14px] leading-[1.2]"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="tone-muted absolute inset-y-0 right-0 z-10 flex items-center px-3 transition-colors hover:text-[color:var(--color-text-primary)]"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                >
                  <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="flex flex-col gap-2.5 text-[13px] sm:flex-row sm:items-center sm:justify-between">
              <label class="tone-body flex items-center text-[13px]">
                <input
                  v-model="rememberMe"
                  type="checkbox"
                  class="h-4 w-4 rounded border-[color:var(--color-border-soft)]"
                  style="accent-color: var(--color-primary)"
                />
                <span class="ml-2">Remember me</span>
              </label>
              <a href="/app/forgot-password" class="brand-link text-sm">
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              :disabled="isLoading"
              class="brand-button h-10 w-full px-4 py-0 text-[14px] disabled:opacity-60 disabled:transform-none"
            >
              <svg v-if="isLoading" class="h-4 w-4 animate-spin text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span v-if="!isLoading">Sign in</span>
              <span v-else>Signing in...</span>
            </button>
          </form>

          <div v-if="socialProviders.length > 0" class="my-4 flex items-center">
            <div class="flex-1 border-t border-[color:var(--color-border-soft)]"></div>
            <span class="tone-muted px-3 text-[10px] font-medium uppercase tracking-[0.12em]">or continue with</span>
            <div class="flex-1 border-t border-[color:var(--color-border-soft)]"></div>
          </div>

          <div v-if="socialProviders.length > 0" class="space-y-2.5">
            <button
              v-for="provider in socialProviders"
              :key="provider.name"
              @click="handleSocialLogin(provider)"
              class="social-button h-10 w-full px-3.5 py-0 text-[14px]"
            >
              <img
                v-if="provider.icon"
                :src="provider.icon"
                :alt="provider.provider_name"
                class="h-4 w-4"
              />
              <svg
                v-else-if="provider.provider_name === 'Google' || provider.provider_name === 'Gmail'"
                class="h-4 w-4"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
              </svg>
              <span>Continue with {{ provider.provider_name }}</span>
            </button>
          </div>

          <div class="mt-4 border-t border-[color:var(--color-border-soft)] pt-3 text-center">
            <p class="tone-body mb-0 text-[13px]">
              Don't have an account?
              <RouterLink to="/register" class="brand-link">Register</RouterLink>
            </p>
          </div>
        </div>

        <p class="tone-muted mt-3.5 text-center text-[10px] leading-4 sm:mt-4">
          By signing in, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import axios from 'axios'
import { isSafeAuthUrl, sanitizeAppRedirectPath } from '../utils/navigation'

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
  if (authStore.isAuthenticated) {
    redirectAfterLogin()
    return
  }

  await fetchSocialProviders()
})

const fetchSocialProviders = async () => {
  try {
    const response = await axios.get('/api/method/all_trails.api.get_social_login_providers', {
      headers: {
        'X-Frappe-CSRF-Token': (window as any).csrf_token || ''
      }
    })

    if (Array.isArray(response.data?.message?.providers)) {
      socialProviders.value = response.data.message.providers.filter((provider: any) => isSafeAuthUrl(provider?.auth_url))
    }
  } catch (err) {
    console.warn('Failed to fetch social providers:', err)
    socialProviders.value = []
  }
}

const handleLogin = async () => {
  isLoading.value = true
  error.value = null

  try {
    const formData = new URLSearchParams()
    formData.append('usr', email.value)
    formData.append('pwd', password.value)

    const response = await axios.post(
      '/api/method/login',
      formData.toString(),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-Frappe-CSRF-Token': (window as any).csrf_token || ''
        },
        withCredentials: true
      }
    )

    const message = response.data?.message
    if (message === 'Logged In' || message === 'No App') {
      try {
        const authenticated = await authStore.checkAuthentication()
        if (authenticated) {
          redirectAfterLogin()
        } else {
          setTimeout(async () => {
            await authStore.checkAuthentication()
            redirectAfterLogin()
          }, 200)
        }
      } catch (err) {
        console.error('Error checking auth after login:', err)
        setTimeout(() => {
          redirectAfterLogin()
        }, 200)
      }
    } else if (message && typeof message === 'object' && message.full_name) {
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

    if (err.response?.data) {
      let errorMsg = err.response.data.message

      if (err.response.data._server_messages) {
        try {
          const messages = JSON.parse(err.response.data._server_messages)
          if (Array.isArray(messages) && messages.length > 0) {
            errorMsg = messages[0].message || messages[0]
          }
        } catch {
          errorMsg = err.response.data._server_messages
        }
      }

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

const handleSocialLogin = (provider: { auth_url: string }) => {
  if (!isSafeAuthUrl(provider.auth_url)) {
    error.value = 'Invalid social login URL.'
    return
  }

  const redirectTo = sanitizeAppRedirectPath(route.query['redirect-to'], '/')
  const target = provider.auth_url.startsWith('/')
    ? new URL(provider.auth_url, window.location.origin)
    : new URL(provider.auth_url)

  target.searchParams.set('redirect-to', `/all-trails${redirectTo === '/' ? '/' : redirectTo}`)
  window.location.href = target.toString()
}

const redirectAfterLogin = () => {
  const redirectTo = sanitizeAppRedirectPath(route.query['redirect-to'], '/')
  router.push(redirectTo)
}
</script>

<style scoped>
/* Page styling comes from global design tokens */
</style>
