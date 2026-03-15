# BRD Addendum: Complete Personas & Missing Features

**Date**: 2026-03-14
**Status**: Research Complete
**Scope**: Adds 4 critical missing personas and features to original BRD

---

## EXECUTIVE SUMMARY

The original BRD was missing critical user personas and features:

### ❌ What Was Missing
- ❌ Guide/Host interface & trail creation
- ❌ Admin/Platform management dashboard
- ❌ Membership/subscription system
- ❌ User registration/signup flow
- ❌ Premium features & exclusive access

### ✅ What This Addendum Provides
- ✅ Complete persona analysis (6 total types)
- ✅ Guide Dashboard specification with full feature list
- ✅ Admin Dashboard specification with moderation tools
- ✅ Membership tier structure (Free/Premium/VIP)
- ✅ Updated implementation roadmap (revised phases 1-4)
- ✅ Database schema requirements for new features
- ✅ API endpoint specifications
- ✅ Frontend page/component list

---

## COMPLETE PERSONA MATRIX

### Persona 1: Anonymous Visitor
**Current Status**: ✅ FULLY IMPLEMENTED (Frontend only)
**Key Pages**: Home, Browse, Detail, Blog, Gallery
**Actions**: Search trails, read blog, view photos
**Missing**: Account signup, wishlist, email newsletter

---

### Persona 2: Registered Member (Hiker)
**Current Status**: ⚠️ PARTIALLY IMPLEMENTED
**Implemented**: Auth, browse, booking UI, profile page
**Missing**:
- User registration/signup form
- Profile image upload
- Dietary preferences & emergency contact
- Skill level assessment
- Wishlist/saved trails
- Trail reviews & ratings
- Email notifications
- Membership tier system

---

### Persona 3: Trail Guide/Host ⚠️ CRITICAL - NOT IMPLEMENTED
**Current Status**: ❌ NOT IMPLEMENTED
**Importance**: CRITICAL (revenue depends on this)
**Missing Dashboard Sections**:
```
Guide Dashboard
├── Stats: Hikes Led, Earnings, Rating
├── Calendar: All scheduled hikes
├── Upcoming Hikes: Participant counts, status
├── Trail Management: Create, edit, archive trails
├── Schedule Management: Set dates, manage capacity
├── Participant Tracking: Check-ins, contact info
├── Earnings Tracker: Monthly breakdown, payouts
├── Reviews & Ratings: Guide reputation
└── Settings: Bank details, certifications
```

**Guide Use Cases**:
1. Guide signs up → Uploads certifications → Waits for admin approval
2. Approval complete → Dashboard activated
3. Guide creates new trail → Sets schedule, capacity, price
4. Hike day → App shows participants → Mark attendance
5. End of month → Request payout → Receives KES to bank account

**Database Models Needed**:
```python
# New DocTypes
TrailGuide:
  - user (Link to User)
  - full_name, bio, profile_image
  - certifications[] (table: name, url, expiry_date)
  - insurance_document_url
  - bank_account_number
  - payout_frequency (weekly/monthly)
  - approval_status (pending/approved/rejected)
  - rating (avg stars from reviews)
  - total_hikes_led
  - reviews[] (table: rating, text, user, date)

GuideEarning:
  - guide (Link to TrailGuide)
  - booking (Link to TrailBooking)
  - amount
  - commission_rate
  - earned_amount
  - payout_status (pending/processed)
  - date

GuidePayout:
  - guide (Link to TrailGuide)
  - amount
  - bank_account
  - status (requested/processing/completed)
  - date_requested
  - date_processed
  - reference_number
```

**API Endpoints Needed**:
```
Guide Authentication & Profile:
POST   /api/method/all_trails/guide_register
GET    /api/method/all_trails/guide_profile
PUT    /api/method/all_trails/guide_profile

Trail Management:
POST   /api/method/all_trails/create_trail
GET    /api/method/all_trails/guide_trails
PUT    /api/method/all_trails/update_trail/:trail_id
DELETE /api/method/all_trails/archive_trail/:trail_id

Hike Management:
GET    /api/method/all_trails/guide_upcoming_hikes
POST   /api/method/all_trails/add_hike_date/:trail_id
GET    /api/method/all_trails/hike_participants/:hike_id
POST   /api/method/all_trails/checkin_participant/:hike_id

Earnings & Payouts:
GET    /api/method/all_trails/guide_earnings
GET    /api/method/all_trails/guide_payouts
POST   /api/method/all_trails/request_payout
```

