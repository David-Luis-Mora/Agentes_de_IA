<template>
  <div class="auth-page animate-fade-in">
    <div class="auth-card">
      <div class="auth-header">
        <div class="auth-icon register">
          <UserPlus :size="32" />
        </div>
        <h1>Join GymAI</h1>
        <p>Start your fitness journey with AI</p>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <div class="form-group">
          <label>Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Pick a username"
            required
          />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="your@email.com"
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
          <span v-else>Create Account</span>
        </button>
      </form>

      <div class="auth-footer">
        Already have an account? <router-link to="/login">Sign In</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { UserPlus, Loader2 } from 'lucide-vue-next';

const username = ref('');
const email = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const handleSubmit = async () => {
  error.value = '';
  loading.value = true;
  try {
    await authStore.register(username.value, password.value, email.value);
    router.push('/');
  } catch (err) {
    error.value = err.response?.data?.error || 'Registration failed. Try a different username.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import '../styles/auth.css';
</style>
