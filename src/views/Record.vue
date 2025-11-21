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

    <!-- 新規記録の入力フォーム -->
    <div>
        <h2>新規記録の追加</h2>
        
        <div>
            <!-- 用途 -->
            <input v-model="newRecord.purpose" placeholder="用途 (例: 備品購入)" maxlength="50"/>
            <!-- 金額 -->
            <input v-model.number="newRecord.amount" type="number" min="0" placeholder="金額 (円)"/>
            <!-- 種別 & カテゴリ (ドロップダウン) -->
            <div class="flex space-x-2">
                <select v-model="newRecord.record_type">
                    <option value="Expense">歳出 (Expense)</option>
                    <option value="Revenue">歳入 (Revenue)</option>
                </select>
                <select v-model="newRecord.category">
                    <option value="">カテゴリを選択 (必須)</option>
                    <option value="備品">備品</option>
                    <option value="交通費">交通費</option>
                    <option value="会費">会費</option>
                    <option value="雑費">雑費</option>
                </select>
            </div>

            <!-- 必須チェックメッセージ -->
            <p v-if="!isFormValid">
                用途、金額、種別、カテゴリは必須です。（金額は0以上）
            </p>
            
            <p v-if="currentUserDiscordId"><strong>あなたのID:</strong> {{ currentUserDiscordId }}</p>
            <p v-else><em>サインインしているユーザのIDを取得できませんでした</em></p>

            <p v-if="whitelistChecking">ホワイトリストを確認中...</p>
            <p v-else-if="!whitelisted && currentUserDiscordId" style="color: #c00;">
              あなたのIDはホワイトリストに登録されていないため、記録登録はできません。
            </p>
        </div>

        <!-- 追加ボタン -->
        <button @click="addRecord" :disabled="!isFormValid || !currentUserDiscordId || !whitelisted"
                class="mt-4 w-full py-2 text-white font-bold rounded-md transition duration-150"
                :class="{
                    'bg-blue-600 hover:bg-blue-700': isFormValid && currentUserDiscordId && whitelisted,
                    'bg-gray-400 cursor-not-allowed': !isFormValid || !currentUserDiscordId || !whitelisted}">
            記録を登録
        </button>
    </div>
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

// フォームの入力チェック
const isFormValid = computed(() => {
    return newRecord.value.purpose.trim() !== '' &&
           newRecord.value.amount !== null &&
           newRecord.value.amount >= 0 &&
           newRecord.value.record_type.trim() !== '' &&
           newRecord.value.category.trim() !== '';
});

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

// 記録を追加（ホワイトリスト未登録なら拒否）
const addRecord = async () => {
  if (!isFormValid.value || !currentUserDiscordId.value) return;

  // 再確認（race 対策）
  if (!whitelisted.value) {
    whitelisted.value = await checkWhitelist(currentUserDiscordId.value);
    if (!whitelisted.value) {
      alert('あなたのIDはホワイトリストに登録されていないため、記録登録できません。');
      return;
    }
  }

  const recordData = {
    user_id: newRecord.value.user_id,
    record_type: newRecord.value.record_type,
    amount: newRecord.value.amount,
    category: newRecord.value.category,
    purpose: newRecord.value.purpose,
    status: 'active',
  };

  const { error } = await supabase
    .from('financial_records')
    .insert([recordData]);

  if (!error) {
    // フォームをリセット
    newRecord.value.purpose = '';
    newRecord.value.amount = null;
    newRecord.value.category = '';
    newRecord.value.record_type = 'Expense';
    fetchRecords();
    console.log('記録が正常に追加されました');
  } else {
     console.error('記録の追加に失敗しました:', error.message);
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