**Frontend Pages/Components Needed**:
```
pages/
├── guide/
│   ├── Dashboard.vue          ← Main stats & upcoming
│   ├── TrailCreation.vue      ← Multi-step form
│   ├── TrailManagement.vue    ← List, edit, archive
│   ├── ScheduleManager.vue    ← Add/manage hike dates
│   ├── HikeDay.vue            ← Participant check-in
│   ├── Earnings.vue           ← Revenue dashboard
│   ├── Payouts.vue            ← Payout history
│   └── Profile.vue            ← Guide profile settings

components/features/guide/
├── GuideStats.vue             ← 4-card stats
├── UpcomingHikesCard.vue      ← Hike calendar
├── TrailForm.vue              ← Trail creation form
├── ParticipantList.vue        ← Check-in list
├── EarningsChart.vue          ← Revenue trends
└── PayoutRequestModal.vue     ← Payout request
```

---

### Persona 4: Instructor/Lead (On-Trail)
**Current Status**: ❌ NOT IMPLEMENTED
**Importance**: MEDIUM (safety-critical)
**Role**: Active during hike to guide participants

**Key Features**:
- Real-time location sharing
- Participant tracking
- Emergency alerts
- Photo uploads during hike
- Group messaging
- Weather monitoring
- Time tracking

**Implementation**: Subset of Guide role, role-based access control

---

### Persona 5: Premium/VIP Member ⚠️ CRITICAL - NOT IMPLEMENTED
**Current Status**: ❌ NOT IMPLEMENTED
**Importance**: CRITICAL (revenue stream)

**Subscription Tiers**:

#### Basic (Free)
- Price: FREE
- Discount: 0%
- Perks: None
- Use Case: Casual explorers

#### Premium
- Price: KES 999/month
- Discount: 20% off all bookings
- Perks:
  - Priority booking (48hr early access)
  - 3 free cancellations per month
  - Member-only exclusive trails
  - Birthday bonus: +10% discount
- Use Case: Regular hikers (1-3 bookings/month)

#### VIP
- Price: KES 4,999/month
- Discount: 35% off all bookings
- Perks:
  - Priority support (1-hour response)
  - Personal recommendations
  - VIP guides only (5-star rated)
  - Unlimited rescheduling
  - Free insurance on all hikes
  - Quarterly VIP-only events
- Use Case: Serious hikers (4+ bookings/month)

**Database Models Needed**:
```python
SubscriptionPlan:
  - name (Basic/Premium/VIP)
  - price
  - discount_percentage
  - features[] (table: name, description)
  - max_free_cancellations
  - access_to_exclusive_trails
  - priority_booking_days
  - is_active

UserSubscription:
  - user (Link to User)
  - plan (Link to SubscriptionPlan)
  - start_date
  - renewal_date
  - status (active/cancelled/expired)
  - payment_method (mpesa/stripe)
  - auto_renew
  - cancellation_date
  - cancellation_reason
```

**Billing & Subscription Logic**:
```python
# Recurring billing with retries
- Monthly auto-charge on renewal_date
- Failed payment → Retry 3x (day 1, 3, 5)
- Max failures → Downgrade to free tier
- Downgrade effective next billing cycle
- Upgrade → Immediate pro-rata charge

# Discount Application
Trail Price: KES 2,000
├── Basic Member → KES 2,000 (0% discount)
├── Premium Member → KES 1,600 (-20%)
└── VIP Member → KES 1,300 (-35%)

# Member-Only Trails
- Marked as "Premium Only" or "VIP Only"
- Non-members: See placeholder with "Upgrade to access"
- Typically higher-end, exclusive experiences
```

