# AI Agent Implementation Prompt
**Copy this entire prompt into your AI chat to start implementation**

---

## Context & Objectives

You are implementing a complete hiker retention system for "All Trails" - a hiking platform built on Vue 3 + Frappe.

**Your Role:** Build Phase 0a (Google OAuth Backend) with zero hallucination, zero syntax errors, and production-ready code.

**Success Definition:** Code that passes linting, has no TypeErrors, follows existing patterns, and is immediately deployable.

---

## Codebase Context

**Stack:**
- Frontend: Vue 3 + TypeScript + Vite + Frappe UI
- Backend: Frappe (Python)
- State Management: Pinia
- Styling: Tailwind CSS

**Key Paths:**
- Frontend: `/Users/salim/frappe/my-bench/apps/all_trails/frontend/src/`
- Backend: `/Users/salim/frappe/my-bench/apps/all_trails/all_trails/`
- Build Output: `/all_trails/public/frontend/`
- API: Frappe RPC at `/api/method/all_trails/`

**Existing Patterns to Follow:**
- Auth store: `stores/authStore.ts` (Pinia store with checkAuthentication, logout)
- API service: `services/api.ts` (Frappe RPC wrapper)
- DocTypes: Located in `all_trails/doctype/*/` with `.py` and `.json` files
- Components: Vue 3 `<script setup>` with TypeScript
- Error handling: Try/catch with frappe.logger() for backend

**Important Files (Read First):**
- `frontend/src/pages/Login.vue` - Shows current auth flow (social login already hooked up)
- `frontend/src/stores/authStore.ts` - Auth state management
- `all_trails/api.py` - Shows `get_social_login_providers()` endpoint pattern
- `all_trails/doctype/` - Shows DocType structure

---

## Task: Implement Phase 0a (Google OAuth Backend)

**Duration:** 4 hours
**Status:** No other work until this phase completes and passes linting

### What Gets Built

```
Backend Files:
✅ all_trails/doctype/google_oauth_settings/
   ├── google_oauth_settings.py (Python class)
   └── google_oauth_settings.json (JSON schema)

✅ all_trails/services/google_oauth.py
   ├── get_google_login_url() - Generate OAuth URL
   ├── handle_google_callback() - Token exchange + user creation
   ├── exchange_code_for_tokens() - Google API call
   ├── fetch_google_userinfo() - Get user data
   ├── handle_user_login() - Find/create user
   └── sync_user_profile() - Update profile picture

✅ all_trails/tests/test_google_oauth.py (test cases)
```

### Implementation Specification

**See:** `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 1 (Backend Setup)

Copy the exact code from the spec. Do NOT improvise or simplify.

### Quality Requirements (CRITICAL)

**Linting:**
- [ ] All Python files pass `flake8` (PEP 8)
- [ ] All Python files pass `pylint` (if available)
- [ ] No unused imports
- [ ] No undefined variables
- [ ] All f-strings are properly formatted

**Type Safety:**
- [ ] All Python type hints correct (or use `# type: ignore` with comment)
- [ ] No `Any` unless unavoidable
- [ ] Error messages are clear and specific

**Security:**
- [ ] No plaintext secrets logged
- [ ] Passwords encrypted with frappe.utils.password
- [ ] CSRF tokens validated (state parameter)
- [ ] Redirect URIs validated

**Code Style:**
- [ ] Follow Frappe conventions (4-space indent, double quotes for strings)
- [ ] Comments explain WHY, not WHAT
- [ ] Error messages are user-friendly
- [ ] Logging uses frappe.logger()

**Testing:**
- [ ] Acceptance criteria from spec met
- [ ] No hardcoded test values in production code
- [ ] Test file structure matches pattern

### Pre-Implementation Checklist

Before you start, verify:

- [ ] User has created Google Cloud project
- [ ] OAuth credentials obtained (Client ID + Secret)
- [ ] Redirect URI configured in Google Console:
  ```
  https://your-domain.com/api/method/all_trails.services.google_oauth.handle_google_callback
  ```
- [ ] You have access to the codebase
- [ ] Frappe dev environment is running

### Detailed Implementation Steps

#### Step 1: Create Google OAuth Settings DocType

**File:** `all_trails/doctype/google_oauth_settings/google_oauth_settings.py`

