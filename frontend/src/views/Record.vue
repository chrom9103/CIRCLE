<template>
  <div>
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

// member_list テーブルに discord_id が存在するか確認（バックエンド経由）
const checkWhitelist = async (discordId) => {
  if (!discordId) return false;
  whitelistChecking.value = true;
  try {
    const url = (BACKEND ? `${BACKEND}` : '') + `/api/is_member?discord_id=${encodeURIComponent(discordId)}`
    const res = await fetch(url)
    if (!res.ok) {
      console.error('is_member check failed:', await res.text())
      return false
    }
    const json = await res.json()
    return !!json.is_member
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

  try {
    const sessionRes = await supabase.auth.getSession()
    const token = sessionRes?.data?.session?.access_token
    const url = (BACKEND ? `${BACKEND}` : '') + '/api/records'
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(recordData),
    })
    if (!res.ok) {
      console.error('記録の追加に失敗しました:', await res.text())
      return
    }
    // リセット
    newRecord.value.purpose = '';
    newRecord.value.amount = null;
    newRecord.value.category = '';
    newRecord.value.record_type = 'Expense';
    console.log('記録が正常に追加されました')
  } catch (e) {
    console.error('記録の追加に失敗しました:', e)
  }
};

onMounted(async () => {
  await loadCurrentUser();
});
</script>

<style scoped>
</style>