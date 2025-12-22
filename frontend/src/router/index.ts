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
    ,
    {
      path: '/null',
      name: 'not-implemented',
      component: () => import('../views/Null.vue'), // 未実装ページ表示
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue'), // アプリの使い方ページ
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
    {
      path: '/record',
      name: 'record',
      component: () => import('../views/Record.vue'), // 記録画面
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/Admin.vue'), // 管理者画面
    },
    {
      path: '/vote',
      name: 'vote',
      component: () => import('../views/Vote.vue'), // 投票画面
    }
    ,
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFound.vue'),
    }
  ],
})

export default router