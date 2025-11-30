<template>
  <div>
    <h1>記録</h1>
    
    <div v-if="loading">
        <p>データを読み込み中...</p>
    </div>

    <!-- 記録一覧 -->
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
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
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

// admin_list テーブルに discord_id が存在するか確認
const checkWhitelist = async (discordId) => {
  if (!discordId) return false;
  whitelistChecking.value = true;
  try {
    const url = (BACKEND ? `${BACKEND}` : '') + `/api/is_admin?discord_id=${encodeURIComponent(discordId)}`
    const res = await fetch(url)
    if (!res.ok) {
      console.error('admin check failed:', await res.text())
      return false
    }
    const json = await res.json()
    return !!json.is_admin
  } catch (e) {
    console.error('checkWhitelist exception:', e);
    return false;
  } finally {
    whitelistChecking.value = false;
  }
};

// newRecord.user_id に Discord の id を設定し、ホワイトリスト確認
const loadCurrentUser = async () => {
  try {
    const { data, error } = await supabase.auth.getUser();
    if (error) {
      console.error('Error fetching user:', error.message);
      return;
    }
    currentUser.value = data.user;

    const discordId = data.user?.identities?.[0]?.id ?? '';
    currentUserDiscordId.value = discordId;
    newRecord.value.user_id = discordId;

    // ホワイトリスト確認
    if (discordId) {
      whitelisted.value = await checkWhitelist(discordId);
    } else {
      whitelisted.value = false;
    }
  } catch (e) {
    console.error('loadCurrentUser error:', e);
    whitelisted.value = false;
  }
};

// 記録を論理削除（バックエンド経由）
const softDeleteRecord = async (id) => {
  try {
    const url = (BACKEND ? `${BACKEND}` : '') + `/api/records/${encodeURIComponent(id)}`
    const res = await fetch(url, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'deleted' }),
    })
    if (!res.ok) {
      console.error('記録の論理削除に失敗しました:', await res.text())
      return
    }
    await fetchRecords()
  } catch (e) {
    console.error('記録の論理削除に失敗しました:', e)
  }
};

onMounted(async () => {
  await loadCurrentUser();
  await fetchRecords();
});

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