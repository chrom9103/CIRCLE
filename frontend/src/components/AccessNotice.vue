<template>
  <div v-if="accessDenied" style="padding:1rem; border:1px solid #f3c; background:#fff5f5;">
    <p style="color:#a00; font-weight:600">アクセスが拒否されました。</p>
    <p v-if="!discordId">サインインしてください。</p>
    <div style="margin-top:0.5rem">
      <router-link to="/signin">サインインページへ</router-link>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  accessDenied: { type: Boolean, required: true },
  discordId: { type: String, default: '' }
})
</script>
