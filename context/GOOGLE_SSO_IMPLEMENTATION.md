# Google SSO (OAuth 2.0) - Frappe Built-in Implementation
**Status:** Simplified Specification Using Frappe Core
**Priority:** Pre-Phase 0 (foundational for user acquisition)
**Duration:** 4-5 hours total
**Complexity:** Low (leverages Frappe's native OAuth2)

---

## Overview

Google SSO using Frappe's built-in OAuth2 integration removes signup friction and drives 40-60% higher conversion. This guide uses Frappe's native social login instead of custom code.

### Why This Matters
- **Signup friction:** Traditional form = 30% drop-off. SSO = 5% drop-off
- **Time to first booking:** Google SSO users book 2x faster
- **Trust signal:** "Continue with Google" = safe, credible, frictionless
- **Data pre-fill:** Profile picture, name, email = one-click account creation

---

## Part 1: Google Cloud Setup (Manual - 30 min)

### 1.1 Create Google Cloud Project

**Steps (do once, outside code):**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" → "New Project"
3. Name: "All Trails"
4. Wait for creation (~1 min)

### 1.2 Enable Required APIs

1. Search for **"Google+ API"** → Enable
2. Search for **"OAuth consent screen"** → Configure:
   - User type: External
   - App name: All Trails
   - User support email: your-email@example.com
   - Developer contact: your-email@example.com
   - Scopes: `email`, `profile` (default)

### 1.3 Create OAuth 2.0 Credentials

1. Go to **Credentials** → **Create Credentials** → **OAuth Client ID**
2. Application type: **Web application**
3. Add Authorized redirect URIs:
   ```
   https://your-domain.com/api/method/frappe.integrations.oauth2_logins.login_via_google
   http://localhost:8000/api/method/frappe.integrations.oauth2_logins.login_via_google
   ```
4. Copy and save:
   - **Client ID** (long string ending in .apps.googleusercontent.com)
   - **Client Secret** (hidden until you click show)

**✅ Keep these credentials safe—you'll need them next.**

---

## Part 2: Frappe Site Configuration (20 min)

### 2.1 Add Google OAuth to Site Settings

**Login to your Frappe admin:**

1. Go to: **Settings** → **System Settings** (or search "System Settings")
2. Scroll to **Social Login Keys**
3. Click **Add Row** and fill:
   - **Provider:** `google`
   - **Client ID:** (paste from Google Cloud)
   - **Client Secret:** (paste from Google Cloud)
4. **Save**

**✅ Frappe now handles the entire OAuth flow.**

---

## Part 3: Frontend Signup Page (2 hours)

### 3.1 Create Signup Page with Google Button

**File:** `frontend/src/pages/Signup.vue` (NEW)

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const step = ref<'form' | 'complete'>('form')
const formData = ref({
  email: '',
  firstName: '',
  lastName: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})
const isLoading = ref(false)
const error = ref<string | null>(null)

onMounted(() => {
  // If already authenticated, redirect
  if (authStore.isAuthenticated) {
    router.push('/all-trails/')
  }
})

const validateForm = (): boolean => {
  error.value = null

  if (!formData.value.email || !formData.value.firstName) {
    error.value = 'Email and first name are required'
    return false
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(formData.value.email)) {
    error.value = 'Please enter a valid email address'
    return false
  }

  if (formData.value.password && formData.value.password.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return false
  }

  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return false
  }

  if (!formData.value.agreeTerms) {
    error.value = 'You must agree to the terms of service'
    return false
  }

  return true
}

