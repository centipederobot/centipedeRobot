<script setup lang="ts">
import { useSpeechRecognition, useScroll } from '@vueuse/core'
import { ref, watchEffect } from 'vue'
import { Icon } from '@iconify/vue'
import { RouterLink } from 'vue-router'
import { useThemeStore } from '@/stores/useTheme'
import { VoiceRecorder } from 'capacitor-voice-recorder'

// 🎤 Speech Recognition از VueUse
const { isSupported, isListening, result, start, stop } = useSpeechRecognition({ lang: 'fa-IR' })

const toggleVoice = async () => {
  if (isListening.value) {
    stop()
  } else {
    // ۱. چک کردن وضعیت مجوز در سیستم عامل
    const status = await VoiceRecorder.requestAudioRecordingPermission()
    if (status.value) {
      start()
      console.log('🎤 دسترسی تایید شد و ضبط شروع شد')
    } else {
      alert('لطفاً دسترسی میکروفون را تایید کنید')
    }
  }
}

const transcript = ref('')
watchEffect(() => {
  if (result.value) {
    transcript.value = result.value
    console.log('🗣️ You said:', result.value)
  }
})

// رفرنس به کانتینر اسکرول
const scrollContainer = ref<HTMLDivElement | null>(null)
const { arrivedState } = useScroll(scrollContainer)

const theme = useThemeStore()
</script>

<template>
  <div ref="container"
    class="d-flex width-window overflow-hidden flex-center height-window flex-column gap-4 text-center"
    :class="theme.backgroundClass">
    <!-- ویدیو placeholder -->
    <!-- <video autoplay loop muted playsinline class="width-full position-relative">
      <source src="/videos/placeholder.gif" type="image/gif" />
      مرورگر شما از ویدیو پشتیبانی نمی‌کند.
    </video> -->
    <img src="../../public/videos/placeholder.gif" class="width-full position-relative" alt="" />

    <RouterLink to="/"
      class="button-style-2 position-absolute top left border-none outline-none d-flex align-flex-start radius-2"
      :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']">
      <Icon icon="solar:arrow-left-linear" width="35" :class="theme.switchPrimaryClass" />
    </RouterLink>

    <div class="bottom position-absolute d-flex flex-center gap-1 flex-column width-full">
      <div class="scroll-wrapper" style="z-index: 1000 !important">
        <div ref="scrollContainer" class="d-flex align-center gap-4 pa-2 overflow-x-auto scroll-container"
          style="width: 100%; z-index: 1000 !important">
          <button class="button-style-2 d-flex pa-2 flex-center radius-20 border-none outline-none" :class="[
            theme.switchPrimaryClass,
            theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200',
          ]">
            {{ $t('ai.forward') }}
          </button>
          <button class="button-style-2 d-flex pa-2 flex-center radius-20 border-none outline-none" :class="[
            theme.switchPrimaryClass,
            theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200',
          ]">
            {{ $t('ai.backward') }}
          </button>
          <button class="button-style-2 d-flex pa-2 flex-center radius-20 border-none outline-none" :class="[
            theme.switchPrimaryClass,
            theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200',
          ]">
            {{ $t('ai.turn') }}
          </button>
          <button class="button-style-2 d-flex pa-2 flex-center radius-20 border-none outline-none" :class="[
            theme.switchPrimaryClass,
            theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200',
          ]">
            {{ $t('ai.forwardTurn') }}
          </button>
          <button class="button-style-2 d-flex pa-2 flex-center radius-20 border-none outline-none" :class="[
            theme.switchPrimaryClass,
            theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200',
          ]">
            {{ $t('ai.jump') }}
          </button>
        </div>
        <div v-if="!arrivedState.left" class="fade-left"></div>
        <div v-if="!arrivedState.right" class="fade-right"></div>
      </div>

      <button @click="toggleVoice" :class="[
        'button-style-2 d-flex pa-2 flex-center radius-20 border-none outline-none voice-btn',
        theme.switchPrimaryClass,
        theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200',
        { 'recording': isListening },
      ]" style="width: fit-content">
        <Icon icon="solar:microphone-3-bold" width="35" />
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
body.theme-dark .voice-btn.recording {
  position: relative;
  animation: pulse 1.2s infinite;
  background-color: oklch(0.145 0 0) !important;
}

body.theme-light .voice-btn.recording {
  position: relative;
  animation: pulse 1.2s infinite;
  background-color: oklch(0.87 0 0) !important;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(#a1a1a1, 0.7);
  }

  70% {
    box-shadow: 0 0 0 15px rgba(255, 0, 0, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(255, 0, 0, 0);
  }
}

.scroll-wrapper {
  position: relative;
}

.fade-left,
.fade-right {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 30px;
  pointer-events: none;
}
</style>
