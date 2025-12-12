<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ transactions: any[] }>()

const total = computed(() => {
  return props.transactions.reduce((sum, t) => {
    const amt = Number(t.amount)
    // API/DBのカラム名の揺れに対応
    const type = (t.record_type || t.type || '').toLowerCase()
    
    // 収入(Revenue/Income)ならプラス、それ以外はマイナス
    if (type.includes('revenue') || type.includes('income')) {
      return sum + amt
    } else {
      return sum - amt
    }
  }, 0)
})
</script>

<template>
  <div class="banner">
    <div class="label">Balance (表示計)</div>
    <div class="amount" :class="{ minus: total < 0 }">
      ¥ {{ total.toLocaleString() }}
    </div>
  </div>
</template>

<style scoped>
.banner {
  background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px;
  display: flex; justify-content: space-between; align-items: center;
  border-left: 5px solid #2c3e50; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.label { font-size: 0.9rem; color: #888; font-weight: bold; }
.amount { font-size: 1.8rem; font-weight: 800; color: #2c3e50; font-family: monospace; }
.amount.minus { color: #e03131; }
</style>