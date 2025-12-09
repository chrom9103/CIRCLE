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
            <li><router-link to="#">概要</router-link></li>
            <li><router-link to="#">機能</router-link></li>
            <li><router-link to="#">よくある質問</router-link></li>
          </ul>
        </div>
        <div>
          <h4>リソース</h4>
          <ul>
            <li><router-link to="#">ドキュメント</router-link></li>
            <li><router-link to="#">サポート</router-link></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="copyright">&copy; 2025 CIRCLE. All rights reserved.</div>
  </footer>
</template>

<style scoped>
/* Clean footer */
.site-footer { background:#ffffff; border-top:1px solid rgba(15,23,42,0.04); padding:2rem 0 }
.footer-inner { display:flex; gap:2rem; align-items:flex-start; max-width:1100px; margin:0 auto; padding:0 1rem }
.brand img { width:48px; height:48px }
.brand p { color:#475569; max-width:36ch }
.links { display:flex; gap:2rem; margin-left:auto }
.links a { color:#0b2540; text-decoration:none }
.copyright { text-align:center; padding-top:1rem; color:#64748b }

@media (max-width:900px) {
  .footer-inner { flex-direction:column; align-items:flex-start }
  .links { margin-left:0 }
}
</style>