**API Endpoints Needed**:
```
Subscription Management:
GET    /api/method/all_trails/subscription_plans
POST   /api/method/all_trails/create_subscription
GET    /api/method/all_trails/user_subscription
PUT    /api/method/all_trails/upgrade_subscription
PUT    /api/method/all_trails/downgrade_subscription
POST   /api/method/all_trails/cancel_subscription
GET    /api/method/all_trails/billing_history

Discount Calculation:
GET    /api/method/all_trails/calculate_trail_price/:trail_id
  (applies subscription discount if applicable)
```

**Frontend Pages/Components Needed**:
```
pages/
├── membership/
│   ├── Plans.vue              ← Show 3 tiers with features
│   ├── Checkout.vue           ← Payment flow
│   └── Management.vue         ← View/upgrade/cancel

components/features/membership/
├── PlanCard.vue               ← Single plan with CTA
├── FeaturesList.vue           ← Plan features checklist
├── SubscriptionCheckout.vue   ← Payment method selection
├── BillingHistory.vue         ← Past charges
└── MembershipBadge.vue        ← Show on profile/cards
```

---

### Persona 6: Admin/Platform Manager ⚠️ CRITICAL - NOT IMPLEMENTED
**Current Status**: ❌ NOT IMPLEMENTED
**Importance**: CRITICAL (platform governance)

**Admin Dashboard Sections**:

#### Home/Overview
```
Stats Bar (Top):
├── Total Users: 1,234
├── Active Guides: 45
├── Total Trails: 78
└── Platform Revenue: KES 345,670

Pending Items:
├── Guide Applications: 3 pending
├── Trail Approvals: 2 pending
├── User Reports: 1 pending

System Health:
├── Payment Success Rate: 99.2%
├── API Response Time: 156ms
├── Email Delivery: 99.2%
└── Background Jobs: 234/234 completed
```

#### User Management
- Search/filter users
- View profiles & activity
- Suspend accounts
- View support tickets
- Ban users

#### Guide Approval Workflow
- List pending guide applications
- Review certifications & insurance
- Approve or request more info
- Reject with explanation
- Status email notifications

#### Trail Moderation
- Pending trail approvals
- Flagged/reported trails
- Participant feedback analysis
- Temporary disable trails
- Permanent removal if needed

#### Payment Monitoring
- Today's transactions
- Failed payment queue (auto-retry)
- MPESA callback health
- Failed callback handling

#### Payout Management
- Pending payout requests
- Batch processing
- Payout history
- Dispute resolution

#### Analytics
- Revenue trends (daily/weekly/monthly)
- User growth charts
- Guide performance
- Top trails by bookings
- Membership conversion rate

#### System Settings
- Commission rate (guide % vs platform %)
- Minimum payout threshold
- Subscription pricing tiers
- Email templates
- Feature toggles

**Database Models Needed**:
```python
AdminSettings:
  - guide_commission_percentage
  - platform_commission_percentage
  - minimum_payout_threshold
  - email_notification_settings
  - featured_trail_count
  - guide_approval_required

GuideApplication:
  - user (Link to User)
  - status (pending/approved/rejected)
  - submitted_date
  - reviewed_date
  - reviewed_by (Link to admin User)
  - certifications_verified
  - insurance_verified
  - rejection_reason
  - notes

TrailReport:
  - trail (Link to Trail)
  - reported_by (Link to User)
  - reason (safety/misleading/inappropriate)
  - description
  - resolved (yes/no)
  - resolution (disabled/deleted/none)
  - resolved_by (Link to admin User)
  - resolved_date

SupportTicket:
  - user (Link to User)
  - subject
  - description
  - category (payment/booking/guide/other)
  - status (open/in_progress/resolved)
  - created_date
  - assigned_to (Link to admin User)
  - resolution_notes
```

