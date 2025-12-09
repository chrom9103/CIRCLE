<template>
  <div>
    <div v-if="loading">
      <p>データを読み込み中...</p>
    </div>

    <ul v-else>
      <li v-for="record in records" :key="record.transaction_id">
        <div>
          <span :class="{'text-red-600': record.record_type === 'Expense', 'text-green-600': record.record_type === 'Revenue'}">
            {{ record.record_type === 'Expense' ? 'ー' : '＋' }} {{ record.amount.toLocaleString() }} 円
          </span>
          <span> | {{ record.purpose }}</span>
          <p>カテゴリ: {{ record.category }} / ID: {{ record.transaction_id.substring(0, 8) }}...</p>
        </div>

        <button @click="onSoftDelete(record.transaction_id)">取消済にする</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  records: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['soft-delete'])

function onSoftDelete(id) {
  emit('soft-delete', id)
}
</script>

<style scoped>
ul { list-style: none; padding: 0; }
li { margin-bottom: 1rem; padding: 0.5rem; border: 1px solid #eee; border-radius: 6px; }
button { margin-top: 0.5rem; }
</style>
