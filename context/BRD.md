# Business Requirements Document (BRD)
## All Trails - Modern Trail Management System with Glassmorphic Design

**Document Version:** 1.0
**Date:** 2026-03-14
**Status:** RESEARCH & PLANNING MODE
**Author:** Claude Code (Research)

---

## EXECUTIVE SUMMARY

All Trails is evolving from a traditional trail booking platform into a **modern, visually sophisticated outdoor activity management system** featuring glassmorphic UI design and enterprise-grade payment processing via MPESA.

### Key Objectives:
1. **Modernize UI/UX** with glassmorphic, minimalist design patterns
2. **Refactor MPESA flow** to leverage STK push & callback architecture
3. **Establish scalable trail management** system with advanced filtering & discovery
4. **Implement async payment processing** for reliable transaction handling

---

## SECTION 1: CURRENT STATE ANALYSIS

### 1.1 Existing Architecture Overview

**Frontend Stack:**
- Vue 3 + TypeScript + Vite (bundled to Frappe)
- Pinia state management
- Tailwind CSS + DaisyUI components
- Leaflet for map visualization
- Design tokens system (CSS variables)

**Backend Integration:**
- Frappe framework (Python)
- Payment processing via `mpesa_tx` app
- Trail & booking models ready for DocType implementation

**Current Payment Flow Issues:**
- Uses traditional callback handling mixed with status queries
- STK push implementation lacks callback verification
- No async job queue optimization
- Missing idempotency checks for duplicate payments
- Payment confirmation logic tightly coupled with UI

### 1.2 Existing UI Patterns

