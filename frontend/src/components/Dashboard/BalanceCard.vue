<script setup lang="ts">
import { computed } from 'vue'

// 親(Dashboard)からデータを受け取る定義
const props = defineProps<{
  transactions: any[] 
}>

// 合計を計算するロジック
const totalBalance = computed(() => {
  return props.transactions.reduce((sum, t) => {
    return t.type === 'revenue' ? sum + t.amount : sum - t.amount
  }, 0)
})

const income = computed(() => {
  return props.transactions
    .filter(t => t.type === 'revenue')
    .reduce((sum, t) => sum + t.amount, 0)
})

const expense = computed(() => {
  return props.transactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0)
})

// 金額をカンマ区切りにする関数 (例: 1000 -> 1,000)
const formatMoney = (amount: number) => amount.toLocaleString()
</script>

<template>
  <div class="balance-card">
    <div class="main-balance">
      <h2>Total Balance</h2>
      <p class="amount">¥ {{ formatMoney(totalBalance) }}</p>
    </div>
    <div class="stats">
      <div class="stat-item income">
        <span>Income</span>
        <p>+ ¥{{ formatMoney(income) }}</p>
      </div>
      <div class="stat-item expense">
        <span>Expense</span>
        <p>- ¥{{ formatMoney(expense) }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.balance-card {
  background: var(--color-balancecard-bg); /* Dashboard card background (configurable) */
  color: var(--color-balancecard-text);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  margin-bottom: 20px;
}
.main-balance h2 { font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 5px; }
.main-balance .amount { font-size: 2.5rem; font-weight: bold; margin: 0; }

.stats { display: flex; gap: 20px; margin-top: 20px; }
.stat-item span { font-size: 0.8rem; color: rgba(255,255,255,0.6); }
.stat-item p { font-size: 1.1rem; font-weight: bold; margin: 0; }
.income p { color: var(--color-accent-success); } /* Pied Piper Green */
.expense p { color: var(--color-accent-danger); }
</style>