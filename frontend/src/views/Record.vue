<script setup>
import { ref, onMounted } from 'vue'
import { supabase } from '../supabase'
import { BACKEND } from '@/runtimeConfig'

import AddRecordModal from '../components/Record/AddRecordModal.vue'
import RecordTable from '../components/Record/RecordTable.vue'
import SummaryBannar from '../components/Record/SummaryBannar.vue'
import YearSelector from '../components/Record/YearSelector.vue'

const transactions = ref([])
const loading = ref(false)
const showModal = ref(false)
const currentYear = ref('all')

function onYearUpdate(y) {
  currentYear.value = y
  fetchTransactions()
}

async function fetchTransactions() {
  loading.value = true
  try {
    // Use backend API to list records (the backend handles Supabase table access).
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const url = (BACKEND ? `${BACKEND}` : '') + '/api/records'

    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    })

    if (!res.ok) {
      const text = await res.text()
      throw new Error(`records api error: ${res.status} ${text}`)
    }

    const data = await res.json()

    // If year filter is set, filter client-side by created_at year
    let items = Array.isArray(data) ? data : []
    // Exclude records marked as deleted
    items = items.filter((t) => {
      const status = (t.status || '').toString().toLowerCase()
      return status !== 'deleted'
    })
    if (currentYear.value !== 'all') {
      const y = Number(currentYear.value)
      items = items.filter((t) => {
        const d = t.created_at ? new Date(t.created_at) : null
        return d ? d.getFullYear() === y : false
      })
    }

    // sort desc by created_at
    items.sort((a, b) => {
      const da = a.created_at ? new Date(a.created_at).getTime() : 0
      const db = b.created_at ? new Date(b.created_at).getTime() : 0
      return db - da
    })

    transactions.value = items
  } catch (e) {
    console.error('fetchTransactions error', e)
    transactions.value = []
  } finally {
    loading.value = false
  }
}

function openModal() { showModal.value = true }
function closeModal() { showModal.value = false }

async function handleSaved() {
  await fetchTransactions()
  closeModal()
}

onMounted(() => {
  fetchTransactions()
})
</script>

<template>
  <section class="record container">
    <header class="record-header">
      <h1>記録</h1>
      <div class="header-actions">
        <YearSelector :currentYear="currentYear" @update:year="onYearUpdate" />
        <button class="btn-add" @click="openModal">新規追加</button>
      </div>
    </header>

    <div class="summary-area">
      <SummaryBannar :transactions="transactions" />
    </div>

    <div class="table-area">
      <RecordTable :transactions="transactions" />
      <div v-if="loading" class="loading">読み込み中...</div>
    </div>

    <AddRecordModal v-if="showModal" @close="closeModal" @saved="handleSaved" />
  </section>
</template>

<style scoped>
.record { padding: 1.25rem }
.record-header { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:1rem }
.header-actions { display:flex; gap:0.75rem; align-items:center }
.btn-add { background:#29B575; color:#fff; border:none; padding:0.6rem 0.9rem; border-radius:8px; cursor:pointer }
.summary-area { margin-bottom:1rem }
.table-area { width: 100% }
.loading { margin-top:12px; color:#666 }

@media (max-width:800px) {
  .record-header { flex-direction:column; align-items:flex-start }
  .header-actions { width:100%; justify-content:space-between }
}
</style>
