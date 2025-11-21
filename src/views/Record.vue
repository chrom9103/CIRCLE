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
        </div>

        <!-- 追加ボタン -->
        <button @click="addRecord" :disabled="!isFormValid"
                class="mt-4 w-full py-2 text-white font-bold rounded-md transition duration-150"
                :class="{'bg-blue-600 hover:bg-blue-700': isFormValid, 'bg-gray-400 cursor-not-allowed': !isFormValid}">
            記録を登録
        </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { supabase } from '../supabase'; 

const records = ref([]);
const newRecord = ref({
    purpose: '',
    amount: null,
    record_type: 'Expense',
    category: '',
    user_id: '', 
});
const loading = ref(false);

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
    records.value = data;
  } else {
    console.error('データの取得に失敗しました:', error.message);
  }
  loading.value = false;
};


// 記録を追加
const addRecord = async () => {
  if (!isFormValid.value) return;

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
    console.log('記録が正常に追加されました\n', newRecord.value);
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

onMounted(fetchRecords);
</script>

<style scoped>
</style>