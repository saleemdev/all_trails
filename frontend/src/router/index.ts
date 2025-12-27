import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/authStore';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/Home.vue'),
  },
  {
    path: '/trails',
    name: 'TrailBrowse',
    component: () => import('../pages/trails/Browse.vue'),
  },
  {
    path: '/trails/:id',
    name: 'TrailDetail',
    component: () => import('../pages/trails/Detail.vue'),
  },
  {
    path: '/trails/:id/book',
    name: 'TrailBooking',
    component: () => import('../pages/trails/Booking.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/bookings',
    name: 'BookingsList',
    component: () => import('../pages/bookings/List.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/bookings/:id',
    name: 'BookingDetail',
    component: () => import('../pages/bookings/Detail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../pages/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../pages/Login.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/blog',
    name: 'BlogList',
    component: () => import('../pages/blog/List.vue'),
  },
  {
    path: '/blog/:slug',
    name: 'BlogDetail',
    component: () => import('../pages/blog/Detail.vue'),
  },
  {
    path: '/gallery/:id',
    name: 'GalleryDetail',
    component: () => import('../pages/blog/GalleryDetail.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
];

// Router base should be /all-trails/ for routing, not the asset path
// Vite base is /assets/all_trails/frontend/ for assets, but router needs /all-trails/
const routerBase = '/all-trails/';

const router = createRouter({
  history: createWebHistory(routerBase),
  routes,
  strict: false, // Allow trailing slashes
});

// Navigation guard for protected routes
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  // If route requires guest (like login page), redirect if authenticated
  if (to.meta.requiresGuest) {
    if (!authStore.user && !authStore.isCheckingAuth) {
      await authStore.checkAuthentication();
    }
    if (authStore.isAuthenticated) {
      const redirectTo = (to.query['redirect-to'] as string) || '/all-trails/';
      next(redirectTo);
      return;
    }
    next();
    return;
  }
  
  // If route requires authentication, check auth status
  if (to.meta.requiresAuth) {
    // If we haven't checked auth yet or user is null, check authentication
    if (!authStore.user && !authStore.isCheckingAuth) {
      await authStore.checkAuthentication();
    }
    
    // If still not authenticated after check, redirect to login
    if (!authStore.isAuthenticated) {
      const redirectTo = encodeURIComponent(to.fullPath);
      next({ name: 'Login', query: { 'redirect-to': redirectTo } });
      return;
    }
  }
  
  next();
});

export default router;

