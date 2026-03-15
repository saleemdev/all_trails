# All Trails - Complete Implementation Roadmap
**Created:** 2026-03-14
**Status:** Ready for Agent Implementation
**Goal:** Build the 3 hiker retention drivers with 0 hallucination

---

## CRITICAL: Google SSO Must Be First

**Why:** Google SSO removes signup friction (40-60% higher conversion). Without it, users bounce at signup form.

**Duration:** 8-10 hours (split as Phase 0a/0b)
- Phase 0a: Backend setup (Google OAuth, user creation, profile sync) - 4h
- Phase 0b: Frontend signup page + router + integration - 3h
- Phase 1a: Signup API endpoint - 2h

**See:** `/context/GOOGLE_SSO_IMPLEMENTATION.md` (complete spec)

**Implementation Order:**
1. **FIRST (Day 1):** Phase 0a - Backend Google OAuth service + settings DocType
2. **THEN (Day 2):** Phase 0b - Frontend signup page + router integration
3. **THEN (Day 3):** Phase 1a - Signup API endpoint
4. **THEN (Day 4):** Phase 0 - Glass components (original Phase 0)

---

## Overview: 3 Retention Drivers

| Driver | Why | Timeline |
|--------|-----|----------|
| **1. Frictionless Booking** | 3-tap booking, instant confirmation, mobile-first | Phase 1 (Week 1-2) |
| **2. Memory & Social** | Photo sharing, badges, friend features | Phase 2 (Week 3-4) |
| **3. Discovery Magic** | Personalization algo, "what next" UX | Phase 3 (Week 5-6) |

---

## Phase 0: Glassmorphic Design System Foundation
**Duration:** 5 hours (complete)
**Goal:** Create reusable glass components before building features

### 0.1 Create Glass CSS Variables
**File:** `frontend/src/styles/glass.css`
**Task:** Add glass-specific CSS variables and base classes
**Acceptance Criteria:**
- [ ] `:root` contains `--glass-bg`, `--glass-border`, `--glass-blur`, `--glass-shadow`
- [ ] Dark mode variants exist (`[data-theme='dark']`)
- [ ] `.glass` base class works in all modern browsers
- [ ] Tested on iPhone Safari, Chrome, Firefox

**Implementation Notes:**
```css
--glass-bg: rgba(255, 255, 255, 0.1);
--glass-border: rgba(255, 255, 255, 0.2);
--glass-backdrop-blur: 30px;
--glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
/* Mobile: reduce blur to 20px for performance */
```

### 0.2 Create Glassmorphic Vue Components
**Files to Create:**
- `frontend/src/components/ui/GlassCard.vue`
- `frontend/src/components/ui/GlassButton.vue`
- `frontend/src/components/ui/GlassPanel.vue`
- `frontend/src/components/ui/GlassChip.vue`

**Each Component Spec:**
- [ ] Accept `variant` prop (default, primary, accent, success, warning)
- [ ] Accept `size` prop (sm, md, lg)
- [ ] Support `blur` prop for customization
- [ ] Work in dark mode (auto-adapt via CSS variables)
- [ ] Include smooth hover transitions
- [ ] Responsive on mobile (reduce blur from 30px → 20px on mobile)

**Example GlassCard Props:**
```typescript
interface Props {
  variant?: 'default' | 'primary' | 'accent' | 'success' | 'warning'
  size?: 'sm' | 'md' | 'lg'
  blur?: number // 0-50, default 30
}
```

### 0.3 Refactor TrailCard with Glassmorphism
**File:** `frontend/src/components/features/trails/TrailCard.vue`
**Changes:**
- [ ] Wrap card content in `GlassCard` component
- [ ] Convert badges (difficulty, availability) to `GlassChip`
- [ ] Add glass overlay effect to image section
- [ ] Convert "View Trail" button to `GlassButton`
- [ ] Maintain all existing functionality and accessibility

**Acceptance Criteria:**
- [ ] Visual match to glassmorphic mockup from BRD
- [ ] All existing props/events work unchanged
- [ ] Stats grid still displays (distance, elevation, duration)
- [ ] Accessibility (tabindex, aria-labels) preserved
- [ ] Mobile responsive (blur reduces on small screens)

