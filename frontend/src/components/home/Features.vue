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
        <div class="feature-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-dollar-sign w-7 h-7 text-gray-900" aria-hidden="true">
            <line x1="12" x2="12" y1="2" y2="22"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
        </div>
        <h3>簡単な収支管理</h3>
        <p>サークルの収入と支出を一目で把握。カテゴリーごとに分類してお金の流れが見えやすくなります。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users w-7 h-7 text-gray-900" aria-hidden="true">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><path d="M16 3.128a4 4 0 0 1 0 7.744"></path>
            <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
            <circle cx="9" cy="7" r="4"></circle>
          </svg>
        </div>
        <h3>メンバーと共有</h3>
        <p>全てのメンバーが会計情報にアクセス可能。透明性の高い運営で信頼関係を築けます。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chart-column w-7 h-7 text-gray-900" aria-hidden="true">
            <path d="M3 3v16a2 2 0 0 0 2 2h16"></path>
            <path d="M18 17V9"></path>
            <path d="M13 17V5"></path>
            <path d="M8 17v-3"></path>
          </svg>
        </div>
        <h3>わかりやすいレポート</h3>
        <p>月次レポートやグラフで収支を可視化。活動の振り返りや予算計画に役立ちます。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield w-7 h-7 text-gray-900" aria-hidden="true">
            <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path>
        </svg>
        </div>
        <h3>Discord認証</h3>
        <p>アカウント作成不要。サークルのDiscordサーバーメンバーなら、すぐにサインインできます。</p>
      </article>

      <article class="feature">
        <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-text w-7 h-7 text-gray-900" aria-hidden="true">
              <path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"></path>
              <path d="M14 2v5a1 1 0 0 0 1 1h5"></path>
              <path d="M10 9H8"></path>
              <path d="M16 13H8"></path>
              <path d="M16 17H8"></path>
            </svg>
        </div>
        <h3>履歴管理</h3>
        <p>すべての取引履歴を保存。過去のデータもいつでも確認できるので安心です。</p>
      </article>
    </div>
  </section>
</template>

<style scoped>
/* Features: centered head + icon cards (white, soft shadow) */
.features-root { background: var(--color-background); padding: 3rem 0 }
.features-head { text-align:center; max-width:900px; margin:0 auto 2rem }
.features-kicker { margin:0; color: var(--color-text); font-size:0.95rem }
.features-lead { margin:0.6rem 0 0; color: var(--color-muted) }

.features-grid { display:grid; grid-template-columns: repeat(4, 1fr); gap:1.5rem; max-width:1200px; margin:1.25rem auto 0; }
.feature { background: var(--color-background); border:1px solid var(--color-border); padding:1.4rem; border-radius:16px; box-shadow: 0 10px 30px rgba(2,6,23,0.04); min-height:160px; display:flex; flex-direction:column; gap:0.75rem }
.feature-icon { width:48px; height:48px; border-radius:50%; background: var(--color-surface-soft); display:inline-flex; align-items:center; justify-content:center; font-size:20px }
.feature h3 { margin:0; font-size:1rem; color: var(--color-heading) }
.feature p { margin:0; color: var(--color-text); font-size:0.95rem; line-height:1.6 }

/* SVG icons should follow theme colors (invert in dark mode) */
.feature-icon svg { color: var(--color-background-mute) !important; }
.feature-icon svg path,
.feature-icon svg line,
.feature-icon svg circle { stroke: currentColor; fill: none; }

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
