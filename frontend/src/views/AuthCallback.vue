<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../supabase'

const router = useRouter()

function parseHash(hash) {
    if (!hash) return {}
    return hash.replace(/^#/, '').split('&').reduce((acc, pair) => {
        const [k, v] = pair.split('=')
        acc[k] = decodeURIComponent(v || '')
        return acc
    }, {})
}

function getRedirectPath() {
    const redirect = sessionStorage.getItem('authRedirect');
    sessionStorage.removeItem('authRedirect');
    return redirect || '/dashboard';
}

onMounted(async () => {
    try {
        // Try supabase helper if available
        if (supabase.auth.getSessionFromUrl) {
            const { data, error } = await supabase.auth.getSessionFromUrl({ storeSession: true })
            if (error) throw error
            if (data?.session) {
                router.push(getRedirectPath())
                return
            }
        }

        // Fallback: parse URL hash and set session manually
        const hash = window.location.hash
        const params = parseHash(hash)
        const access_token = params.access_token
        const refresh_token = params.refresh_token

        if (access_token) {
            if (supabase.auth.setSession) {
                const { data, error } = await supabase.auth.setSession({ access_token, refresh_token })
                if (error) throw error
                router.push(getRedirectPath())
                return
            }
        }

        // If no session could be established, try to read existing session
        const { data: { session }, error } = await supabase.auth.getSession()
        if (error) {
            console.error('認証エラー:', error.message)
            router.push({ name: 'signin' })
        } else if (session) {
            router.push(getRedirectPath())
        } else {
            router.push({ name: 'home' })
        }
    } catch (e) {
        console.error('Auth callback error:', e)
        router.push({ name: 'signin' })
    }
})
</script>

<template>
    <div>
        <h1>認証を処理しています...</h1>
    </div>
</template>
