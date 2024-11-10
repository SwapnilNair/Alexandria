import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore';
import Dashboard from '../components/Dashboard.vue'
import Login from '../components/Login.vue'
import Library from '../components/Library.vue'
import Section from '@/components/Section.vue'
import Requests from '@/components/Requests.vue';
import Mybooks from '@/components/Mybooks.vue';
import MyRequests from '@/components/MyRequests.vue';
import Grants from '@/components/Grants.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/library',
      name: 'library',
      component: Library
    },
    {
      path: '/section',
      name: 'section',
      component: Section
    },
    {
      path: "/requests",
      name : "requests",
      component: Requests
    },
    {
      path: '/',
      name: 'home',
      component: Dashboard
    },
    {
      path: '/mybooks',
      name: 'home',
      component: Mybooks
    },
    {
      path: '/myrequests',
      name: 'myrequests',
      component: MyRequests
    },
    {
      path: '/issued',
      name: 'issued',
      component: Grants
    },
  ]
})

router.beforeEach((to,from,next)=>{
  const authStore = useAuthStore();
  const isLibrarian = authStore.isLibrarian
  const isAuthenticated = authStore.isAuthenticated

  console.log(isAuthenticated,isLibrarian)
  if (!isAuthenticated && to.name !== 'login') {
    next({ name: 'login' });
  }else{  
    next();
  }

})
export default router
