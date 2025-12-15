<script setup>
import { ref } from 'vue';
import { supabase } from '../supabase';
import { useRouter } from 'vue-router';

const router = useRouter();
const error = ref(null);

const signInWithDiscord = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
        provider: 'discord',
        options: {
            redirectTo: `${window.location.origin}${import.meta.env.BASE_URL}auth/callback`,
            queryParams: {
                prompt: 'select_account'
            }
        }
    });

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
