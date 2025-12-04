<template>
  <div style="margin: 1rem 0;">
    <button @click="emitSyncAdmins" :disabled="syncingAdmins">管理者(sync admin_list)</button>
    <button @click="emitSyncMembers" :disabled="syncingMembers" style="margin-left: 0.5rem;">メンバー(sync member_list)</button>
    <span v-if="syncMessage" style="margin-left:0.75rem">{{ syncMessage }}</span>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  syncingAdmins: { type: Boolean, default: false },
  syncingMembers: { type: Boolean, default: false },
  syncMessage: { type: String, default: '' },
})

const emit = defineEmits(['sync-admins', 'sync-members'])

const emitSyncAdmins = () => emit('sync-admins')
const emitSyncMembers = () => emit('sync-members')
</script>
