<script setup>
import { useAuthStore } from '../stores/auth';
import HelloWorld from '../components/HelloWorld.vue'
import TheWelcome from '../components/TheWelcome.vue'

const auth = useAuthStore();
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="../assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <main class="container">
    <nav class="nav" role="navigation" aria-label="primary">
      <router-link
        v-if="auth.isLoggedIn"
        to="/dashboard"
        class="nav-link"
      >Dashboard</router-link>

      <router-link
        v-else
        to="/signin"
        class="nav-link primary"
      >Sign In</router-link>
    </nav>

    <TheWelcome />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem;
}

.nav {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.nav-link {
  display: inline-block;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  text-decoration: none;
  color: var(--text-color, #2d3748);
  background: var(--nav-bg, transparent);
  border: 1px solid transparent;
  transition: background-color 0.15s ease, transform 0.08s ease;
  font-weight: 600;
}

.nav-link:hover {
  background: rgba(0,0,0,0.04);
  transform: translateY(-1px);
}

.nav-link.primary {
  background: var(--primary, #3b82f6);
  color: white;
  border-color: rgba(0,0,0,0.05);
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
