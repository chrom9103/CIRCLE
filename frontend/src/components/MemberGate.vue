<template>
  <div><!-- MemberGate does not render UI; it emits ready events to parent --></div>
</template>

<script setup>
import { onMounted } from 'vue'
import { supabase } from '../supabase'

const emit = defineEmits(['ready'])

onMounted(async () => {
  try {
    const sessionRes = await supabase.auth.getSession()
    const session = sessionRes?.data?.session
    const token = session?.access_token ?? null
    let discordId = ''
    if (session?.user) {
      const user = session.user
      discordId = (user?.identities && user.identities[0]?.id) || user?.user_metadata?.provider_id || ''
    }

    const { BACKEND } = await import('@/runtimeConfig')
    const url = (BACKEND ? `${BACKEND}` : '') + `/api/is_member?discord_id=${encodeURIComponent(discordId)}`
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const res = await fetch(url, { headers })
    let allowed = false
    if (res.ok) {
      try {
        const json = await res.json()
        allowed = !!json.is_member
      } catch (e) {
        allowed = false
      }
    } else {
      allowed = false
    }

    emit('ready', { allowed, discordId, token })
  } catch (e) {
    emit('ready', { allowed: false, discordId: '', token: null })
  }
})
</script>