From `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Copy the exact Python class code.

**Requirements:**
- [ ] Class inherits from `frappe.model.document.Document`
- [ ] `get_settings()` static method returns or creates settings
- [ ] `validate()` checks required fields when enabled
- [ ] No syntax errors (run `python -m py_compile`)

**After creating:**
```bash
# Run this to register the DocType
cd /path/to/bench
bench execute all_trails.doctype.google_oauth_settings.google_oauth_settings
```

#### Step 2: Create Google OAuth Settings DocType JSON Schema

**File:** `all_trails/doctype/google_oauth_settings/google_oauth_settings.json`

From `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Copy the exact JSON schema.

**Requirements:**
- [ ] Valid JSON (no trailing commas)
- [ ] Field types correct (Check, Password, Data, Section Break)
- [ ] is_single: 1 (this is a single DocType, not list)
- [ ] All field dependencies are valid

**Verify:**
```bash
# Validate JSON
python -m json.tool google_oauth_settings.json > /dev/null && echo "Valid JSON"
```

#### Step 3: Create Google OAuth Service Module

**File:** `all_trails/services/google_oauth.py`

From `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Copy the exact service code.

**Requirements:**
- [ ] All imports are available:
  ```python
  import requests  # pip install requests (likely already installed)
  import frappe
  from urllib.parse import quote
  from datetime import datetime, timedelta
  ```
- [ ] All functions are whitelisted correctly: `@frappe.whitelist(allow_guest=True)`
- [ ] CSRF protection: state parameter stored in `frappe.session.data`
- [ ] Error handling: All exceptions caught and logged
- [ ] No secrets logged (check frappe.logger() calls)
- [ ] Token exchange uses POST to Google
- [ ] User creation uses `frappe.new_doc()` and `.insert()`
- [ ] Profile picture download implemented (requests.get + FrappeFile)

**Lint Checks:**
```bash
# Check for PEP 8 violations
flake8 all_trails/services/google_oauth.py --max-line-length=100

# Check for undefined names
pylint all_trails/services/google_oauth.py
```

#### Step 4: Create Tests

**File:** `all_trails/tests/test_google_oauth.py`

From `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Create test file with test structure.

