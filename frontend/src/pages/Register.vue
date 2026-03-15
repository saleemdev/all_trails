<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../services/api'

const router = useRouter()

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const confirmPassword = ref('')

const isSubmitting = ref(false)
const error = ref('')
const success = ref('')

const submitRegistration = async () => {
  error.value = ''
  success.value = ''

  if (!firstName.value.trim() || !email.value.trim() || !password.value) {
    error.value = 'First name, email, and password are required.'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Password must be at least 8 characters long.'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  isSubmitting.value = true
  try {
    const response = await apiService.registerMember({
      first_name: firstName.value.trim(),
      last_name: lastName.value.trim() || undefined,
      email: email.value.trim().toLowerCase(),
      phone: phone.value.trim() || undefined,
      password: password.value,
    })

    success.value = response.message || 'Registration completed successfully.'
    setTimeout(() => {
      router.push({ name: 'Login', query: { 'redirect-to': '/' } })
    }, 1000)
  } catch (reason: any) {
    error.value = reason?.message || 'Unable to complete registration.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <section class="dense-ui page-shell relative isolate grid min-h-dvh overflow-hidden px-4 py-4 sm:px-6 sm:py-5 lg:px-8">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute left-1/2 top-[-12rem] h-[26rem] w-[26rem] -translate-x-1/2 rounded-full blur-3xl" style="background: radial-gradient(circle, rgba(149, 177, 165, 0.26) 0%, transparent 68%)"></div>
      <div class="absolute left-[-7rem] top-[28%] h-72 w-72 rounded-full blur-3xl" style="background: radial-gradient(circle, rgba(255, 255, 255, 0.5) 0%, transparent 74%)"></div>
      <div class="absolute bottom-[-9rem] right-[-8rem] h-80 w-80 rounded-full blur-3xl" style="background: radial-gradient(circle, rgba(211, 192, 169, 0.22) 0%, transparent 72%)"></div>
    </div>

    <div class="relative z-10 mx-auto grid w-full max-w-[30rem] place-items-center self-center">
      <div class="glass-panel-strong rounded-[1.2rem] border border-[color:var(--color-border-soft)] p-4 shadow-[0_26px_76px_rgba(17,31,26,0.14)] sm:p-5 w-full">
        <div class="mb-4 border-b border-[color:var(--color-border-soft)] pb-3">
          <p class="tone-kicker text-[10px]">Join the community</p>
          <h1 class="tone-heading mt-1.5 text-[clamp(1.4rem,3.3vw,1.9rem)] font-medium leading-tight tracking-[-0.02em]">Create your trail account</h1>
          <p class="tone-body mt-1.5 mb-0 text-[13px] leading-5">This route uses `register_member` and sets up your `Trail Member` access.</p>
        </div>

        <form class="space-y-3.5" @submit.prevent="submitRegistration">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="tone-kicker mb-1.5 block text-[10px]">First name</label>
              <input v-model="firstName" class="soft-input h-10 w-full text-[14px]" type="text" required />
            </div>
            <div>
              <label class="tone-kicker mb-1.5 block text-[10px]">Last name</label>
              <input v-model="lastName" class="soft-input h-10 w-full text-[14px]" type="text" />
            </div>
          </div>

          <div>
            <label class="tone-kicker mb-1.5 block text-[10px]">Email</label>
            <input v-model="email" class="soft-input h-10 w-full text-[14px]" type="email" required />
          </div>

          <div>
            <label class="tone-kicker mb-1.5 block text-[10px]">Phone (optional)</label>
            <input v-model="phone" class="soft-input h-10 w-full text-[14px]" type="tel" placeholder="0712345678 or 254712345678" />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="tone-kicker mb-1.5 block text-[10px]">Password</label>
              <input v-model="password" class="soft-input h-10 w-full text-[14px]" type="password" minlength="8" required />
            </div>
            <div>
              <label class="tone-kicker mb-1.5 block text-[10px]">Confirm password</label>
              <input v-model="confirmPassword" class="soft-input h-10 w-full text-[14px]" type="password" minlength="8" required />
            </div>
          </div>

          <div v-if="error" class="surface-danger-subtle rounded-[0.9rem] px-3.5 py-2.5 text-[13px]">{{ error }}</div>
          <div v-if="success" class="surface-card-muted rounded-[0.9rem] px-3.5 py-2.5 text-[13px] text-green-800">{{ success }}</div>

          <button
            type="submit"
            :disabled="isSubmitting"
            class="brand-button h-10 w-full px-4 py-0 text-[14px] disabled:opacity-60 disabled:transform-none"
          >
            <span v-if="!isSubmitting">Create Account</span>
            <span v-else>Creating...</span>
          </button>
        </form>

        <div class="mt-4 border-t border-[color:var(--color-border-soft)] pt-3 text-center text-[13px] space-y-1">
          <p class="tone-body mb-0">
            Already have an account?
            <RouterLink to="/login" class="brand-link">Sign in</RouterLink>
          </p>
          <p class="tone-body mb-0">
            Prefer Frappe signup?
            <a href="/signup" class="brand-link">Use /signup</a>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
