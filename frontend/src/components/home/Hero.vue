<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { supabase } from '@/supabase'

const router = useRouter()
const auth = useAuthStore()
const isLoggedIn = computed(() => !!(auth && auth.isLoggedIn))

async function signInWithDiscord() {
  try {
    const runtime = (typeof window !== 'undefined' && window.__APP_ENV__) ? window.__APP_ENV__ : import.meta.env
    const siteBase = runtime.VITE_SITE_URL || `${window.location.origin}${import.meta.env.BASE_URL}`
    const redirectTo = `${siteBase.replace(/\/+$/, '')}/auth/callback`

    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'discord',
      options: {
        redirectTo,
        queryParams: { prompt: 'select_account' }
      }
    })

    if (error) {
      console.error('Login failed:', error.message)
    }
  } catch (e) {
    console.error('signInWithDiscord error', e)
  }
}

function primaryAction() {
  if (isLoggedIn.value) router.push('/record')
  else signInWithDiscord()
}
</script>

<template>
  <section class="hero-root">
    <div class="hero-content container">
      <div class="hero-inner">
        <div class="hero-pill">PiedPiper青山テック愛好会 部内システム</div>
        <h2 class="hero-kicker">つながりを、<br>もっとシンプルに</h2>
        <p class="hero-desc">PiedPiper青山テック愛好会の会計管理システムです。<br>Discordでサインインするだけで、すぐに使い始められます。</p>

        <div class="hero-ctas">
          <button class="btn primary large" @click="primaryAction">{{ isLoggedIn ? '会計を記録する →' : 'Discordでサインイン →' }}</button>
          <router-link to="/about" class="btn outline large">使い方を見る</router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* White-based, minimal, modern hero */
.hero-root { background: #ffffff; color: #0f172a; padding-bottom: 3.5rem; }
.nav { display:flex; justify-content:space-between; align-items:center; padding:1.25rem 0; }
.nav-brand { display:flex; align-items:center; gap:0.75rem; font-weight:700; color:#0b2540 }
.nav-brand img { width:44px; height:44px; display:block; border-radius:50%; background:#10b981 }
.contact-btn { background:#0b1220; color:#fff; padding:10px 16px; border-radius:999px; border:none; font-weight:700 }
.container { max-width:1100px; margin:0 auto; padding: 4.5rem 1rem; display:flex; align-items:center; justify-content:center }
.hero-inner { text-align:center; max-width:760px }
.hero-pill { display:inline-block; background:#f1f5f9; color:#334155; padding:10px 18px; border-radius:999px; font-weight:600; margin-bottom:2rem }
.hero-kicker { margin:0; font-size:2rem; color:#0b2540; font-weight:700; margin-bottom:1.25rem; line-height:1.2 }
.hero-desc { color:#475569; margin:0 auto 1.75rem; max-width:56ch; line-height:1.8 }
.hero-ctas { display:flex; gap:1rem; justify-content:center; margin-top:0.5rem }
.btn { padding:0.85rem 1.25rem; border-radius:999px; font-weight:700; cursor:pointer; border:1px solid transparent; font-size:1rem }
.btn.large { padding:0.95rem 1.5rem; font-size:1.02rem }
.btn.primary { background:#0b1220; color:#fff; box-shadow: 0 10px 30px rgba(2,6,23,0.08) }
.btn.outline { background:transparent; border:1px solid rgba(15,23,42,0.08); color:#0b1220 }

@media (max-width:900px) {
  .container { padding: 2.5rem 1rem }
  .hero-kicker { font-size:1.375rem }
  .hero-pill { margin-bottom:1rem }
  .hero-desc { font-size:0.98rem }
  .hero-ctas { flex-direction:column; gap:0.75rem }
  .btn.large { width:100% }
}
</style>