**Requirements:**
- [ ] Imports from unittest + unittest.mock
- [ ] Mock Google API responses (don't call real API)
- [ ] Test token exchange
- [ ] Test user creation
- [ ] Test profile sync
- [ ] Test error cases
- [ ] All tests are descriptive (docstrings)

**Test Patterns to Follow:**
```python
def test_get_google_login_url(self):
    """Test getting Google login URL"""
    # Arrange: Set up test data
    # Act: Call function
    # Assert: Verify result
```

---

## Acceptance Criteria (MUST PASS ALL)

### Functionality
- [ ] `get_google_login_url()` returns valid OAuth URL with state
- [ ] State parameter stored in session
- [ ] `handle_google_callback()` exchanges code for tokens
- [ ] User auto-created if email not found (when enabled)
- [ ] Existing users logged in by email match
- [ ] Profile picture downloaded from Google and stored
- [ ] All errors return user-friendly messages (no stack traces)
- [ ] No secrets logged (client_secret never in logs)

### Code Quality
- [ ] Zero flake8 violations
- [ ] Zero undefined variables
- [ ] All imports used
- [ ] No print() statements (use frappe.logger())
- [ ] Consistent indentation (4 spaces)
- [ ] Consistent quotes (double quotes)
- [ ] Type hints on all function signatures (or # type: ignore)

### Security
- [ ] CSRF protection via state parameter
- [ ] Redirect URI validated
- [ ] Email verification checked (`verified_email: true`)
- [ ] Secrets encrypted (frappe.utils.password)
- [ ] No hardcoded credentials
- [ ] Timeout on HTTP requests (timeout=10)
- [ ] HTTPs enforced in production

### Testing
- [ ] Test file exists with 5+ test cases
- [ ] Tests mock Google API (no real API calls)
- [ ] Error cases covered
- [ ] All tests pass: `python -m pytest all_trails/tests/test_google_oauth.py -v`

---

## How to Verify Your Work

### Step 1: Syntax Check
```bash
# Check Python syntax
python -m py_compile all_trails/doctype/google_oauth_settings/google_oauth_settings.py
python -m py_compile all_trails/services/google_oauth.py
python -m py_compile all_trails/tests/test_google_oauth.py

# Check JSON syntax
python -m json.tool all_trails/doctype/google_oauth_settings/google_oauth_settings.json > /dev/null
```

### Step 2: Lint Check
```bash
# Install if needed: pip install flake8 pylint
flake8 all_trails/doctype/google_oauth_settings/ --max-line-length=100
flake8 all_trails/services/google_oauth.py --max-line-length=100
pylint all_trails/doctype/google_oauth_settings/google_oauth_settings.py
pylint all_trails/services/google_oauth.py
```

### Step 3: Import Check
```bash
# In Python shell
from all_trails.doctype.google_oauth_settings.google_oauth_settings import GoogleOAuthSettings
from all_trails.services.google_oauth import *
# Should import without errors
```

### Step 4: Manual Testing (In Frappe Shell)
```bash
bench shell
> from all_trails.doctype.google_oauth_settings.google_oauth_settings import GoogleOAuthSettings
> settings = GoogleOAuthSettings.get_settings()
> print(settings.name)  # Should print: Google OAuth Settings
> exit()
```

### Step 5: Run Tests
```bash
# If pytest installed: pip install pytest
pytest all_trails/tests/test_google_oauth.py -v

# If using Frappe's test runner:
bench test-site --module all_trails
```

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'requests'` | requests not installed | `pip install requests` |
| `SyntaxError: invalid syntax` | Bad Python syntax | Check line numbers, review indentation |
| `NameError: name 'frappe' is not defined` | Missing import | Add `import frappe` at top |
| `JSONDecodeError` in json.tool | Malformed JSON | Check for trailing commas, missing quotes |
| `flake8: E501 line too long` | Line exceeds 100 chars | Break long lines (use `\` or move to next line) |
| `undefined name 'requests'` | requests not imported | Add `import requests` |

---

## When You're Done

### Deliverables
```
✅ all_trails/doctype/google_oauth_settings/
   ├── google_oauth_settings.py (100+ lines)
   └── google_oauth_settings.json (valid JSON)

✅ all_trails/services/google_oauth.py (500+ lines)
   ├── get_google_login_url()
   ├── handle_google_callback()
   ├── exchange_code_for_tokens()
   ├── fetch_google_userinfo()
   ├── handle_user_login()
   └── sync_user_profile()

✅ all_trails/tests/test_google_oauth.py (200+ lines)
   ├── test_get_google_login_url()
   ├── test_handle_google_callback_*()
   ├── test_create_user_from_google()
   └── test_*_error_cases()

✅ All lint checks pass
✅ All imports valid
✅ All tests pass
✅ All acceptance criteria met
```

### Sign-Off Checklist
- [ ] All files created
- [ ] Syntax valid (python -m py_compile)
- [ ] JSON valid (python -m json.tool)
- [ ] Linting clean (flake8, pylint)
- [ ] Imports work (test in Python shell)
- [ ] Tests pass (pytest or bench test-site)
- [ ] No secrets logged
- [ ] CSRF protection implemented
- [ ] Error handling complete
- [ ] Acceptance criteria all met

### Next Phase
Once Phase 0a passes all checks:
1. Report results (all checks passed ✅)
2. Wait for approval
3. Proceed to Phase 0b (Frontend Signup Page)

---

## Reference Documents

**For implementation details:**
- `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 1 (complete code to copy)
- `/context/IMPLEMENTATION_ROADMAP.md` - Phase 0a specification

**For context:**
- `frontend/src/pages/Login.vue` - See social login button pattern
- `all_trails/api.py` - See `get_social_login_providers()` pattern
- `frontend/src/stores/authStore.ts` - See Pinia store pattern

---

## Important Notes

1. **Don't improvise:** Copy code from `/context/GOOGLE_SSO_IMPLEMENTATION.md` exactly. Don't simplify or skip parts.

2. **Lint is not optional:** Every file must pass linting. This is production code.

3. **No hallucination:** If something is unclear, ask. Don't guess.

4. **Google credentials:** User must have Client ID and Secret ready before frontend work starts.

5. **Test everything:** Don't skip tests. They catch issues early.

6. **Security first:** Never log secrets. Always validate redirects. Always verify email.

---

## Questions?

If you encounter:
- **Unclear spec** → Check `/context/GOOGLE_SSO_IMPLEMENTATION.md` Part 1 again
- **Syntax error** → Show the error, I'll help fix it
- **Lint failure** → Show the flake8 output, we'll fix it
- **Test failure** → Show the pytest output, we'll debug it
- **Missing pattern** → Check `all_trails/` for similar code

---

**Ready?** Let's build Phase 0a!

Start by creating the first file: `all_trails/doctype/google_oauth_settings/google_oauth_settings.py`