**API Endpoints Needed**:
```
Admin Dashboard:
GET    /api/method/all_trails/admin_dashboard
  (returns stats, pending counts, recent activity)

User Management:
GET    /api/method/all_trails/admin_users
POST   /api/method/all_trails/admin_suspend_user/:user_id
POST   /api/method/all_trails/admin_unsuspend_user/:user_id

Guide Approvals:
GET    /api/method/all_trails/admin_guide_applications
POST   /api/method/all_trails/admin_approve_guide/:guide_id
POST   /api/method/all_trails/admin_reject_guide/:guide_id

Trail Moderation:
GET    /api/method/all_trails/admin_pending_trails
GET    /api/method/all_trails/admin_flagged_trails
POST   /api/method/all_trails/admin_approve_trail/:trail_id
POST   /api/method/all_trails/admin_disable_trail/:trail_id
POST   /api/method/all_trails/admin_delete_trail/:trail_id

Payment Monitoring:
GET    /api/method/all_trails/admin_payments
  (today's transactions, failures, queue status)
GET    /api/method/all_trails/admin_payment_queue

Payout Management:
GET    /api/method/all_trails/admin_pending_payouts
POST   /api/method/all_trails/admin_process_payouts
GET    /api/method/all_trails/admin_payout_history

Analytics:
GET    /api/method/all_trails/admin_analytics
  (revenue, users, guides, subscription metrics)

Support Tickets:
GET    /api/method/all_trails/admin_support_tickets
POST   /api/method/all_trails/admin_resolve_ticket/:ticket_id
```

**Frontend Pages/Components Needed**:
```
pages/admin/
├── Dashboard.vue              ← Stats, pending items, health
├── Users.vue                  ← User management
├── GuideApplications.vue      ← Approve guides
├── TrailModeration.vue        ← Approve/flag trails
├── Payments.vue               ← Payment monitoring
├── Payouts.vue                ← Payout processing
├── Analytics.vue              ← Charts & reports
├── Settings.vue               ← System configuration
└── SupportTickets.vue         ← Help desk

components/features/admin/
├── StatsCard.vue              ← Stat with trend
├── PendingApprovals.vue       ← List of pending items
├── UserTable.vue              ← Searchable user list
├── GuideApplicationCard.vue   ← Review single application
├── TrailModerationCard.vue    ← Review/flag single trail
├── PaymentMonitor.vue         ← Transaction status
├── AnalyticsChart.vue         ← Revenue/user trends
└── AdminSidebar.vue           ← Admin-only navigation
```

---

## REVISED IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Weeks 1-2) - 40 hours

**Priority: Critical Backend Models + Design System**

**Backend:**
- [ ] Create 5 new DocTypes: Trail, TrailBooking, TrailGuide, SubscriptionPlan, UserSubscription
- [ ] Create payment models: GuideEarning, GuidePayout
- [ ] Setup Frappe User roles: guide_user, premium_member, admin
- [ ] Design database schema & relationships

**Frontend - Design System:**
- [ ] Glassmorphic CSS framework
- [ ] 5 base glass components

**Deliverables:**
- Complete database schema
- Glass UI component library
- MPESA callback handler (from original BRD)

---

### Phase 2: Core Interfaces (Weeks 3-4) - 80 hours

**Priority: Guide Dashboard + Admin Dashboard + Membership System**

**Guide Interface** (40 hours):
- [ ] Guide Dashboard (stats, calendar, upcoming hikes)
- [ ] TrailCreation wizard (5-step form)
- [ ] TrailManagement (list, edit, archive)
- [ ] ParticipantCheckin interface
- [ ] EarningsTracker with payout requests
- [ ] Guide profile with certifications

**Admin Interface** (25 hours):
- [ ] Admin Dashboard (stats, pending items)
- [ ] UserManagement (list, suspend, view history)
- [ ] GuideApprovalWorkflow
- [ ] TrailModerationQueue
- [ ] PaymentMonitoring + Payout processing
- [ ] BasicAnalyticsDashboard

**Membership System** (15 hours):
- [ ] SubscriptionPlans page (show 3 tiers)
- [ ] SubscriptionCheckout (select plan → payment)
- [ ] Discount calculation & application logic
- [ ] Member-only trail badges
- [ ] SubscriptionManagement (upgrade/downgrade/cancel)

**Backend:**
- [ ] CRUD APIs for Trail, TrailBooking, Subscription
- [ ] Guide approval workflows
- [ ] Discount calculation logic
- [ ] Subscription billing logic (auto-charge, retry)
- [ ] Admin approval/moderation endpoints
- [ ] Analytics data aggregation

