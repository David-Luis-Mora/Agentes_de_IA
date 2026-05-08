import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Home from '../views/Home.vue';
import ProfileSetup from '../views/ProfileSetup.vue';
import Routine from '../views/Routine.vue';
import Profile from '../views/Profile.vue';

import ExerciseView from '../views/ExerciseView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/routine',
    name: 'Routine',
    component: Routine,
    meta: { requiresAuth: true }
  },
  {
    path: '/exercise/:id',
    name: 'ExerciseView',
    component: ExerciseView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/profile-setup',
    name: 'ProfileSetup',
    component: ProfileSetup,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
];


const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  if (authStore.loading) {
    await authStore.checkUser();
  }

  const isAuthenticated = !!authStore.user;
  const isRequiresAuth = to.meta.requiresAuth;

  if (isRequiresAuth && !isAuthenticated) {
    return next('/login');
  }

  // Redirect to profile setup if profile is incomplete, 
  // unless we are already going to profile-setup or login/register
  if (isAuthenticated && authStore.isNewProfile && to.name !== 'ProfileSetup' && to.name !== 'Login' && to.name !== 'Register') {
    return next('/profile-setup');
  }

  // If already setup and trying to go to setup, go home
  if (isAuthenticated && !authStore.isNewProfile && to.name === 'ProfileSetup') {
    return next('/');
  }

  next();
});

export default router;
