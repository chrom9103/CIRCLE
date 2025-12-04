<template>
  <div style="margin: 1rem 0;">
    <button @click="syncAdmins" :disabled="syncingAdmins">管理者(sync admin_list)</button>
    <button @click="syncMembers" :disabled="syncingMembers" style="margin-left: 0.5rem;">メンバー(sync member_list)</button>
    <span v-if="syncMessage" style="margin-left:0.75rem">{{ syncMessage }}</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { supabase } from '../../supabase'

const BACKEND = import.meta.env.VITE_API_BASE_URL ?? ''

const syncingAdmins = ref(false)
const syncingMembers = ref(false)
const syncMessage = ref('')

const emit = defineEmits(['synced'])

const syncAdmins = async () => {
  syncingAdmins.value = true
  syncMessage.value = ''
  try {
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const url = (BACKEND ? `${BACKEND}` : '') + '/admin/sync-admins'
    const res = await fetch(url, { method: 'POST', headers })
    const text = await res.text()
    if (!res.ok) throw new Error(text)
    syncMessage.value = '管理者同期が完了しました'
    emit('synced', { type: 'admin' })
  } catch (e) {
    console.error('syncAdmins error', e)
    syncMessage.value = '管理者同期に失敗しました'
  } finally {
    syncingAdmins.value = false
  }
}

const syncMembers = async () => {
  syncingMembers.value = true
  syncMessage.value = ''
  try {
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const url = (BACKEND ? `${BACKEND}` : '') + '/admin/sync-members'
    const res = await fetch(url, { method: 'POST', headers })
    const text = await res.text()
    if (!res.ok) throw new Error(text)
    syncMessage.value = 'メンバー同期が完了しました'
    emit('synced', { type: 'member' })
  } catch (e) {
    console.error('syncMembers error', e)
    syncMessage.value = 'メンバー同期に失敗しました'
  } finally {
    syncingMembers.value = false
  }
}
</script>
