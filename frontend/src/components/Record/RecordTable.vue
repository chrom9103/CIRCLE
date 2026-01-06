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
          <th>証憑</th>
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
          <td class="evidence-col">
            <div v-if="t.evidence_file_link">
              <a :href="t.evidence_file_link" target="_blank" rel="noopener noreferrer">表示</a>
            </div>
            <div v-else>-</div>
          </td>
          <td :class="['amount-col', (t.record_type || t.type || '').toLowerCase()]">
            {{ (t.record_type || t.type || '').toLowerCase().includes('revenue') ? '+' : '-' }} 
            ¥{{ Number(t.amount).toLocaleString() }}
          </td>
        </tr>
        <tr v-if="transactions.length === 0">
          <td colspan="4" class="empty-state">データがありません</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container { overflow-x: auto; background: var(--color-background); border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.ledger-table { width: 100%; border-collapse: collapse; min-width: 500px; }
th { background: var(--color-background-soft); padding: 12px; text-align: left; font-size: 0.85rem; color: var(--color-text); border-bottom: 2px solid var(--color-border); }
td { padding: 12px; border-bottom: 1px solid var(--color-border); }
.text-right { text-align: right; }
.purpose { font-weight: 600; color: var(--color-heading); }
.meta { display: flex; gap: 8px; align-items: center; margin-top: 4px; }
.category { font-size: 0.75rem; color: var(--color-text); background: var(--color-background-mute); padding: 2px 6px; border-radius: 4px; }
.amount-col { text-align: right; font-family: monospace; font-weight: bold; }
.amount-col[class*="revenue"], .amount-col[class*="income"] { color: var(--color-accent-success); }
.amount-col[class*="expense"], .amount-col[class*="expenditure"] { color: var(--color-accent-danger); }
.empty-state { text-align: center; padding: 30px; color: var(--color-text); opacity: 0.7; }
</style>