import Default from '@/layouts/default.vue'
import AIMode from '@/views/AIMode.vue'
import Home from '@/views/home.vue'
import HumanMode from '@/views/humanMode.vue'
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: Default,
    children: [{ path: '', component: Home }]
  },
  {
    path: '/humanMode',
    component: Default,
    children: [{ path: '', component: HumanMode }]
  },
  {
    path: '/aiMode',
    component: Default,
    children: [{ path: '', component: AIMode }]
  },
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
