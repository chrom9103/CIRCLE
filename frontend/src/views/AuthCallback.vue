<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { supabase } from '../supabase';

const router = useRouter();

onMounted(async () => {
    const { data: { session }, error } = await supabase.auth.getSession();

    if (error) {
        console.error('認証エラー:', error.message);
        router.push({ name: 'signin' });
    } else if (session) {
        router.push({ name: 'dashboard' });
    } else {
        router.push({ name: 'home' });
    }
});
</script>

<template>
    <div>
        <h1>認証を処理しています...</h1>
    </div>
</template>
