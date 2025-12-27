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
    path: '/all-trails',
    redirect: '/',
  },
  {
    path: '/all-trails/',
    redirect: '/',
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
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Navigation guard for protected routes
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redirect to Frappe login
    window.location.href = '/app/login';
  } else {
    next();
  }
});

export default router;

