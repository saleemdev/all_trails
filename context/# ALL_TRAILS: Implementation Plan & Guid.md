# ALL_TRAILS: Implementation Plan & Guide
## Frappe App with Vue3 Frontend

---

## PROJECT OVERVIEW

**Frappe App Name**: all_trails  
**Vue App Location**: all_trails/frontend  
**Backend**: Frappe DocTypes, Doppio API, PostgreSQL  
**Frontend**: Vue 3, TypeScript, Frappe UI, Pinia, Vite  
**Build Integration**: Custom build script executed by `bench migrate`
**State Management**: Pinia (compatible with Vue3 composition API)
**UI Components**: Frappe UI (https://ui.frappe.io/)
**Authentication**: Leverage Frappe session (no custom auth needed)

### Build Architecture
- Custom build script (similar to frappe_devsecops_dashboard pattern)
- Executed automatically during `bench migrate`
- Builds Vue assets and outputs to frappe/public for serving
- Assets served by Frappe bench at `/all-trails`

---

## DESIGN SYSTEM

### Visual Identity
- **Primary**: Forest Dark (#1B3A2D) - backgrounds, navigation
- **Secondary**: Charcoal Black (#0F1419) - text, high-contrast
- **Accent**: Warm Orange (#E85D1F) - CTAs, highlights, action
- **Neutral**: Sage Gray (#8B9E8F) - secondary text, subtle elements

**Semantic Colors**:
- Success: #4CAF50
- Warning: #FFA726
- Error: #EF5350
- Info: #29B6F6

### Typography
- **Display**: Sora (weights 600, 700) - headings
- **Body**: Inter (weights 400, 500, 600) - content
- **Monospace**: JetBrains Mono - timestamps, codes

### Design Principles
- Minimalist: Every pixel serves purpose
- Clear Visual Hierarchy: Size, weight, color create priority
- Consistent Spacing: 8px grid system
- Subtle Interactions: 200ms transitions, no jarring animations
- Trust-Building: Professional, uncluttered, accessible interface
- Mobile-First: Responsive from 320px+

### Component Library
- Frappe UI components (https://ui.frappe.io/)
- Custom CSS variables for forest/orange theme
- Reusable composables: useTheme, useAsyncState, useForm
- Consistent error states, loading indicators, success feedback

---

## FRAPPE DOCTYPES (Data Models)

### 1. Trail
Core hiking event/itinerary entity.

**Key Fields**:
- title (required)
- description (rich text)
- difficulty_level (Easy/Moderate/Hard/Expert)
- location (string)
- coordinates (GPS lat,lng)
- distance_km (float)
- elevation_gain_m (integer)
- duration_hours (float)
- scheduled_date (required)
- start_time, end_time
- max_capacity (required)
- price_kshs (currency)
- host (Link to User)
- featured_image (attach image)
- route_geojson (for map visualization)
- status (Active/Cancelled/Completed)

**Custom Methods**:
- get_available_spots() - returns remaining spots
- get_bookings() - returns confirmed bookings
- validate() - ensures date >= today, capacity > 0, times valid

---

### 2. Trail Booking
User subscription/booking for a trail.

**Key Fields**:
- user (Link to User, required)
- trail (Link to Trail, required)
- booking_date (auto-set on creation)
- status (Pending/Confirmed/Cancelled/Completed)
- spots_booked (required)
- total_price (auto-calculated)
- payment_status (Pending/Completed/Failed/Refunded)
- confirmation_code (unique, auto-generated)
- cancellation_reason (optional)
- cancellation_date (optional)
- payment_id (Link to Payment DocType)

**Custom Methods**:
- validate() - check available spots, prevent double booking
- before_insert() - generate confirmation code, calculate total price
- after_insert() - send confirmation email with calendar invite
- on_update() - update cancellation_date if cancelled

---

### 3. Trail Photo
Photo archive from hiking trips.

**Key Fields**:
- user (Link to User, required)
- trail (Link to Trail, optional - auto-detect from EXIF)
- image (attach image, required)
- title (optional)
- description (optional)
- upload_date (auto-set)
- photo_date (extracted from EXIF or user-provided)
- coordinates (GPS from EXIF)
- album (Link to Trail Photo Album)
- is_public (checkbox, default true)
- tags (comma-separated)

**Custom Methods**:
- before_insert() - auto-assign album based on upload date/location, extract EXIF

---

### 4. Trail Photo Album
Smart organization of photos by date, location, or trail.

**Key Fields**:
- user (Link to User, required)
- title (required)
- description (optional)
- cover_image (attach image)
- trail (Link to Trail, optional)
- created_date (auto-set)

---

### 5. Blog Post (Extended)
Use Frappe's built-in Blog DocType with addition of:
- trail (Link to Trail) - link blog reviews to specific trails
- Enable comments system (already built into Frappe Blog)

---

## API ENDPOINTS (Frappe Whitelisted Methods)

All endpoints are Frappe whitelisted methods called from Vue via Frappe RPC or custom fetch wrapper.

### Trail Endpoints
- `get_trails(filters, page, page_size)` - Returns list of trails with pagination, filtering by difficulty/price/date/search
- `get_trail_detail(trail_id)` - Returns single trail with bookings count, reviews, comments
- `create_trail(data)` - Admin/host only, creates new trail
- `update_trail(trail_id, data)` - Admin/host only, updates trail
- `delete_trail(trail_id)` - Admin/host only, delete if no active bookings

### Booking Endpoints
- `create_booking(trail_id, spots_booked)` - Creates booking, returns confirmation code and total price
- `get_user_bookings(status)` - Returns current user's bookings (active/history/cancelled)
- `get_booking_detail(booking_id)` - Returns single booking details
- `cancel_booking(booking_id, reason)` - Cancel booking, process refund if applicable

### Payment Endpoints
- `create_payment_intent(booking_id)` - Creates Stripe PaymentIntent, returns client_secret
- `confirm_payment(intent_id)` - Confirms payment, updates booking status, sends confirmation
- `get_payment_history()` - Returns current user's transaction history

### Photo Endpoints
- `upload_photo(trail_id, title, description)` - Handle photo upload, auto-album assignment
- `get_user_photos()` - Returns current user's photos with album organization
- `get_photo_detail(photo_id)` - Returns single photo with metadata
- `get_photo_albums()` - Returns user's photo albums with cover images
- `delete_photo(photo_id)` - Delete photo

### Blog Endpoints
- `get_blog_posts(filters)` - Returns blog feed, filterable by trail, tag, author
- `get_blog_detail(slug)` - Returns single blog post with comments
- `create_blog_post(data)` - Create new blog post (markdown support)
- `update_blog_post(name, data)` - Update blog post
- `get_blog_comments(post_id)` - Get comments for post (nested threads)
- `create_blog_comment(post_id, content, parent_id)` - Add comment or reply

---

## VUE3 FRONTEND STRUCTURE

### Directory Organization

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/              (Header, Sidebar, Navigation, Footer)
│   │   ├── features/
│   │   │   ├── trails/          (TrailBrowse, TrailDetail, BookingFlow)
│   │   │   ├── bookings/        (BookingsList, BookingDetail, BookingHistory)
│   │   │   ├── photos/          (PhotoGallery, PhotoUpload, AlbumView)
│   │   │   ├── blog/            (BlogFeed, BlogDetail, BlogCreate, Comments)
│   │   │   └── auth/            (ProtectedRoute, ProfileMenu)
│   │   └── ui/                  (Custom wrappers/extensions of Frappe UI components)
│   ├── composables/
│   │   ├── useAuth.ts           (Frappe session, user state)
│   │   ├── useTrails.ts         (Fetch, filter, cache trails)
│   │   ├── useBookings.ts       (Manage bookings state)
│   │   ├── usePhotos.ts         (Photo gallery state)
│   │   └── useApi.ts            (Frappe RPC wrapper)
│   ├── stores/
│   │   ├── auth.ts              (Pinia auth store - Frappe session integration)
│   │   ├── trails.ts            (Trail list, filters, detail)
│   │   ├── bookings.ts          (User bookings, status)
│   │   ├── photos.ts            (Photo gallery, albums)
│   │   ├── blog.ts              (Blog posts, comments)
│   │   └── ui.ts                (Modals, notifications, loading)
│   ├── lib/
│   │   ├── frappe.ts            (Frappe RPC wrapper)
│   │   ├── formatters.ts        (Currency, date, distance)
│   │   └── constants.ts         (App constants, routes)
│   ├── styles/
│   │   ├── globals.css          (CSS variables, base styles)
│   │   ├── components.css       (Component-specific styles)
│   │   └── responsive.css       (Breakpoints, mobile)
│   ├── types/
│   │   └── index.ts             (TypeScript interfaces)
│   ├── pages/
│   │   ├── index.vue            (Landing/Dashboard)
│   │   ├── trails/              (Browse, Detail, Create)
│   │   ├── bookings/            (List, Detail, History)
│   │   ├── photos/              (Gallery, Detail, Upload)
│   │   ├── blog/                (Feed, Detail, Create)
│   │   └── profile/             (User profile, settings)
│   ├── router/
│   │   └── index.ts             (Vue Router with protected routes)
│   ├── App.vue                  (Main app component)
│   └── main.ts                  (Entry point)
├── index.html
├── vite.config.ts
├── tsconfig.json
├── package.json
├── build.mjs                    (Custom build script - executed by bench migrate)
├── .env
└── README.md
```

### Key Integration Points
- Frappe session is checked on app initialization via `useAuth` composable
- All API calls go through Frappe RPC wrapper (handles authentication automatically)
- Pinia stores manage Vue component state (filters, UI state, temporary data)
- Frappe manages all persistent data via DocTypes
- Protected routes check Frappe session, redirect to login if needed
- Build script runs on `bench migrate` and outputs to Frappe public folder

---

## BUILD SCRIPT INTEGRATION

### Custom Build Script (build.mjs)

The build script is executed during `bench migrate` and handles:

1. **Build Vue Assets** - Compile Vue3 + TypeScript to production bundles
2. **Output to Frappe** - Place assets in appropriate Frappe public directory
3. **Integration with Frappe** - Assets served at `/app/all-trails/frontend`
4. **Environment Configuration** - Handle Frappe bench URL, auth tokens

**Key Implementation Details**:
- Written as `build.mjs` in frontend root
- Called by `all_trails/hooks.py` in `after_migrate()` hook
- Modeled after frappe_devsecops_dashboard pattern
- Outputs manifest file for Frappe to serve assets
- Handles environment-specific configuration

### Hooks Integration

In `all_trails/hooks.py`:

```
def after_migrate():
    # Execute build script
    os.system('npm run build')
```

### Development vs Production

**Development**:
- `npm run dev` - Vite dev server on localhost:5173
- Frappe bench serves Frappe API endpoints
- CORS configured for dev environment

**Production**:
- `bench migrate` triggers build
- Vue assets bundled and minified
- Assets served by Frappe at `/app/all-trails/frontend`
- No separate dev server needed

---

## DELIVERABLES BY PHASE

### Phase 1: Core Infrastructure & Trails
**Deliverable**: Browse and book hiking trails with authenticated users

1. **Frappe Backend**
   - Trail DocType with validation, methods, status tracking
   - Trail Booking DocType with confirmation codes, payment status
   - API endpoints: get_trails, get_trail_detail, create_booking, get_user_bookings

2. **Vue3 Frontend**
   - Frappe UI theme configured (forest/orange palette)
   - Frappe session integration via useAuth composable
   - Navigation component (Sidebar desktop, Bottom nav mobile)
   - Trail browse page with filters (difficulty, price, date, search)
   - Trail detail page with map, booking form
   - Booking flow (modal-based: select spots → enter info → confirmation)
   - User dashboard showing upcoming/past bookings
   - Protected routes using Frappe session
   - Build script integrated with bench migrate

3. **User Experience**
   - Clear visual hierarchy with forest green/orange accent
   - Responsive design (mobile, tablet, desktop)
   - Loading indicators on all async operations
   - Error handling with clear messages
   - Success confirmations (toast notifications)
   - Consistent spacing and typography

---

### Phase 2: Payments & Photo Archive
**Deliverable**: Complete bookings with payment processing, smart photo management

1. **Frappe Backend**
   - Integration with Frappe Payments app
   - Payment DocType linked to Trail Booking
   - Trail Photo and Trail Photo Album DocTypes
   - API endpoints: create_payment_intent, confirm_payment, get_payment_history, upload_photo, get_user_photos, get_photo_albums

2. **Vue3 Frontend**
   - Payment modal with Stripe card integration
   - Transaction history page
   - Photo upload component (drag-drop using Frappe UI)
   - Photo gallery with grid layout
   - Smart album view (grouped by date, location, trail)
   - Photo detail modal with metadata display

3. **Smart Photo Features**
   - Auto-extract EXIF data (date, GPS location)
   - Auto-assign photos to trails based on GPS
   - Auto-create albums by month/year
   - Tag system for searching
   - Download/share functionality

---

### Phase 3: Blog & Community
**Deliverable**: User-generated content platform with reviews and discussions

1. **Frappe Backend**
   - Extended Blog DocType with trail links, comments
   - API endpoints: get_blog_posts, get_blog_detail, create_blog_post, get_blog_comments, create_blog_comment

2. **Vue3 Frontend**
   - Blog feed page (filterable by trail, tag, author)
   - Blog detail page with comments thread
   - Blog create/edit form (markdown editor, image insertion)
   - Comment system with nested replies
   - User profile with bio, photo count, trails attended
   - Leaderboard (trails completed, reviews written)

3. **Content Features**
   - Rich text editor for blog posts
   - Markdown support with preview
   - Image insertion from photo gallery
   - Comment threading (replies to specific comments)
   - Like/flag comments for moderation
   - Author mini-card on posts and comments

---

### Phase 4: Admin Tools & Polish
**Deliverable**: Admin dashboard, moderation, analytics, production-ready platform

1. **Frappe Backend**
   - Admin-only endpoints for trail management
   - Content moderation hooks
   - Analytics data aggregation
   - Email notifications (booking confirmation, comment replies, trail updates)

2. **Vue3 Frontend**
   - Admin dashboard (create/edit/delete trails)
   - User management (ban, verify, roles)
   - Content moderation queue (flag management)
   - Analytics dashboard (bookings, revenue, engagement)
   - Settings page (notifications, privacy, account)

3. **Platform Maturity**
   - Performance optimization (code splitting, lazy loading)
   - SEO optimization (meta tags, structured data)
   - Accessibility audit (WCAG AA compliance)
   - Security review (XSS, CSRF, SQL injection prevention)
   - Error handling and recovery flows
   - Rate limiting on API endpoints

---

## IMPLEMENTATION GUIDE FOR AUGMENT

### Prerequisites
1. Frappe bench setup with all_trails app
2. Frappe Payments app installed
3. Frappe Blog app available
4. Node.js 16+ with npm/pnpm
5. Vue 3, TypeScript, Frappe UI familiarity

### Setup Instructions

1. **Initialize Frontend Directory**
   ```
   cd all_trails
   mkdir frontend
   cd frontend
   ```

2. **Create package.json** with:
   - Vue 3
   - Pinia
   - Frappe UI
   - Vite
   - TypeScript
   - Vue Router

3. **Install Dependencies**
   ```
   npm install
   ```

4. **Configure Vite** (vite.config.ts):
   - Source: src/
   - Output: dist/
   - Base: /app/all-trails/frontend/
   - Proxy: dev server proxies to Frappe bench

5. **Create Build Script** (build.mjs):
   - Builds Vue assets
   - Outputs to Frappe public directory
   - Creates manifest for asset serving
   - Handles environment variables

6. **Add Bench Hook** (all_trails/hooks.py):
   - `after_migrate()` calls `npm run build`
   - Ensures assets built before serving

7. **Test Build**
   ```
   npm run build
   bench migrate
   ```

### Development Workflow

1. **Start Frappe Bench**
   ```
   bench serve
   ```

2. **Start Vite Dev Server** (in frontend/)
   ```
   npm run dev
   ```

3. **Access App**
   - Dev: http://localhost:5173
   - Frappe: http://localhost:8000

4. **Build for Production**
   ```
   npm run build
   bench migrate
   ```

### Code Organization Principles
- Keep Frappe logic in DocTypes and whitelisted methods
- Keep Vue logic in components and stores
- Use Frappe RPC for all API calls
- Never duplicate data between Frappe and Vue state
- Pinia stores are thin (filters, UI state only)
- All persistent data lives in Frappe database

### Authentication Flow
1. Vue checks Frappe session on app initialization
2. If session exists, user is authenticated via useAuth composable
3. Frappe RPC calls automatically include auth token (handled by Frappe SDK)
4. Protected routes check auth state, redirect to /app/login if needed
5. Logout redirects to Frappe logout endpoint

### Frappe UI Component Usage

Use Frappe UI components from https://ui.frappe.io/:
- Button, Card, Input, Modal, Form components
- Dropdown, Autocomplete, Badge, etc.
- Consistent with Frappe design language
- Override CSS variables for forest/orange theme

### Design Implementation
1. Configure CSS variables for forest green, orange, sage colors
2. Override Frappe UI component styles as needed
3. Use CSS variables for spacing, colors, typography
4. Ensure all interactive elements have clear hover/focus states
5. Add loading indicators during async operations
6. Show error messages in user-friendly language
7. Provide success confirmations after actions

### Pinia Store Pattern

Stores handle:
- API call orchestration
- Data caching
- Filter state
- UI state (modals, notifications)
- Computed derived state

Keep stores simple - complex logic goes in composables.

### Testing Checklist
- Responsive design on mobile, tablet, desktop
- Keyboard navigation (no mouse required)
- Screen reader compatibility (semantic HTML, aria labels)
- Error states (invalid inputs, API failures, network issues)
- Loading states (show spinners during async work)
- Success feedback (confirmations, toast notifications)
- Performance (bundle size, load time, interaction speed)
- Accessibility (color contrast, form labels, focus management)

---

## KEY TECHNICAL DECISIONS

**Why Vue3**: Component-based, performant, excellent TypeScript support, great for Frappe ecosystem, Frappe UI components are Vue3-native.

**Why Pinia**: Lightweight state management, Vue3 composition API compatible, no boilerplate, direct store mutation, superior to Vuex for modern Vue apps.

**Why Frappe UI**: Native Frappe components, consistent design language, built by Frappe team, perfect alignment with Frappe backend, accessibility-focused.

**Why Custom Build Script**: Automates build on `bench migrate`, ensures assets always in sync with code, follows Frappe ecosystem patterns, no separate deployment step.

**Why Leverage Frappe Session**: Frappe's auth is battle-tested, integrated with user management, permissions, and DocType access control. No custom auth needed, RPC calls handle tokens automatically.

**Why Composables + Stores**: Composables handle API logic, stores handle state management. Clean separation, reusable across components.

---

## HANDOFF NOTES FOR AUGMENT

1. **Start with Phase 1**: Get trails browsing and basic booking working before adding payments/photos/blog
2. **Use Frappe Console**: Test API endpoints with `frappe.call()` in browser console before wiring to Vue
3. **Component-First**: Build reusable components using Frappe UI before connecting to stores
4. **Check Frappe UI Docs**: Component API, theming, examples at https://ui.frappe.io/
5. **Responsive First**: Design mobile experience first, scale up to desktop
6. **Accessibility Matters**: Use semantic HTML, test with keyboard, check color contrast
7. **Error Handling**: Every async operation needs error state, loading indicator, user message
8. **Build Script Testing**: Verify build script works with `npm run build` and `bench migrate` locally
9. **Iterate on UX**: Test with real users early, gather feedback on clarity and trust

---

## SUCCESS CRITERIA

### Phase 1 Complete
- Users can browse trails filtered by difficulty, price, date
- Users can see trail details with map, distance, elevation
- Authenticated users can book trails
- Booking confirmation sent via email
- Upcoming bookings show on dashboard
- Mobile design is responsive and usable
- Build script executes on bench migrate

### Phase 2 Complete
- Users can pay for bookings via Stripe
- Payment success/failure is clearly communicated
- Users can upload photos from hikes
- Photos auto-organize into albums
- Users can view their photo gallery
- Transaction history is accessible

### Phase 3 Complete
- Users can write blog posts about trails
- Users can see blog feed with filters
- Users can comment on blog posts
- Comments are threaded
- User profiles show statistics
- Leaderboard ranks users by activity

### Phase 4 Complete
- Admins can manage trails (create, edit, delete)
- Admins can moderate content
- Analytics show key metrics
- Platform meets accessibility standards
- Performance is optimized
- Ready for public launch

---

**Status**: Ready for Implementation by Augment  
**Architecture**: Frappe-First, Vue3 Frontend, Pinia State Management  
**UI Framework**: Frappe UI Components  
**Build System**: Custom script, bench migrate integration  
**Aesthetic**: Minimalist Professional, Superior UX, Trust-Building  
**Focus**: Implementation, not explanation

## FRAPPE DOCTYPES (Data Models)

### 1. Trail
Core hiking event/itinerary entity.

**Key Fields**:
- title (required)
- description (rich text)
- difficulty_level (Easy/Moderate/Hard/Expert)
- location (string)
- coordinates (GPS lat,lng)
- distance_km (float)
- elevation_gain_m (integer)
- duration_hours (float)
- scheduled_date (required)
- start_time, end_time
- max_capacity (required)
- price_kshs (currency)
- host (Link to User)
- featured_image (attach image)
- route_geojson (for map visualization)
- status (Active/Cancelled/Completed)

**Custom Methods**:
- get_available_spots() - returns remaining spots
- get_bookings() - returns confirmed bookings
- validate() - ensures date >= today, capacity > 0, times valid

---

### 2. Trail Booking
User subscription/booking for a trail.

**Key Fields**:
- user (Link to User, required)
- trail (Link to Trail, required)
- booking_date (auto-set on creation)
- status (Pending/Confirmed/Cancelled/Completed)
- spots_booked (required)
- total_price (auto-calculated)
- payment_status (Pending/Completed/Failed/Refunded)
- confirmation_code (unique, auto-generated)
- cancellation_reason (optional)
- cancellation_date (optional)
- payment_id (Link to Payment DocType)

**Custom Methods**:
- validate() - check available spots, prevent double booking
- before_insert() - generate confirmation code, calculate total price
- after_insert() - send confirmation email with calendar invite
- on_update() - update cancellation_date if cancelled

---

### 3. Trail Photo
Photo archive from hiking trips.

**Key Fields**:
- user (Link to User, required)
- trail (Link to Trail, optional - auto-detect from EXIF)
- image (attach image, required)
- title (optional)
- description (optional)
- upload_date (auto-set)
- photo_date (extracted from EXIF or user-provided)
- coordinates (GPS from EXIF)
- album (Link to Trail Photo Album)
- is_public (checkbox, default true)
- tags (comma-separated)

**Custom Methods**:
- before_insert() - auto-assign album based on upload date/location, extract EXIF

---

### 4. Trail Photo Album
Smart organization of photos by date, location, or trail.

**Key Fields**:
- user (Link to User, required)
- title (required)
- description (optional)
- cover_image (attach image)
- trail (Link to Trail, optional)
- created_date (auto-set)

---

### 5. Blog Post (Extended)
Use Frappe's built-in Blog DocType with addition of:
- trail (Link to Trail) - link blog reviews to specific trails
- Enable comments system (already built into Frappe Blog)

---

## API ENDPOINTS (Frappe Whitelisted Methods)

All endpoints are Frappe whitelisted methods called from Vue3 via Frappe SDK or custom wrapper.

### Trail Endpoints
- `get_trails(filters, page, page_size)` - Returns list of trails with pagination, filtering by difficulty/price/date/search
- `get_trail_detail(trail_id)` - Returns single trail with bookings count, reviews, comments
- `create_trail(data)` - Admin/host only, creates new trail
- `update_trail(trail_id, data)` - Admin/host only, updates trail
- `delete_trail(trail_id)` - Admin/host only, delete if no active bookings

### Booking Endpoints
- `create_booking(trail_id, spots_booked)` - Creates booking, returns confirmation code and total price
- `get_user_bookings(status)` - Returns current user's bookings (active/history/cancelled)
- `get_booking_detail(booking_id)` - Returns single booking details
- `cancel_booking(booking_id, reason)` - Cancel booking, process refund if applicable

### Payment Endpoints
- `create_payment_intent(booking_id)` - Creates Stripe PaymentIntent, returns client_secret
- `confirm_payment(intent_id)` - Confirms payment, updates booking status, sends confirmation
- `get_payment_history()` - Returns current user's transaction history

### Photo Endpoints
- `upload_photo(trail_id, title, description)` - Handle photo upload, auto-album assignment
- `get_user_photos()` - Returns current user's photos with album organization
- `get_photo_detail(photo_id)` - Returns single photo with metadata
- `get_photo_albums()` - Returns user's photo albums with cover images
- `delete_photo(photo_id)` - Delete photo

### Blog Endpoints
- `get_blog_posts(filters)` - Returns blog feed, filterable by trail, tag, author
- `get_blog_detail(slug)` - Returns single blog post with comments
- `create_blog_post(data)` - Create new blog post (markdown support)
- `update_blog_post(name, data)` - Update blog post
- `get_blog_comments(post_id)` - Get comments for post (nested threads)
- `create_blog_comment(post_id, content, parent_id)` - Add comment or reply

---

## REACT FRONTEND STRUCTURE

### Directory Organization

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/              (Header, Sidebar, Navigation, Footer)
│   │   ├── features/
│   │   │   ├── trails/          (TailBrowse, TrailDetail, BookingFlow)
│   │   │   ├── bookings/        (BookingsList, BookingDetail, BookingHistory)
│   │   │   ├── photos/          (PhotoGallery, PhotoUpload, AlbumView)
│   │   │   ├── blog/            (BlogFeed, BlogDetail, BlogCreate, Comments)
│   │   │   └── auth/            (ProtectedRoute, ProfileMenu)
│   │   └── ui/                  (Button, Card, Input, Modal, Form components)
│   ├── stores/
│   │   ├── authStore.ts         (Frappe auth integration)
│   │   ├── trailStore.ts        (Trail list, filters, detail)
│   │   ├── bookingStore.ts      (User bookings, status)
│   │   ├── photoStore.ts        (Photo gallery, albums)
│   │   ├── blogStore.ts         (Blog posts, comments)
│   │   └── uiStore.ts           (Modals, notifications, loading)
│   ├── lib/
│   │   ├── frappe.ts            (Frappe SDK wrapper)
│   │   ├── api.ts               (HTTP client, interceptors)
│   │   ├── formatters.ts        (Currency, date, distance)
│   │   └── constants.ts         (App constants, routes)
│   ├── styles/
│   │   ├── globals.css          (CSS variables, base styles)
│   │   ├── components.css       (Component-specific styles)
│   │   └── responsive.css       (Breakpoints, mobile)
│   ├── types/
│   │   └── index.ts             (TypeScript interfaces)
│   ├── pages/
│   │   ├── index.tsx            (Landing/Dashboard)
│   │   ├── trails/              (Browse, Detail, Create)
│   │   ├── bookings/            (List, Detail, History)
│   │   ├── photos/              (Gallery, Detail, Upload)
│   │   ├── blog/                (Feed, Detail, Create)
│   │   └── profile/             (User profile, settings)
│   ├── App.tsx                  (Main app component)
│   └── main.tsx                 (Entry point)
├── index.html
├── vite.config.ts               (Copy from existing app)
├── tsconfig.json                (Copy from existing app)
├── package.json                 (Copy from existing app, adapt scripts)
└── .env                         (Frappe bench URL, etc.)
```

### Key Integration Points
- Frappe auth is checked on app load via `useAuthStore`
- All API calls go through Frappe whitelisted methods
- Pinia stores manage Vue3-side state (filters, UI state, temporary data)
- Frappe manages all persistent data via DocTypes
- Protected routes check Frappe session, not Vue3 state

---

## DELIVERABLES BY PHASE

### Phase 1: Core Infrastructure & Trails
**Deliverable**: Browse and book hiking trails with authenticated users

1. **Frappe Backend**
   - Trail DocType with validation, methods, status tracking
   - Trail Booking DocType with confirmation codes, payment status
   - API endpoints: get_trails, get_trail_detail, create_booking, get_user_bookings

2. **Vue3 Frontend**
   - Frappe UI theme configured (forest/orange palette)
   - Frappe auth wrapper (checks Frappe session)
   - Navigation component (Sidebar desktop, Bottom nav mobile)
   - Trail browse page with filters (difficulty, price, date, search)
   - Trail detail page with map, booking form
   - Booking flow (modal-based: select spots → enter info → confirmation)
   - User dashboard showing upcoming/past bookings
   - Protected routes using Frappe authentication

3. **User Experience**
   - Clear visual hierarchy with forest green/orange accent
   - Responsive design (mobile, tablet, desktop)
   - Loading indicators on all async operations
   - Error handling with clear messages
   - Success confirmations (toast notifications)
   - Consistent spacing and typography

---

### Phase 2: Payments & Photo Archive
**Deliverable**: Complete bookings with payment processing, smart photo management

1. **Frappe Backend**
   - Integration with Frappe Payments app
   - Payment DocType linked to Trail Booking
   - Trail Photo and Trail Photo Album DocTypes
   - API endpoints: create_payment_intent, confirm_payment, get_payment_history, upload_photo, get_user_photos, get_photo_albums

2. **Vue3 Frontend**
   - Payment modal with Stripe card integration
   - Transaction history page
   - Photo upload component (drag-drop)
   - Photo gallery with masonry layout
   - Smart album view (grouped by date, location, trail)
   - Photo detail modal with metadata display

3. **Smart Photo Features**
   - Auto-extract EXIF data (date, GPS location)
   - Auto-assign photos to trails based on GPS
   - Auto-create albums by month/year
   - Tag system for searching
   - Download/share functionality

---

### Phase 3: Blog & Community
**Deliverable**: User-generated content platform with reviews and discussions

1. **Frappe Backend**
   - Extended Blog DocType with trail links, comments
   - API endpoints: get_blog_posts, get_blog_detail, create_blog_post, get_blog_comments, create_blog_comment

2. **Vue3 Frontend**
   - Blog feed page (filterable by trail, tag, author)
   - Blog detail page with comments thread
   - Blog create/edit form (markdown editor, image insertion)
   - Comment system with nested replies
   - User profile with bio, photo count, trails attended
   - Leaderboard (trails completed, reviews written)

3. **Content Features**
   - Rich text editor for blog posts
   - Markdown support with preview
   - Image insertion from photo gallery
   - Comment threading (replies to specific comments)
   - Like/flag comments for moderation
   - Author mini-card on posts and comments

---

### Phase 4: Admin Tools & Polish
**Deliverable**: Admin dashboard, moderation, analytics, production-ready platform

1. **Frappe Backend**
   - Admin-only endpoints for trail management
   - Content moderation hooks
   - Analytics data aggregation
   - Email notifications (booking confirmation, comment replies, trail updates)

2. **Vue3 Frontend**
   - Admin dashboard (create/edit/delete trails)
   - User management (ban, verify, roles)
   - Content moderation queue (flag management)
   - Analytics dashboard (bookings, revenue, engagement)
   - Settings page (notifications, privacy, account)

3. **Platform Maturity**
   - Performance optimization (lazy loading, code splitting)
   - SEO optimization (meta tags, structured data)
   - Accessibility audit (WCAG AA compliance)
   - Security review (XSS, CSRF, SQL injection prevention)
   - Error handling and recovery flows
   - Rate limiting on API endpoints

---

## IMPLEMENTATION GUIDE FOR AUGMENT

### Prerequisites
1. Frappe bench setup with all_trails app
2. Frappe Payments app installed
3. Frappe Blog app available
4. Existing Frappe app with vite setup available for copying
5. Vue3 18, TypeScript, Frappe UI familiarity

### Setup Instructions
1. Copy vite.config.ts, tsconfig.json, package.json, .env setup from existing app to frontend/
2. Adapt paths in vite.config.ts to reference all_trails app correctly
3. Install frontend dependencies: `npm install`
4. Verify build script works: `npm run build`
5. Verify dev server starts: `npm run dev`

### Development Workflow
1. Start Frappe bench: `bench serve`
2. Start Vite dev server in frontend/: `npm run dev`
3. Access Vue3 app at `http://localhost:5173` (or Vite dev port)
4. Access Frappe at `http://localhost:8000`
5. Build Vue3 for production: `npm run build`
6. Frappe automatically serves built frontend at /app/all-trails

### Code Organization Principles
- Keep Frappe logic in DocTypes and whitelisted methods
- Keep Vue3 logic in components and Pinia stores
- Use Frappe SDK or custom wrapper for all API calls
- Never duplicate data between Frappe and Vue3 state
- Pinia stores should be thin (filtering, UI state only)
- All persistent data lives in Frappe database

### Authentication Flow
1. Vue3 checks Frappe session on app load
2. If session exists, user is authenticated (no separate login needed)
3. Protected routes check Frappe session, redirect to /app/login if not authenticated
4. All API calls automatically include Frappe auth token
5. Logout redirects to Frappe logout endpoint

### Design Implementation
1. Configure Frappe UI theme with forest green primary, orange accent
2. Override component styles to match minimalist aesthetic
3. Use CSS variables for spacing, colors, typography
4. Ensure all interactive elements have clear hover/focus states
5. Add loading indicators during async operations
6. Show error messages in user-friendly language
7. Provide success confirmations after actions

### Testing Checklist
- Responsive design on mobile, tablet, desktop
- Keyboard navigation (no mouse required)
- Screen reader compatibility (semantic HTML, aria labels)
- Error states (invalid inputs, API failures, network issues)
- Loading states (show spinners during async work)
- Success feedback (confirmations, toast notifications)
- Performance (bundle size, load time, interaction speed)
- Accessibility (color contrast, form labels, focus management)

---

## KEY TECHNICAL DECISIONS

**Why Frappe-First**: All data models, validation, permissions, and business logic live in Frappe. Vue3 is purely presentational. This ensures single source of truth and leverages Frappe's built-in features.

**Why Pinia**: Minimal boilerplate, no providers, perfect for thin client-side state. Frappe handles persistence.

**Why Frappe UI**: Professional component library with excellent accessibility, theming, and built-in features (form validation, modals, tables). Theme customization supports minimalist forest/orange aesthetic.

**Why Copy Existing Setup**: Prevents re-engineering auth, vite, build scripts, environment configs that are already working in your other Frappe app.

**Why Leverage Frappe Auth**: Frappe's authentication is battle-tested, integrated with user management, permissions, and DocType access control. No need for custom auth logic.

---

## HANDOFF NOTES FOR AUGMENT

1. **Start with Phase 1**: Get trails browsing and basic booking working before adding payments/photos/blog
2. **Use Frappe Console**: Test API endpoints with `frappe.call()` in browser console before wiring to Vue3
3. **Component-First**: Build reusable UI components in isolation before connecting to stores
4. **Check Frappe Docs**: For DocType setup, whitelisting, permissions - Frappe docs are authoritative
5. **Responsive First**: Design mobile experience first, scale up to desktop
6. **Accessibility Matters**: Use semantic HTML, test with keyboard, check color contrast
7. **Error Handling**: Every async operation needs error state, loading indicator, user message
8. **Iterate on UX**: Test with real users early, gather feedback on clarity and trust

---

## SUCCESS CRITERIA

### Phase 1 Complete
- Users can browse trails filtered by difficulty, price, date
- Users can see trail details with map, distance, elevation
- Authenticated users can book trails
- Booking confirmation sent via email
- Upcoming bookings show on dashboard
- Mobile design is responsive and usable

### Phase 2 Complete
- Users can pay for bookings via Stripe
- Payment success/failure is clearly communicated
- Users can upload photos from hikes
- Photos auto-organize into albums
- Users can view their photo gallery
- Transaction history is accessible

### Phase 3 Complete
- Users can write blog posts about trails
- Users can see blog feed with filters
- Users can comment on blog posts
- Comments are threaded
- User profiles show statistics
- Leaderboard ranks users by activity

### Phase 4 Complete
- Admins can manage trails (create, edit, delete)
- Admins can moderate content
- Analytics show key metrics
- Platform meets accessibility standards
- Performance is optimized
- Ready for public launch

---

**Status**: Ready for Implementation by Augment  
**Architecture**: Frappe-First, Vue3 Frontend, Pinia State Management  
**Aesthetic**: Minimalist Professional, Superior UX, Trust-Building  
**Focus**: Implementation, not explanation