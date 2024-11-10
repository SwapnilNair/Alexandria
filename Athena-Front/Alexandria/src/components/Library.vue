<template>
      <br/>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="msg" class="alert alert-success">{{ msg }}</div>

      <div v-if="loading" class="spinner-border text-primary" role="status">
        <span class="sr-only">Loading</span>
      </div>

      <div v-else>
        <div class="container">
            <div class="row align-items-center header-container">
              <div class="col">
                <h3 style="margin-left: 1%">Library </h3>
              </div>
              <div class="col-2 d-flex align-items-center align-justified">

<div class="form-group me-2">
  <input type="text" class="form-control" id="name" v-model="searchName" placeholder="Search books" required>
</div>
<button v-if="isLibrarian" @click="toggleForm" type="button" class="btn btn-sm btn-outline-secondary" style="margin-right: 4%;"> Add  </button>
</div>
            </div>
            <hr />
        </div>
 

          <div class="container mt-4 " v-if="showForm">
            <form @submit.prevent="addBook" style="margin-left: 2%;">
              <div class="form-group">
                <label for="name">Name</label>
                <input type="text" class="form-control" id="name" v-model="newBook.name" required>

                <label for="description">Description</label>
                <input type="text" class="form-control" id="description" v-model="newBook.description" required>

                <label for="description">Contents</label>
                <input type="text" class="form-control" id="contents" v-model="newBook.contents" required>

                <label for="description">Section ID</label>
                <input type="int" class="form-control" id="sectionID" v-model="newBook.sectionID" required>

                <label for="Image URL">Image URL</label>
                <input type="text" class="form-control" id="ImageURL" v-model="newBook.image_url" required>
              </div>
              <br/>
              <button type="submit" class="btn btn-sm btn-secondary">Add this book &#x2192;</button>
            </form>
           </div>
       
        
        <br/>
        <div v-if="books.length === 0">No books available.</div>

        <div v-else class="container text-center" >
          <div class="row row-cols-2">
            <div v-for="book in filteredBooks" :key="book.id" class="col mb-4">

                <div class="card" style="display: flex; flex-direction: row; align-items: left; " >

                      <img :src="book.image_url" class="card-img-left" alt="image" style="width: 15%; height: 5%; padding: 5px;">
                      <div class="card-body" style="flex: 1; text-align: left;">
                          <h4 class="card-title font-weight-bold" >{{ book.name }}</h4>
                          <p class="card-text">{{ book.description }}</p>
                      </div>
                      <div style="padding: 1%;">
                        
                        <div class="d-flex flex-column mb-3">
                          <button v-if="!isLibrarian" href="#" class="btn btn-sm btn-dark" @click="reqBook(book.id)">Borrow &#x2197;</button>
                          <button v-if="isLibrarian" href="#" class="btn btn-sm btn-dark" @click="editBook(book)">Edit &#x2197;</button>
                          <button v-if="isLibrarian" href="#" class="btn btn-sm btn-danger" style="margin-top: 10%;"  @click.prevent="delBook(book.id)">Delete</button>

                        </div>
                      </div>           
                </div>
                <div v-if="editingBook && editingBook.id === book.id" class="edit-dropdown container" style="margin: 2%;">
                  <input class="form-control"  v-model="editingBook.name" placeholder="New name" />
                  <input class="form-control"  v-model="editingBook.description" placeholder="New description" />
                  <input class="form-control"  v-model="editingBook.image_url" placeholder="New image" />
                  <button class="btn btn-sm btn-secondary" @click="updateBook(editingBook.id)">Update</button>
                  <button class="btn btn-sm btn-danger" @click="editingBook = null" style="margin: 2%;">Cancel</button>
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
    name: 'Library',
    data() {
      return {
        books: [],
        loading: false,
        error: null,
        showForm: false,
        isLibrarian:false,
        editingBook: null,
        msg : null,
        searchName:"",
        newBook : {
          name : "",
          description : "",
          contents : "",
          sectionID : "",
          image_url : "",
        },
      };
    },
    computed: {
    filteredBooks() {
      const searchTerm = this.searchName.toLowerCase();
      if (!searchTerm) return this.books;
      
      return this.books.filter(book =>
        book.name.toLowerCase().startsWith(searchTerm)
      );
    },
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
        this.books = response.data;
      } catch (error) {
        console.error('Error fetching books:', error);
        this.error = 'Failed to load books. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    methods: {
    toggleForm() {
      this.showForm = !this.showForm;
    },
    editBook(book) {
      this.editingBook = { ...book }; 
    },
    async addBook() {
      const authStore = useAuthStore();
      try {
        const response = await axios.post('http://127.0.0.1:8090/api/books/add', this.newBook, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.books.push(this.newBook);
        this.newBook.name = '';
        this.newBook.description = '';
        this.newBook.contents = "",
        this.newBook.sectionID = "",
        this.newBook.image_url = "",
        this.showForm = false;
      } catch (error) {
        console.error('Error adding books:', error);
        this.error = 'Failed to add the book. Please try again later.';
      }
    },
    async delBook(id){
      const authStore = useAuthStore();
      try {
        const response = await axios.post('http://127.0.0.1:8090/api/books/del/'+id, null, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.books = this.books.filter(book => book.id !== id);
      } catch (error) {
        console.error('Error deleting book:', error);
        this.error = 'Failed to delete the book. Please try again later.';
      }
    },
    async updateBook(id) {
      const authStore = useAuthStore();
      try {
        await axios.post(`http://127.0.0.1:8090/api/books/update/${id}`, this.editingBook , {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });

        const index = this.books.findIndex(book => book.id === id);
        if (index !== -1) {
          this.books[index] = { ...this.editingBook };
        }

        this.editingBook = null; 
      } catch (error) {
        console.error('Error updating book:', error);
        this.error = 'Failed to update the book. Please try again later.';
      }
    },
    async reqBook(id){
      const authStore = useAuthStore();
      try {
        const response = await axios.post('http://127.0.0.1:8090/api/acl/requestBook', {book_id : id} , {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.msg = response.data.msg
      } catch (error) {
        console.error('Error requesting book:', error);
        this.error = error.response.data.msg;
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
  