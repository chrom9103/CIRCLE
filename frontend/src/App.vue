<script setup>
import { onMounted } from 'vue'
import { supabase } from './supabase'
import { useAuthStore } from './stores/auth'

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
  <RouterView>
  </RouterView>
</template>