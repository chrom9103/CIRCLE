<script setup>
import { ref, onMounted, computed } from 'vue';
import { supabase } from '@/supabase'; 
import { BACKEND } from '@/runtimeConfig'
const emit = defineEmits(['close', 'saved'])

const currentUserDiscordId = ref('');
const whitelisted = ref(false);
const whitelistChecking = ref(false);
const isSubmitting = ref(false);

const newRecord = ref({
    purpose: '',
    amount: null,
    record_type: 'Expense',
    category: '',
    user_id: '', 
    evidence_file_link: '',
});

// category length limit kept for validation but free-text removed

const revenueCategories = [
  '会費',
  '前年度繰越金',
  'イベント参加費',
  '大学公認助成金',
  '協賛金・寄付金',
  '雑収入',
]

const expenseCategories = [
  '旅費交通費',
  '広報・宣伝費',
  '行事・イベント費',
  '活動助成・補助',
  '消耗品費',
  '事務手数料',
  '備品費',
  '雑費',
]

const categoryOptions = computed(() => {
  return (newRecord.value.record_type || '').toString().toLowerCase() === 'revenue'
    ? revenueCategories
    : expenseCategories
})

const isFormValid = computed(() => {
    const cat = (newRecord.value.category || '').toString().trim()
    return newRecord.value.purpose.trim() !== '' &&
           newRecord.value.amount !== null &&
           newRecord.value.amount >= 0 &&
           newRecord.value.record_type.trim() !== '' &&
           cat !== '';
});

// ホワイトリストチェック (Record.vueから移植)
const checkWhitelist = async (discordId) => {
  if (!discordId) return false;
  whitelistChecking.value = true;
  try {
    const url = (BACKEND ? `${BACKEND}` : '') + `/api/is_member?discord_id=${encodeURIComponent(discordId)}`
    const res = await fetch(url)
    if (!res.ok) return false
    const json = await res.json()
    return !!json.is_member
  } catch (e) {
    console.error('checkWhitelist exception:', e);
    return false;
  } finally {
    whitelistChecking.value = false;
  }
};

// ユーザー取得
onMounted(async () => {
  const { data } = await supabase.auth.getUser();
  const discordId = data.user?.identities?.[0]?.id ?? '';
  currentUserDiscordId.value = discordId;
  newRecord.value.user_id = discordId;
  
  if (discordId) {
    whitelisted.value = await checkWhitelist(discordId);
  }
});

// 送信処理
const submit = async () => {
  if (!isFormValid.value || !whitelisted.value) return;
  isSubmitting.value = true;

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
      body: JSON.stringify({
        ...newRecord.value,
        status: 'active'
      }),
    })

    if (!res.ok) throw new Error(await res.text())
    
    emit('saved') // 保存成功を親に通知
    emit('close') // 閉じる
  } catch (e) {
    console.error('Error:', e)
    alert('登録に失敗しました')
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content">
      <h3>新規記録の追加</h3>
      
      <div v-if="whitelistChecking" class="loading-text">権限を確認中...</div>
      
      <div v-else-if="!whitelisted && currentUserDiscordId" class="error-box">
        <p>あなたのIDはホワイトリストに登録されていないため、記録できません。</p>
      </div>

      <div v-else>
        <div class="form-group">
          <label>用途</label>
          <input v-model="newRecord.purpose" placeholder="例: 備品購入" maxlength="50" class="input-field"/>
        </div>

        <div class="form-group">
          <label>金額 (円)</label>
          <input v-model.number="newRecord.amount" type="number" min="0" placeholder="0" class="input-field"/>
        </div>

        <div class="form-row">
          <div class="form-group half">
            <label>種別</label>
            <select v-model="newRecord.record_type" class="input-field">
              <option value="Expense">歳出 (Expense)</option>
              <option value="Revenue">歳入 (Revenue)</option>
            </select>
          </div>
          <div class="form-group half">
            <label>カテゴリ</label>
            <select v-model="newRecord.category" class="input-field">
              <option value="">選択してください</option>
              <option v-for="opt in categoryOptions" :key="opt" :value="opt">{{ opt }}</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>領収書リンク（任意）</label>
          <input v-model="newRecord.evidence_file_link" placeholder="https://..." class="input-field" />
        </div>

        <div class="actions">
          <button @click="emit('close')" class="cancel-btn">キャンセル</button>
          <button @click="submit" class="save-btn" :disabled="!isFormValid || isSubmitting">
            {{ isSubmitting ? '送信中...' : '登録する' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); z-index: 1000; display: flex; justify-content: center; align-items: center; }
.modal-content { background: var(--color-background); padding: 25px; border-radius: 12px; width: 90%; max-width: 450px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
h3 { margin-top: 0; color: var(--color-heading); border-bottom: 1px solid var(--color-border); padding-bottom: 10px; }
.form-group { margin-bottom: 15px; }
.form-row { display: flex; gap: 10px; }
.half { flex: 1; }
label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 0.9rem; color: var(--color-text); }
.input-field { width: 100%; padding: 10px; border: 1px solid var(--color-border); border-radius: 6px; font-size: 1rem; box-sizing: border-box; background: var(--color-background-soft); color: var(--color-text); }
.actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.cancel-btn { padding: 10px 20px; background: var(--color-background-soft); border: none; border-radius: 6px; cursor: pointer; color: var(--color-text); }
.save-btn { padding: 10px 20px; background: var(--color-accent-success); border: none; border-radius: 6px; cursor: pointer; color: var(--vt-c-white); font-weight: bold; }
.save-btn:disabled { background: var(--color-border-weak); cursor: not-allowed; }
.error-box { background: var(--color-alert-danger-bg); color: var(--color-alert-danger-text); padding: 10px; border-radius: 6px; font-size: 0.9rem; }
</style>