<template>
  <div class="d-flex flex-column width-full height-full">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import { onMounted } from 'vue';
import { useLanguageStore } from './stores/useLanguage';
onMounted(() => {
  document.body.classList.add(`font-${useLanguageStore().language}`)
});
</script>

<style lang="scss" scoped></style>