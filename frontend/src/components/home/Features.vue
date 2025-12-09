<script setup>
</script>

<template>
  <section class="features-root container">
    <div class="features-head">
      <p class="features-kicker">サークル運営をもっとスムーズに</p>
      <p class="features-lead">PiedPiper青山テック愛好会の活動に必要な会計機能をすべて備えています</p>
    </div>

    <div class="features-grid">
      <article class="feature">
        <div class="feature-icon">💲</div>
        <h3>簡単な収支管理</h3>
        <p>サークルの収入と支出を一目で把握。カテゴリーごとに分類してお金の流れが見えやすくなります。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">👥</div>
        <h3>メンバーと共有</h3>
        <p>全てのメンバーが会計情報にアクセス可能。透明性の高い運営で信頼関係を築けます。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">📊</div>
        <h3>わかりやすいレポート</h3>
        <p>月次レポートやグラフで収支を可視化。活動の振り返りや予算計画に役立ちます。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">🛡️</div>
        <h3>Discord認証</h3>
        <p>アカウント作成不要。サークルのDiscordサーバーメンバーなら、すぐにサインインできます。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">🔔</div>
        <h3>通知機能</h3>
        <p>重要な更新や承認リクエストを通知。見逃しなく、タイムリーな対応が可能です。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">📄</div>
        <h3>履歴管理</h3>
        <p>すべての取引履歴を保存。過去のデータもいつでも確認できるので安心です。</p>
      </article>
    </div>
  </section>
</template>

<style scoped>
/* Features: centered head + icon cards (white, soft shadow) */
.features-root { background: #fff; padding: 3rem 0 }
.features-head { text-align:center; max-width:900px; margin:0 auto 2rem }
.features-kicker { margin:0; color:#475569; font-size:0.95rem }
.features-lead { margin:0.6rem 0 0; color:#64748b }

.features-grid { display:grid; grid-template-columns: repeat(4, 1fr); gap:1.5rem; max-width:1200px; margin:1.25rem auto 0; }
.feature { background:#fff; border:1px solid rgba(15,23,42,0.04); padding:1.4rem; border-radius:16px; box-shadow: 0 10px 30px rgba(2,6,23,0.04); min-height:160px; display:flex; flex-direction:column; gap:0.75rem }
.feature-icon { width:48px; height:48px; border-radius:50%; background: #ecfdf5; display:inline-flex; align-items:center; justify-content:center; font-size:20px }
.feature h3 { margin:0; font-size:1rem; color:#0b2540 }
.feature p { margin:0; color:#475569; font-size:0.95rem; line-height:1.6 }

@media (max-width:1100px) {
  .features-grid { grid-template-columns: repeat(3,1fr); padding:0 1rem }
}

@media (max-width:800px) {
  .features-grid { grid-template-columns: repeat(2,1fr) }
}

@media (max-width:520px) {
  .features-grid { grid-template-columns: 1fr }
  .features-head { padding: 0 1rem }
}
</style>
