# All Trails: Complete Implementation Roadmap (Including Google SSO)
**Status:** Ready for Implementation
**Updated:** 2026-03-14
**Total Duration:** 80 hours (5 weeks)

---

## The Complete Picture: User Acquisition → Retention Loop

```
SIGNUP FRICTION (Days 1-3)
├─ ❌ Current: Email + password form = 70% drop-off
├─ ✅ Solution: Google SSO (1-click signup)
└─ Impact: +40-60% signup conversion

↓

BOOKING FRICTION (Days 4-9)
├─ ❌ Current: Multi-step modal, manual payment = 30-40% drop-off
├─ ✅ Solution: 3-tap booking, auto STK confirmation
└─ Impact: +40% booking conversion

↓

POST-HIKE ENGAGEMENT (Days 10-19)
├─ ❌ Current: Nothing happens after booking
├─ ✅ Solution: Photo sharing, badges, social feed
└─ Impact: +50% repeat bookings

↓

DISCOVERY & RETENTION (Days 20-29)
├─ ❌ Current: Generic filters, no personalization
├─ ✅ Solution: AI recommendation algorithm + "what next"
└─ Impact: 2-3x booking rate from discovery

↓

ENGAGEMENT LOOP (Days 30-35)
├─ Pre-hike reminders + hike tracker
└─ Repeat user becomes power user
```

---

## Quick Timeline

```
WEEK 1 (Days 1-5): User Acquisition
├─ Days 1-3: Google OAuth setup + signup page  (10h)
├─ Day 3-4: Glass components foundation       (5h)
├─ Days 4-5: Frictionless booking UX          (7h)

WEEK 2 (Days 6-10): Memory & Social
├─ Days 6-8: Photo upload + badges            (13h)
├─ Days 8-10: Activity feed                   (5h)

WEEK 3 (Days 11-15): Discovery
├─ Days 11-13: Personalization algorithm      (8h)
├─ Days 13-15: Recommendation UI              (9h)

WEEK 4 (Days 16-20): Engagement
├─ Days 16-17: User preferences               (3h)
├─ Days 17-18: Pre-hike reminders             (3h)
├─ Days 18-19: Hike tracker                   (6h)
├─ Day 20: Guide check-in                     (6h)

WEEK 5 (Days 21-25): Testing & Polish
├─ Days 21-23: Testing & bug fixes            (10h)
├─ Days 23-25: Performance & polish           (10h)

Total: ~80 hours across 5 weeks
```

---

## Phase Breakdown

### Phase 0a: Google OAuth Backend (4 hours)
**What:**
- Google OAuth2 settings DocType
- Token exchange service
- User auto-creation from Google profile
- Profile picture sync

**Files Created:**
- `all_trails/doctype/google_oauth_settings/`
- `all_trails/services/google_oauth.py`

**Acceptance Criteria:**
- [ ] Token exchange works with Google API
- [ ] New users auto-created with email + profile picture
- [ ] Existing users logged in by email match
- [ ] No secrets logged
- [ ] CSRF protection (state parameter)

**See:** `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 1

---

### Phase 0b: Google OAuth Frontend (3 hours)
**What:**
- Signup page with Google SSO button
- Email/password signup form (fallback)
- Form validation
- Router setup

**Files Created:**
- `frontend/src/pages/Signup.vue`
- Update `frontend/src/router/index.ts` (add /signup route)
- Update `frontend/src/pages/Login.vue` (link to signup)

**Acceptance Criteria:**
- [ ] Google button renders and redirects correctly
- [ ] Email form validates (email format, password min 8)
- [ ] Mobile responsive (375px screens)
- [ ] Form submission calls backend
- [ ] Error messages display clearly

**See:** `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 2

---

### Phase 1a: Signup API (2 hours)
**What:**
- Traditional signup endpoint (email + password)
- User creation + validation
- Auto-login after signup
- Welcome email

**Files Modified:**
- `all_trails/api.py` (add `signup_user()` function)

**Acceptance Criteria:**
- [ ] Validates email format
- [ ] Prevents duplicate emails
- [ ] Creates user with proper role
- [ ] Auto-logs in user
- [ ] Welcome email sent

