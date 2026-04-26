<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-logo">
        <Dumbbell :size="28" class="logo-icon" />
        <span>GymAI</span>
      </router-link>

      <div class="navbar-links">
        <template v-if="authStore.user">
          <router-link to="/routine" class="nav-link">
            <Calendar :size="20" />
            <span>Rutina</span>
          </router-link>
          <router-link to="/profile" class="nav-link">
            <User :size="20" />
            <span>{{ authStore.user.username }}</span>
          </router-link>
          <button @click="handleLogout" class="logout-btn">
            <LogOut :size="20" />
            <span>Logout</span>
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="register-btn">Join Now</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { Dumbbell, LogOut, User, Calendar } from 'lucide-vue-next';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.navbar {
  height: 70px;
  background: var(--glass);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
}

.navbar-container {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--text-main);
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.logo-icon {
  color: var(--primary);
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: var(--text-muted);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s;
}

.nav-link:hover {
  color: var(--text-main);
}

.register-btn {
  background: var(--primary);
  color: white;
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}

.register-btn:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.logout-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  transition: color 0.2s;
}

.logout-btn:hover {
  color: var(--error);
}
</style>
