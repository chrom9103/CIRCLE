<script setup lang="ts">
defineProps<{
  transactions: any[]
}>

const emit = defineEmits(['delete'])

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString()
}
</script>

<template>
  <div class="list-container">
    <h3>Recent Activity</h3>
    <ul>
      <li v-for="t in transactions" :key="t.id" class="list-item">
        <div class="info">
          <span class="purpose">{{ t.purpose }}</span>
          <span class="date">{{ formatDate(t.created_at) }}</span>
        </div>
        <div class="right">
          <span :class="['amount', t.type]">
            {{ t.type === 'revenue' ? '+' : '-' }} ¥{{ t.amount.toLocaleString() }}
          </span>
          <button @click="emit('delete', t.id)" class="delete-btn">×</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.list-container { background: #fff; padding: 20px; border-radius: 12px; color: #333; }
h3 { margin-top: 0; font-size: 1.1rem; border-bottom: 1px solid #eee; padding-bottom: 10px; }
ul { list-style: none; padding: 0; }
.list-item { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
.info { display: flex; flex-direction: column; }
.purpose { font-weight: bold; }
.date { font-size: 0.8rem; color: #888; }
.right { display: flex; align-items: center; gap: 10px; }
.amount.revenue { color: #29B575; }
.amount.expense { color: #ff4d4d; }
.delete-btn { background: none; border: none; color: #ccc; cursor: pointer; font-size: 1.2rem; }
.delete-btn:hover { color: red; }
</style>