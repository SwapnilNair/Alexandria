<template>
<nav class="navbar navbar-expand-lg border-bottom border-top" style="margin-right: 1%; margin-left: -1%; ">
  <div class="container-fluid" >
    <a class="navbar-brand" href="#">Alexandria <span v-if="isLibrarian">Admin</span></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" v-if="isLibrarian">
            <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="!isLibrarian">
            <router-link class="nav-link" to="/mybooks">MyBooks</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/library">Books</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/section">Sections</router-link>
          </li>
          <li class="nav-item" v-if="!isLibrarian">
            <router-link class="nav-link" to="/myrequests">MyRequests</router-link>
          </li>

          <li class="nav-item" v-if="isLibrarian">
            <router-link class="nav-link" to="/requests">Requests</router-link>
          </li>

          <li class="nav-item" v-if="isLibrarian">
            <router-link class="nav-link" to="/issued">Issued</router-link>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
          </li>
        </ul>
      
    </div>
  </div>
</nav>
    
  </template>
  
  <script>
  import { computed } from 'vue';
  import { useAuthStore } from '@/stores/authStore';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'Navbar',
    setup() {
      const authStore = useAuthStore();
      const router = useRouter();
      
      const isLibrarian = computed(() => authStore.role === 'true');
  
      const logout = () => {
        authStore.clearAuth();
        router.push('/login');
      };
  
      const goHome = () => {
        router.push('/');
      };
  
      return {
        isLibrarian,
        logout,
        goHome,
      };
    },
  };
  </script>
  
  <style scoped>
  .navbar-brand {
    font-weight: bold;
    cursor: pointer;
  }
  </style>
  