---

## Phase 1: Frictionless Booking UX
**Duration:** 12 hours
**Goal:** Reduce booking from 5 steps to 3 taps (discovery → select spots → payment)

### 1.1 Redesign Booking Modal for Mobile-First
**File:** `frontend/src/components/features/trails/BookingModal.vue`
**Current State:** 3-step flow (booking → payment → confirm) works but has friction
**New State:** 2-step flow (details → payment) optimized for mobile

**Changes:**
- [ ] Move activity selection to secondary "Add-Ons" tab (not default expanded)
- [ ] Simplify spots selection to simple +/- buttons (not dropdown)
- [ ] Show price summary as sticky bottom bar (always visible)
- [ ] Move confirmation to inline success state (don't reload modal)
- [ ] Make "Book Now" button fill 80% of mobile viewport width

**Step 1: Details (Pre-Filled if Possible)**
```
[Trail Image - auto-filled from trail]
[Spots Selector: - 1 +] (default 1)
[Price Display: KES 2,500] (sticky, always visible)
[Add-Ons Link] (optional, collapsed)
[Book Now Button] (green, 80% width)
```

**Step 2: Payment (Real STK Push, Not Manual)**
```
[Amount Display: KES 2,500]
[Phone Number Input: 254XXXXXXXXX] (pre-fill if available)
[Pay via MPESA Button]
↓
[System: STK prompt on phone - automatic]
↓
[Waiting for Payment... 30s timeout]
↓
[✅ Success with booking details]
```

**Acceptance Criteria:**
- [ ] Booking completion time: <60 seconds on mobile
- [ ] Spots selection works with +/- buttons (no dropdown)
- [ ] Price updates in real-time as user changes spots
- [ ] Activity selection is optional and collapsible
- [ ] Mobile viewport width: button takes 85% of width
- [ ] Form pre-fills user's stored phone number (if available)
- [ ] Payment flow shows real STK push (when backend ready)

### 1.2 Create Pre-Hike Experience Component
**Files to Create:**
- `frontend/src/components/features/bookings/PreHikeCard.vue`
- `frontend/src/pages/bookings/PreHike.vue`

**PreHikeCard Component:**
Shows on booking detail page after confirmation
**Content:**
- [ ] Itinerary summary (date, time, location, guide)
- [ ] Meeting point map (Leaflet integration)
- [ ] "What to Bring" checklist (safety gear, water, etc.)
- [ ] Guide introduction card (name, photo, bio, rating)
- [ ] Weather forecast for hike date
- [ ] Download PDF itinerary button

**Spec:**
```typescript
interface PreHikeProps {
  booking: TrailBooking
  trail: Trail
}
```

**Acceptance Criteria:**
- [ ] Displays itinerary with all key info
- [ ] Map shows meeting point with +5min walk radius
- [ ] "What to Bring" list is customized per trail difficulty
- [ ] Guide profile card shows name, photo, 5-star rating
- [ ] Weather forecast fetches from [OpenWeatherMap API](https://openweathermap.org/) if available
- [ ] PDF download works (use jsPDF or similar)
- [ ] Mobile responsive (all text readable on 375px screen)

### 1.3 Booking Confirmation Email/PDF
**Backend Task** (Frappe DocType hook)
**File:** `all_trails/api.py` or new `all_trails/doctype/trail_booking/trail_booking.py`

**Changes:**
- [ ] Create email template: `all_trails/templates/emails/booking_confirmation.html`
- [ ] Email sent immediately after payment confirmation
- [ ] PDF generated with itinerary (meeting point, guide, what to bring)
- [ ] Email includes direct link to pre-hike page

**Email Content:**
```
Subject: Your Trail Booking Confirmed! ✅

Body:
- Confirmation code (copy-to-clipboard)
- Trail name + date
- Meeting point with map link
- Guide contact info
- "View Full Itinerary" button → pre-hike page
- Weather forecast
```

**Acceptance Criteria:**
- [ ] Email sent to user immediately after payment
- [ ] PDF contains all booking details
- [ ] PDF is attachment to email
- [ ] Pre-hike page link in email works
- [ ] No typos or formatting issues in email

---

## Phase 2: Memory Capture & Social Features
**Duration:** 18 hours
**Goal:** Post-hike photo sharing, badges, and social validation

### 2.1 Post-Hike Photo Upload Component
**Files to Create:**
- `frontend/src/components/features/bookings/PostHikePhotos.vue`
- `frontend/src/pages/bookings/PostHike.vue`
- Backend: `all_trails/api.py` - add `upload_hike_photos()` endpoint

**Photo Upload Flow:**
```
1. User opens booking after hike date
2. "Add Photos" button appears
3. Click → photo picker opens (auto-limits to 5 best)
4. Photos displayed in grid (can reorder)
5. Add captions per photo (optional)
6. "Share" button → auto-curation and social options
```

**Component Spec:**
```typescript
interface PostHikeProps {
  booking: TrailBooking
  trail: Trail
}

// Photos stored in booking.hike_photos[]
interface HikePhoto {
  id: string
  url: string // Frappe file path
  caption?: string
  order: number
  liked_by?: string[] // user IDs
  likes_count?: number
}
```

**Acceptance Criteria:**
- [ ] User can upload max 5 photos per hike
- [ ] Photos display in responsive grid (3 cols on desktop, 1 on mobile)
- [ ] Each photo can have optional caption
- [ ] Photos can be reordered with drag-and-drop (desktop) or buttons (mobile)
- [ ] Photos persist to booking after save
- [ ] File size validation (max 5MB per photo)
- [ ] Image optimization (compress to <500KB)
- [ ] Works offline (cache photos, sync when online)

### 2.2 Badge/Achievement System
**Files to Create:**
- `frontend/src/components/features/profile/BadgeCard.vue`
- `frontend/src/components/features/bookings/BadgeCelebration.vue`
- Backend DocType: `Badge` (tracks user achievements)
- Backend DocType: `UserBadge` (user's earned badges)

**Badge Types:**
```
🥇 First Trail - Book 1st trail
🏔️ Peak Bagger - Complete 5 trails
⛰️ Elevation Master - Gain 5,000m+ elevation
🏃 Speed Demon - Complete trail faster than expected
🌄 Early Riser - Complete trail before 8am
🤝 Social Butterfly - Share 5+ photos
🎯 Collections Master - Complete 3 trails in same location
```

**Frontend Badge Display:**
- [ ] Show badge grid on profile page (3 cols)
- [ ] Each badge card shows: icon, name, description, unlock criteria
- [ ] Earned badges have checkmark
- [ ] Locked badges are grayed out with "Unlock by..."
- [ ] Clicking badge shows user's progress toward unlock

**Celebration Moment (Post-Booking):**
When new badge earned:
```
Confetti animation
"🎉 New Badge Unlocked: Peak Bagger"
"Complete 5 trails to unlock"
Button: "Share on Instagram"
```

**Acceptance Criteria:**
- [ ] 8+ badge types defined
- [ ] Badge unlock logic works (triggered after booking marked complete)
- [ ] Celebration animation plays on unlock (confetti, sound optional)
- [ ] Profile page shows all badges in grid
- [ ] Locked badges show unlock criteria
- [ ] "Share Badge" functionality works (Instagram, WhatsApp)

### 2.3 Activity Feed (Friends' Hikes)
**Files to Create:**
- `frontend/src/components/features/discover/ActivityFeed.vue`
- `frontend/src/pages/ActivityFeed.vue`
- Pinia store: `stores/feedStore.ts`

**Activity Feed Shows:**
```
[Friend completed "Mount Kenya Summit"]
Photos: [3 photos from hike]
Badges earned: 🏔️ Peak Bagger
Time: 4h 32m (faster than expected!)
Weather: Sunny
Reactions: 👍 12 likes, 3 comments

[Friend bookmarked "Lake Nakuru Trail"]
```

**Feed Logic:**
- [ ] Show activities from friends/followers
- [ ] Display completed hikes with photos
- [ ] Show badges earned
- [ ] Show bookmarks and wishlist items
- [ ] Sort by recency
- [ ] Pagination (load more)
- [ ] Infinite scroll on mobile

**Acceptance Criteria:**
- [ ] Feed loads in <2 seconds
- [ ] Shows only public activities (respect privacy settings)
- [ ] Photo galleries render smoothly (lazy-load images)
- [ ] Like/comment functionality works
- [ ] Follows/unfollows work
- [ ] Works offline (cache last 20 activities)

---

## Phase 3: Discovery & Personalization
**Duration:** 20 hours
**Goal:** "What should I hike next?" feels magical

### 3.1 Personalization Algorithm Backend
**Files to Create:**
- `all_trails/services/recommendation_engine.py` (NEW)
- Frappe DocType: `UserTrailPreference` (track preferences)
- Frappe DocType: `TrailInteraction` (clicks, views, saves)

**Data Tracked (Non-Intrusive):**
```
UserTrailPreference:
- user_id
- preferred_difficulty: easy/moderate/hard/expert
- preferred_distance_km: 0-30 range
- preferred_elevation_m: 0-3000 range
- preferred_duration_h: 0-8 range
- trail_interests: [mountain, forest, lake, desert, urban]
- fitness_level: beginner/intermediate/advanced

TrailInteraction:
- user_id
- trail_id
- action: view | bookmark | click | search_click
- timestamp
- duration_seconds (how long they viewed)
```

**Recommendation Algorithm:**
```python
def get_next_trail_recommendations(user_id, limit=10):
    """
    Rank trails by:
    1. Content-based: Similar to trails user completed (distance ±20%, difficulty +1 level)
    2. Collaborative: Popular with users who hiked what this user hiked
    3. Trending: High bookmark/booking rate in last 30 days
    4. Personal fit: Matches user's preferred distance/difficulty/interests
    5. Unexplored: User hasn't seen/clicked this trail yet
    6. Time-sensitive: Matches current weather/season

    Return: [
        { trail_id, score, reason: "Similar to Mount Kenya" },
        { trail_id, score, reason: "Friends completed this" },
        ...
    ]
    """
```

**Acceptance Criteria:**
- [ ] Algorithm returns top 10 trails ranked by relevance
- [ ] Includes "why recommended" explanation
- [ ] Works with <100 completed hikes (bootstrapping problem solved)
- [ ] Runs in <500ms for user with 1000 interactions
- [ ] A/B test ready (can compare algo versions)
- [ ] Logs recommendations for analysis
- [ ] No personalized data shared externally

### 3.2 Recommendation UI Components
**Files to Create:**
- `frontend/src/components/features/discover/RecommendedCarousel.vue`
- `frontend/src/components/features/trails/WhatsNextModal.vue`
- `frontend/src/pages/discover/Discover.vue`

**Recommended Carousel (Home Page):**
```
"Recommended for You" (after user completes a hike)
[Trail Card] → [Trail Card] → [Trail Card]
Horizontal scroll on mobile, grid on desktop

Each card shows:
- Trail image
- Title + location
- Why: "Similar to Mount Kenya" or "Friends hiked this"
- Quick book button (click to modal)
```

**"What's Next?" Modal (Post-Booking View):**
Shows when user views completed booking
```
Heading: "What should you hike next?"

Your recent stats:
├─ Completed: Mount Kenya (4,500m)
├─ Time: 4h 32m (faster than expected!)
├─ Difficulty: Felt easy

Recommendations:
├─ Mount Kenya West Point (⬆️ 500m elevation)
   "Even more challenging"
├─ Lake Nakuru Trail
   "Friends loved this" (3 friends)
└─ Amboseli National Park
   "Popular with advanced hikers"

"View All Recommendations" button → Discover page
```

**Discover Page Layout:**
```
[Search + Filters] (sticky)
[Recommended For You Carousel]
[Trending This Week Carousel]
[By Your Interests Carousel]
[All Trails Grid with pagination]
```

**Acceptance Criteria:**
- [ ] Recommended carousel loads in <1 second
- [ ] Each recommendation has explanation ("Why recommended")
- [ ] Quick book button works from carousel
- [ ] Discover page shows 3 recommendation sections
- [ ] All trails pagination works (load 20 at a time)
- [ ] Mobile responsive (single column)
- [ ] Filters work client-side (fast)
- [ ] Search returns results in <100ms

### 3.3 Personalization User Preferences Modal
**File:** `frontend/src/components/features/profile/PreferencesModal.vue`

**User Can Set:**
```
Preferred Difficulty: [Easy] [Moderate] [Hard] [Expert]
Preferred Distance: [0-5km] [5-15km] [15-30km] [30km+]
Preferred Duration: [1-2h] [2-4h] [4-8h] [8h+]
Preferred Elevation: [<500m] [500-1000m] [1000-2000m] [2000m+]

Interests: [Mountain] [Forest] [Lake] [Desert] [Urban] [Historic]

Fitness Level: [Beginner] [Intermediate] [Advanced] [Expert]
```

**Acceptance Criteria:**
- [ ] Form saves to `UserTrailPreference` DocType
- [ ] Recommendations update immediately after save
- [ ] Preferences persist across sessions
- [ ] Optional (users can skip)
- [ ] Can update anytime from profile

---

## Phase 4: Pre-Hike & During-Hike Features
**Duration:** 15 hours
**Goal:** Engagement before, during, and after the hike

### 4.1 Pre-Hike Reminders & Notifications
**Backend Task** (Frappe Scheduled Job)
**File:** `all_trails/scheduled_tasks.py` (NEW)

**Reminder Timeline:**
- [ ] 7 days before: "Your hike is coming up! Check the weather"
- [ ] 1 day before: "Prepare your gear! Here's what to bring"
- [ ] 2 hours before: "See you soon! Meeting point is [location]"
- [ ] 30 mins after start: "Rate your hike and share photos!"

**Implementation:**
```python
@frappe.whitelist()
def schedule_hike_reminders():
    """
    Find all bookings with scheduled_date = today + N days
    Send SMS or push notification
    Log reminder sent
    """
```

**Acceptance Criteria:**
- [ ] Reminders sent on schedule (not too early/late)
- [ ] Works via SMS (if Frappe SMS configured) or in-app notifications
- [ ] User can opt-out of reminders
- [ ] No duplicate reminders (idempotent)
- [ ] Includes relevant link (pre-hike page, guide contact, etc.)

### 4.2 During-Hike Real-Time Features
**Files to Create:**
- `frontend/src/components/features/trails/HikeTracker.vue`
- `frontend/src/pages/bookings/HikeTracker.vue`
- Backend: WebSocket or polling endpoint

**Hike Tracker Component:**
Shows during hike day
```
[Live Timer: 02:34:21]
[Progress: 8.5 / 12 km] [Progress Bar]
[Elevation Gained: 847 / 1,200 m]
[Average Pace: 5.2 km/h]

[Trail Map with location]
[Guide Location: "123m ahead"]

[Photo Capture Button]
[Chat with Group]
[Emergency Alert]
```

**Live Features:**
- [ ] GPS tracking (if user allows location permission)
- [ ] Real-time stats (pace, elevation, time)
- [ ] Photo capture (optimized for mobile)
- [ ] Group chat (not live messages, just bookmark moments)
- [ ] Emergency button (alerts guide)

**Acceptance Criteria:**
- [ ] Location tracking works with permission (optional)
- [ ] Stats update every 10 seconds
- [ ] Photo capture stores offline, syncs when online
- [ ] Works with poor connectivity (graceful degradation)
- [ ] Battery efficient (not continuous GPS)

### 4.3 Guide Check-In & Attendance
**Backend Endpoint** (Frappe RPC)
**File:** `all_trails/api.py`

**Endpoint: `/api/method/all_trails/check_in_user`**
```python
@frappe.whitelist()
def check_in_user(booking_id, trail_id):
    """
    Guide marks user as checked in
    Returns: { success: bool, message: str }
    """
```

**Frontend: Guide Check-In Card**
**File:** `frontend/src/components/features/bookings/GuideCheckin.vue` (guide-only)
```
[List of booked participants]
├─ John (checked in) ✅
├─ Sarah (not checked in) ❌
├─ Mike (checked in) ✅

[Quick check-in buttons]
[Mark all as present]
[Print attendance sheet]
```

**Acceptance Criteria:**
- [ ] Guide can check in users via app
- [ ] Check-in recorded with timestamp
- [ ] Can download attendance sheet (PDF)
- [ ] Works offline (sync when online)

---

## Implementation Order (For Agent)

### Week 1: Google SSO + Foundation + Booking UX
```
Day 1: Phase 0a (Backend: Google OAuth service + DocType)
Day 2: Phase 0b (Frontend: Signup page + router)
Day 2: Phase 1a (Backend: Signup API endpoint)
Day 3: Phase 0.1 + 0.2 (Glass CSS + Components)
Day 3-4: Phase 0.3 (Refactor TrailCard)
Day 4-5: Phase 1.1 (Redesign BookingModal) + Phase 1.2 (PreHikeCard)
```

### Week 2: Confirmation + Memory
```
Day 1: Phase 1.3 (Booking email/PDF)
Day 2-4: Phase 2.1 (Photo upload)
Day 4-5: Phase 2.2 (Badge system)
```

### Week 3: Social + Discovery
```
Day 1-2: Phase 2.3 (Activity feed)
Day 2-3: Phase 3.1 (Recommendation algorithm)
Day 4-5: Phase 3.2 (Recommendation UI)
```

### Week 4: Finishing
```
Day 1: Phase 3.3 (User preferences)
Day 2-3: Phase 4.1 (Reminders)
Day 4: Phase 4.2 (Hike tracker)
Day 5: Phase 4.3 (Guide check-in) + Testing
```

---

## Testing Strategy (Per Phase)

### Phase 0 Testing
- [ ] Visual regression: Glass effects on light/dark backgrounds
- [ ] Browser compatibility: iOS Safari, Chrome, Firefox
- [ ] Performance: No jank on animations (60fps target)
- [ ] Mobile: Blur reduces from 30px → 20px on <600px screens

### Phase 1 Testing
- [ ] Booking completion time: <60s on 4G mobile
- [ ] Form autofill works (phone number from stored data)
- [ ] Payment flow integrates with MPESA (mock for tests)
- [ ] Pre-hike card loads all required data
- [ ] PDF download works without errors

### Phase 2 Testing
- [ ] Photo upload max 5 files, <5MB each
- [ ] Badge unlock logic triggers correctly
- [ ] Activity feed loads <2s, infinite scroll works
- [ ] Like/comment functionality works
- [ ] Privacy: Only public activities shown in feed

### Phase 3 Testing
- [ ] Algorithm returns 10 trails ranked correctly
- [ ] Recommendations change after new booking
- [ ] Works with 0 user interactions (cold start)
- [ ] Explain "why recommended" is accurate
- [ ] Discover page fast (<1s)

### Phase 4 Testing
- [ ] Reminders send at correct times
- [ ] Hike tracker updates in real-time
- [ ] Guide check-in persists correctly
- [ ] Works offline (cache + sync)

---

## Success Metrics (Post-Launch)

| Metric | Target | Why |
|--------|--------|-----|
| Booking → Payment time | <90 seconds | Frictionless UX |
| Booking completion rate | +40% vs current | Reduced friction |
| Photo upload rate | >60% of hikers | Memory capture |
| 2nd booking rate | +50% vs current | Retention driver |
| Recommendation click rate | >30% | Discovery algo working |
| Badge earning rate | >70% of users earn 1+ | Gamification engagement |

---

## Agent Constraints (Avoid Hallucination)

**✅ DO:**
- [ ] Create files exactly as specified (path, name, extension)
- [ ] Follow component props/events spec exactly
- [ ] Test each phase before moving to next
- [ ] Use existing Frappe/Vue patterns (don't reinvent)
- [ ] Reference BRD for design decisions
- [ ] Ask for clarification if spec is ambiguous

**❌ DON'T:**
- [ ] Add features not in spec (e.g., "wouldn't it be cool if...")
- [ ] Change existing APIs/props (breaks compatibility)
- [ ] Skip acceptance criteria testing
- [ ] Assume backend endpoints exist (implement stubs if needed)
- [ ] Use unfamiliar libraries without approval
- [ ] Optimize prematurely (finish > perfect)

---

## File Tree (End State)

```
all_trails/
├── frontend/src/
│   ├── components/
│   │   ├── ui/
│   │   │   ├── GlassCard.vue ✨ NEW
│   │   │   ├── GlassButton.vue ✨ NEW
│   │   │   ├── GlassPanel.vue ✨ NEW
│   │   │   └── GlassChip.vue ✨ NEW
│   │   ├── features/
│   │   │   ├── bookings/
│   │   │   │   ├── PreHikeCard.vue ✨ NEW
│   │   │   │   ├── PostHikePhotos.vue ✨ NEW
│   │   │   │   ├── BadgeCelebration.vue ✨ NEW
│   │   │   │   ├── GuideCheckin.vue ✨ NEW
│   │   │   │   └── HikeTracker.vue ✨ NEW
│   │   │   ├── discover/
│   │   │   │   ├── ActivityFeed.vue ✨ NEW
│   │   │   │   └── RecommendedCarousel.vue ✨ NEW
│   │   │   ├── profile/
│   │   │   │   ├── BadgeCard.vue ✨ NEW
│   │   │   │   └── PreferencesModal.vue ✨ NEW
│   │   │   └── trails/
│   │   │       ├── TrailCard.vue 🔄 REFACTOR
│   │   │       └── BookingModal.vue 🔄 REFACTOR
│   ├── pages/
│   │   ├── Login.vue 🔄 MODIFY (link to signup)
│   │   ├── Signup.vue ✨ NEW (Google SSO + email/password)
│   │   ├── bookings/
│   │   │   ├── PreHike.vue ✨ NEW
│   │   │   ├── PostHike.vue ✨ NEW
│   │   │   └── HikeTracker.vue ✨ NEW
│   │   ├── discover/
│   │   │   └── Discover.vue ✨ NEW
│   │   └── ActivityFeed.vue ✨ NEW
│   ├── stores/
│   │   └── feedStore.ts ✨ NEW
│   ├── router/
│   │   └── index.ts 🔄 MODIFY (add /signup route)
│   └── styles/
│       └── glass.css ✨ NEW
├── all_trails/
│   ├── doctype/
│   │   ├── google_oauth_settings/ ✨ NEW (OAuth config storage)
│   │   ├── badge/ ✨ NEW
│   │   ├── user_badge/ ✨ NEW
│   │   ├── user_trail_preference/ ✨ NEW
│   │   ├── trail_interaction/ ✨ NEW
│   │   └── hike_photo/ ✨ NEW
│   ├── services/
│   │   ├── google_oauth.py ✨ NEW (OAuth token exchange, user creation)
│   │   └── recommendation_engine.py ✨ NEW
│   ├── tests/
│   │   └── test_google_oauth.py ✨ NEW
│   ├── api.py 🔄 EXTEND (add signup_user, Google SSO methods)
│   ├── scheduled_tasks.py ✨ NEW
│   └── templates/emails/
│       └── booking_confirmation.html ✨ NEW
```

---

## Dependencies & Blockers

| Item | Status | Notes |
|------|--------|-------|
| MPESA STK Push API | ⏳ Pending | Phase 1 depends on this |
| Frappe Email Config | ⏳ Pending | Phase 1.3 depends on this |
| OpenWeatherMap API Key | ⏳ Optional | Phase 1.2 can work without it |
| File Storage (S3/Local) | ✅ Exists | For photos in Phase 2 |
| WebSocket Support | ⏳ Optional | Phase 4.2 can use polling instead |

---

## Sign-Off Checklist

- [ ] Product Owner (Salim) approves spec
- [ ] Design review (glassmorphic components)
- [ ] Backend lead reviews DocType specs
- [ ] Agent ready to implement Phase 0

