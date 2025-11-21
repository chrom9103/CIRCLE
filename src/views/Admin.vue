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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { supabase } from '../supabase'; 

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

const whitelisted = ref(false);
const whitelistChecking = ref(false);

// status='active' の記録のみを表示
const activeRecords = computed(() => {
    return records.value.filter(r => r.status === 'active');
});

// DBから記録を取得
const fetchRecords = async () => {
  loading.value = true;
  const { data, error } = await supabase
    .from('financial_records')
    .select('*')
    .order('created_at', { ascending: false });
    
    if (!error) {
      records.value = data || [];
    } else {
      console.error('データの取得に失敗しました:', error.message);
    }
  loading.value = false;
};

// member_list テーブルに discord_id が存在するか確認
const checkWhitelist = async (discordId) => {
  if (!discordId) return false;
  whitelistChecking.value = true;
  try {
    console.log('supabase config', import.meta.env.VITE_SUPABASE_URL)
    const { data, error } = await supabase
      .from('member_list')
      .select('*')
      .eq('discord_id', discordId)
      .limit(1);
    console.log(discordId, data, error);

    if (error) {
      console.error('whitelist check error:', error.message || error);
      return false;
    }
    return Array.isArray(data) && data.length > 0;
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

// 記録を論理削除 
const softDeleteRecord = async (id) => {
  const { error } = await supabase
    .from('financial_records')
    .update({ status: 'deleted' })
    .eq('id', id);

  if (!error) {
    fetchRecords();
  } else {
    console.error('記録の論理削除に失敗しました:', error.message);
  }
};

onMounted(async () => {
  await loadCurrentUser();
  await fetchRecords();
});
</script>

<style scoped>
</style>