<template>
    <div class="container" style = "margin-top: 10%;">
      <h1 align="center">Welcome to Alexandria</h1>
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card mt-5">
            <div class="card-header">
              <h3>Login</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleLogin">
                <div class="form-group">
                  <label for="username">Username</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="username" 
                    v-model="username" 
                    required 
                  />
                </div>
                <br/>
                <div class="form-group">
                  <label for="password">Password</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="password" 
                    required 
                  />
                </div>
                <br/>
                <button type="submit" class="btn btn-primary btn-block">Login</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useAuthStore } from '@/stores/authStore';
  
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    setup() {
      const authStore = useAuthStore();
      return { authStore };
    },
    methods: {
      async handleLogin() {
        try {
          await this.authStore.login(this.username,this.password)
        } catch (error) {
          console.error('Login failed:', error);
          alert('Login failed. Please check your username and password.');
          return
        }
        this.$router.push('/dashboard');
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin-top: 50px;
  }
  </style>
  