const handleSignup = async () => {
  if (!validateForm()) return

  isLoading.value = true
  error.value = null

  try {
    const response = await axios.post(
      '/api/method/all_trails.api.signup_user',
      {
        email: formData.value.email,
        first_name: formData.value.firstName,
        last_name: formData.value.lastName,
        password: formData.value.password
      },
      {
        headers: {
          'X-Frappe-CSRF-Token': (window as any).csrf_token || ''
        }
      }
    )

    if (response.data?.message?.success) {
      step.value = 'complete'
      setTimeout(() => {
        router.push('/all-trails/')
      }, 2000)
    } else {
      error.value = response.data?.message?.error || 'Signup failed'
    }
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Signup failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleGoogleSignup = () => {
  // Redirect to Frappe's Google OAuth endpoint
  // Frappe will handle the entire OAuth flow and redirect back
  window.location.href = '/api/method/frappe.integrations.oauth2_logins.login_via_google'
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gradient-to-br from-emerald-600 to-teal-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
        </div>
        <h1 class="text-3xl font-black bg-gradient-to-r from-emerald-900 to-teal-800 bg-clip-text text-transparent mb-2">
          All Trails
        </h1>
        <p class="text-gray-600 font-medium">Create your account and start exploring</p>
      </div>

      <!-- Signup Card -->
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
        <!-- Success Message -->
        <div v-if="step === 'complete'" class="text-center py-8">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-2">Account Created!</h2>
          <p class="text-gray-600 mb-4">Welcome to All Trails. Redirecting...</p>
        </div>

        <!-- Form -->
        <div v-else>
          <!-- Error Message -->
          <div v-if="error" class="mb-6 p-4 bg-red-50 border-2 border-red-200 rounded-xl">
            <p class="text-sm font-medium text-red-800">{{ error }}</p>
          </div>

          <!-- Google Signup Button -->
          <button
            @click="handleGoogleSignup"
            class="w-full py-3.5 px-4 bg-white border-2 border-gray-200 rounded-xl hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center justify-center gap-3 font-medium text-gray-700 shadow-sm hover:shadow-md mb-6"
          >
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            <span>Sign up with Google</span>
          </button>

          <div class="my-6 flex items-center">
            <div class="flex-1 border-t border-gray-200"></div>
            <span class="px-4 text-sm text-gray-500 font-medium">or</span>
            <div class="flex-1 border-t border-gray-200"></div>
          </div>

          <!-- Email Form -->
          <form @submit.prevent="handleSignup" class="space-y-4">
            <!-- Email -->
            <div>
              <label for="email" class="block text-sm font-bold text-gray-700 mb-2">Email</label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
                placeholder="you@example.com"
              />
            </div>

            <!-- First Name -->
            <div>
              <label for="firstName" class="block text-sm font-bold text-gray-700 mb-2">First Name</label>
              <input
                id="firstName"
                v-model="formData.firstName"
                type="text"
                required
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
                placeholder="Jane"
              />
            </div>

            <!-- Last Name -->
            <div>
              <label for="lastName" class="block text-sm font-bold text-gray-700 mb-2">Last Name</label>
              <input
                id="lastName"
                v-model="formData.lastName"
                type="text"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
                placeholder="Doe"
              />
            </div>

            <!-- Password -->
            <div>
              <label for="password" class="block text-sm font-bold text-gray-700 mb-2">Password</label>
              <input
                id="password"
                v-model="formData.password"
                type="password"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
                placeholder="••••••••"
              />
              <p class="text-xs text-gray-500 mt-1">Min 8 characters</p>
            </div>

            <!-- Confirm Password -->
            <div>
              <label for="confirm" class="block text-sm font-bold text-gray-700 mb-2">Confirm Password</label>
              <input
                id="confirm"
                v-model="formData.confirmPassword"
                type="password"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all outline-none"
                placeholder="••••••••"
              />
            </div>

            <!-- Terms -->
            <div class="flex items-start">
              <input
                id="terms"
                v-model="formData.agreeTerms"
                type="checkbox"
                class="mt-1 w-4 h-4 text-emerald-600 border-gray-300 rounded"
              />
              <label for="terms" class="ml-3 text-sm text-gray-600">
                I agree to the <a href="/terms" class="text-emerald-600 hover:underline">Terms of Service</a> and
                <a href="/privacy" class="text-emerald-600 hover:underline">Privacy Policy</a>
              </label>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="isLoading"
              class="w-full py-3.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isLoading ? 'Creating account...' : 'Sign Up' }}
            </button>
          </form>

          <!-- Login Link -->
          <div class="mt-6 text-center">
            <p class="text-sm text-gray-600">
              Already have an account?
              <RouterLink to="/login" class="font-medium text-emerald-600 hover:text-emerald-700">
                Sign in
              </RouterLink>
            </p>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <p class="mt-8 text-center text-xs text-gray-500">
        By signing up, you agree to our Terms of Service and Privacy Policy
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Additional styles if needed */
</style>
```

**Key points:**
- Google button redirects to: `/api/method/frappe.integrations.oauth2_logins.login_via_google`
- Frappe handles entire OAuth flow automatically
- After Google login, user is redirected back and auto-logged in
- Traditional email/password signup still available as fallback

---

## Part 4: Backend Signup API (1 hour)

### 4.1 Add Signup Endpoint

**File:** `all_trails/api.py` (ADD THIS FUNCTION)

```python
@frappe.whitelist(allow_guest=True)
def signup_user(email, first_name, last_name=None, password=None):
    """
    Register a new user (for traditional signup, not Google SSO)

    Args:
        email: User email
        first_name: First name
        last_name: Last name (optional)
        password: Password (optional for SSO users)

    Returns:
        dict with success status or error
    """

    # Validate input
    if not email or not first_name:
        return {
            'success': False,
            'error': 'Email and first name are required'
        }

    # Check if user already exists
    if frappe.get_value('User', email):
        return {
            'success': False,
            'error': 'Email already registered. Please login or use Google SSO.'
        }

    try:
        # Create user
        user = frappe.new_doc('User')
        user.email = email
        user.first_name = first_name
        user.last_name = last_name or ''
        user.username = email
        user.enabled = True
        user.send_welcome_email = True
        user.user_type = 'Website User'

        # Set password if provided
        if password and len(password) >= 8:
            user.new_password = password
        else:
            # Generate random password if not provided
            user.new_password = frappe.generate_hash(length=32)

        user.insert(ignore_permissions=True)

        # Log signup
        frappe.logger().info(f"New user signup: {email}")

        # Auto-login if possible
        frappe.login_manager.user = email
        frappe.login_manager.post_login()

        return {
            'success': True,
            'message': 'Account created successfully!'
        }

    except frappe.ValidationError as e:
        return {
            'success': False,
            'error': f'Validation error: {str(e)}'
        }
    except Exception as e:
        frappe.logger().error(f"Signup error: {str(e)}")
        return {
            'success': False,
            'error': 'Failed to create account. Please try again.'
        }
```

---

## Part 5: Router Configuration (10 min)

### 5.1 Add Signup Route

**File:** `frontend/src/router/index.ts` (ADD)

```typescript
{
  path: '/signup',
  name: 'Signup',
  component: () => import('../pages/Signup.vue'),
  meta: {
    requiresAuth: false,
    title: 'Sign Up'
  }
}
```

---

## Part 6: Update Login Page (10 min)

### 6.1 Add Google Button to Login

**File:** `frontend/src/pages/Login.vue` (ADD before email form)

```vue
<!-- Google Login Button -->
<button
  @click="handleGoogleLogin"
  class="w-full py-3.5 px-4 bg-white border-2 border-gray-200 rounded-xl hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center justify-center gap-3 font-medium text-gray-700 shadow-sm hover:shadow-md mb-6"
>
  <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
  </svg>
  <span>Sign in with Google</span>
</button>

<div class="my-4 flex items-center">
  <div class="flex-1 border-t border-gray-200"></div>
  <span class="px-4 text-sm text-gray-500 font-medium">or</span>
  <div class="flex-1 border-t border-gray-200"></div>
</div>
```

Add method in script:

```typescript
const handleGoogleLogin = () => {
  window.location.href = '/api/method/frappe.integrations.oauth2_logins.login_via_google'
}
```

---

## Implementation Checklist

### Step 1: Google Cloud Setup (30 min)
- [ ] Google Cloud project created
- [ ] Google+ API enabled
- [ ] OAuth consent screen configured
- [ ] OAuth 2.0 credentials created
- [ ] Client ID and Secret copied

### Step 2: Frappe Configuration (20 min)
- [ ] Login to Frappe admin
- [ ] Go to System Settings
- [ ] Add Google OAuth credentials in Social Login Keys
- [ ] Save and test

### Step 3: Frontend Implementation (2 hours)
- [ ] Create `frontend/src/pages/Signup.vue`
- [ ] Add signup route to router
- [ ] Update Login.vue with Google button
- [ ] Test both pages load without errors

### Step 4: Backend API (1 hour)
- [ ] Add `signup_user()` to `all_trails/api.py`
- [ ] Test traditional signup works
- [ ] Verify auto-login after signup

### Step 5: Testing & Launch (1 hour)
- [ ] Test Google signup flow (end-to-end)
- [ ] Test Google login flow
- [ ] Test traditional email/password signup
- [ ] Verify user profile auto-created
- [ ] Mobile responsive testing

---

## How It Works (Diagram)

```
User clicks "Sign in with Google"
         ↓
Browser → /api/method/frappe.integrations.oauth2_logins.login_via_google
         ↓
Frappe redirects to Google OAuth consent screen
         ↓
User authorizes
         ↓
Google redirects back with auth code
         ↓
Frappe backend exchanges code for tokens
         ↓
Frappe creates/finds user by email
         ↓
Session created, redirect to /all-trails/
         ↓
User logged in ✅
```

---

## Important Notes

### What Frappe Handles Automatically
- ✅ OAuth token exchange
- ✅ CSRF protection (state parameter)
- ✅ User creation from Google email
- ✅ Session management
- ✅ Secure credential storage

### What You Need to Add
- 📄 Signup page UI
- 📄 Login page Google button
- 📄 Backend signup endpoint (traditional form)
- 🧪 Tests

### Security Built-in
- HTTPS-only cookies
- CSRF tokens validated
- Secrets encrypted in database
- No secrets logged
- Google API verified

---

## Testing

### Manual Testing Checklist
- [ ] Click Google button on login page → redirects to Google
- [ ] Authorize → redirected back and logged in
- [ ] Check user created with correct email
- [ ] Test signup with email/password
- [ ] Test login with email/password
- [ ] Test on mobile (375px width)

### Automated Tests
```python
# Backend test
def test_signup_user():
    """Test signup endpoint"""
    result = frappe.call('all_trails.api.signup_user', {
        'email': 'test@example.com',
        'first_name': 'Test',
        'password': 'TestPassword123'
    })
    assert result['success'] == True
```

---

## Success Metrics

After launch, track:
- **Google signup adoption:** >60% of new signups
- **Traditional signup fallback:** <40% of signups
- **Time to booking:** SSO users 2x faster
- **Profile completion:** >95% (email pre-filled)
- **Abandonment rate:** <10%

---

## Next Steps (After Launch)

- [ ] Monitor signup analytics
- [ ] Add "Sign in with Apple" (iOS)
- [ ] Add email verification (optional)
- [ ] Add password reset flow
- [ ] Phone number OAuth (future)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Client ID not found" | Check System Settings → Social Login Keys |
| "Invalid redirect URI" | Verify URI in Google Cloud matches exactly |
| User not auto-created | Check user_type in Frappe, should be "Website User" |
| Redirect loop | Clear browser cookies and try again |
| "Not whitelisted" error | Ensure endpoint has `@frappe.whitelist()` |
