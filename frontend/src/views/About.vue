<script setup>
const homeImg = new URL('../assets/about/HomeView.png', import.meta.url).href
const recordImg = new URL('../assets/about/RecordView.png', import.meta.url).href
const modalImg = new URL('../assets/about/RecordModal.png', import.meta.url).href
const adminImg = new URL('../assets/about/AdminView.png', import.meta.url).href
</script>

<template>
  <div>
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-text">
          <h1 class="title">CIRCLE — 使い方ガイド</h1>
          <p class="lead">記録の閲覧と追加は同じ画面で直感的に行えます。ここでは主要なワークフローを短く、視覚的に説明します。</p>
          <router-link to="/record" class="cta">記録を確認・追加する</router-link>
        </div>
        <div class="hero-media">
          <div class="media-box">
            <img :src="homeImg" alt="Home View" />
          </div>
        </div>
      </div>
    </section>

    <main class="container">
      <section class="feature-split">
        <div class="text">
          <h2>記録一覧と記録の追加 — ワンストップ</h2>
          <p class="remark">
            member権限保有者のみ
          </p>
          <p>「記録」ページでは一覧表示と新規作成が同じインターフェース上に統合されています。上部で検索・フィルタ、右上のボタンでモーダルを開き、即座に記録を追加できます。追加された記録は即時に一覧へ反映されます。</p>
          <ul>
            <li>一覧: 期間やステータスで絞り込み可能</li>
            <li>追加: モーダルで素早く入力、必須項目は金額と用途</li>
            <li>安全: 認証済ユーザーのみ編集・追加が可能</li>
          </ul>
        </div>
        <div class="visuals">
          <div class="card">
            <div class="media-box main-shot">
              <img :src="recordImg" alt="Record List" />
            </div>
            <div class="overlay">
              <div class="media-box">
                <img :src="modalImg" alt="Add Modal" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="panel admin">
        <div>
          <h2>管理者向け機能</h2>
          <p class="remark">
            administrator権限保有者のみ
          </p>
          <p>管理者は記録の承認、論理削除、メンバー同期などを行えます。管理者専用の操作は `管理` ページでまとめて実行できます。</p>
        </div>
        <div class="card visuals">
          <div class="media-box">
            <img :src="adminImg" alt="Admin View" />
          </div>
        </div>
      </section>

      <section class="panel get-started">
        <h2>はじめる</h2>
        <ol>
          <li>右上のサインインで Discord アカウントを使ってログインしてください。</li>
          <li>ログイン後、上部ナビの「記録」へ移動すると一覧と追加が使えます。</li>
          <li>管理者は「管理」画面で追加の操作を行ってください。</li>
        </ol>
      </section>

    </main>
  </div>
</template>

<style scoped>
:root { --container-max:1200px }
.container { max-width: var(--container-max); margin: 2rem auto; padding:0 1rem }
.hero { background: linear-gradient(180deg,#fff 0%,#fbfdff 100%); border-bottom: 1px solid #eef2f7; padding: 3rem 0 }
.hero-grid { display: grid; grid-template-columns: 1fr auto; gap: 2rem; align-items: center }
.hero-text .title { font-size: 2rem; margin: 0 0 0.5rem }
.lead { color: #475569; margin-bottom: 1rem }
.cta { display: inline-block; background: #00bd7e; color: white; padding: 0.6rem 1rem; border-radius: 8px; text-decoration: none; font-weight: 700 }

.remark {
  display: inline-block;
  background: rgba(0, 189, 126, 0.08);
  color: #065f46;
  padding: 0.22rem 0.6rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.95rem;
  border: 1px solid rgba(0, 189, 126, 0.12);
  margin: 0.5rem 0 0.5rem;
}

.feature-split { display: grid; grid-template-columns: 1fr auto; gap: 2rem; margin: 2.5rem 0 }
.feature-split .text h2 { margin-top: 0 }
.feature-split .text p { color: #475569 }
.feature-split ul { margin: 0.5rem 0 0 1.1rem }

.media-box { width: 100%; max-width: 540px; aspect-ratio: 16 / 9; border-radius: 10px; overflow: hidden; border: 1px solid #e6eef2; background: #fff }
.media-box img { width: 100%; height: 100%; object-fit: cover; display: block }

.visuals .card { display: block; position: relative; max-width: 540px }
.visuals .main-shot { width: 100%; }
.visuals .overlay { aspect-ratio: 16/9; border-radius: 8px; overflow: hidden; box-shadow: 0 8px 24px rgba(2,6,23,0.12) }

.panel { margin: 2rem 0 }
.panel.admin { display: grid; grid-template-columns: 1fr auto; gap: 1.5rem; padding: 1rem; background: #fff; border-radius: 10px; border: 1px solid #eef2f7 }
.panel.admin .media-box { max-width: 540px; width: 100% }

.get-started ol { padding-left: 1.1rem }

@media (max-width: 1000px) {
  .hero-grid { grid-template-columns: 1fr }
  .feature-split { grid-template-columns: 1fr }
  .visuals { display: block }
  .visuals .card { flex-direction: column; align-items: center }
  .visuals .overlay { width: 60% }
  .panel.admin { flex-direction: column }
}
</style>
