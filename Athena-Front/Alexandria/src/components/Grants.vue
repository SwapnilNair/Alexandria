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
                  <h3 style="margin-left: 1%;">Issued Books</h3>
                </div>
                <div class="col-auto">
                  <button type="button" class="btn btn-sm btn-outline-secondary"> Home</button>
                </div>
              </div>
              <hr />
          </div>
  
      <div class="container text-left ">
        <div v-if="issuedbooks.length === 0">
  
  <div class="container-fluid d-flex justify-content-center align-items-center full-height" style="margin-top: 20%;">
    <h2 style="margin-left: 1%;">No books issued</h2>
</div>

</div>
        <div class="row row-cols-2">


          <div v-for="issuedbook in issuedbooks" :key="issuedbook.id" class="col mb-2 ">
              <div class="card mb-4 " style="border: 1px solid #ddd;">
                    <div class="card-body" style="display: flex; flex-direction: column; align-items: flex-start;">
                        <h4 class="card-title font-weight-bold mb-2">
                            {{ issuedbook.user_name }} was issued "{{ issuedbook.book_name }}"
                        </h4>
                        <p class="card-text mb-2">
                            <strong>Issue Date:</strong> {{ issuedbook.borrowed_on }}
                        </p>
                    </div>
                    <button type="button" class="btn btn-sm btn-dark" @click="revokerequest(issuedbook.id)" style="margin: 2px;"> Revoke</button>
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
        name: 'issuedbooks',
        data() {
          return {
            issuedbooks: [],
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
            const response = await axios.post('http://localhost:8090/api/acl/allissued', null, {
              headers: {
                Authorization: `Bearer ${authStore.token}`,
              },
            });
            this.issuedbooks = response.data;
            
          } catch (error) {
            console.error('Error fetching your issuedbooks:', error);
            this.error = 'Failed to load issue requests. Please try again later.';
          } finally {
            this.loading = false;
          }
        },
        methods: {
        async revokerequest(id){
            const authStore = useAuthStore();
            try {
                const response = await axios.post('http://127.0.0.1:8090/api/acl/revokeRequest', {request_id:id}, {
                headers: {
                    Authorization: `Bearer ${authStore.token}`,
                },
                });
                this.issuedbooks = this.issuedbooks.filter(ireq => ireq.id !== id);
            } catch (error) {
                console.error('Error approving the book request:', error);
                this.error = 'Failed to approve the book request. Please try again later.';
            }
            },
        }
      };
      </script>
      
      
      <style scoped>
      .spinner-border {
        display: block;
        margin: 20px auto;
      }
      </style>