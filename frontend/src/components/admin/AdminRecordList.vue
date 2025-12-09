<style scoped>
    ul { list-style: none; padding: 0; }
    li { margin-bottom: 1rem; padding: 0.5rem; border: 1px solid #eee; border-radius: 6px; }
    button { margin-top: 0.5rem; }
</style>
<template>
  <div class="record-list-wrapper">
    <div v-if="loading">
      <p>データを読み込み中...</p>
    </div>

    <div v-else>
      <div class="table-scroll">
        <table class="records-table">
          <thead>
            <tr>
              <th>user_id</th>
              <th>record_type</th>
              <th>amount</th>
              <th>category</th>
              <th>purpose</th>
              <th>evidence</th>
              <th>status</th>
              <th>created_at</th>
              <th>actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in records" :key="record.transaction_id">
              <td class="mono">{{ record.user_id || '-' }}</td>
              <td>{{ record.record_type || '-' }}</td>
              <td class="mono">{{ formatAmount(record.amount) }}</td>
              <td>{{ record.category || '-' }}</td>
              <td class="purpose">{{ record.purpose || '-' }}</td>
              <td>
                <a v-if="record.evidence_file_link" :href="record.evidence_file_link" target="_blank" rel="noopener">表示</a>
                <span v-else>-</span>
              </td>
              <td>
                <span :class="['status-badge', record.status]">{{ record.status || '-' }}</span>
              </td>
              <td>{{ formatDate(record.created_at) }}</td>
              <td>
                <button class="small" @click="onSoftDelete(record.transaction_id)">取消済にする</button>
                <button class="small" style="margin-left:0.5rem" @click="onMarkProcessed(record.transaction_id)">清算済みにする</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-if="Array.isArray(records) && records.length === 0">No records found.</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  records: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['soft-delete', 'mark-processed'])

function onSoftDelete(id) {
  emit('soft-delete', id)
}

function onMarkProcessed(id) {
  emit('mark-processed', id)
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
    return t.toLocaleString()
  } catch (_) {
    return String(d)
  }
}
</script>

<style scoped>
.table-scroll { overflow-x: auto; }
.records-table { width: 100%; border-collapse: collapse; min-width: 900px; }
.records-table th, .records-table td { padding: 0.5rem 0.75rem; border: 1px solid #e6e6e6; text-align: left; vertical-align: top; }
.records-table th { background: #fafafa; font-weight: 700; font-size: 0.95rem; }
.records-table td.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace; font-size: 0.85rem; }
.records-table td.purpose { max-width: 360px; white-space: pre-wrap; word-break: break-word; }
.status-badge { padding: 0.15rem 0.5rem; border-radius: 6px; font-size: 0.8rem; display: inline-block; }
.status-badge.active { background: #e6ffed; color: #036a2a; border: 1px solid #c2f0d0; }
.status-badge.deleted { background: #fff1f0; color: #9b1b1b; border: 1px solid #f5c2c0; }
.small { padding: 0.25rem 0.5rem; font-size: 0.85rem; border-radius: 6px; }
@media (max-width: 720px) {
  .records-table { min-width: 720px; }
}
</style>
