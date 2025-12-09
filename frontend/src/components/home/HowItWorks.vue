<script setup>
</script>

<template>
  <section class="how-root">
    <div class="how-container">
      <header class="how-head">
        <h2 class="how-title">使い方はとてもシンプル</h2>
        <p class="how-sub">3つのステップで、すぐに会計管理を始められます</p>
      </header>

      <div class="steps">
        <div class="step">
          <div class="icon-wrap">
            <div class="icon">⤴️</div>
            <div class="badge">1</div>
          </div>
          <h3>Discordでサインイン</h3>
          <p>サークルのDiscordサーバーに参加済みなら、アカウント作成は不要。Discordでサインインするだけで認証完了です。</p>
        </div>

        <div class="step">
          <div class="icon-wrap">
            <div class="icon">🧾</div>
            <div class="badge">2</div>
          </div>
          <h3>収支を記録</h3>
          <p>会計情報を簡単に入力。直感的なインターフェースで、誰でもすぐに使いこなせます。</p>
        </div>

        <div class="step">
          <div class="icon-wrap">
            <div class="icon">👥</div>
            <div class="badge">3</div>
          </div>
          <h3>メンバーと共有</h3>
          <p>サークルメンバー全員と会計情報をリアルタイムで共有。透明性の高い運営を実現します。</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* HowItWorks - centered steps with connecting line and badge */
.how-root { background: #fbfdfe; padding: 3.5rem 0 }
.how-container { max-width:1100px; margin:0 auto; padding:0 1rem }
.how-head { text-align:center; margin-bottom:2rem }
.how-title { margin:0; font-size:1.125rem; color:#0b2540 }
.how-sub { margin:0.6rem 0 0; color:#64748b }

.steps { display:flex; gap:2rem; align-items:flex-start; justify-content:space-between; position:relative; padding:2rem 1rem 0 }

.step { background:transparent; flex:1; text-align:center; padding-top:1rem }
.icon-wrap { position:relative; width:96px; height:96px; margin:0 auto 0.75rem; display:flex; align-items:center; justify-content:center }
.icon { width:72px; height:72px; border-radius:50%; background:#ffffff; display:flex; align-items:center; justify-content:center; font-size:24px; box-shadow:0 6px 18px rgba(2,6,23,0.06); border:1px solid rgba(15,23,42,0.04) }
.badge { position:absolute; right:-6px; top:-6px; min-width:36px; height:36px; padding:0 8px; background:#06b684; color:white; border-radius:999px; display:inline-flex; align-items:center; justify-content:center; font-weight:700 }

.step h3 { margin:0.75rem 0 0.5rem; color:#0b2540 }
.step p { margin:0; color:#475569; max-width:320px; margin-left:auto; margin-right:auto; line-height:1.8 }

@media (max-width:900px) {
  .steps { gap:1rem; padding-top:1rem }
}

@media (max-width:720px) {
  .steps { flex-direction:column; align-items:center; padding-top:0 }
  .steps::before { display:none }
  .step { padding:0.75rem 0 }
  .icon-wrap { width:80px; height:80px }
  .icon { width:64px; height:64px }
  .badge { min-width:30px; height:30px; right:-4px; top:-4px }
}
</style>
