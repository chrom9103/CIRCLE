<script setup>
import { ref } from 'vue';
import { supabase } from '../supabase';
import { useRouter } from 'vue-router';

const router = useRouter();
const error = ref(null);

const signInWithDiscord = async () => {
    const runtime = (typeof window !== 'undefined' && (window as any).__APP_ENV__) ? (window as any).__APP_ENV__ : import.meta.env
    const siteBase = runtime.VITE_SITE_URL || `${window.location.origin}${import.meta.env.BASE_URL}`
    const redirectTo = `${siteBase.replace(/\/$/, '')}${import.meta.env.BASE_URL.endsWith('/') ? '' : import.meta.env.BASE_URL}${'auth/callback'}`

    const { error } = await supabase.auth.signInWithOAuth({
        provider: 'discord',
        options: {
            redirectTo,
            queryParams: {
                prompt: 'select_account'
            }
        }
    })

    if (error) {
        console.error('Login failed:', error.message);
    }
};
</script>

<template>
    <div>
        <h1>Sign In</h1>
        <button @click="signInWithDiscord">Sign in with Discord</button>
        <p v-if="error">{{ error }}</p>
    </div>
</template>
