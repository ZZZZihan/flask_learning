import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue')
    },
    {
      path: '/achievements',
      name: 'achievements',
      component: () => import('@/views/AchievementList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/achievements/new',
      name: 'new-achievement',
      component: () => import('@/views/AchievementForm.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/achievements/:id',
      name: 'achievement-detail',
      component: () => import('@/views/AchievementDetail.vue')
    },
    {
      path: '/achievements/:id/edit',
      name: 'edit-achievement',
      component: () => import('@/views/AchievementForm.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router 