<template>
  <div class="home-page">
    <div class="welcome-section animate-fade-in">
      <h1>Hola, <span class="highlight">{{ authStore.user?.username }}</span></h1>
      <p>Tu entrenador personal está listo para ayudarte con tu entrenamiento de hoy.</p>
    </div>
    
    <Chat />
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import Chat from '../components/Chat.vue';

const authStore = useAuthStore();
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  height: calc(100vh - 70px);
  display: flex;
  flex-direction: column;
}

.welcome-section {
  margin-bottom: 1.5rem;
}

.welcome-section h1 {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  letter-spacing: -0.5px;
}

.highlight {
  color: var(--primary);
}

.welcome-section p {
  color: var(--text-muted);
  font-size: 1rem;
}
</style>