**Current Design:**
- Tailwind utility classes + DaisyUI components
- Forest Dark (#1B3A2D) primary color
- Warm Orange (#E85D1F) accent
- Flat, minimalist aesthetic
- Dark mode support via CSS variables

**Limitations:**
- No glassmorphic depth/layering
- Standard button/card styling
- Limited visual hierarchy differentiation
- No blur/frosted glass effects

### 1.3 What's Already Built vs. What's Missing

**✅ FULLY IMPLEMENTED (Frontend):**
- All public pages (Home, Browse, Detail, Blog, Gallery)
- Trail browsing with search & difficulty filtering
- Booking creation flow with multi-step booking modal
- User authentication (Frappe session + social login)
- User profile & bookings management
- Payment UI hooks (MPESA phone input ready)
- Responsive design (mobile/tablet/desktop)
- Design system tokens & utilities
- State management (Pinia stores)

**❌ MISSING (Backend & Features):**
- Database models (Trail, TrailBooking, User DocTypes) - Types only
- Real API endpoints (skeleton exists)
- Payment processing logic
- Guide/Host management interfaces
- Admin/Platform management dashboard
- Membership/Subscription system
- User registration/signup
- Post-booking workflows (PDFs, reminders, emails)

**⚠️ PARTIALLY DONE:**
- Payment flow designed in BRD, MPESA integration spec written
- TrailMap component exists but elevation profiles not wired
- Email templates not created
- Background job infrastructure not configured

---

## SECTION 1.4: USER PERSONAS & USE CASES

This section outlines ALL user personas and their specific workflows. **This is critical - many features were missing from initial BRD.**

### Persona 1: Public Website Visitor (Anonymous)
**Goal:** Discover hiking trails and learn about the platform

**Current Features:**
- ✅ Browse all published trails with search & filters
- ✅ Read blog articles about hiking
- ✅ View photo galleries
- ✅ See trail details without booking

**Missing Features:**
- ❌ Account creation/signup flow
- ❌ Wishlist (save favorite trails)
- ❌ Email signup for newsletters
- ❌ Trail reviews/ratings from community

**Use Cases:**
1. Land on home page → view trending trails → read blog → decide to signup
2. Search for "Nairobi easy trails" → filter by difficulty → bookmark favorite
3. Read blog post "Beginners Guide to Hiking" → follow link to related trails

---

### Persona 2: Member/Registered User (Hiker)
**Goal:** Book trails, track bookings, manage profile

**Current Features:**
- ✅ User authentication & session management
- ✅ Browse & filter trails
- ✅ Create bookings with extra activities
- ✅ View upcoming & past bookings
- ✅ Basic user profile page
- ✅ Cancel bookings with reason
- ✅ Payment via MPESA (designed, not yet implemented)

**Missing Features:**
- ❌ User registration/signup form
- ❌ Profile image upload
- ❌ Social profile integration (Google, Facebook)
- ❌ Dietary preferences & allergies
- ❌ Skill level assessment
- ❌ Emergency contact details
- ❌ Wishlist/saved trails
- ❌ Trail reviews & ratings
- ❌ Past activity history with statistics
- ❌ Email notifications/preferences
- ❌ Membership tier (basic/premium)

**Use Cases:**
1. Sign up with email → complete profile → browse trails → book trail with spots → pay MPESA
2. View "My Upcoming Trails" → reschedule booking → receive email confirmation
3. Save favorite trail → get notified when spots become available
4. Write review of completed trail → earn points/badges
5. Switch to premium membership → access exclusive trails → get 20% discount

---

### Persona 3: Trail Guide/Host (Event Creator)
**Goal:** Create & manage trails, earn commission, track participants

**Critical Missing Features:**
- ❌ Guide dashboard (this is a MAJOR gap!)
- ❌ Trail creation interface
- ❌ Schedule/date management
- ❌ Participant tracking & checklist
- ❌ Real-time location sharing during hike
- ❌ Post-hike photo uploads to gallery
- ❌ Guide ratings & reviews
- ❌ Earnings dashboard
- ❌ Payout management
- ❌ Equipment inventory management
- ❌ Safety/liability documents

**Use Cases:**
1. Guide logs in → Dashboard shows "Hike Tomorrow at 6 AM, 12 participants booked"
2. Create new trail → Set name, location, difficulty, max capacity, schedule dates
3. On hike day → Mark attendance, collect payments, track real-time participants on map
4. After hike → Upload photos → Participants can see gallery → Request reviews
5. End of month → Dashboard shows earnings, guide commission breakdown → Request payout
6. Manage liability → Upload insurance docs, emergency protocols, guide certifications

**Dashboard Sections:**
```
Guide Dashboard (from research)
├── Stats: Total Trails, Upcoming Hikes, Earnings This Month, Rating
├── Calendar: Shows all scheduled hikes with participant counts
├── Upcoming Hikes (Next 7 Days)
│   └── Each hike shows: date, spots filled, status, participants list
├── Recent Bookings: Latest participants who booked
├── Earnings: Commission breakdown, payouts, payment methods
├── My Trails: Edit, archive, view stats for each trail
└── Settings: Bank details, payout preferences, guide profile
```

---

### Persona 4: Instructor/Lead (On-Trail Role)
**Goal:** Guide participants during hike, manage safety, collect feedback

**Features (Subset of Guide, Role-Based):**
- ✅ View participant list for assigned hike
- ✅ Mark attendance/check-in
- ❌ Real-time location sharing with participants
- ❌ Chat/messaging with group
- ❌ Emergency alert system
- ❌ Photo uploads during hike
- ❌ Weather updates & alerts
- ❌ Time tracking for hike duration

**Use Cases:**
1. Start hike → App shows participant list → Mark as "Started"
2. Real-time map shows all participants' locations
3. Weather alert pops up → Options to abort or continue
4. Take group photo → Upload to gallery during hike
5. Issue emergency alert → All participants notified, SOS activated
6. End hike → Request ratings & feedback from each participant

---

### Persona 5: Premium Member (Subscription)
**Goal:** Access exclusive trails, discounts, special privileges

**Critical Missing Features:**
- ❌ Membership/subscription system (MAJOR gap!)
- ❌ Subscription plans (Basic/Premium/VIP)
- ❌ Recurring billing via MPESA/Stripe
- ❌ Member-only trails
- ❌ Discount application (20% off all trails)
- ❌ Priority booking (skip waitlist)
- ❌ Early-bird pricing access
- ❌ Exclusive events

**Subscription Tiers (Recommended):**
```
Basic (Free)
├── Access: All published trails
├── Discounts: None
├── Perks: None
└── Price: Free

Premium (KES 999/month)
├── Access: All trails + exclusive premium trails
├── Discounts: 20% off all bookings
├── Perks:
│   ├── Priority booking (reserve before general release)
│   ├── Free cancellation (up to 3 times/month)
│   ├── Member-only exclusive hikes
│   └── Early access to new trails
└── Price: KES 999/month, auto-renewable

VIP (KES 4,999/month)
├── Access: All trails + VIP-only experiences
├── Discounts: 35% off, free equipment rental
├── Perks:
│   ├── Priority support (call/chat within 1 hour)
│   ├── Personal trail recommendations
│   ├── VIP guides (experienced guides only)
│   ├── Flexible rescheduling (unlimited)
│   └── Free insurance for all hikes
└── Price: KES 4,999/month
```

**Use Cases:**
1. Member clicks "Upgrade to Premium" → See pricing tiers → Select Premium → Pay MPESA
2. Subscription active → All trail prices show 20% discount automatically
3. New exclusive trail released → Premium members notified → Can book 2 weeks early
4. Premium member books full trail → "Premium members get 5% more spots reserved"
5. Cancellation > 3 times → Premium member can still cancel free, basic member charged fee

---

### Persona 6: Admin/Platform Manager
**Goal:** Oversee platform, approve guides, moderate content, monitor payments

**Critical Missing Features:**
- ❌ Admin dashboard (MAJOR gap!)
- ❌ User management interface
- ❌ Guide approval workflow
- ❌ Trail moderation queue
- ❌ Payment monitoring
- ❌ Analytics & reporting
- ❌ Support ticket system
- ❌ System configuration

**Admin Dashboard (from research):**
```
Admin Dashboard
├── System Stats (at top):
│   ├── Total Users | Total Guides | Total Trails | Platform Revenue
│   └── This Month: New Users, Bookings, Revenue
├── Quick Actions:
│   ├── Manage Users (activate, suspend, view activity)
│   ├── Approve Guides (review applications, certifications)
│   ├── Moderate Trails (pending approval, flagged for review)
│   ├── Monitor Payments (check MPESA transactions, payouts)
│   └── View Analytics (charts, trends, reports)
├── Pending Approvals:
│   ├── New Guide Applications (5 waiting)
│   ├── Trail Submissions (3 waiting)
│   └── User Reports (2 waiting)
├── System Health:
│   ├── Payment Queue Status
│   ├── Email Delivery Rate
│   ├── System Uptime
│   └── Error Rate
└── Recent Activity Feed:
    ├── New guides joined
    ├── Large payments processed
    ├── User complaints/reports
    └── System events/alerts
```

**Admin Use Cases:**
1. Morning check-in → Dashboard shows 2 new guides waiting approval
2. Click "Review Guide" → See certifications, reviews from past hikes → Approve or reject
3. Flag monitoring → Trail reported 3 times → Review reason → Take down trail
4. Payment issue → Payment failed for 10 bookings → Click to see queue → Retry all
5. Analytics → "Premium members have 3x booking rate" → Recommend marketing push
6. User support → Help desk ticket → "User charged twice" → Admin reverses one transaction

---

## SECTION 2: MODERN TRAIL MANAGEMENT SYSTEM REQUIREMENTS

### 2.1 Trail Discovery & Filtering

**Enhanced Trail Features:**
- **Advanced Filtering:**
  - Difficulty levels (Easy, Moderate, Hard, Expert)
  - Distance range (km)
  - Elevation gain range (m)
  - Duration range (hours)
  - Price range (KES)
  - Date availability
  - Seasonal tags (peak season, dry season)
  - Activity types (hiking, wildlife, water-crossing, camping)

- **Discovery Mechanisms:**
  - Personalized recommendations based on user history
  - Trending trails (booked in last 7 days)
  - New trails (added in last 30 days)
  - "Similar trails" carousel on detail view
  - Saved/wishlisted trails

- **Map Integration:**
  - Interactive trail route visualization
  - Elevation profile chart
  - Distance/duration indicators
  - Start/end point markers
  - Difficulty heat-mapping on routes
  - Satellite imagery toggle
  - Offline map caching support

### 2.2 Booking & Experience Management

**Booking Enhancements:**
- **Calendar-based booking:**
  - Monthly calendar showing available dates
  - Visual availability indicators
  - Real-time spot updates
  - Waitlist functionality for full trails

- **Group & Activity Management:**
  - Multiple participant selection
  - Individual dietary preferences
  - Skill level assessment
  - Emergency contact details
  - Equipment rental add-ons
  - Insurance packages

- **Booking Confirmation:**
  - Unique confirmation codes (QR-able)
  - Detailed itinerary PDF generation
  - Reminders (7 days, 24 hours, 1 hour before)
  - Trail guide contact information
  - Weather updates for scheduled date

### 2.3 Trail Host/Guide Features

**Trail Management (Future Phase):**
- Trail creation & editing
- Schedule management
- Participant tracking
- Real-time location sharing
- Post-hike photo uploads & gallery
- Rating & review moderation
- Earnings dashboard
- Cancellation & rescheduling policies

### 2.4 Payment & Monetization

**Payment Features:**
- Multiple payment methods:
  - MPESA (primary for Kenya market)
  - Card payments (Stripe integration - future)
  - Bank transfer (corporate groups)
  - Cash on trail (with hold payment)

- **Pricing Models:**
  - Per-person pricing
  - Group discounts
  - Early-bird pricing
  - Off-season rates
  - Seasonal dynamic pricing

- **Revenue Tracking:**
  - Trail earnings dashboard
  - Payment breakdown (guide/platform commission)
  - Refund management
  - Tax reporting

---

## SECTION 2.5: GUIDE/HOST INTERFACE & FEATURES

### 2.5.1 Guide Dashboard

**Purpose:** Central hub for trail guides to manage bookings, earn money, and build reputation

**Dashboard Layout:**
```
├── Header: Guide name, rating stars, verified badge
├── Stats Bar (4 cards):
│   ├── Upcoming Hikes (next 7 days)
│   ├── Active Participants (all hikes combined)
│   ├── This Month Earnings (KES)
│   └── Guide Rating (4.8 / 5.0)
├── Calendar Section:
│   ├── Monthly calendar showing all scheduled hikes
│   ├── Click date to see hike details & participants
│   └── Add new dates for trail availability
├── Upcoming Hikes (Card Grid):
│   ├── For each hike:
│   │   ├── Trail name & location
│   │   ├── Date & time
│   │   ├── Participants: 12/15 spots filled
│   │   ├── Status: Scheduled, In Progress, Completed
│   │   └── Actions: Edit, View Participants, Start Hike
│   └── "Create New Hike" button
├── Recent Bookings (Last 10):
│   ├── New participant booked trail
│   ├── Show participant name, amount, payment status
│   └── Quick actions: Message, Refund
├── Earnings Section:
│   ├── Chart: Earnings over last 12 months
│   ├── Breakdown: Hikes led, total bookings, commission
│   ├── Pending payouts (waiting to hit minimum)
│   └── Request Payout button
└── Settings:
    ├── Edit guide profile (bio, certifications, photo)
    ├── Bank account details
    ├── Payout preferences (weekly, monthly)
    ├── Guide certifications & insurance docs
    └── Cancellation policies
```

### 2.5.2 Trail Management

**Create/Edit Trail:**
- Trail name, description, detailed itinerary
- Location (map pin, coordinates, address)
- Difficulty level with visual indicator
- Distance (km), elevation gain (m), duration (hours)
- Max capacity per hike date
- Price per person
- Extra activities with add-on pricing
- Featured image & gallery photos
- Equipment provided (boots, water, snacks)
- What to bring checklist
- Age restrictions, fitness requirements
- Insurance & liability info

**Schedule Management:**
- Select which dates trail is offered
- Set start & end time for each date
- Availability per date (spots filled/available)
- Waitlist when full
- Auto-notifications when spots become available

### 2.5.3 Participant Management

**On Hike Day:**
- Check-in: Mark participants as arrived
- Real-time tracking: GPS location of group
- Chat: Communicate with participants
- Photos: Upload during hike, visible to group
- Safety: Emergency alert system

**Post-Hike:**
- Mark as completed
- Request ratings & reviews
- Upload final gallery
- Generate invoice/receipt
- Payment processing

### 2.5.4 Ratings & Reputation

**Guide Ratings:**
- Star rating (1-5) from participants
- Number of reviews
- Avg rating displayed on profile
- Top guide badge (>4.8 rating)
- Review text & photos from participants

**Trust Indicators:**
- Verified guide checkmark
- Number of hikes led
- Completion rate
- Certifications displayed (if provided)

---

## SECTION 2.6: ADMIN/PLATFORM MANAGEMENT INTERFACE

### 2.6.1 Admin Dashboard

**Home/Overview Page:**
```
Top Stats Row (4 large cards):
├── Total Users: 1,234 (up 12% this month)
├── Active Guides: 45 (up 5%)
├── Total Trails: 78 (up 8%)
└── Platform Revenue: KES 345,670 (up 22%)

Pending Approvals Section:
├── New Guide Applications: 3 pending
├── Trail Submissions: 2 pending
└── User Reports: 1 pending

Payment Monitoring:
├── Successful transactions today: 42
├── Failed transactions: 1
├── Failed MPESA callbacks: 0
├── Pending payouts to guides: KES 50,000

System Health:
├── Email delivery rate: 99.2%
├── API response time: 156ms
├── Background jobs processed: 234/234
└── Active errors: 0

Recent Activity Feed:
├── New user "Jane Smith" signed up
├── Guide "John Doe" submitted new trail "Mt Kenya"
├── Payment of KES 5,000 processed for booking #123
├── Guide "Mary Jane" requested payout of KES 25,000
└── User "Bob Wilson" reported trail "Ngong Hills" for safety issue
```

### 2.6.2 User Management

**User List:**
- Search & filter by status (active, suspended, new)
- View user details: email, phone, join date, total bookings
- Quick actions:
  - View activity history
  - Suspend/unsuspend account
  - Reset password
  - Send message
  - View support tickets

**User Roles Management:**
- Assign roles: Member, Guide, Admin
- View role-based access
- Suspend specific roles (ban guide without banning user)

### 2.6.3 Guide Approval System

**Workflow:**
1. Guide submits application (from settings page)
2. Admin sees "Pending Applications" count
3. Click to review:
   - Guide profile & bio
   - Certifications uploaded
   - Insurance documents
   - References/reviews from previous hikes
   - Background check status (if integrated)
4. Admin actions: Approve, Request More Info, Reject
5. Guide notified via email of decision

**Criteria for Approval:**
- Certifications (must have at least one)
- Insurance coverage
- Clean background check
- Minimum 3 reviews from past hikes

### 2.6.4 Trail Moderation

**Pending Trails:**
- Guide submits trail → shows in "Pending Approval"
- Admin views:
  - Trail details
  - Photos (safety concern checks)
  - Safety & liability info
  - Participant feedback from similar trails
- Actions: Approve, Request Changes, Reject with reason

**Flagged Trails:**
- Users can report trails (safety issue, misleading info, inappropriate)
- Shows in "Flagged for Review"
- Admin can:
  - View reports & reasons
  - Temporarily disable trail
  - Contact guide for explanation
  - Investigate complaints
  - Reinstate or permanently remove

**Trail Quality Monitoring:**
- Track completion rate (how many people finish hike safely)
- Monitor cancellation rate
- Track participant satisfaction (avg rating)
- Identify problematic guides

### 2.6.5 Payment Monitoring & Payouts

**Payment Dashboard:**
- Today's transactions: $2,350 in 42 bookings
- Failed payments: 2 (auto-retry queue shows 3 pending)
- Payment methods breakdown: MPESA 92%, Stripe 8%
- MPESA callback health: 100% success rate

**Payout Management:**
- Guides requesting payout: 7 (totaling KES 175,000)
- Minimum payout threshold: KES 1,000
- Payout frequency: Weekly
- View payout history: Last 30 payouts
- Batched payout processing

**Dispute Resolution:**
- User claims double charge → Admin sees 2 MPESA receipts
- Admin can issue refund
- Audit trail tracks all actions

### 2.6.6 Analytics & Reporting

**Dashboards:**
- Revenue trends (daily, weekly, monthly)
- User growth (new signups over time)
- Guide performance (total hikes, earnings)
- Top trails by bookings
- Participation patterns (which days popular)
- Membership conversion rate (free → premium)

**Reports:**
- Monthly revenue report (by guide, by trail, by payment method)
- User acquisition source (organic, ads, referral)
- Churn rate (users who cancel subscription)
- Guide attrition rate
- Safety incident summary

### 2.6.7 System Settings

**Platform Configuration:**
- Commission rate (guide gets X%, platform takes Y%)
- Minimum payout threshold
- Payment processing settings (MPESA credentials)
- Email sender configuration
- Subscription pricing tiers
- Featured trail selection
- Marketing banner configuration

**Support & Help:**
- Help desk/ticket system (built-in)
- FAQ management
- Email templates editing
- SMS notification settings

---

## SECTION 2.7: MEMBERSHIP/SUBSCRIPTION SYSTEM

### 2.7.1 Subscription Tiers

**Basic (Free)**
- Price: Free
- Billing: None
- Access: All published trails
- Discounts: None
- Perks: None
- Use Case: Casual hikers exploring

**Premium**
- Price: KES 999/month
- Billing: Auto-renewable via MPESA/Stripe
- Access: All trails + exclusive premium trails
- Discounts: 20% off all bookings (applies at checkout)
- Perks:
  - Priority booking (48hr early access before general public)
  - Free cancellation (3x per month, after that 50% fee)
  - Member-only exclusive hikes
  - Early access to new trails
  - Birthday month bonus: extra 10% discount
- Use Case: Regular hikers (monthly bookings)

**VIP**
- Price: KES 4,999/month
- Billing: Auto-renewable
- Access: All trails + VIP-only experiences
- Discounts: 35% off all bookings, free equipment rental
- Perks:
  - Priority support (1-hour response time)
  - Personal trail recommendations (AI-based)
  - Access to VIP guides (5-star rated only)
  - Flexible rescheduling (unlimited)
  - Free trip insurance for all hikes
  - Quarterly VIP-only hiking events
  - Priority waitlist (move to front of line)
- Use Case: Serious hikers (frequent bookings)

### 2.7.2 Subscription Billing System

**Setup:**
- User selects tier → Payment method selection
- MPESA: Enter phone, system sends STK push, process same as today
- Stripe: Card details (future integration)
- Confirm subscription → Auto-billing starts immediately

**Recurring Billing:**
- Auto-charge on same date each month
- Failed payment → Retry 3x (day 1, 3, 5)
- On retry failure → Send email asking to update payment
- If not updated within 7 days → Downgrade to free tier

**Billing Page (User View):**
- Current subscription: "Premium - KES 999/month"
- Next billing date: "15 April 2024"
- Payment method: "MPESA - ***9276"
- Actions:
  - Change plan (upgrade/downgrade)
  - Update payment method
  - View billing history
  - Cancel subscription

**Upgrade/Downgrade:**
- Upgrade (Free → Premium): Immediate charge, immediate activation
- Downgrade (Premium → Free): Effective next billing cycle (no refund)
- Downgrade (Premium → VIP): Pro-rata charge for difference
- Cancellation: Confirmation email, immediate downgrade to free

### 2.7.3 Member-Only Content

**Exclusive Trails:**
- Guide can mark trail as "Premium Only"
- Only visible to premium/VIP members
- Typically shorter, more exclusive experiences
- Example: "Sunset Dinner Hike at Mt. Kenya" - premium only, KES 3,500
- Non-members see placeholder: "Premium Member Only" with upgrade CTA

**Member-Only Events:**
- VIP-exclusive group hikes (e.g., monthly CEO networking hikes)
- Curated experiences (e.g., photo workshop on wildlife trail)
- Expert-led geological hikes
- Early-morning/sunset exclusive slots

### 2.7.4 Discount Application

**How Discounts Work:**
```
Non-member Trail Booking:
├── Trail price: KES 2,000
├── No discount applied
└── Total: KES 2,000

Premium Member Trail Booking:
├── Trail price: KES 2,000
├── Discount applied: -20% (KES 400)
└── Total: KES 1,600

VIP Member Trail Booking:
├── Trail price: KES 2,000
├── VIP discount: -35% (KES 700)
├── Equipment rental: Free (normally KES 500)
├── Insurance: Free (normally KES 300)
└── Total: KES 1,300 (66% discount vs. original equipment/insurance bundle)
```

**Discount Display:**
- On trail cards: "You save KES 400 with Premium membership!"
- At checkout: "Premium member discount applied: -KES 400"
- Email receipt: Shows original price, discount, final amount

---

## SECTION 3: GLASSMORPHIC DESIGN SYSTEM REFACTOR

### 3.1 Design Philosophy

**Glassmorphism Definition:**
Modern design style using frosted glass effects with:
- Semi-transparent backgrounds
- Backdrop blur (CSS `backdrop-filter`)
- Layered depth perception
- Minimal color saturation
- Clean, minimalist aesthetic
- Apple-inspired premium feel

### 3.2 Implementation Strategy

#### 3.2.1 CSS Foundation
```css
/* Global Glass Variables */
:root {
  /* Glass Effect Base */
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
  --glass-backdrop-blur: 30px;
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);

  /* Primary Glass Variants */
  --glass-primary-bg: rgba(27, 58, 45, 0.15);      /* Forest Dark */
  --glass-primary-border: rgba(27, 58, 45, 0.3);

  /* Accent Glass Variants */
  --glass-accent-bg: rgba(232, 93, 31, 0.15);     /* Warm Orange */
  --glass-accent-border: rgba(232, 93, 31, 0.3);

  /* Semantic Glass */
  --glass-success-bg: rgba(76, 175, 80, 0.15);
  --glass-warning-bg: rgba(255, 167, 38, 0.15);
  --glass-error-bg: rgba(239, 83, 80, 0.15);
}

/* Dark Mode Adjustments */
[data-theme='dark'] {
  --glass-bg: rgba(255, 255, 255, 0.08);
  --glass-border: rgba(255, 255, 255, 0.15);
}

/* Glass Base Class */
.glass {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(var(--glass-backdrop-blur));
  box-shadow: var(--glass-shadow);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

/* Glass Interactive Hover Effect */
.glass:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
}

/* Glass Variants */
.glass-primary {
  background: var(--glass-primary-bg);
  border-color: var(--glass-primary-border);
}

.glass-accent {
  background: var(--glass-accent-bg);
  border-color: var(--glass-accent-border);
}
```

#### 3.2.2 Vue Component System

**New Component Hierarchy:**
```
components/
├── ui/
│   ├── GlassCard.vue           # Base glass container
│   ├── GlassButton.vue         # CTA buttons with glass effect
│   ├── GlassPanel.vue          # Content panels
│   ├── GlassModal.vue          # Modal dialogs
│   ├── GlassInput.vue          # Form inputs with glass styling
│   ├── GlassSelect.vue         # Dropdown selects
│   ├── GlassChip.vue           # Tag/filter chips
│   └── GlassLoadingOverlay.vue # Loading states
├── features/
│   ├── trails/
│   │   ├── TrailCard.vue       # Refactored with glass effect
│   │   ├── TrailGallery.vue    # Image gallery with glass overlays
│   │   ├── TrailFilters.vue    # Advanced filter panel (glass)
│   │   ├── TrailMap.vue        # Map with glass info windows
│   │   ├── BookingCalendar.vue # Calendar booking with glass
│   │   └── BookingFlow.vue     # Multi-step glass modals
│   └── payments/
│       ├── PaymentMethod.vue   # Payment option selector
│       ├── MPESAFlow.vue       # STK push flow (glass)
│       └── PaymentStatus.vue   # Transaction status display
```

#### 3.2.3 Glassmorphic Component Examples

**GlassCard Component:**
```vue
<!-- components/ui/GlassCard.vue -->
<template>
  <div
    class="glass"
    :class="[variantClass, sizeClass]"
    :style="customStyle"
  >
    <slot />
  </div>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: v => ['default', 'primary', 'accent', 'success', 'warning'].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v)
  },
  blur: {
    type: Number,
    default: 30
  }
})

const variantClass = computed(() => {
  const variants = {
    default: 'glass',
    primary: 'glass glass-primary',
    accent: 'glass glass-accent',
    success: 'glass-success-bg',
    warning: 'glass-warning-bg'
  }
  return variants[props.variant]
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  }
  return sizes[props.size]
})

const customStyle = computed(() => ({
  '--glass-backdrop-blur': `${props.blur}px`
}))
</script>
```

**RefactoredTrailCard:**
```vue
<!-- Enhanced with glassmorphic layering -->
<template>
  <GlassCard variant="primary" class="overflow-hidden group">
    <!-- Image with glass overlay -->
    <div class="relative h-48 overflow-hidden rounded-lg">
      <img :src="trail.featured_image" class="w-full h-full object-cover" />

      <!-- Glassmorphic overlay with trail info -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent
                   glass-overlay group-hover:glass-overlay-active">
        <div class="absolute bottom-0 left-0 right-0 p-4">
          <GlassChip :difficulty="trail.difficulty_level" />
        </div>
      </div>
    </div>

    <!-- Content with glass separators -->
    <div class="p-6 space-y-4">
      <h3 class="text-xl font-bold">{{ trail.title }}</h3>

      <!-- Glass divider -->
      <div class="h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />

      <!-- Trail metadata in glass grid -->
      <div class="grid grid-cols-2 gap-3">
        <GlassPanel size="sm" class="text-center">
          <div class="text-sm text-gray-600">Distance</div>
          <div class="font-semibold">{{ trail.distance_km }}km</div>
        </GlassPanel>
        <GlassPanel size="sm" class="text-center">
          <div class="text-sm text-gray-600">Duration</div>
          <div class="font-semibold">{{ trail.duration_hours }}h</div>
        </GlassPanel>
      </div>

      <!-- Price & CTA in glass button -->
      <GlassButton variant="accent" class="w-full">
        Book at KES {{ trail.price_kshs }}
      </GlassButton>
    </div>
  </GlassCard>
</template>
```

### 3.3 Design Tokens & Customization

**Implement Context7 Glass UI pattern:**
```typescript
// types/glass.ts
interface GlassCustomization {
  color?: string           // rgba, rgb, or hex
  transparency?: number    // 0-1, overrides alpha
  blur?: number | string   // 20 or "20px"
  outline?: string         // Border color
  outlineWidth?: number | string
  shadow?: string          // Box shadow
  innerGlow?: string       // Inner glow for depth
  innerGlowBlur?: number | string
}

// utils/glass.ts
export function getGlassStyles(customization: GlassCustomization): React.CSSProperties {
  const {
    color = 'rgba(255, 255, 255, 0.1)',
    transparency,
    blur = 30,
    outline = 'rgba(255, 255, 255, 0.2)',
    outlineWidth = 1,
    shadow = '0 8px 32px rgba(0, 0, 0, 0.1)',
    innerGlow
  } = customization

  return {
    backgroundColor: transparency !== undefined
      ? color.replace(/[\d.]+\)$/, `${transparency})`)
      : color,
    backdropFilter: `blur(${typeof blur === 'number' ? `${blur}px` : blur})`,
    borderColor: outline,
    borderWidth: typeof outlineWidth === 'number' ? `${outlineWidth}px` : outlineWidth,
    borderStyle: 'solid',
    boxShadow: shadow,
    ...(innerGlow && {
      boxShadow: `inset 0 0 20px ${innerGlow}, ${shadow}`
    })
  }
}
```

### 3.4 Responsive Glassmorphism

**Mobile-First Glass Strategy:**
```css
/* Mobile: Slightly reduced blur for performance */
@media (max-width: 768px) {
  .glass {
    --glass-backdrop-blur: 20px;  /* Reduced from 30px */
  }
}

/* Tablet & Desktop: Full glassmorphism */
@media (min-width: 769px) {
  .glass {
    --glass-backdrop-blur: 30px;
  }

  /* Layered glass effects for rich depth */
  .glass-elevated {
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 0 20px rgba(255, 255, 255, 0.2);
  }
}
```

---

## SECTION 4: MPESA STK CALLBACK ARCHITECTURE REFACTOR

### 4.1 Current State Issues

**Problems Identified:**
1. **Callback Handling:** Callbacks stored but not verified before payment confirmation
2. **Status Query Dependency:** Over-reliance on polling for transaction status
3. **Loose Integration:** MPESA Payload processing tightly coupled to API layer
4. **Missing Idempotency:** No duplicate payment prevention mechanisms
5. **Limited Error Recovery:** Failed transactions not properly queued for retry
6. **No Audit Trail:** Limited logging of payment state transitions

### 4.2 Target Architecture: Event-Driven Callback System

**Core Principles:**
- **Async-First:** All MPESA operations as background jobs
- **Event-Driven:** State machine for payment lifecycle
- **Idempotent:** Webhook handlers can be safely retried
- **Resilient:** Failed callbacks queued for retry
- **Audited:** Complete transaction history logging

#### 4.2.1 Payment State Machine

```python
# States and Transitions
"""
┌─────────────────────────────────────────────────────────────┐
│                    MPESA PAYMENT LIFECYCLE                   │
└─────────────────────────────────────────────────────────────┘

                        ┌─────────────┐
                        │   INITIATED │  (STK push sent)
                        └──────┬──────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
            ┌───────▼────────┐   ┌────────▼──────┐
            │   AWAITING_PIN │   │  TIMEOUT      │
            │ (User enters)  │   │ (30 mins)     │
            └───────┬────────┘   └───────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
   ┌────▼──────┐         ┌──────▼──────┐
   │  CALLBACK │         │  CALLBACK   │
   │  RECEIVED │         │  NOT_RECEIVED
   │  (Success)│         │  (Timeout)  │
   └────┬──────┘         └─────────────┘
        │
   ┌────▼──────────┐
   │  VERIFIED &   │ (Double-check with query)
   │  CONFIRMED    │
   └────┬──────────┘
        │
   ┌────▼──────────┐
   │  PAYMENT      │
   │  PROCESSED    │
   └───────────────┘

Retryable States: AWAITING_PIN, CALLBACK_RECEIVED
Terminal States: VERIFIED_CONFIRMED, PAYMENT_PROCESSED, TIMEOUT
```

#### 4.2.2 Webhook Handler Architecture

```python
# mpesa_tx/api/callback_handler.py

from frappe import enqueue
from frappe.utils import get_datetime
from mpesa_tx.mpesa_tx.doctype.mpesa_ticket.mpesa_ticket import MPESATicket

class MPESACallbackHandler:
    """
    Idempotent webhook handler for M-Pesa STK callbacks.
    Safe to retry on network failures.
    """

    def __init__(self, payload: dict):
        self.payload = payload
        self.transaction_id = payload.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        self.result_code = payload.get('Body', {}).get('stkCallback', {}).get('ResultCode')

    def handle(self) -> dict:
        """
        Main handler - idempotent operation.
        Returns: {success: bool, message: str, ticket_id?: str}
        """
        try:
            # Step 1: Find the MPESA Ticket
            ticket = self._find_or_create_ticket()

            # Step 2: Check if already processed (idempotency)
            if ticket.ticket_status in ['Completed', 'Failed']:
                return {
                    'success': True,
                    'message': f'Callback already processed for {ticket.name}',
                    'ticket_id': ticket.name
                }

            # Step 3: Process based on result code
            if self.result_code == 0:  # Success
                result = self._handle_successful_callback(ticket)
            else:  # User cancelled or timeout
                result = self._handle_failed_callback(ticket)

            return result

        except Exception as e:
            # Log but don't fail - Frappe will retry the webhook
            frappe.log_error(f"MPESA Callback handling failed: {str(e)}")
            raise

    def _find_or_create_ticket(self) -> MPESATicket:
        """Find existing ticket or create placeholder"""
        try:
            ticket = frappe.get_doc('MPESA Ticket', self.transaction_id)
            return ticket
        except frappe.DoesNotExistError:
            # Create placeholder ticket for matching
            ticket = frappe.new_doc('MPESA Ticket')
            ticket.name = self.transaction_id
            ticket.ticket_status = 'Awaiting Pin'
            return ticket

    def _handle_successful_callback(self, ticket: MPESATicket) -> dict:
        """
        Process successful STK callback.
        Enqueue verification job to double-check with M-Pesa.
        """
        payload_data = self.payload.get('Body', {}).get('stkCallback', {})

        # Create MPESA Payload record with callback data
        mpesa_payload = frappe.new_doc('MPESA Payload')
        mpesa_payload.account_number = ticket.name
        mpesa_payload.phone = payload_data.get('PhoneNumber', '')
        mpesa_payload.amount = payload_data.get('CallbackMetadata', {}).get('Item', [{}])[0].get('Value', 0)
        mpesa_payload.transaction_reference = payload_data.get('MerchantRequestID', '')
        mpesa_payload.json_dump = frappe.as_json(self.payload)
        mpesa_payload.is_processed = False
        mpesa_payload.insert()

        # Enqueue verification job
        enqueue(
            'mpesa_tx.api.callback_handler.verify_and_process_payment',
            ticket_id=ticket.name,
            payload_id=mpesa_payload.name,
            job_name=f'mpesa_verify_{ticket.name}'
        )

        return {
            'success': True,
            'message': 'Callback received and queued for verification',
            'ticket_id': ticket.name
        }

    def _handle_failed_callback(self, ticket: MPESATicket) -> dict:
        """Process failed/cancelled STK request"""
        ticket.ticket_status = 'Failed'
        ticket.save()

        # Notify user
        enqueue(
            'mpesa_tx.api.notifications.notify_payment_failed',
            ticket_id=ticket.name,
            reason=self._get_failure_reason()
        )

        return {
            'success': True,
            'message': 'Payment failed/cancelled',
            'ticket_id': ticket.name
        }

    def _get_failure_reason(self) -> str:
        """Map result code to user-friendly message"""
        reasons = {
            1: 'User cancelled the operation',
            2: 'Request timeout',
            17: 'Transaction timeout',
        }
        return reasons.get(self.result_code, 'Payment declined')


def verify_and_process_payment(ticket_id: str, payload_id: str):
    """
    Background job to verify callback with M-Pesa before processing.
    This prevents processing unverified payments.
    """
    import requests
    from mpesa_tx.api.mpesa_handler import MPESAHandler

    ticket = frappe.get_doc('MPESA Ticket', ticket_id)
    payload = frappe.get_doc('MPESA Payload', payload_id)

    handler = MPESAHandler()

    # Step 1: Query transaction status from M-Pesa
    is_valid = handler.get_stk_transaction_status(ticket)

    if not is_valid:
        # Transaction not found in M-Pesa - reject it
        ticket.ticket_status = 'Failed'
        ticket.add_comment('Comment', f'Callback verification failed - transaction not found in M-Pesa')
        ticket.save()
        return

    # Step 2: Process the payment (create Payment Entry, submit charges, etc.)
    try:
        payload.process_payment()  # Existing method
        ticket.ticket_status = 'Completed'
        ticket.save()
    except Exception as e:
        ticket.ticket_status = 'Failed'
        ticket.add_comment('Comment', f'Payment processing failed: {str(e)}')
        ticket.save()
        raise


def handle_callback_webhook():
    """
    Frappe endpoint for M-Pesa callbacks.
    Route: /api/resource/MPESA%20Callback/webhook
    """
    import json
    from flask import request

    # Parse callback payload
    payload = request.get_json() or {}

    # Validate signature (if required by Safaricom)
    # validate_mpesa_signature(payload)

    # Handle callback
    handler = MPESACallbackHandler(payload)
    result = handler.handle()

    return {
        'ResultCode': 0 if result['success'] else 1,
        'ResultDesc': result['message']
    }
```

#### 4.2.3 Enhanced MPESA Ticket DocType

```python
# mpesa_tx/mpesa_tx/doctype/mpesa_ticket/mpesa_ticket.py

from frappe import enqueue
from enum import Enum

class TicketStatus(Enum):
    INITIATED = 'Initiated'
    AWAITING_PIN = 'Awaiting Pin'
    CALLBACK_RECEIVED = 'Callback Received'
    VERIFIED = 'Verified'
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    TIMEOUT = 'Timeout'

class MPESATicket(Document):
    """Enhanced MPESA Ticket with state machine and audit trail"""

    def before_save(self):
        """Validate state transitions"""
        if self.has_value_changed('ticket_status'):
            self._validate_status_transition()
            self._log_status_change()

    def _validate_status_transition(self):
        """Prevent invalid state transitions"""
        valid_transitions = {
            'Initiated': ['Awaiting Pin', 'Timeout'],
            'Awaiting Pin': ['Callback Received', 'Timeout'],
            'Callback Received': ['Verified', 'Failed'],
            'Verified': ['Completed', 'Failed'],
        }

        current = self.db_get('ticket_status') or 'Initiated'
        next_status = self.ticket_status

        if next_status not in valid_transitions.get(current, []):
            frappe.throw(f'Invalid transition: {current} -> {next_status}')

    def _log_status_change(self):
        """Audit trail for debugging"""
        old_status = self.db_get('ticket_status') or 'Initiated'
        new_status = self.ticket_status
        timestamp = frappe.utils.now()

        # Add to audit comments
        self.add_comment(
            'Comment',
            f'Status changed: {old_status} → {new_status} [{timestamp}]',
            comment_type='Info'
        )

    def enqueue_payment_initiation(self):
        """Queue STK push as background job"""
        enqueue(
            'mpesa_tx.api.mpesa_handler.initiate_payment',
            ticket_id=self.name,
            job_name=f'mpesa_initiate_{self.name}',
            timeout=60
        )

        self.ticket_status = 'Initiated'
        self.save()

    def get_callback_wait_time(self) -> int:
        """Seconds elapsed since initiation (for timeout detection)"""
        from frappe.utils import get_datetime
        elapsed = (get_datetime() - self.creation).total_seconds()
        return int(elapsed)

    def has_callback_timeout(self) -> bool:
        """Check if callback should be considered lost (30 min timeout)"""
        return self.get_callback_wait_time() > 1800
```

#### 4.2.4 Frontend Payment Flow (Vue/Pinia)

```typescript
// frontend/src/stores/paymentStore.ts

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const usePaymentStore = defineStore('payment', () => {
  // State
  const currentPayment = ref<PaymentState | null>(null)
  const paymentHistory = ref<PaymentRecord[]>([])
  const isPolling = ref(false)

  const paymentStatuses = {
    IDLE: 'idle',
    INITIATING: 'initiating',
    STK_SHOWN: 'stk_shown',
    AWAITING_PIN: 'awaiting_pin',
    PROCESSING: 'processing',
    COMPLETED: 'completed',
    FAILED: 'failed',
    TIMEOUT: 'timeout'
  }

  // Actions
  async function initiatePayment(bookingId: string, phoneNumber: string) {
    try {
      currentPayment.value = {
        status: paymentStatuses.INITIATING,
        bookingId,
        phoneNumber,
        startTime: Date.now(),
        ticketId: ''
      }

      // Call backend to queue STK push
      const response = await api.call('mpesa_tx.api.mpesa_handler.initiate_stk_transaction', {
        booking_id: bookingId,
        msisdn: phoneNumber
      })

      currentPayment.value.ticketId = response.ticket_id
      currentPayment.value.status = paymentStatuses.STK_SHOWN

      // Start polling for callback
      startPaymentPolling(response.ticket_id)

    } catch (error) {
      currentPayment.value.status = paymentStatuses.FAILED
      currentPayment.value.error = error.message
    }
  }

  function startPaymentPolling(ticketId: string) {
    if (isPolling.value) return

    isPolling.value = true
    const pollInterval = setInterval(async () => {
      try {
        // Poll backend for status
        const status = await api.call('mpesa_tx.api.mpesa_handler.get_stk_status', {
          ticket_id: ticketId
        })

        // Update local state
        updatePaymentStatus(status)

        // Stop polling on terminal state
        if (['Completed', 'Failed', 'Timeout'].includes(status.ticket_status)) {
          clearInterval(pollInterval)
          isPolling.value = false
        }

      } catch (error) {
        console.error('Polling error:', error)
      }
    }, 3000) // Poll every 3 seconds

    // Timeout after 30 minutes
    setTimeout(() => {
      if (isPolling.value) {
        clearInterval(pollInterval)
        isPolling.value = false
        currentPayment.value.status = paymentStatuses.TIMEOUT
      }
    }, 1800000)
  }

  function updatePaymentStatus(status: any) {
    if (!currentPayment.value) return

    const statusMap = {
      'Initiated': paymentStatuses.INITIATING,
      'Awaiting Pin': paymentStatuses.AWAITING_PIN,
      'Callback Received': paymentStatuses.PROCESSING,
      'Verified': paymentStatuses.PROCESSING,
      'Completed': paymentStatuses.COMPLETED,
      'Failed': paymentStatuses.FAILED,
      'Timeout': paymentStatuses.TIMEOUT
    }

    currentPayment.value.status = statusMap[status.ticket_status]
    currentPayment.value.transactionRef = status.transaction_ref
    currentPayment.value.receipt = status.receipt_number
  }

  // Computed
  const isPaymentInProgress = computed(() =>
    currentPayment.value &&
    ![paymentStatuses.COMPLETED, paymentStatuses.FAILED, paymentStatuses.TIMEOUT]
      .includes(currentPayment.value.status)
  )

  const paymentMessage = computed(() => {
    const messages = {
      [paymentStatuses.INITIATING]: 'Sending payment prompt to your phone...',
      [paymentStatuses.STK_SHOWN]: 'Payment prompt sent! Please complete on your phone.',
      [paymentStatuses.AWAITING_PIN]: 'Waiting for PIN entry...',
      [paymentStatuses.PROCESSING]: 'Verifying payment...',
      [paymentStatuses.COMPLETED]: 'Payment successful!',
      [paymentStatuses.FAILED]: 'Payment failed. Please try again.',
      [paymentStatuses.TIMEOUT]: 'Payment timed out. Please retry.'
    }
    return messages[currentPayment.value?.status] || ''
  })

  return {
    currentPayment,
    paymentHistory,
    paymentStatuses,
    initiatePayment,
    isPaymentInProgress,
    paymentMessage
  }
})
```

**Frontend UI Component:**
```vue
<!-- frontend/src/components/features/payments/MPESAFlow.vue -->
<template>
  <GlassModal v-if="isPaymentInProgress" variant="primary">
    <!-- Header with progress indicator -->
    <div class="glass-header border-b border-white/20 pb-4 mb-4">
      <h2 class="text-xl font-bold">M-Pesa Payment</h2>
      <ProgressIndicator :status="paymentStore.currentPayment.status" />
    </div>

    <!-- Message & Instructions -->
    <div class="text-center py-6">
      <Icon :name="getStatusIcon()" class="text-4xl mb-3" />
      <p class="text-lg font-medium">{{ paymentStore.paymentMessage }}</p>
      <p class="text-sm text-gray-600 mt-2">
        Phone: {{ maskPhoneNumber(paymentStore.currentPayment.phoneNumber) }}
      </p>
    </div>

    <!-- Status Timeline -->
    <div class="glass-timeline space-y-3 mb-6">
      <TimelineStep
        status="completed"
        label="Payment initiated"
        :timestamp="paymentStartTime"
      />
      <TimelineStep
        :status="getTimelineStatus('pin')"
        label="Enter M-Pesa PIN"
      />
      <TimelineStep
        :status="getTimelineStatus('verify')"
        label="Verifying with M-Pesa"
      />
      <TimelineStep
        :status="getTimelineStatus('complete')"
        label="Payment complete"
      />
    </div>

    <!-- Error Display -->
    <div v-if="paymentError" class="glass glass-error-bg p-4 rounded-lg mb-4">
      <p class="text-sm text-red-700">{{ paymentError }}</p>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-3 mt-6">
      <GlassButton
        variant="default"
        @click="closeModal"
        :disabled="isPaymentInProgress"
      >
        Cancel
      </GlassButton>
      <GlassButton
        v-if="isFailed"
        variant="accent"
        @click="retryPayment"
      >
        Retry Payment
      </GlassButton>
    </div>
  </GlassModal>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { usePaymentStore } from '@/stores/paymentStore'

const paymentStore = usePaymentStore()
const paymentStartTime = ref(new Date())

const isPaymentInProgress = computed(() => paymentStore.isPaymentInProgress)
const paymentError = computed(() => paymentStore.currentPayment?.error)
const isFailed = computed(() =>
  paymentStore.currentPayment?.status === paymentStore.paymentStatuses.FAILED
)

function getStatusIcon() {
  const iconMap = {
    [paymentStore.paymentStatuses.INITIATING]: 'phone',
    [paymentStore.paymentStatuses.STK_SHOWN]: 'send',
    [paymentStore.paymentStatuses.AWAITING_PIN]: 'lock',
    [paymentStore.paymentStatuses.PROCESSING]: 'loader',
    [paymentStore.paymentStatuses.COMPLETED]: 'check-circle',
    [paymentStore.paymentStatuses.FAILED]: 'alert-circle',
    [paymentStore.paymentStatuses.TIMEOUT]: 'clock'
  }
  return iconMap[paymentStore.currentPayment?.status] || 'phone'
}

function getTimelineStatus(step) {
  const status = paymentStore.currentPayment?.status
  const steps = {
    pin: ['awaiting_pin', 'processing', 'completed'],
    verify: ['processing', 'completed'],
    complete: ['completed']
  }
  return steps[step].includes(status) ? 'active' : 'pending'
}

function maskPhoneNumber(phone) {
  return phone.slice(0, -4).replace(/\d/g, '*') + phone.slice(-4)
}

async function retryPayment() {
  if (!paymentStore.currentPayment) return
  await paymentStore.initiatePayment(
    paymentStore.currentPayment.bookingId,
    paymentStore.currentPayment.phoneNumber
  )
}

function closeModal() {
  // Reset payment state
  paymentStore.currentPayment = null
}
</script>
```

### 4.3 Callback Reliability & Retry Strategy

**Webhook Retry Logic:**
```python
# mpesa_tx/hooks.py

app_name = "mpesa_tx"
app_title = "M-Pesa Payment Integration"

# Webhook retry configuration
webhooks = {
    "doctype": "MPESA Callback",
    "max_retries": 5,
    "retry_backoff": [60, 300, 900, 3600, 7200],  # 1m, 5m, 15m, 1h, 2h
    "timeout": 30,
    "verify_ssl": True
}

# Schedule jobs for failed callback processing
cron_jobs = {
    'mpesa_tx.tasks.process_failed_callbacks': {
        'method': 'mpesa_tx.tasks.process_failed_callbacks',
        'cron': '*/15 * * * *'  # Every 15 minutes
    },
    'mpesa_tx.tasks.cleanup_stale_tickets': {
        'method': 'mpesa_tx.tasks.cleanup_stale_tickets',
        'cron': '0 * * * *'  # Every hour
    }
}
```

**Failed Callback Handler:**
```python
# mpesa_tx/tasks.py

def process_failed_callbacks():
    """
    Periodically process callbacks that failed initial handling.
    Retries with exponential backoff.
    """
    failed_payloads = frappe.get_list(
        'MPESA Payload',
        filters=[
            ['MPESA Payload', 'is_processed', '=', False],
            ['MPESA Payload', 'retry_count', '<', 5]
        ],
        order_by='creation asc',
        limit=100
    )

    for payload_id in failed_payloads:
        payload = frappe.get_doc('MPESA Payload', payload_id)
        try:
            payload.process_payment()
            payload.is_processed = True
            payload.save()
        except Exception as e:
            payload.retry_count = (payload.retry_count or 0) + 1
            payload.last_error = str(e)
            payload.save()


def cleanup_stale_tickets():
    """
    Clean up tickets that have been pending for >30 minutes.
    Mark as TIMEOUT and notify user.
    """
    stale_tickets = frappe.get_list(
        'MPESA Ticket',
        filters=[
            ['MPESA Ticket', 'ticket_status', '=', 'Awaiting Pin'],
            ['MPESA Ticket', 'creation', '<', frappe.utils.add_days(frappe.utils.now(), -0.021)]  # 30 mins
        ]
    )

    for ticket_id in stale_tickets:
        ticket = frappe.get_doc('MPESA Ticket', ticket_id)
        ticket.ticket_status = 'Timeout'
        ticket.save()

        # Notify user
        frappe.sendmail(
            recipients=[ticket.customer_email],
            subject='M-Pesa Payment Timeout',
            message='Your M-Pesa payment request has timed out. Please try again.'
        )
```

### 4.4 Security Hardening

**HMAC Signature Verification:**
```python
import hmac
import hashlib

def verify_mpesa_signature(payload: dict, signature: str, secret: str) -> bool:
    """
    Verify M-Pesa callback signature using HMAC-SHA256.
    Prevents spoofed callbacks.
    """
    # Extract signature payload (all fields except signature)
    payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))

    # Calculate expected signature
    expected_sig = hmac.new(
        secret.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()

    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected_sig, signature)

def validate_callback_signature():
    """Middleware to validate all incoming callbacks"""
    from flask import request

    signature = request.headers.get('X-MPESA-Signature')
    payload = request.get_json()
    secret = frappe.db.get_value('MPESA Settings', {}, 'callback_secret')

    if not verify_mpesa_signature(payload, signature, secret):
        frappe.throw('Invalid callback signature', exc=frappe.PermissionError)
```

---

## SECTION 5: IMPLEMENTATION ROADMAP

### 5.1 Phase 1: Foundation (Weeks 1-2) - 40 hours

**Backend Models (Priority 1 - Critical):**
- [ ] Create Trail DocType (location, difficulty, schedule, capacity, pricing)
- [ ] Create TrailBooking DocType (user, trail, spots, status, activities)
- [ ] Create TrailGuide DocType (user role, certifications, insurance, rating)
- [ ] Create Subscription DocType (user, tier, start_date, status, payment_method)
- [ ] Create SubscriptionPlan DocType (Basic/Premium/VIP configs)
- [ ] Create Guide Earning/Payout models
- [ ] Add Frappe User role customization (guide, premium, admin)

**Glassmorphic Design System:**
- [ ] Create glass CSS tokens & utility classes
- [ ] Build GlassCard, GlassButton, GlassPanel Vue components
- [ ] Create glass-specific design guidelines documentation
- [ ] Implement dark mode support for glass effects
- [ ] Add responsive breakpoints for glass blur effects

**MPESA Architecture:**
- [ ] Design callback state machine
- [ ] Create MPESACallbackHandler class
- [ ] Implement idempotent webhook endpoint
- [ ] Add status verification job
- [ ] Create Frappe webhook configuration

**API Endpoints (Skeleton):**
- [ ] POST /api/method/all_trails/create_trail (guide only)
- [ ] POST /api/method/all_trails/create_subscription (user)
- [ ] GET /api/method/all_trails/admin_dashboard (admin only)

**Deliverables:**
- Trail, Booking, Guide, Subscription DocTypes
- Glass UI component library (5 core components)
- MPESA callback handler with verification
- API skeleton for new features

### 5.2 Phase 2: Refactoring (Weeks 3-4)

**Frontend Refactoring:**
- [ ] Refactor TrailCard with glass effects
- [ ] Refactor TrailFilters panel to glass
- [ ] Update BookingModal with glass styling
- [ ] Create glass-based payment flow modal
- [ ] Update all form inputs to use GlassInput

**Backend Refactoring:**
- [ ] Implement callback retry job queue
- [ ] Add MPESA Ticket state machine validation
- [ ] Create failed callback cleanup jobs
- [ ] Add HMAC signature verification
- [ ] Implement idempotency checking

**Deliverables:**
- Refactored UI with glassmorphic effects
- Production-ready callback handler
- Retry & cleanup job infrastructure

### 5.3 Phase 3: Advanced Features (Weeks 5-6)

**Trail Management Enhancements:**
- [ ] Calendar-based booking system
- [ ] Advanced filtering UI
- [ ] Trail map with elevation profiles
- [ ] Trending/recommended trails carousel
- [ ] Wishlist functionality

**Payment Enhancements:**
- [ ] Real-time payment status polling UI
- [ ] Payment history dashboard
- [ ] Transaction receipt generation
- [ ] Failed payment retry flow
- [ ] Multi-currency support (future)

**Deliverables:**
- Advanced booking features
- Enhanced payment UX
- Trail discovery improvements

### 5.4 Phase 4: Testing & Optimization (Weeks 7-8)

**Testing:**
- [ ] Callback idempotency tests
- [ ] Payment state machine tests
- [ ] UI component snapshot tests
- [ ] E2E booking flow tests
- [ ] MPESA integration tests (sandbox)

**Performance:**
- [ ] Optimize glass blur rendering on mobile
- [ ] Lazy load trail images
- [ ] Implement payment polling optimization
- [ ] CSS-in-JS tree-shaking
- [ ] Bundle size analysis

**Deliverables:**
- Comprehensive test suite
- Performance benchmarks
- Production deployment checklist

---

## SECTION 6: TECHNICAL SPECIFICATIONS

### 6.1 API Endpoints

**Trail Management:**
```
GET    /api/method/all_trails/get_trails
  Params: filters, page, page_size, sort_by

GET    /api/method/all_trails/get_trail_detail/:trail_id
GET    /api/method/all_trails/get_trending_trails
GET    /api/method/all_trails/get_trail_recommendations/:user_id
```

**Booking:**
```
POST   /api/method/all_trails/create_booking
  Body: { trail_id, user_id, spots_booked, activities }

GET    /api/method/all_trails/get_user_bookings
GET    /api/method/all_trails/get_booking_detail/:booking_id
POST   /api/method/all_trails/cancel_booking/:booking_id
```

**Payment (MPESA):**
```
POST   /api/method/mpesa_tx.api.mpesa_handler/initiate_stk_transaction
  Body: { booking_id, msisdn, amount }
  Response: { ticket_id, stk_push_response }

POST   /api/method/mpesa_tx.api.callback_handler/handle_callback_webhook
  (Frappe webhook endpoint - idempotent)

GET    /api/method/mpesa_tx.api.mpesa_handler/get_stk_status
  Params: { ticket_id }
  Response: { ticket_status, transaction_ref, receipt_number }
```

### 6.2 Database Schema Extensions

**MPESA Enhancements:**
```python
# Additional fields for MPESA Ticket
mpesa_ticket = {
    'ticket_status': 'Select' -> Add 'Verified' status
    'callback_received_at': 'DateTime' -> Track callback arrival
    'callback_verified_at': 'DateTime' -> Track verification
    'retry_count': 'Int' -> Retry counter
    'last_error': 'Text' -> Error logging
    'stk_response_code': 'Data' -> Full STK response
}

# Additional fields for MPESA Payload
mpesa_payload = {
    'retry_count': 'Int' -> Default 0
    'last_error': 'Text' -> Error tracking
    'is_verified': 'Check' -> Callback verified flag
}
```

### 6.3 CSS Architecture

**Glass Effect Layers:**
1. **Base**: `--glass-bg`, `--glass-border`, `--glass-backdrop-blur`
2. **Elevation**: `--glass-shadow` for depth
3. **Interaction**: `:hover` states with increased opacity
4. **Semantic**: `glass-success-bg`, `glass-error-bg`, etc.
5. **Responsive**: Mobile blur reduction, desktop enhancement

### 6.4 State Management (Pinia)

**Store Structure:**
```
stores/
├── authStore.ts        # User authentication (existing)
├── trailsStore.ts      # Trail CRUD (existing, enhanced)
├── bookingsStore.ts    # Booking CRUD (existing, enhanced)
├── paymentStore.ts     # Payment state machine (NEW)
├── uiStore.ts          # UI state (existing)
└── filterStore.ts      # Advanced filtering (NEW)
```

---

## SECTION 7: SUCCESS CRITERIA

### 7.1 Design System
- [ ] 90%+ component pixel-perfect match to Figma glassmorphic mockups
- [ ] Glassmorphic effects work on iOS Safari, Chrome, Firefox
- [ ] Mobile performance: <16ms frame time for glass animations
- [ ] Dark mode fully supported across all components

### 7.2 MPESA Payment Flow
- [ ] 100% callback idempotency (can handle duplicate webhooks)
- [ ] 99.5%+ payment success rate with automatic retry
- [ ] Max 5-second STK push latency
- [ ] Complete audit trail for all transactions
- [ ] Callback processing <1s response time

### 7.3 Trail Discovery
- [ ] Sub-100ms filter response time
- [ ] Support 10,000+ trails with pagination
- [ ] Map rendering <2s for 100+ trail markers
- [ ] Trending/recommended trails update daily

### 7.4 User Experience
- [ ] Booking confirmation within 10 seconds of payment
- [ ] Mobile-first responsive design (all breakpoints)
- [ ] Payment status visible in real-time
- [ ] Clear error messaging for all failure scenarios
- [ ] Accessibility: WCAG 2.1 AA compliance

---

## SECTION 8: RISK MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| M-Pesa API changes | Medium | High | Version control API, wrapper abstraction, test suite |
| Glass effect browser support | Low | Medium | Progressive enhancement, feature detection |
| Payment callback loss | Low | High | Webhook retry queue, status polling, 30-min timeout |
| High traffic scaling | Medium | High | Connection pooling, caching, async job optimization |
| Data migration | Medium | Medium | Dry-run migration scripts, rollback procedures |

---

## SECTION 9: APPENDIX

### A. Design Token Reference
See: `/context/DESIGN_TOKENS.md` (detailed color, spacing, typography specs)

### B. MPESA Integration Guide
See: `/context/MPESA_INTEGRATION.md` (step-by-step setup with Safaricom)

### C. Component Library
See: `/context/COMPONENT_LIBRARY.md` (complete glass UI component catalog)

### D. API Reference
See: `/context/API_REFERENCE.md` (OpenAPI/Swagger documentation)

---

**Document Sign-Off**

| Role | Name | Date | Approval |
|------|------|------|----------|
| Product Owner | Salim | 2026-03-14 | Pending |
| Tech Lead | Claude Code | 2026-03-14 | Draft |
| Design | TBD | TBD | Pending |

