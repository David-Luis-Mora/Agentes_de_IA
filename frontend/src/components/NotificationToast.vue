<template>
  <div class="notification-container">
    <TransitionGroup name="toast">
      <div 
        v-for="n in notificationStore.notifications" 
        :key="n.id" 
        :class="['toast-item', n.type || 'success']"
        @click="notificationStore.markAsRead(n.id)"
      >
        <div class="toast-icon">
          <CheckCircle v-if="n.type === 'success'" :size="20" />
          <AlertCircle v-else-if="n.type === 'error'" :size="20" />
          <Info v-else :size="20" />
        </div>
        <div class="toast-content">
          <p>{{ n.message }}</p>
        </div>
        <button class="close-btn" @click.stop="notificationStore.markAsRead(n.id)">
          <X :size="16" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import { useNotificationStore } from '../stores/notification';
import { useAuthStore } from '../stores/auth';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-vue-next';

const notificationStore = useNotificationStore();
const authStore = useAuthStore();

let interval = null;

onMounted(() => {
  if (authStore.user) {
    notificationStore.fetchNotifications();
    // Poll for new notifications every 10 seconds
    interval = setInterval(() => {
      notificationStore.fetchNotifications();
    }, 10000);
  }
});

onUnmounted(() => {
  if (interval) clearInterval(interval);
});
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 85px;
  right: 2rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  pointer-events: none;
}

.toast-item {
  pointer-events: auto;
  min-width: 300px;
  max-width: 400px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-item:hover {
  transform: translateX(-5px);
  border-color: var(--primary);
}

.toast-icon {
  flex-shrink: 0;
}

.success .toast-icon { color: #10b981; }
.error .toast-icon { color: #ef4444; }
.info .toast-icon { color: var(--primary); }

.toast-content {
  flex: 1;
}

.toast-content p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
  color: var(--text-main);
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-main);
}

/* Animations */
.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.toast-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
