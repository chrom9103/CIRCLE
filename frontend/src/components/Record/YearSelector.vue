<script setup lang="ts">
defineProps<{ currentYear: number | 'all' }>()
const emit = defineEmits(['update:year'])

const years = [2024, 2025] 
</script>

<template>
  <div class="year-selector">
    <button 
      class="tab" 
      :class="{ active: currentYear === 'all' }" 
      @click="emit('update:year', 'all')"
    >
      全期間
    </button>
    <button 
      v-for="y in years" 
      :key="y" 
      class="tab"
      :class="{ active: currentYear === y }"
      @click="emit('update:year', y)"
    >
      {{ y }}年度
    </button>
  </div>
</template>

<style scoped>
.year-selector { display: flex; gap: 8px; overflow-x: auto; }
.tab {
  padding: 8px 16px; border: none; background: #eee; border-radius: 20px;
  font-weight: bold; color: #666; cursor: pointer; transition: 0.2s; white-space: nowrap;
}
.tab:hover { background: #ddd; }
.tab.active { background: #2c3e50; color: white; }
</style>