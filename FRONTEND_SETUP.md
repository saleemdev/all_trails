# ALL_TRAILS Frontend Setup Guide

## Overview

The ALL_TRAILS frontend is a Vue 3 application with TypeScript, Pinia state management, and Vue Router. It uses mock data initially and is designed to seamlessly transition to real APIs in Phase 2.

## Build Integration

The frontend is automatically built when you run `bench migrate`:

```bash
cd /home/erpuser/frappe-bench
bench migrate
```

This triggers the `after_migrate` hook in `hooks.py` which:
1. Runs `npm install` (if needed)
2. Runs `npm run build` to compile the Vue application
3. Outputs assets to `apps/all_trails/all_trails/public/frontend/`

## Frontend Assets

After building, the following assets are available:

- **HTML**: `apps/all_trails/all_trails/public/frontend/index.html`
- **JavaScript**: `apps/all_trails/all_trails/public/frontend/js/`
- **CSS**: `apps/all_trails/all_trails/public/frontend/css/`

## Accessing the Frontend

### Development Mode

For development with hot reload:

```bash
cd apps/all_trails/frontend
npm run dev
```

This starts a Vite dev server at `http://localhost:5173`

### Production Mode

The built frontend is served from the Frappe public directory. To access it:

1. Ensure `bench migrate` has been run
2. Start the Frappe bench: `bench start`
3. Access the frontend at: `http://localhost:8000/app/all-trails/frontend/`

## Project Structure

```
apps/all_trails/frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Navigation.vue      # Main navigation component
│   │   │   └── Notifications.vue   # Notification system
│   │   └── features/
│   │       └── trails/
│   │           ├── TrailCard.vue   # Trail card component
│   │           └── BookingModal.vue # Booking modal
│   ├── pages/
│   │   ├── Home.vue                # Landing page
│   │   ├── Profile.vue             # User profile
│   │   ├── trails/
│   │   │   ├── Browse.vue          # Trail listing
│   │   │   └── Detail.vue          # Trail details
│   │   └── bookings/
│   │       ├── List.vue            # User bookings
│   │       └── Detail.vue          # Booking details
│   ├── stores/
│   │   ├── authStore.ts            # Authentication state
│   │   ├── trailsStore.ts          # Trails state
│   │   ├── bookingsStore.ts        # Bookings state
│   │   └── uiStore.ts              # UI state (modals, notifications)
│   ├── services/
│   │   ├── api.ts                  # API service layer
│   │   └── mockData.ts             # Mock data for development
│   ├── router/
│   │   └── index.ts                # Vue Router configuration
│   ├── types/
│   │   └── index.ts                # TypeScript type definitions
│   ├── styles/
│   │   └── globals.css             # Global styles & design system
│   ├── App.vue                     # Root component
│   └── main.ts                     # Application entry point
├── vite.config.ts                  # Vite configuration
├── tsconfig.json                   # TypeScript configuration
├── package.json                    # Dependencies
└── index.html                      # HTML template
```

## Design System

The frontend uses a comprehensive design system with CSS variables:

### Colors
- **Primary**: Forest Dark (#1B3A2D)
- **Secondary**: Charcoal Black (#0F1419)
- **Accent**: Warm Orange (#E85D1F)
- **Neutral**: Sage Gray (#8B9E8F)

### Spacing
- 8px grid system (xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px)

### Typography
- **Display**: Sora font
- **Body**: Inter font
- **Code**: JetBrains Mono

## Mock Data

The application uses mock data for development. To switch to real APIs:

1. Update `USE_MOCK_DATA` flag in `src/services/api.ts` to `false`
2. Implement real API endpoints in the backend
3. Update the API service methods to call real endpoints

## State Management

The application uses Pinia for state management:

- **authStore**: User authentication and session
- **trailsStore**: Trail list, filtering, and details
- **bookingsStore**: User bookings management
- **uiStore**: Modal and notification state

## Routing

Vue Router is configured with protected routes:

- `/` - Home page (public)
- `/trails` - Trail browse (public)
- `/trails/:id` - Trail details (public)
- `/bookings` - User bookings (protected)
- `/bookings/:id` - Booking details (protected)
- `/profile` - User profile (protected)

Protected routes redirect to `/app/login` if not authenticated.

## Development Workflow

1. **Install dependencies**: `npm install`
2. **Start dev server**: `npm run dev`
3. **Build for production**: `npm run build`
4. **Preview production build**: `npm run preview`

## Troubleshooting

### Build fails with TypeScript errors
- Ensure all type imports use `type` keyword
- Check that all unused variables are removed
- Run `npm run build` to see full error messages

### Frontend not loading after migrate
- Check that `apps/all_trails/all_trails/public/frontend/` directory exists
- Verify `index.html` and asset files are present
- Check browser console for 404 errors on asset paths

### Mock data not loading
- Verify `USE_MOCK_DATA` is set to `true` in `src/services/api.ts`
- Check browser console for errors
- Ensure Pinia stores are initialized correctly

## Next Steps (Phase 2)

When ready to implement real APIs:

1. Create Frappe DocTypes (Trail, TrailBooking, etc.)
2. Implement API endpoints in `all_trails/api/`
3. Update `src/services/api.ts` to call real endpoints
4. Implement authentication with Frappe session
5. Add payment integration
6. Implement photo upload functionality

