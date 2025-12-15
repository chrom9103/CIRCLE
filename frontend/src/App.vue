<script setup>
import { onMounted } from 'vue'
import { supabase } from './supabase'
import { useAuthStore } from './stores/auth'

import HeaderLayout from './components/HeaderLayout.vue'

const auth = useAuthStore()

onMounted(async () => {
  function parseHash(hash) {
    if (!hash) return {}
    return hash.replace(/^#/, '').split('&').reduce((acc, pair) => {
      const [k, v] = pair.split('=')
      acc[k] = decodeURIComponent(v || '')
      return acc
    }, {})
  }

  try {
    const hash = window.location.hash
    if (hash && hash.includes('access_token')) {
      if (supabase.auth.getSessionFromUrl) {
        await supabase.auth.getSessionFromUrl({ storeSession: true })
      } else {
        const params = parseHash(hash)
        const access_token = params.access_token
        const refresh_token = params.refresh_token
        if (access_token && supabase.auth.setSession) {
          await supabase.auth.setSession({ access_token, refresh_token })
        }
      }
      // remove hash to avoid reprocessing
      history.replaceState(null, '', location.pathname + location.search)
    }
  } catch (e) {
    console.warn('Error processing OAuth hash:', e)
  }

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