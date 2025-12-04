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
    <ul>
      <li v-for="record in activeRecords" :key="record.transaction_id">
        <div>
            <!-- 金額と用途を表示 -->
            <span :class="{'text-red-600': record.record_type === 'Expense', 'text-green-600': record.record_type === 'Revenue'}">
                {{ record.record_type === 'Expense' ? 'ー' : '＋' }} {{ record.amount.toLocaleString() }} 円
            </span>
            <span >| {{ record.purpose }}</span>
            <p>カテゴリ: {{ record.category }} / ID: {{ record.transaction_id.substring(0, 8) }}...</p>
        </div>
        
        <!-- 論理削除ボタン -->
        <button @click="softDeleteRecord(record.transaction_id)">
            取消済にする
        </button>
      </li>
    </ul>

    <!-- 管理者/メンバー同期ボタン -->
    <div style="margin: 1rem 0;">
      <button @click="syncAdmins" :disabled="syncingAdmins">管理者(sync admin_list)</button>
      <button @click="syncMembers" :disabled="syncingMembers" style="margin-left: 0.5rem;">メンバー(sync member_list)</button>
      <span v-if="syncMessage" style="margin-left:0.75rem">{{ syncMessage }}</span>
    </div>

    <p>aaaa</p>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import AdminGate from '../components/AdminGate.vue'
import AccessNotice from '../components/AccessNotice.vue'
import { supabase } from '../supabase'; 

const BACKEND = import.meta.env.VITE_API_BASE_URL ?? ''

const records = ref([]);
const currentUser = ref(null);
const currentUserDiscordId = ref('');
const newRecord = ref({
    purpose: '',
    amount: null,
    record_type: 'Expense',
    category: '',
    user_id: '', 
});
const loading = ref(false);
const syncingAdmins = ref(false);
const syncingMembers = ref(false);
const syncMessage = ref('');

const whitelisted = ref(false);
const whitelistChecking = ref(false);
const accessDenied = ref(false);

// status='active' の記録のみを表示
const activeRecords = computed(() => {
    return records.value.filter(r => r.status === 'active');
});

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

onMounted(() => {})

// 管理者同期をトリガー
const syncAdmins = async () => {
  syncingAdmins.value = true;
  syncMessage.value = '';
  try {
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const url = (BACKEND ? `${BACKEND}` : '') + '/admin/sync-admins'
    const res = await fetch(url, { method: 'POST', headers })
    const text = await res.text()
    if (!res.ok) throw new Error(text)
    syncMessage.value = '管理者同期が完了しました'
    // 同期後に最新データを取得
    await fetchRecords()
  } catch (e) {
    console.error('syncAdmins error', e)
    syncMessage.value = '管理者同期に失敗しました'
  } finally {
    syncingAdmins.value = false
  }
}

// メンバー同期をトリガー
const syncMembers = async () => {
  syncingMembers.value = true;
  syncMessage.value = '';
  try {
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const url = (BACKEND ? `${BACKEND}` : '') + '/admin/sync-members'
    const res = await fetch(url, { method: 'POST', headers })
    const text = await res.text()
    if (!res.ok) throw new Error(text)
    syncMessage.value = 'メンバー同期が完了しました'
    await fetchRecords()
  } catch (e) {
    console.error('syncMembers error', e)
    syncMessage.value = 'メンバー同期に失敗しました'
  } finally {
    syncingMembers.value = false
  }
}
</script>

<style scoped>
</style>