<template>
  <div
    :dir="useLanguageStore().language == 'fa' ? 'rtl' : 'ltr'"
    class="d-flex flex-column align-center gap-2 width-window py-2 px-4 height-full position-relative"
    :class="theme.backgroundClass"
  >
    <h1 :class="theme.switchPrimaryClass">{{ $t('emergency.title') }}</h1>

    <RouterLink
      to="/"
      class="button-style-2 position-absolute top left border-none outline-none d-flex align-flex-start radius-2"
      :class="theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-300'"
    >
      <Icon icon="solar:arrow-left-linear" width="35" :class="theme.switchPrimaryClass" />
    </RouterLink>

    <img
      src="/images/error.png"
      class="width-full height-full max-width-300 max-height-300"
      alt=""
    />

    <p class="font-size-4 width-full max-width-500" :class="theme.switchPrimaryClass">
      {{ $t('emergency.description') }}
    </p>

    <div class="d-flex align-center gap-4">
      <!-- دکمه فعال -->
      <button
        @click="enabled = true"
        class="button-style-2 text-center px-6 font-size-5 border-none outline-none radius-10 py-2 font-500"
        :class="[
          enabled
            ? 'bg-red-600 text-white'
            : theme.colors === 'black'
              ? 'bg-neutral-700 text-white'
              : 'bg-neutral-200',
        ]"
      >
        {{ $t('emergency.enabled') }}
      </button>

      <!-- دکمه غیرفعال -->
      <button
        @click="enabled = false"
        class="button-style-2 text-center px-6 font-size-5 border-none outline-none radius-10 py-2 font-500"
        :class="[
          theme.colors === 'black' ? 'bg-neutral-700 text-white' : 'bg-neutral-200 text-black',
        ]"
      >
        {{ $t('emergency.disabled') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useLanguageStore } from '@/stores/useLanguage'
import { useThemeStore } from '@/stores/useTheme'
import { Icon } from '@iconify/vue'
import { ref } from 'vue'
const enabled = ref(false)
const theme = useThemeStore()
</script>

<style lang="scss" scoped>
.bg-red-600 {
  background-color: oklch(0.577 0.245 27.325) !important;
}
</style>
