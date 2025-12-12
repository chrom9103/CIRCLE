<script setup lang="ts">
defineProps<{ transactions: any[] }>()

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString()
}
</script>

<template>
  <div class="table-container">
    <table class="ledger-table">
      <thead>
        <tr>
          <th>日付</th>
          <th>用途 / カテゴリ</th>
          <th class="text-right">金額</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in transactions" :key="t.transaction_id || t.id">
          <td class="date-col">{{ formatDate(t.created_at) }}</td>
          <td>
            <div class="purpose">{{ t.purpose }}</div>
            <div class="meta">
              <span class="category">{{ t.category }}</span>
            </div>
          </td>
          <td :class="['amount-col', (t.record_type || t.type || '').toLowerCase()]">
            {{ (t.record_type || t.type || '').toLowerCase().includes('revenue') ? '+' : '-' }} 
            ¥{{ Number(t.amount).toLocaleString() }}
          </td>
        </tr>
        <tr v-if="transactions.length === 0">
          <td colspan="3" class="empty-state">データがありません</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container { overflow-x: auto; background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.ledger-table { width: 100%; border-collapse: collapse; min-width: 500px; }
th { background: #f8f9fa; padding: 12px; text-align: left; font-size: 0.85rem; color: #666; border-bottom: 2px solid #eee; }
td { padding: 12px; border-bottom: 1px solid #eee; }
.text-right { text-align: right; }
.purpose { font-weight: 600; color: #333; }
.meta { display: flex; gap: 8px; align-items: center; margin-top: 4px; }
.category { font-size: 0.75rem; color: #888; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; }
.amount-col { text-align: right; font-family: monospace; font-weight: bold; }
.amount-col[class*="revenue"], .amount-col[class*="income"] { color: #29B575; }
.amount-col[class*="expense"], .amount-col[class*="expenditure"] { color: #e03131; }
.empty-state { text-align: center; padding: 30px; color: #999; }
</style>