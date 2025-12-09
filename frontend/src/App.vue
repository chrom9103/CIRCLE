<script setup>
import { onMounted } from 'vue'
import { supabase } from './supabase'
import { useAuthStore } from './stores/auth'

import HeaderLayout from './components/HeaderLayout.vue'

const auth = useAuthStore()

onMounted(async () => {
  const { data, error } = await supabase.auth.getSession()
  if (error) {
    console.error('Error fetching session:', error)
    auth.clearUser()
  } else {
    auth.setUser(data.session?.user ?? null)
  }

  supabase.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN' && session) {
      auth.setUser(session.user)
    } else if (event === 'SIGNED_OUT') {
      auth.clearUser()
    }
  })
})
</script>

<template>
  <HeaderLayout />
  <div class="app-router-view">
    <RouterView />
  </div>
</template>

<style scoped>
.app-router-view {
  padding: 10px;
  box-sizing: border-box;
}
</style>