**Deliverables:**
- Full Guide Dashboard
- Full Admin Dashboard
- Membership & subscription system
- All new API endpoints

---

### Phase 3: Advanced Features (Weeks 5-6) - 50 hours

**Priority: Enhanced Features + Real-Time + Notifications**

- [ ] Real-time location tracking on hikes
- [ ] Guide approval email notifications
- [ ] Subscription auto-renewal & failure handling
- [ ] Trail reviews & ratings system
- [ ] Trending trails display
- [ ] Personalized trail recommendations
- [ ] Email notifications for bookings/payouts/approvals
- [ ] Support ticket system
- [ ] Member-only exclusive events

**Deliverables:**
- Real-time hike tracking
- Notification system (email + in-app)
- Enhanced analytics & reporting

---

### Phase 4: Testing & Optimization (Weeks 7-8) - 50 hours

**Priority: Quality, Performance, Security**

- [ ] E2E tests for guide workflows
- [ ] E2E tests for admin workflows
- [ ] E2E tests for subscription flows
- [ ] Payment scenario testing
- [ ] Load testing (1000+ concurrent users)
- [ ] Security audit (payment data, admin access)
- [ ] Performance optimization
- [ ] Browser compatibility testing

**Deliverables:**
- Comprehensive test suite (>80% coverage)
- Performance benchmarks
- Security validation
- Production deployment checklist

---

## CRITICAL IMPLEMENTATION NOTES

### Database Schema Priorities
1. **Week 1**: Trail, TrailBooking, TrailGuide, SubscriptionPlan, UserSubscription
2. **Week 1**: GuideEarning, GuidePayout, GuideApplication
3. **Week 2**: TrailReport, SupportTicket, AdminSettings

### API Endpoint Priorities
1. **Week 2**: Guide CRUD (create, update trail)
2. **Week 2**: Admin approval endpoints
3. **Week 3**: Subscription creation & renewal
4. **Week 3**: Dashboard data endpoints

### Frontend Page Priorities
1. **Week 2**: Guide Dashboard (critical for guide signup)
2. **Week 2**: Admin Dashboard (critical for approvals)
3. **Week 3**: Subscription Plans page
4. **Week 3**: TrailCreation wizard

---

## RESOURCE ALLOCATION RECOMMENDATION

| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Total |
|------|---------|---------|---------|---------|-------|
| **Backend Dev** | 20h | 35h | 15h | 10h | **80h** |
| **Frontend Dev** | 15h | 35h | 20h | 15h | **85h** |
| **DevOps/QA** | 5h | 10h | 10h | 25h | **50h** |
| **Product** | 5h | 5h | 5h | 0h | **15h** |
| **Total** | **45h** | **85h** | **50h** | **50h** | **230h** |

---

## SUCCESS METRICS FOR NEW FEATURES

### Guide Interface
- ✅ Guides can create trails in <5 minutes
- ✅ Dashboard loads in <2 seconds
- ✅ 50+ guides activated in first month
- ✅ Average guide rating >4.0 stars

### Admin Interface
- ✅ Admin approval time <2 hours for guides
- ✅ Trail moderation time <1 hour for submissions
- ✅ Zero payment disputes unresolved >7 days

### Membership System
- ✅ 10%+ of users convert to Premium in first month
- ✅ Premium member LTV 5x higher than free users
- ✅ Subscription churn <5% monthly

---

## RISK MITIGATION FOR NEW FEATURES

| Feature | Risk | Mitigation |
|---------|------|-----------|
| Guide Dashboard | Complexity, performance | MVP with essential features only |
| Subscription Billing | Payment failures | 3x retry + fallback notifications |
| Admin Moderation | Approval bottleneck | Clear criteria, auto-approve some |
| Real-time Tracking | Mobile battery drain | Optional feature, compression |

---

## REFERENCES

- Event Management reference: `/bhushanrevankar/event_management` (Context7)
- Stripe Subscription: `/stripe-samples/checkout-single-subscription` (Context7)
- Original BRD: `/context/BRD.md`

