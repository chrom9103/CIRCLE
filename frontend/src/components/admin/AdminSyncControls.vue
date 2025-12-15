<template>
  <div class="sync-card-wrapper">
    <div class="sync-card">
      <div class="sync-card__header">
        <div class="sync-title">同期</div>
        <div class="sync-status" v-if="syncMessage">{{ syncMessage }}</div>
      </div>

      <div class="sync-card__body">
        <button class="sync-btn" @click="syncAdmins" :disabled="syncingAdmins">
          <span>管理者を同期</span>
        </button>

        <button class="sync-btn" @click="syncMembers" :disabled="syncingMembers">
          <span>メンバーを同期</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { supabase } from '../../supabase'
import { BACKEND } from '@/runtimeConfig'

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

<style scoped>
.sync-card-wrapper { padding: 8px; box-sizing: border-box; }
.sync-card { background: #fff; border: 1px solid #e6e6e6; border-radius: 8px; padding: 0.75rem; box-shadow: 0 1px 2px rgba(16,24,40,0.04); max-width: 900px; margin: 0.75rem auto; }
.sync-card__header { display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem }
.sync-title { font-weight:700 }
.sync-status { color:#6b7280; font-size:0.95rem }
.sync-card__body { display:flex; gap:0.75rem }
.sync-btn { display:inline-flex; align-items:center; gap:0.5rem; padding:0.5rem 0.75rem; border-radius:6px; border:1px solid transparent; background:#f7fafc; cursor:pointer }
.sync-btn:disabled { opacity:0.5; cursor:not-allowed }
.sync-icon { width:20px; height:20px }
</style>
