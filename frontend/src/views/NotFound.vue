<template>
  <div class="notfound-root container">
    <section class="hero">
      <div class="hero-text">
        <h1 class="title">404 — ページが見つかりません</h1>
        <p class="lead">お探しのページは存在しないか、移動した可能性があります。</p>
        <router-link to="/" class="cta">ホームへ戻る</router-link>
      </div>
    </section>
  </div>
</template>

<script setup>

</script>

<style scoped>
:root { --container-max:1200px }
.container { max-width: var(--container-max); margin: 2rem auto; padding:0 1rem }
.hero-text .title { font-size: 1.75rem; margin: 0 0 0.5rem }
.lead { color: #475569; margin-bottom: 1rem }
.cta { display: inline-block; background: #00bd7e; color: white; padding: 0.5rem 0.9rem; border-radius: 8px; text-decoration: none; font-weight: 700 }
</style>