**See:** `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 3

---

### Phase 0: Glassmorphic Design System (5 hours)
**What:**
- Glass CSS variables + base classes
- 4 reusable glass components
- TrailCard refactor with glassmorphism

**Files Created:**
- `frontend/src/styles/glass.css`
- `frontend/src/components/ui/GlassCard.vue`
- `frontend/src/components/ui/GlassButton.vue`
- `frontend/src/components/ui/GlassPanel.vue`
- `frontend/src/components/ui/GlassChip.vue`

**Files Modified:**
- `frontend/src/components/features/trails/TrailCard.vue`

**Acceptance Criteria:**
- [ ] Glass effects work on iOS Safari, Chrome, Firefox
- [ ] Blur: 30px desktop, 20px mobile
- [ ] Dark mode auto-adapts
- [ ] No performance jank (60fps)
- [ ] TrailCard matches glassmorphic design

**See:** `/context/IMPLEMENTATION_ROADMAP.md` - Phase 0

---

### Phase 1: Frictionless Booking (12 hours)
**What:**
- 2-screen booking flow (down from 3)
- Pre-filled data (name, email, phone)
- Auto STK push (not manual entry)
- Pre-hike itinerary card
- Booking confirmation email + PDF

**Files Created:**
- `frontend/src/components/features/bookings/PreHikeCard.vue`
- `all_trails/templates/emails/booking_confirmation.html`

**Files Modified:**
- `frontend/src/components/features/trails/BookingModal.vue`

**Files (New Pages):**
- `frontend/src/pages/bookings/PreHike.vue`

**Acceptance Criteria:**
- [ ] Booking completion time: <60 seconds
- [ ] Spots +/- buttons work
- [ ] Price updates in real-time
- [ ] Phone number pre-filled (from stored data)
- [ ] Pre-hike card shows map, weather, guide, what to bring
- [ ] Confirmation email sent immediately
- [ ] PDF download works

**See:** `/context/IMPLEMENTATION_ROADMAP.md` - Phase 1

---

### Phase 2: Memory & Social (18 hours)
**What:**
- Photo upload (max 5, <5MB each)
- Badge system (8+ badge types)
- Badge celebration animations
- Activity feed (friends' hikes, bookmarks)

**Files Created:**
- `frontend/src/components/features/bookings/PostHikePhotos.vue`
- `frontend/src/components/features/bookings/BadgeCelebration.vue`
- `frontend/src/components/features/profile/BadgeCard.vue`
- `frontend/src/components/features/discover/ActivityFeed.vue`
- `frontend/src/pages/bookings/PostHike.vue`
- `frontend/src/pages/ActivityFeed.vue`
- `frontend/src/stores/feedStore.ts`
- `all_trails/doctype/badge/`
- `all_trails/doctype/user_badge/`
- `all_trails/doctype/hike_photo/`

**Acceptance Criteria:**
- [ ] Photo upload max 5, auto-compressed
- [ ] Responsive grid (3 cols desktop, 1 mobile)
- [ ] Drag-to-reorder (desktop) + buttons (mobile)
- [ ] 8+ badge types with unlock criteria
- [ ] Celebration animation + sound (optional)
- [ ] Activity feed loads <2s
- [ ] Infinite scroll on mobile
- [ ] Works offline (cache + sync)

**See:** `/context/IMPLEMENTATION_ROADMAP.md` - Phase 2

---

### Phase 3: Personalization (20 hours)
**What:**
- Recommendation algorithm (content + collaborative + trending)
- "What should I hike next?" UX
- Discover page with 3 recommendation carousels
- User preferences modal

**Files Created:**
- `all_trails/services/recommendation_engine.py`
- `frontend/src/components/features/discover/RecommendedCarousel.vue`
- `frontend/src/components/features/trails/WhatsNextModal.vue`
- `frontend/src/components/features/profile/PreferencesModal.vue`
- `frontend/src/pages/discover/Discover.vue`
- `all_trails/doctype/user_trail_preference/`
- `all_trails/doctype/trail_interaction/`

**Acceptance Criteria:**
- [ ] Algorithm returns 10 trails with "why recommended"
- [ ] Works with 0 user data (cold start)
- [ ] Runs in <500ms
- [ ] Recommended carousel loads <1s
- [ ] Discover page shows 3 carousel sections
- [ ] User preferences save and affect recommendations
- [ ] Mobile responsive

**See:** `/context/IMPLEMENTATION_ROADMAP.md` - Phase 3

---

### Phase 4: Engagement (15 hours)
**What:**
- Pre-hike reminders (7d, 1d, 2h, 30m)
- Hike tracker (real-time stats, map, photos)
- Guide check-in (mark attendance)

**Files Created:**
- `all_trails/scheduled_tasks.py`
- `frontend/src/components/features/bookings/HikeTracker.vue`
- `frontend/src/components/features/bookings/GuideCheckin.vue`
- `frontend/src/pages/bookings/HikeTracker.vue`

**Acceptance Criteria:**
- [ ] Reminders sent on schedule
- [ ] Hike tracker updates real-time
- [ ] Guide check-in works offline
- [ ] Works on poor connectivity
- [ ] Battery efficient

**See:** `/context/IMPLEMENTATION_ROADMAP.md` - Phase 4

---

## Document Reference

| Document | Purpose | Read Time | Phase |
|----------|---------|-----------|-------|
| `/context/GOOGLE_SSO_IMPLEMENTATION.md` | Complete OAuth setup | 30 min | 0a/0b/1a |
| `/context/IMPLEMENTATION_ROADMAP.md` | Detailed specs for phases | 40 min | 0-4 |
| `/context/ROADMAP_SUMMARY.md` | High-level overview | 15 min | All |
| `/context/UX_AUDIT_VS_ROADMAP.md` | Why decisions were made | 20 min | Context |
| `/context/START_HERE.md` | Quick start guide | 5 min | Navigation |
| `/context/BRD.md` | Original requirements | 60 min | Reference |

---

## Getting Started

### Pre-Implementation (Before Day 1)
1. Read `/context/START_HERE.md` (5 min)
2. Read `/context/GOOGLE_SSO_IMPLEMENTATION.md` section "Pre-Implementation" (10 min)
3. Create Google Cloud project:
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Create new project "All Trails"
   - Enable Google+ API
   - Create OAuth 2.0 credentials (Web)
   - Configure redirect URI:
     ```
     https://your-domain.com/api/method/all_trails.services.google_oauth.handle_google_callback
     ```
   - Copy Client ID and Client Secret

### Day 1-3: Phase 0a/0b/1a (User Acquisition)
1. Implement Phase 0a (backend): 4 hours
   - Use `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 1
   - Test with Google API
