<template>
  <br/>
  <div v-if="error" class="alert alert-danger">{{ error }}</div>
  <div v-if="loading" class="spinner-border text-primary" role="status">
    <span class="sr-only">Loading</span>
  </div>

  <div v-else>

    <div class="container">
            <div class="row align-items-center header-container">
              <div class="col">
                <h3 style="margin-left: 1%;">My Requests</h3>
              </div>
   
            </div>
            <hr />
        </div>

    <div class="container text-left ">
      <div class="row row-cols-1">
        <div v-if="books.length === 0">

        <div class="container-fluid d-flex justify-content-center align-items-center full-height" style="margin-top: 20%;">
            <h2 style="margin-left: 1%;">You currently have no books requested</h2>
        </div>

    </div>
        <div v-for="book in books" :key="book.id" class="col mb-2">
          <div class="card" style="display: flex; flex-direction: row; align-items: left;">
            <div class="card-body" style="flex: 1; text-align: left;">
              <h4 class="card-title font-weight-bold" style="margin-top: 1%;">{{ book.name }}</h4>
            </div>
            
            <button type="button" class="btn btn-sm btn-dark" style="margin: 2px;"> Requested On  <br/>{{ book.borrowed_on }}</button>
            
          </div>
        </div>
      </div>
    </div>
  </div>



</template>

    
  <script>
    import axios from 'axios';
    import { useAuthStore } from '@/stores/authStore';
    import { computed } from 'vue';
    
    export default {
      name: 'Myrequests',
      data() {
        return {
          books: [],
          loading: false,
          error: null,
          isLibrarian: false,
        };
      },
      async created() {
        this.loading = true;
        const authStore = useAuthStore();
    
        const isLibrarian = computed(() => authStore.role === 'true');
        this.isLibrarian = isLibrarian
    
        try {
          const response = await axios.post('http://localhost:8090/api/books/list/myreqs', null, {
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
          });
          this.books = response.data;
          
        } catch (error) {
          console.error('Error fetching your books:', error);
          this.error = 'Failed to load books. Please try again later.';
        } finally {
          this.loading = false;
        }
      },
      methods: {

      }
    };
    </script>
    
    
    <style scoped>
    .spinner-border {
      display: block;
      margin: 20px auto;
    }
    </style>