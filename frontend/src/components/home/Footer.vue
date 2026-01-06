<script setup>
</script>

<template>
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="brand">
        <img src="../../assets/logo.svg" alt="CIRCLE" />
        <p>PiedPiper青山テック愛好会の活動を支える会計管理システムです。</p>
      </div>

      <div class="links">
        <div>
          <h4>プロダクト</h4>
          <ul>
            <li><router-link to="/">ホーム</router-link></li>
            <li><router-link to="/about">機能</router-link></li>
            <li><router-link to="/null">よくある質問</router-link></li>
          </ul>
        </div>
        <div>
          <h4>リソース</h4>
          <ul>
            <li><router-link to="/null">ドキュメント</router-link></li>
            <li><router-link to="/null">サポート</router-link></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="copyright">&copy; 2025 CIRCLE. All rights reserved.</div>
  </footer>
</template>

<style scoped>
/* Clean footer */
.site-footer { background: var(--color-background); border-top:1px solid var(--color-border-hover); padding:2rem 0 }
.footer-inner { display:flex; gap:2rem; align-items:flex-start; max-width:1100px; margin:0 auto; padding:0 1rem }
.brand img { width:48px; height:48px }
.brand p { color: var(--color-text); max-width:36ch }
.links { display:flex; gap:2rem; margin-left:auto }
.links a { color: var(--color-heading); text-decoration:none }
.copyright { text-align:center; padding-top:1rem; color: var(--color-muted) }

@media (max-width:900px) {
  .footer-inner { flex-direction:column; align-items:flex-start }
  .links { margin-left:0 }
}
</style>
