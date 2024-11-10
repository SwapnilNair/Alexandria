<template>
  
  <div class="container" style="margin-top: 2%;">
    
      <div class="row align-items-center header-container">
        <div class="col">
          <h3 style="margin-left: 1%">My Dashboard </h3>
        </div>
        <div class="col-auto" >
        </div>
      </div>
      <hr />
  </div>


  <div class="container mt-4">
    <div class="row">
      <div class="col-md-6 mb-6">
        <div class="card text-white bg-primary">
          <div class="card-body">
            <h5 class="card-title">Number of Users</h5>
            <p class="card-text">{{ numberOfUsers }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-4">
        <div class="card text-white bg-secondary">
          <div class="card-body">
            <h5 class="card-title">Number of Books</h5>
            <p class="card-text">{{ numberOfBooks }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-4">
        <div class="card text-white bg-info">
          <div class="card-body">
            <h5 class="card-title">Number of Sections</h5>
            <p class="card-text">{{ numberOfSections }}</p>
          </div>
        </div>
      </div>

      <div class="col-md-6 mb-4">
        <div class="card text-white bg-warning">
          <div class="card-body">
            <h5 class="card-title">Books Requested</h5>
            <p class="card-text">{{ booksRequested }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-4">
        <div class="card text-white bg-success">
          <div class="card-body">
            <h5 class="card-title">Books Issued</h5>
            <p class="card-text">{{ booksIssued }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>


  </template>
  

  <script>
  import { computed } from 'vue';
  import { useAuthStore } from '@/stores/authStore';
  import axios from 'axios';

  export default {
    name: 'Dashboard',
    data() {
        return {
          booksRequested : 1,
          numberOfSections : 2,
          numberOfBooks : 2,
          numberOfUsers: 5,
          booksIssued : 0,
        };
      },
    async created() {
      this.loading = true;
      const authStore = useAuthStore();
      const isLibrarian = computed(() => authStore.role === 'true');

      this.isLibrarian = isLibrarian
      try {
        const response = await axios.post('http://localhost:8090/api/books/list', {}, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
          this.numberOfBooks = response.data.length;
          
          const response2 = await axios.post('http://localhost:8090/api/sections/list', {}, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
          this.numberOfSections = response2.data.length;

          const response3 = await axios.post('http://localhost:8090/api/acl/all', null, {
              headers: {
                Authorization: `Bearer ${authStore.token}`,
              },
            });
          this.booksRequested = response3.data.length;

          const response4 = await axios.post('http://localhost:8090/api/acl/allissued', null, {
              headers: {
                Authorization: `Bearer ${authStore.token}`,
              },
            });
          this.booksIssued = response4.data.length;

          const response5 = await axios.post('http://localhost:8090/api/acl/allusers', null, {
              headers: {
                Authorization: `Bearer ${authStore.token}`,
              },
            });
          this.numberOfUsers = response5.data.users;
        } catch (error) {
          console.error('Error fetching your books:', error);
          this.error = 'Failed to load books. Please try again later.';
        } finally {
          this.loading = false;
        }
    },
  };
  </script>
  
  <style>
</style>