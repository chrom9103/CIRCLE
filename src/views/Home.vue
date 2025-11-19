<script setup>
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
</script>

<template>
  <ul>
    <li v-if="auth.isLoggedIn">
      <router-link to="/dashboard">Dashboard</router-link>
    </li>
    <li v-if="!auth.isLoggedIn">
      <router-link to="/signin">SignIn</router-link>
    </li>
  </ul>
  <h1>Supabase + Vue3 + Pinia</h1>
</template>

<style scoped>
</style>
