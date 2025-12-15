<template>
  <div>
    <h1>記録</h1>

    <!-- accessDenied または未サインイン時の案内 -->
    <AccessNotice v-if="accessDenied" :accessDenied="accessDenied" :discordId="currentUserDiscordId" />

    <div v-else>
      <div v-if="loading">
          <p>データを読み込み中...</p>
      </div>

    <!-- 記録一覧 -->
    <AdminGate @ready="onAdminReady" />
    <AdminRecordList :records="activeRecordsLimited" :loading="loading" 
      @soft-delete="softDeleteRecord"
      @mark-processed="markProcessedRecord"
      @mark-unprocessed="markUnprocessedRecord"
    />

    <!-- 管理者/メンバー同期ボタン -->
    <AdminSyncControls @synced="() => fetchRecords()" />

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import AdminGate from '../components/AdminGate.vue'
import AccessNotice from '../components/AccessNotice.vue'
import AdminSyncControls from '../components/admin/AdminSyncControls.vue'
import AdminRecordList from '../components/admin/AdminRecordList.vue'
import { supabase } from '../supabase'; 
import { BACKEND } from '@/runtimeConfig'

const records = ref([]);
const currentUserDiscordId = ref('');
const newRecord = ref({
    purpose: '',
    amount: null,
    record_type: 'Expense',
    category: '',
    user_id: '', 
});
const loading = ref(false);

const whitelisted = ref(false);
const accessDenied = ref(false);

const activeRecords = computed(() => {
  return records.value.filter(r => r.status !== 'deleted');
});

// 表示件数を制限
const activeRecordsLimited = computed(() => {
  return activeRecords.value.slice(0, 100)
})

// DBから記録を取得
const fetchRecords = async () => {
  loading.value = true;
  try {
    const url = (BACKEND ? `${BACKEND}` : '') + '/api/records'
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const res = await fetch(url, { headers })
    if (!res.ok) throw new Error(await res.text())
    const data = await res.json()
    records.value = data || []
  } catch (e) {
    console.error('データの取得に失敗しました:', e)
  } finally {
    loading.value = false
  }
};

// newRecord.user_id に Discord の id を設定し、ホワイトリスト確認
const onAdminReady = async ({ allowed, discordId, token }) => {
  currentUserDiscordId.value = discordId || ''
  newRecord.value.user_id = discordId || ''
  whitelisted.value = !!allowed
  accessDenied.value = !allowed
  if (!allowed) {
    return
  }
  // if allowed, fetch records
  await fetchRecords()
}

// 記録を論理削除（バックエンド経由）
const softDeleteRecord = async (id) => {
  try {
    const url = (BACKEND ? `${BACKEND}` : '') + `/api/records/${encodeURIComponent(id)}`
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    }
    const res = await fetch(url, {
      method: 'PATCH',
      headers,
      body: JSON.stringify({ status: 'deleted' }),
    })
    if (res.status === 403) {
      alert('この操作には管理者権限が必要です（403）。')
      return
    }
    if (!res.ok) {
      console.error('記録の論理削除に失敗しました:', await res.text())
      return
    }
    await fetchRecords()
  } catch (e) {
    console.error('記録の論理削除に失敗しました:', e)
  }
};

// 記録を清算済みにする（status=processed）
const markProcessedRecord = async (id) => {
  try {
    const url = (BACKEND ? `${BACKEND}` : '') + `/api/records/${encodeURIComponent(id)}`
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    }
    const res = await fetch(url, {
      method: 'PATCH',
      headers,
      body: JSON.stringify({ status: 'processed' }),
    })
    if (res.status === 403) {
      alert('この操作には管理者権限が必要です（403）。')
      return
    }
    if (!res.ok) {
      console.error('記録の清算更新に失敗しました:', await res.text())
      return
    }
    await fetchRecords()
  } catch (e) {
    console.error('記録の清算更新に失敗しました:', e)
  }
};

// 記録を未清算（status=active）に戻す
const markUnprocessedRecord = async (id) => {
  try {
    const url = (BACKEND ? `${BACKEND}` : '') + `/api/records/${encodeURIComponent(id)}`
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    }
    const res = await fetch(url, {
      method: 'PATCH',
      headers,
      body: JSON.stringify({ status: 'active' }),
    })
    if (res.status === 403) {
      alert('この操作には管理者権限が必要です（403）。')
      return
    }
    if (!res.ok) {
      console.error('記録の状態更新に失敗しました:', await res.text())
      return
    }
    await fetchRecords()
  } catch (e) {
    console.error('記録の状態更新に失敗しました:', e)
  }
};

onMounted(() => {})

</script>

<style scoped>
</style>