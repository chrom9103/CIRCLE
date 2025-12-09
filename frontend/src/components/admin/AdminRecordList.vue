<template>
  <div class="record-list-wrapper">
    <div v-if="loading">
      <p>データを読み込み中...</p>
    </div>

    <div v-else>
      <div class="records-stack">
        <template v-if="Array.isArray(records) && records.length > 0">
          <div v-for="record in records" :key="record.transaction_id" class="record-card">
            <div class="record-card__header">
              <div class="record-card__left">
                <div class="record-purpose">{{ record.purpose || '-' }}</div>
                <div class="record-meta">{{ record.category || '' }}</div>
              </div>
              <div class="record-card__right">
                <div :class="['record-amount', amountClass(record)]">{{ formatAmount(record.amount) }}</div>
                <div class="record-date">{{ formatDate(record.created_at) }}</div>
                <div class="details-actions">
                  <button class="small icon-btn" @click="onSoftDelete(record.transaction_id)" title="取消済にする"><img :src="trashIcon" alt="取消" /></button>
                  <button v-if="record.status !== 'processed'" class="small icon-btn" @click="onMarkProcessed(record.transaction_id)" title="清算済みにする"><img :src="proceedIcon" alt="清算済みにする" /></button>
                  <button v-if="record.status !== 'active'" class="small icon-btn" @click="onMarkUnprocessed(record.transaction_id)" title="未清算にする"><img :src="activeIcon" alt="未清算にする" /></button>
                </div>
                <button class="expand-btn" @click="toggleExpand(record.transaction_id)" :aria-expanded="isExpanded(record.transaction_id)">
                  <span v-if="isExpanded(record.transaction_id)">▾</span>
                  <span v-else>▸</span>
                </button>
              </div>
            </div>

            <transition name="fade">
              <div v-if="isExpanded(record.transaction_id)" class="record-card__body">
                <div class="record-detail"><strong>user_id:</strong> {{ record.user_id || '-' }}</div>
                <div class="record-detail"><strong>record_type:</strong> {{ record.record_type || '-' }}</div>
                <div class="record-detail"><strong>status:</strong> <span :class="['status-badge', record.status]">{{ record.status || '-' }}</span></div>
                <div class="record-detail"><strong>evidence:</strong>
                  <a v-if="record.evidence_file_link" :href="record.evidence_file_link" target="_blank" rel="noopener">表示</a>
                  <span v-else>-</span>
                </div>
                
              </div>
            </transition>
          </div>
        </template>
        <div v-else class="empty-stack">No records found.</div>
      </div>

      <p v-if="Array.isArray(records) && records.length === 0">No records found.</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue'
import trashIcon from '../../assets/admin/trashcan-icon.png'
import activeIcon from '../../assets/admin/active-icon.png'
import proceedIcon from '../../assets/admin/proceed-icon.png'

const props = defineProps({
  records: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['soft-delete', 'mark-processed', 'mark-unprocessed'])

// expanded row state (array of transaction_id)
const expanded = ref([])

function toggleExpand(id) {
  const i = expanded.value.indexOf(id)
  if (i === -1) expanded.value.push(id)
  else expanded.value.splice(i, 1)
}

function isExpanded(id) {
  return expanded.value.includes(id)
}

function amountClass(record) {
  const amt = Number(record?.amount)
  if (!Number.isNaN(amt) && amt < 0) return 'expense'
  const t = String(record?.record_type || '').toLowerCase()
  if (t.includes('expense') || t.includes('支出') || t.includes('歳出')) return 'expense'
  return 'income'
}

function onSoftDelete(id) {
  emit('soft-delete', id)
}

function onMarkProcessed(id) {
  emit('mark-processed', id)
}

function onMarkUnprocessed(id) {
  emit('mark-unprocessed', id)
}

function formatAmount(v) {
  if (v === null || v === undefined || v === '') return '-'
  const n = Number(v)
  if (Number.isNaN(n)) return String(v)
  return n.toLocaleString()
}

function formatDate(d) {
  if (!d) return '-'
  try {
    const t = new Date(d)
    if (Number.isNaN(t.getTime())) return String(d)
    const y = t.getFullYear()
    const m = String(t.getMonth() + 1).padStart(2, '0')
    const day = String(t.getDate()).padStart(2, '0')
    return `${y}/${m}/${day}`
  } catch (_) {
    return String(d)
  }
}
</script>

<style scoped>
.record-list-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; padding: 8px; }

/* Stack container */
.records-stack { display: flex; flex-direction: column; gap: 0.75rem; max-width: 100%; align-items: center; }

/* Card */
.record-card { background: #fff; border: 1px solid #e6e6e6; border-radius: 8px; box-shadow: 0 1px 2px rgba(16,24,40,0.04); overflow: hidden; width: 100%; max-width: 900px; margin: 0 auto; }
.record-card__header { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; gap: 0.5rem; }
.record-card__left { display: flex; flex-direction: column; }
.record-purpose { font-weight: 600; color: #0f172a; }
.record-meta { font-size: 0.85rem; color: #6b7280; }
.record-card__right { display: flex; align-items: center; gap: 0.75rem; }
.record-amount { font-weight: 700; color: #0b5; min-width: 90px; text-align: right; }
.record-amount.income { color: #059669; }
.record-amount.expense { color: #dc2626; }
.record-date { font-size: 0.85rem; color: #6b7280; white-space: nowrap; }
.expand-btn { background: transparent; border: none; padding: 4px 8px; cursor: pointer; color: #374151; font-size: 24px; }

.record-card__body { padding: 0.5rem 0.75rem 0.75rem 0.75rem; background: #fbfbfe; border-top: 1px solid #eef2ff; display: flex; flex-direction: column; gap: 0.5rem; }
.record-detail { font-size: 0.9rem; color: #334155; }
.details-actions { display: flex; gap: 0.5rem; }

.small { padding: 0.25rem 0.5rem; font-size: 0.85rem; border-radius: 6px; }
/* Icon button for actions */
.icon-btn { display: inline-flex; align-items: center; justify-content: center; padding: 0.25rem; border: 1px solid transparent; background: transparent; border-radius: 6px; cursor: pointer; }
.icon-btn img { width: 20px; height: 20px; display: block; }

.empty-stack { padding: 1rem; color: #6b7280; }

/* simple fade transition */
.fade-enter-active, .fade-leave-active { transition: opacity 160ms ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (min-width: 900px) {
  .record-card { max-width: 900px; }
}

</style>

