<template>
  <header class="app-header">
    <div class="left">
      <img alt="Logo" class="logo" src="../assets/logo.svg" width="40" height="40" />
      <router-link to="/"><h1 class="title">CIRCLE</h1></router-link>
    </div>

    <div class="right">
      <button :class="['burger', { open: showMenu }]" @click="toggleMenu" aria-label="Open navigation" :aria-expanded="showMenu">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </button>

      <div v-if="showMenu" class="mobile-backdrop" @click="toggleMenu"></div>
      <div v-if="showMenu" class="mobile-menu" role="menu" @click.stop>
        <router-link to="/" class="mobile-link" @click="toggleMenu" role="menuitem">ホーム</router-link>
        <router-link to="/about" class="mobile-link" @click="toggleMenu" role="menuitem">使い方</router-link>
        <router-link to="/record" class="mobile-link" @click="toggleMenu" role="menuitem">記録</router-link>
        <router-link to="/admin" class="mobile-link" @click="toggleMenu" role="menuitem">管理</router-link>
        <router-link to="/dashboard" class="mobile-link" @click="toggleMenu" role="menuitem">ダッシュボード</router-link>
        <button v-if="auth.user" class="signout" @click="signOut" role="menuitem">Sign Out</button>
        <button v-else class="signout" @click="signInWithDiscord" role="menuitem">Sign In</button>
      </div>

      <div class="user-wrap">
        <router-link v-if="auth.user" to="/dashboard">
          <img :src="userAvatar" alt="User Avatar" class="avatar" />
        </router-link>
        <button v-else class="avatar-btn" @click="signInWithDiscord" aria-label="Sign in">
          <img :src="userAvatar" alt="User Avatar" class="avatar" />
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { supabase } from '../supabase'

const auth = useAuthStore()
const showMenu = ref(false)
const discordAvatar = ref(null)

function toggleMenu() {
  showMenu.value = !showMenu.value
}

async function signOut() {
  try {
    if (auth && typeof auth.signOut === 'function') {
      await auth.signOut()
    } else if (supabase && supabase.auth && typeof supabase.auth.signOut === 'function') {
      await supabase.auth.signOut()
    } else {
      console.log('signOut not implemented on auth store or supabase')
    }

    // Clear local auth store state
    if (auth && typeof auth.clearUser === 'function') {
      try { auth.clearUser() } catch (e) { /* ignore */ }
    }
    window.location.href = window.location.origin + window.location.pathname
  } catch (e) {
    console.error('Failed to sign out:', e)
    try { window.location.href = '/signin' } catch (_) { /* noop */ }
  }
}

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

onMounted(async () => {
  try {
    const { data, error } = await supabase.auth.getUser()
    if (!error && data && data.user) {
      // user_metadata に discord 情報があれば優先して使う
      const meta = data.user.user_metadata || {}
      // よくある形: meta.discord.avatar_url または meta.avatar_url
      discordAvatar.value = meta.discord?.avatar_url || meta.avatar_url || null
    }
  } catch (e) {
    console.warn('Failed to load supabase user for avatar', e)
  }
})

// close mobile menu on Escape key
function onKeydown(e) {
  if (e.key === 'Escape' || e.key === 'Esc') {
    if (showMenu.value) showMenu.value = false
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})

const userAvatar = computed(() => {
  // Discord アバターを優先、次に auth ストアの avatar、最後にデフォルト画像
  if (discordAvatar.value) return discordAvatar.value
  if (auth && auth.user && (auth.user.avatar_url || auth.user.user_metadata?.avatar_url)) {
    return auth.user.avatar_url || auth.user.user_metadata.avatar_url
  }
  return new URL('../assets/default-avatar.png', import.meta.url).href
})
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.6rem 1rem;
  width: 100%;
  box-sizing: border-box;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background);
  gap: 1rem;
}

.left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.title {
  font-size: 1.05rem;
  font-weight: 700;
  margin: 0;
  color: var(--color-heading);
}

.right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  text-decoration: none;
  color: var(--color-on-surface);
  padding: 0.4rem 0.7rem;
  border-radius: 6px;
  font-weight: 600;
}

.nav-link:hover {
  background: rgba(0,0,0,0.04);
}

.signout {
  background: var(--color-accent-brand);
  color: var(--vt-c-white);
  border: none;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
}

.user-wrap {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  position: relative;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  object-fit: cover;
  border: 2px solid var(--color-border);
}
.avatar-btn {
  padding: 0;
  border: none;
  background: transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.burger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 44px;
  height: 44px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  padding: 6px;
  border-radius: 8px;
}

.burger:focus {
  outline: 2px solid rgba(59,130,246,0.3);
}

.burger span {
  display: block;
  height: 2px;
  background: var(--color-text);
  margin: 3px 0;
  border-radius: 2px;
  width: 18px;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.burger.open span:nth-child(1) { transform: translateY(8px) rotate(45deg); }
.burger.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
.burger.open span:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }

.mobile-menu {
  position: absolute;
  right: 8px;
  top: 56px;
  background: var(--color-background);
  border: 1px solid var(--color-border);
  box-shadow: 0 6px 18px rgba(15,23,42,0.06);
  border-radius: 8px;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 160px;
  z-index: 1000;
  pointer-events: auto;
}

.mobile-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.12);
  z-index: 900;
}

.mobile-link {
  display: block;
  width: 100%;
  padding: 0.5rem;
  text-decoration: none;
  color: var(--color-on-surface);
}

.mobile-link:focus,
.mobile-link:hover {
  background: rgba(0,0,0,0.04);
}

@media (max-width: 768px) {
  .nav-links { display: none; }
  .burger { display: inline-flex; }
}
</style>