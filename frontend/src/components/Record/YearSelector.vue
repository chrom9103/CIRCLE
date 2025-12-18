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
  padding: 8px 16px; border: none; background: var(--color-background-mute); border-radius: 20px;
  font-weight: bold; color: var(--color-text); cursor: pointer; transition: 0.2s; white-space: nowrap;
}
.tab:hover { background: var(--color-background-soft); }
.tab.active { background: var(--vt-c-indigo); color: var(--vt-c-white); }
</style>