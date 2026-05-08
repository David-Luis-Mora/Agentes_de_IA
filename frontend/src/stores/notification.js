import { defineStore } from 'pinia';
import api from '../services/api';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],
    loading: false
  }),
  actions: {
    async fetchNotifications() {
      if (this.loading) return;
      try {
        const res = await api.get('/notifications/');
        this.notifications = res.data;
      } catch (err) {
        console.error("Error fetching notifications:", err);
      }
    },
    async markAsRead(id = null) {
      try {
        await api.post('/notifications/', { id });
        if (id) {
          this.notifications = this.notifications.filter(n => n.id !== id);
        } else {
          this.notifications = [];
        }
      } catch (err) {
        console.error("Error marking notifications as read:", err);
      }
    },
    addToast(message, type = 'success') {
       // Simple local toast implementation
       const id = Date.now();
       this.notifications.push({ id, message, type, isToast: true });
       setTimeout(() => {
         this.notifications = this.notifications.filter(n => n.id !== id);
       }, 10000);

    }
  }
});
