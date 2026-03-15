import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import { sanitizeAppRedirectPath } from '../utils/navigation';

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
    meta: { requiresGuest: true, hideNavigation: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../pages/Register.vue'),
    meta: { requiresGuest: true, hideNavigation: true },
  },
  {
    path: '/signup',
    redirect: '/register',
  },
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: () => import('../pages/Unauthorized.vue'),
  },
  {
    path: '/blog',
    name: 'BlogList',
    component: () => import('../pages/blog/List.vue'),
  },
  {
    path: '/blog/create',
    name: 'BlogCreate',
    component: () => import('../pages/blog/Create.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/blog/:slug',
    name: 'BlogDetail',
    component: () => import('../pages/blog/Detail.vue'),
  },
  {
    path: '/shop',
    name: 'ShopBrowse',
    component: () => import('../pages/shop/Browse.vue'),
  },
  {
    path: '/shop/cart',
    name: 'ShopCart',
    component: () => import('../pages/shop/Cart.vue'),
  },
  {
    path: '/shop/checkout',
    name: 'ShopCheckout',
    component: () => import('../pages/shop/Checkout.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/shop/payment/:orderId',
    name: 'ShopPaymentProcessing',
    component: () => import('../pages/shop/PaymentProcessing.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/shop/confirmation/:orderId',
    name: 'ShopConfirmation',
    component: () => import('../pages/shop/Confirmation.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/shop/tracking/:orderId',
    name: 'ShopTracking',
    component: () => import('../pages/shop/Tracking.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/shop/:itemCode',
    name: 'ShopDetail',
    component: () => import('../pages/shop/Detail.vue'),
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
      const redirectTo = sanitizeAppRedirectPath(to.query['redirect-to'], '/');
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
      next({ name: 'Login', query: { 'redirect-to': to.fullPath } });
      return;
    }
  }
  
  next();
});

export default router;
