<script setup lang="ts">
import { ref } from 'vue'
import { supabase } from '@/supabase' // あなたが作ったsupabase.tsをインポート

const emit = defineEmits(['close', 'saved'])

const form = ref({
  type: 'expense', // 初期値は支出
  amount: 0,
  purpose: ''
})

const isSubmitting = ref(false)

const submit = async () => {
  isSubmitting.value = true
  
  // 1. ログイン中のユーザーを取得
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    alert('ログインしてください')
    return
  }

  // 2. Supabaseに保存
  const { error } = await supabase.from('transactions').insert({
    user_id: user.id,
    type: form.value.type,
    amount: form.value.amount,
    purpose: form.value.purpose,
    status: 'active'
  })

  if (error) {
    console.error(error)
    alert('エラーが発生しました')
  } else {
    emit('saved') // 保存完了を親に伝える
    emit('close') // 閉じる
  }
  isSubmitting.value = false
}
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content">
      <h3>新規記録</h3>
      
      <div class="form-group">
        <label>種別</label>
        <div class="radio-group">
          <label><input type="radio" value="revenue" v-model="form.type"> 収入</label>
          <label><input type="radio" value="expense" v-model="form.type"> 支出</label>
        </div>
      </div>

      <div class="form-group">
        <label>金額 (円)</label>
        <input type="number" v-model="form.amount" placeholder="0">
      </div>

      <div class="form-group">
        <label>用途</label>
        <input type="text" v-model="form.purpose" placeholder="例: サーバー代">
      </div>

      <div class="actions">
        <button @click="emit('close')" class="cancel">キャンセル</button>
        <button @click="submit" class="save" :disabled="isSubmitting">
          {{ isSubmitting ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; }
.modal-content { background: white; padding: 25px; border-radius: 12px; width: 90%; max-width: 400px; color: #333; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 0.9rem; }
input[type="text"], input[type="number"] { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 6px; }
.radio-group { display: flex; gap: 15px; }
.actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
button { padding: 8px 16px; border-radius: 6px; border: none; cursor: pointer; }
.save { background: #29B575; color: white; font-weight: bold; }
.cancel { background: #f0f0f0; color: #333; }
</style>