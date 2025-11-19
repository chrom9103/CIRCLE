<script setup>
import { onMounted, ref, onUnmounted } from 'vue';
import { supabase } from '../supabase';
import { useRouter } from 'vue-router';

const router = useRouter();
const user = ref(null);

const handleSignOut = async () => {
    try {
        const { error } = await supabase.auth.signOut();
        if (error) throw error;
        router.push({
            name: 'home',
        });
    } catch (error) {
        alert(error.message);
    }
};

async function getUser() {
    const { data, error } = await supabase.auth.getUser();
    if (error) {
        console.error('Error fetching user:', error.message);
    } else {
        console.log(data); // デバッグ用
        user.value = data.user;
    }
}

onMounted(async () => {
    await getUser();
});


</script>

<template>
    <h1>DashBoard</h1>
    <div v-if="user">
        <button @click="handleSignOut">SignOut</button>
    </div>
    <p>Welcome to our service</p>
    <div v-if="user">
        <p><strong>Name:</strong> {{ user.user_metadata.full_name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <img v-if="user.user_metadata.avatar_url" :src="user.user_metadata.avatar_url" alt="User Avatar">
    </div>
    <div>

    </div>
</template>
