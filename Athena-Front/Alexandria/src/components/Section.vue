<template>
  <br/>

  <div v-if="error" class="alert alert-danger">{{ error }}</div>
  <div v-if="loading" class="spinner-border text-primary" role="status">
    <span class="sr-only">Loading</span>
  </div>

  <div v-else>
    <div v-if="sections.length === 0">No sections available.</div>

    <div class="container">
            <div class="row align-items-center header-container">
              <div class="col">
                <h3 style="margin-left: 1%;">Sections </h3>
              </div>
              
              <div class="col-2 d-flex align-items-center align-justified">

                  <div class="form-group me-2">
                    <input type="text" class="form-control" id="name" v-model="searchName" placeholder="Search sections" required>
                  </div>
                  <button v-if="isLibrarian" @click="toggleForm" type="button" class="btn btn-sm btn-outline-secondary" style="margin-right: 4%;"> Add  </button>
              </div>
            </div>
            <hr />
        </div>


        <div class="container mt-4 " v-if="showForm" style="margin-left: 5%">
          <form @submit.prevent="addSection">
            <div class="form-group">
              <label for="name">Name</label>
              <input type="text" class="form-control" id="name" v-model="newSection.name" required>
            </div>
            <div class="form-group">
              <label for="description">Description</label>
              <input type="text" class="form-control" id="description" v-model="newSection.description" required>
            </div>
            <br/>
            
            <button type="submit" class="btn btn-sm btn-secondary">Add Section</button>
          </form>
          <br/>
      
        </div>
        
    <div class="container text-left ">
      <div class="row row-cols-1">
        <div v-for="section in filteredSections" :key="section.id" class="col mb-2">
          <div class="card" style="display: flex; flex-direction: row; align-items: left;">
            <div class="card-body" style="flex: 1; text-align: left;">
              <h4 class="card-title font-weight-bold">{{ section.name }}</h4>
              <p class="card-text">{{ section.description }}</p>
            </div>
            
            <button v-if="isLibrarian" type="button" class="btn btn-sm btn-light" disabled style="margin: 2px;">Section ID {{ section.id }}</button>
            <button v-if="isLibrarian" type="button" class="btn btn-sm btn-dark" @click="editSection(section)" style="margin: 2px;">Edit </button>

            <button v-if="isLibrarian" type="button" class="btn btn-sm btn-danger" @click="delSection(section.id)" style="margin: 2px;" > X </button>
            
          </div>

          <div v-if="editingSection && editingSection.id === section.id" class="container bg-secondary-subtle" style="margin-top: 1%;">
                  <label for="description">Name</label>
                  <input class="form-control" v-model="editingSection.name" placeholder="New name" />

                  <label for="description">Description</label>
                  <input class="form-control" v-model="editingSection.description" placeholder="New description" />
                  <button class="btn btn-sm btn-secondary" @click="updateSection(editingSection.id)">Update</button>
                  <button class="btn btn-sm btn-danger" @click="editingSection = null" style="margin: 2%;">Cancel</button>
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
  name: 'Sections',
  data() {
    return {
      sections: [],
      loading: false,
      error: null,
      showForm: false,
      editingSection: null,
      isLibrarian: false,
      newSection: {
        name: '',
        description: ''
      },
      searchName: '',
    };
  },
  computed: {
    filteredSections() {
      const searchTerm = this.searchName.toLowerCase();
      if (!searchTerm) return this.sections;
      
      return this.sections.filter(section =>
        section.name.toLowerCase().startsWith(searchTerm)
      );
    },
  },
  async created() {
    this.loading = true;
    const authStore = useAuthStore();

    const isLibrarian = computed(() => authStore.role === 'true');
    this.isLibrarian = isLibrarian

    try {
      const response = await axios.post('http://localhost:8090/api/sections/list', {}, {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
        },
      });
      this.sections = response.data;
    } catch (error) {
      console.error('Error fetching sections:', error);
      this.error = 'Failed to load sections. Please try again later.';
    } finally {
      this.loading = false;
    }
  },
  methods: {
    toggleForm() {
      this.showForm = !this.showForm;
    },

    editSection(section) {
      this.editingSection = { ...section }; 
    },
    async addSection() {
      const authStore = useAuthStore();
      try {
        const response = await axios.post('http://127.0.0.1:8090/api/sections/add', this.newSection, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.sections.push(this.newSection);
        this.newSection.name = '';
        this.newSection.description = '';
        this.showForm = false;
      } catch (error) {
        console.error('Error adding section:', error);
        this.error = 'Failed to add section. Please try again later.';
      }
    },
    async updateSection(id) {
      const authStore = useAuthStore();
      try {
        await axios.post(`http://127.0.0.1:8090/api/sections/update/${id}`, this.editingSection , {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });

        const index = this.sections.findIndex(section => section.id === id);
        if (index !== -1) {
          this.sections[index] = { ...this.editingSection };
        }

        this.editingSection = null; 
      } catch (error) {
        console.error('Error updating section:', error);
        this.error = 'Failed to update the section. Please try again later.';
      }
    },
    async delSection(id){
      const authStore = useAuthStore();
      try {
        const response = await axios.post('http://127.0.0.1:8090/api/sections/del/'+id, null, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.sections = this.sections.filter(section => section.id !== id);
      } catch (error) {
        console.error('Error deleting book:', error);
        this.error = 'Failed to delete the book. Please try again later.';
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
