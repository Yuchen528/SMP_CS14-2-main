// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import AboutPage from '@/views/AboutPage.vue'
import HomePage from '@/views/HomePage.vue'
import Output from '@/views/OutputPage.vue';

const routes = [
  { path: '/', redirect: '/about' },
  { path: '/home', name: 'Home', component: HomePage },
  { path: '/about', name: 'About', component: AboutPage },
  {path: '/output', name: 'Output', component: Output}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
