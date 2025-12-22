<template>
  <div class="null-root container">
    <section class="hero">
      <div class="hero-text">
        <h1 class="title">未実装 — この機能は準備中です</h1>
        <p class="lead">現在このページはまだ実装されていません。作業中の機能ですので、しばらくお待ちください。</p>
        <div style="display:flex;gap:0.5rem;align-items:center;margin-top:0.75rem">
          <router-link to="/" class="cta">ホームへ戻る</router-link>
          <router-link to="/about" class="cta" style="background:#2b6cb0">使い方を見る</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>

</script>

<style scoped>
:root { --container-max:1200px }
.container { max-width: var(--container-max); margin: 2rem auto; padding:0 1rem }
.hero-text .title { font-size: 1.5rem; margin: 0 0 0.5rem }
.lead { color: #475569; margin-bottom: 1rem }
.cta { display: inline-block; background: #00bd7e; color: white; padding: 0.5rem 0.9rem; border-radius: 8px; text-decoration: none; font-weight: 700 }
@media (max-width: 800px) {
  .hero { grid-template-columns: 1fr }
}
</style>
