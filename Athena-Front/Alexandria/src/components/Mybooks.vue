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
                <h3 style="margin-left: 1%;">My Books</h3>
              </div>
              <div class="col-auto">
                <button type="button" class="btn btn-sm btn-outline-secondary"> Past Reads</button>
              </div>
            </div>
            <hr />
        </div>

    <div class="container text-left ">
      <div class="row row-cols-1">
        <div v-if="books.length === 0">

        <div class="container-fluid d-flex justify-content-center align-items-center full-height" style="margin-top: 20%;">
            <h2 style="margin-left: 1%;">You currently have no books borrowed</h2>
        </div>

    </div>
        <div v-for="book in books" :key="book.id" class="col mb-2">
          <div class="card" style="display: flex; flex-direction: row; align-items: left;">
            <div class="card-body" style="flex: 1; text-align: left;">
              <h4 class="card-title font-weight-bold">{{ book.name }}</h4>
              <p class="card-text">{{ book.description }}</p>
            </div>
            <button type="button" class="btn btn-sm btn-dark" disabled style="margin: 2px;">{{book.due_on}}</button>
            <button type="button" class="btn btn-sm btn-dark" @click="returnBook(book.id)" style="margin: 2px;"> Return</button>
            
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
      name: 'Books',
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
          const response = await axios.post('http://localhost:8090/api/books/list/mybooks', null, {
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
    async returnBook(id){
      const authStore = useAuthStore();
      try {
        const response = await axios.post('http://127.0.0.1:8090/api/acl/books/return', {book_id : id}, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.books = this.books.filter(book => book.id !== id);
      } catch (error) {
        console.error('Error returning book:', error);
        this.error = 'Failed to return the book :'+ error.response.data.msg;
      }
    }
      }
    };
    </script>
    
    
    <style scoped>
    .spinner-border {
      display: block;
      margin: 20px auto;
    }
    </style>