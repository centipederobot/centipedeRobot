<template>
  <div
    class="d-flex flex-column width-window height-window overflow-hidden"
    :class="theme.backgroundClass"
  >
    <div class="position-absolute top left">
      <h1 class="font-size-12 font-us font-700" :class="theme.switchPrimaryClass">Tinco</h1>
    </div>

    <!-- منو سمت راست -->
    <div class="d-flex flex-column flex-center gap-4 position-absolute center right">
      <RouterLink
        style="width: 180px"
        class="button-style text-center px-6 font-size-5 radius-10 py-2 font-500"
        :class="[
          theme.switchPrimaryClass,
          theme.colors === 'black' ? 'bg-neutral-500' : 'bg-neutral-200',
        ]"
        to="/aiMode"
      >
        {{ $t('home.aiMode') }}
      </RouterLink>

      <RouterLink
        style="width: 180px"
        class="button-style text-center px-6 font-size-5 radius-10 py-2 font-500"
        :class="[
          theme.switchPrimaryClass,
          theme.colors === 'black' ? 'bg-neutral-500' : 'bg-neutral-200',
        ]"
        to="/humanMode"
      >
        {{ $t('home.humanMode') }}
      </RouterLink>

      <RouterLink
        style="width: 180px"
        class="button-style text-center px-6 font-size-5 radius-10 py-2 font-500"
        :class="[
          theme.switchPrimaryClass,
          theme.colors === 'black' ? 'bg-neutral-500' : 'bg-neutral-200',
        ]"
        to="/emergency"
      >
        {{ $t('home.emergency') }}
      </RouterLink>
    </div>

    <!-- نوار پایین -->
    <div class="bottom position-absolute width-full px-4 d-flex flex-space-between">
      <div class="d-flex flex-1 align-center gap-2">
        <button
          @click="useLanguage.toggleLanguage()"
          class="button-style border-none outline-none d-flex flex-column flex-center radius-20"
          style="width: 40px; height: 40px"
          :class="theme.colors === 'black' ? 'bg-neutral-400' : 'bg-neutral-200'"
        >
          <Icon :icon="useLanguage.languageIcon" width="30" :class="theme.switchPrimaryClass" />
        </button>

        <button
          @click="showSettingDialog = true"
          class="button-style border-none outline-none d-flex flex-column flex-center radius-20"
          style="width: 40px; height: 40px"
          :class="theme.colors === 'black' ? 'bg-neutral-400' : 'bg-neutral-200'"
        >
          <Icon
            icon="solar:settings-bold"
            width="30"
            style="transform: translateX(-1px)"
            :class="theme.switchPrimaryClass"
          />
        </button>

        <button
          @click="showInfoDialog = true"
          class="button-style border-none outline-none d-flex flex-column flex-center radius-20"
          style="width: 40px; height: 40px"
          :class="theme.colors === 'black' ? 'bg-neutral-400' : 'bg-neutral-200'"
        >
          <Icon icon="solar:info-circle-bold" width="30" :class="theme.switchPrimaryClass" />
        </button>

        <button
          @click="showHotSpotDialog = true"
          class="button-style border-none outline-none d-flex flex-column flex-center radius-20"
          style="width: 40px; height: 40px"
          :class="theme.colors === 'black' ? 'bg-neutral-400' : 'bg-neutral-200'"
        >
          <Icon icon="solar:bluetooth-wave-bold" width="30" :class="theme.switchPrimaryClass" />
        </button>
      </div>

      <div class="d-flex flex-1 flex-center gap-2" :class="theme.switchPrimaryClass">
        <p>&copy; {{ new Date().getFullYear() }} copyright</p>
      </div>

      <div class="d-flex flex-1 align-center gap-2">
        <p></p>
      </div>
    </div>

    <!-- Settings Dialog -->
    <Dialog
      :model-value="showSettingDialog"
      :dir="useLanguage.language == 'fa' ? 'rtl' : 'ltr'"
      @dialog:close="showSettingDialog = !showSettingDialog"
    >
      <template v-slot:title>
        <div class="d-flex flex-space-between width-full gap-4">
          <Icon
            icon="solar:close-circle-bold"
            @click="showSettingDialog = !showSettingDialog"
            width="30"
            class="text-red-500 cursor-pointer"
          />
          <h3 :class="theme.switchPrimaryClass">{{ $t('home.settings') }}</h3>
        </div>
      </template>
      <div class="width-full d-flex flex-column gap-4" :class="theme.switchPrimaryClass">
        <div class="d-flex align-center gap-2">
          <strong>{{ $t('home.theme') }}</strong>
          <div
            :class="theme.colors == 'black' && 'text-blue-500'"
            class="d-flex cursor-pointer align-center gap-1"
            @click="theme.colors = 'black'"
          >
            <Icon icon="solar:moon-stars-bold" width="30" />
            <p>{{ $t('home.dark') }}</p>
          </div>
          <div
            :class="theme.colors == 'white' && 'text-yellow-500'"
            class="d-flex cursor-pointer align-center gap-1"
            @click="theme.colors = 'white'"
          >
            <Icon icon="solar:sun-bold" width="30" />
            <p>{{ $t('home.light') }}</p>
          </div>
        </div>

        <div class="d-flex align-center gap-2">
          <strong>{{ $t('home.joystick') }}</strong>
          <div
            :class="theme.colors === 'black' && 'text-red-400'"
            class="d-flex align-center gap-1"
          >
            <Icon icon="bx:joystick" width="40" />
            <p>{{ $t('home.ps4') }}</p>
          </div>
          <div
            :class="theme.colors === 'white' && 'text-red-400'"
            class="d-flex align-center gap-1"
          >
            <Icon icon="icon-park-outline:game-ps" width="30" />
            <p>{{ $t('home.ps5') }}</p>
          </div>
        </div>
      </div>
    </Dialog>

    <!-- Info Dialog -->
    <Dialog
      :model-value="showInfoDialog"
      :dir="useLanguage.language == 'fa' ? 'rtl' : 'ltr'"
      @dialog:close="showInfoDialog = !showInfoDialog"
    >
      <template v-slot:title>
        <div class="d-flex flex-space-between width-full gap-4">
          <Icon
            icon="solar:close-circle-bold"
            @click="showInfoDialog = !showInfoDialog"
            width="30"
            class="text-red-500 cursor-pointer"
          />
          <h3 :class="theme.switchPrimaryClass">{{ $t('home.info') }}</h3>
        </div>
      </template>
      <div class="d-flex flex-column gap-3" :class="theme.switchPrimaryClass">
        <div class="d-flex flex-column">
          <h4 class="font-700">{{ $t('home.version') }}</h4>
          <p :class="theme.switchPrimaryClass" class="font-size-4">1.0.0</p>
        </div>
        <p :class="theme.switchPrimaryClass" class="font-size-4">{{ $t('home.description') }}</p>
      </div>
    </Dialog>
    <!-- Hotspot Dialog -->
    <Dialog
      :model-value="showHotSpotDialog"
      :dir="useLanguage.language == 'fa' ? 'rtl' : 'ltr'"
      @dialog:close="showHotSpotDialog = !showHotSpotDialog"
    >
      <template v-slot:title>
        <div class="d-flex flex-space-between width-full gap-4">
          <Icon
            icon="solar:close-circle-bold"
            @click="showHotSpotDialog = !showHotSpotDialog"
            width="30"
            class="text-red-500 cursor-pointer"
          />
          <h3 :class="theme.switchPrimaryClass">{{ $t('home.hotspot') }}</h3>
        </div>
      </template>

      <div class="d-flex flex-column gap-4 width-full pa-2" :class="theme.switchPrimaryClass">
        <div
          v-for="item in 3"
          :key="item"
          class="width-full d-flex flex-space-between gap-4 px-2 py-2 radius-2"
          :class="theme.colors === 'black' ? 'bg-neutral-400' : 'bg-neutral-200'"
        >
          <div class="d-flex align-center gap-2">
            <img src="/images/robot.jpg" class="avatar radius-3" alt="" />
            <strong :class="theme.switchPrimaryClass">{{ $t('home.robot') }} {{ item }}</strong>
          </div>
          <div class="d-flex flex-space-between gap-2">
            <button
              class="button-style-success px-4 py-2 radius-2 d-flex flex-center gap-1 border-none outline-none"
              :class="
                theme.colors === 'black' ? 'bg-emerald-500 text-white' : 'bg-emerald-300 text-black'
              "
            >
              {{ $t('home.connect') }}
              <Icon icon="solar:bluetooth-wave-bold" width="15" />
            </button>
          </div>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import Dialog from '@/components/ui/dialog.vue'
import { useLanguageStore } from '@/stores/useLanguage'
import { useThemeStore } from '@/stores/useTheme'
import { Icon } from '@iconify/vue'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
const showSettingDialog = ref(false)
const showInfoDialog = ref(false)
const showHotSpotDialog = ref(false)
const useLanguage = useLanguageStore()
const theme = useThemeStore()
</script>

<style lang="scss" scoped></style>
