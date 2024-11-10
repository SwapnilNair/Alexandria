// stores/authStore.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || false,
  }),
  actions: {
    setAuth(token,role) {
      this.token = token;
      this.role = role;
      localStorage.setItem('token', token);
      localStorage.setItem('role', role);
    },

    clearAuth() {
      this.token = null;
      this.role = null;
      localStorage.removeItem('token');
      localStorage.removeItem('role');
    },

    async login(username, password) {
      try {
        const response = await axios.post('http://localhost:8090/api/auth/login', {
          username,
          password,
        });
        this.setAuth(response.data.access_token,response.data.isLibrarian)
        console.log(this.token,this.isLibrarian)
      } catch (error) {
        console.error('Login failed:', error);
        throw error
      }
    }
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    isLibrarian: (state)=> state.role
  },
});
