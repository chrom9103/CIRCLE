import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signin',
      name: 'signin',
      component: () => import('../views/SignIn.vue'),　　// サインイン画面
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashBoard.vue'), // ログイン後のダッシュボード
    },
    {
      path: '/auth/callback',
      name: 'authCallback',
      component: () => import('../views/AuthCallback.vue'), // 認証後の処理を行うビュー
    },
  ],
})

export default router