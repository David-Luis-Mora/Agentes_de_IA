<template>
  <div class="app-layout">
    <Navbar />
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue';
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';

const authStore = useAuthStore();

onMounted(() => {
  authStore.checkUser();
});
</script>

<style>
@import './styles/main.css';

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
