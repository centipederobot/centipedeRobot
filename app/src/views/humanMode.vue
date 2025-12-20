<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { RouterLink } from 'vue-router'
import { useThemeStore } from '@/stores/useTheme'

const theme = useThemeStore()
</script>

<template>
  <div
    ref="container"
    class="d-flex width-window overflow-hidden flex-center height-window flex-column gap-4 text-center"
    :class="theme.backgroundClass"
  >
    <!-- ویدیو placeholder -->
    <!-- <video autoplay loop muted playsinline class="width-full position-relative">
      <source src="/videos/placeholder.gif" type="image/gif" />
      مرورگر شما از ویدیو پشتیبانی نمی‌کند.
    </video> -->
    <img src="../../public/videos/placeholder.gif" class="width-full position-relative" alt="" />
    <!-- Arrow Key Controller -->
    <div class="arrow-key-controller-container transition">
      <button
        style="width: 35px; height: 55px"
        class="button-style-2 border-none outline-none d-flex align-flex-start radius-2"
        :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
      >
        <Icon
          icon="solar:double-alt-arrow-up-line-duotone"
          width="30"
          :class="theme.switchPrimaryClass"
        />
      </button>

      <div class="arrow-key-controller-middle">
        <button
          style="width: 55px; height: 35px"
          class="button-style-2 border-none outline-none d-flex align-center justify-flex-start radius-2"
          :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
        >
          <Icon
            icon="solar:double-alt-arrow-left-line-duotone"
            width="30"
            :class="theme.switchPrimaryClass"
          />
        </button>
        <button
          style="width: 55px; height: 35px"
          class="button-style-2 border-none outline-none d-flex align-center justify-flex-end radius-2"
          :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
        >
          <Icon
            icon="solar:double-alt-arrow-right-line-duotone"
            width="30"
            :class="theme.switchPrimaryClass"
          />
        </button>
      </div>

      <button
        style="width: 35px; height: 55px"
        class="button-style-2 border-none outline-none d-flex align-flex-end radius-2"
        :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
      >
        <Icon
          icon="solar:double-alt-arrow-down-line-duotone"
          width="30"
          :class="theme.switchPrimaryClass"
        />
      </button>
    </div>

    <!-- Functional Key Controller -->
    <div class="functional-key-controller-container transition">
      <button
        class="button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
        :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
      >
        <Icon icon="tabler:triangle" width="40" class="text-green-300" />
      </button>

      <div class="functional-key-controller-middle">
        <button
          class="button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
          :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
        >
          <Icon icon="tabler:square" width="40" class="text-pink-300" />
        </button>
        <button
          class="button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
          :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
        >
          <Icon icon="tabler:circle" width="40" class="text-red-300" />
        </button>
      </div>

      <button
        class="button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
        :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
      >
        <Icon icon="tabler:letter-x" width="40" class="text-blue-300" />
      </button>
    </div>

    <!-- Back Button -->
    <RouterLink
      to="/"
      class="button-style-2 position-absolute top left border-none outline-none d-flex align-flex-start radius-2"
      :class="[theme.colors === 'black' ? 'bg-neutral-700' : 'bg-neutral-200']"
    >
      <Icon icon="solar:arrow-left-linear" width="35" :class="theme.switchPrimaryClass" />
    </RouterLink>
  </div>
</template>

<style lang="scss" scoped>
.arrow-key-controller-container {
  width: fit-content;
  position: absolute;
  left: 20px;
  bottom: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
}

.arrow-key-controller-middle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
}

.functional-key-controller-container {
  width: fit-content;
  position: absolute;
  right: 20px;
  bottom: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;

  button {
    width: 40px !important;
    height: 40px !important;
  }
}

.functional-key-controller-middle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
}
</style>
