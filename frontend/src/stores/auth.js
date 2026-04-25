import { defineStore } from 'pinia';
import api from '../services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: true,
  }),
  actions: {
    async checkUser() {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const res = await api.get('/profile/');
          this.user = res.data;
        } catch (err) {
          console.error("Auth check failed", err);
          this.logout();
        }
      }
      this.loading = false;
    },
    async login(username, password) {
      const res = await api.post('/login/', { username, password });
      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      
      const profileRes = await api.get('/profile/');
      this.user = profileRes.data;
      return res.data;
    },
    async register(username, password, email) {
      const res = await api.post('/register/', { username, password, email });
      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      
      const profileRes = await api.get('/profile/');
      this.user = profileRes.data;
      return res.data;
    },
    logout() {
      localStorage.clear();
      this.user = null;
    },
  },
  getters: {
    isNewProfile: (state) => state.user && state.user.weight === null,
  }
});
