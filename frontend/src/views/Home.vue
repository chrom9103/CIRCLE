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
.container { max-width: var(--container-max); margin: 2rem auto; padding:0 1rem; box-sizing: border-box }

main { display: flex; flex-direction: column; gap: 2rem }

@media (max-width: 1000px) {
  :root { --container-max: 900px }
}

@media (max-width: 600px) {
  :root { --container-max: 100% }
  .container { margin: 1rem auto; padding: 0 0.75rem }
  main { gap: 1rem }
  .container > * { width: 100% }
}
</style>
