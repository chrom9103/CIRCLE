<script setup>
import Hero from '../components/home/Hero.vue'
import Features from '../components/home/Features.vue'
import HowItWorks from '../components/home/HowItWorks.vue'
import Footer from '../components/home/Footer.vue'
</script>

<template>
  <div>
    <Hero />
    <main>
      <Features />
      <HowItWorks />
    </main>
    <Footer />
  </div>
</template>

<style scoped>
:root { --container-max:1100px }
.container { max-width: var(--container-max); margin: 2rem auto; padding:0 1rem }
</style>