2. Implement Phase 0b (frontend): 3 hours
   - Use `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 2
   - Test signup flow
3. Implement Phase 1a (API): 2 hours
   - Use `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 3
   - Test email signup

### Day 4-5: Phase 0 (Glass Foundation)
1. Use `/context/IMPLEMENTATION_ROADMAP.md` - Phase 0
2. Implement glass CSS + components (5 hours)

### Day 6+: Phases 1-4
1. Follow `/context/IMPLEMENTATION_ROADMAP.md` sequentially
2. Test after each phase
3. Deploy weekly

---

## Success Metrics

### After Phase 0a/0b (Day 3)
- ✅ Users can sign up with Google
- ✅ Profile auto-created with name + picture
- ✅ Existing users can login with Google

### After Phase 1 (Day 5)
- ✅ Booking completion time: <90 seconds
- ✅ Booking completion rate: +40% (vs current)

### After Phase 2 (Day 10)
- ✅ Photo upload rate: >60%
- ✅ Badge earning rate: >70%
- ✅ 2nd booking rate: +50%

### After Phase 3 (Day 15)
- ✅ Recommendation click rate: >30%
- ✅ Average bookings per user: +2x

### After Phase 4 (Day 20)
- ✅ Hike day engagement: >80%
- ✅ Reminder open rate: >70%

---

## Agent Implementation Checklist

### Phase 0a (Backend Google OAuth)
- [ ] Read `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 1
- [ ] Create `google_oauth_settings/` DocType
- [ ] Create `services/google_oauth.py`
- [ ] Implement token exchange
- [ ] Implement user creation
- [ ] Implement profile picture sync
- [ ] Test with Google API
- [ ] No secrets logged

### Phase 0b (Frontend Signup)
- [ ] Read `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 2
- [ ] Create `pages/Signup.vue`
- [ ] Add `/signup` route to router
- [ ] Update Login page link
- [ ] Test form validation
- [ ] Test Google redirect
- [ ] Mobile responsive test

### Phase 1a (Signup API)
- [ ] Read `/context/GOOGLE_SSO_IMPLEMENTATION.md` - Part 3
- [ ] Add `signup_user()` to `api.py`
- [ ] Email validation
- [ ] Duplicate email check
- [ ] User creation + role
- [ ] Auto-login logic
- [ ] Welcome email template

---

## Key Insights

1. **Google SSO is mandatory** — 40-60% higher conversion, must be first
2. **Booking friction kills everything** — Reduce from 5 min to 60 sec
3. **Memory capture is retention** — Photos + badges = emotional anchor
4. **Discovery is the multiplier** — Personalization drives repeat bookings
5. **Engagement loops close the cycle** — Reminders + tracking keep users active

---

## Questions?

1. **Why Google SSO first?** → Users bounce at signup forms. SSO removes friction.
2. **Why not do glassmorphism first?** → Beauty doesn't matter if no users can sign up.
3. **Can I skip phases?** → No. Each phase enables the next. Do 0a→0b→1a→0→1→2→3→4.
4. **How long will this take?** → 5 weeks, ~80 hours (assuming 16 hours/week)
5. **Should I hire someone to help?** → 2 engineers can do this in 3 weeks in parallel

---

**Ready? Start with `/context/GOOGLE_SSO_IMPLEMENTATION.md` → `/context/START_HERE.md` → `/context/IMPLEMENTATION_ROADMAP.md`**

