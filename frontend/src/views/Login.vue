<template>
  <div class="auth-page animate-fade-in">
    <div class="auth-card">
      <div class="auth-header">
        <div class="auth-icon">
          <LogIn :size="32" />
        </div>
        <h1>Welcome Back</h1>
        <p>Enter your credentials to access your coach</p>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <div class="form-group">
          <label>Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Enter your username"
            required
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            required
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          <Loader2 v-if="loading" class="spinner" />
          <span v-else>Sign In</span>
        </button>
      </form>

      <div class="auth-footer">
        Don't have an account? <router-link to="/register">Create one</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { LogIn, Loader2 } from 'lucide-vue-next';

const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const handleSubmit = async () => {
  error.value = '';
  loading.value = true;
  try {
    await authStore.login(username.value, password.value);
    router.push('/');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Invalid username or password';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import '../styles/auth.css';
</style>
