<template>
    <div class="d-flex flex-column width-window height-window overflow-hidden bg-neutral-800">
        <div class="position-absolute top left">
            <h1 class="font-size-12 font-700 text-white">tinco</h1>
        </div>
        <div class="d-flex flex-column flex-center gap-4 position-absolute center right">
            <RouterLink style="width: 160px;"
                class="button-style text-white text-center px-6 font-size-5 bg-neutral-500 radius-10 py-2 font-500"
                to="/aiMode">
                AI mode
            </RouterLink>

            <RouterLink style="width: 160px;"
                class="button-style text-white text-center px-6 font-size-5 bg-neutral-500 radius-10 py-2 font-500"
                to="/humanMode">
                joystick
            </RouterLink>

            <RouterLink style="width: 160px;"
                class="button-style text-white text-center px-6 font-size-5 bg-neutral-500 radius-10 py-2 font-500"
                to="/">
                emergency
            </RouterLink>
        </div>
        <div class="bottom position-absolute width-full px-4 d-flex flex-space-between">

            <!-- دکمه‌های سمت چپ -->
            <div class="d-flex flex-1 align-center gap-2">
                <button @click="useLanguage.toggleLanguage()"
                    class="button-style border-none outline-none d-flex flex-column flex-center radius-20 bg-neutral-400"
                    style="width: 40px; height: 40px;">
                    <Icon :icon="useLanguage.languageIcon" width="30" class="text-white" />
                </button>
                <button @click="showSettingDialog = true"
                    class="button-style border-none outline-none d-flex flex-column flex-center radius-20 bg-neutral-400"
                    style="width: 40px; height: 40px;">
                    <Icon icon="solar:settings-bold" width="30" style="transform: translateX(-1px);"
                        class="text-white" />
                </button>
                <button @click="showInfoDialog = true"
                    class="button-style border-none outline-none d-flex flex-column flex-center radius-20 bg-neutral-400"
                    style="width: 40px; height: 40px;">
                    <Icon icon="solar:info-circle-bold" width="30" class="text-white" />
                </button>
                <button @click="showHotSpotDialog = true"
                    class="button-style border-none outline-none d-flex flex-column flex-center radius-20 bg-neutral-400"
                    style="width: 40px; height: 40px;">
                    <Icon icon="solar:bluetooth-wave-bold" width="30" class="text-white" />
                </button>
            </div>
            <div class="d-flex flex-1 flex-center text-white gap-2">
                <p>&copy; {{ new Date().getFullYear() }} copyright</p>
            </div>
            <div class="d-flex flex-1 text-neutral-800 align-center gap-2">
                <p></p>
            </div>
        </div>
        <Dialog :model-value="showSettingDialog" class="text-white"
            @dialog:close="showSettingDialog = !showSettingDialog">
            <template v-slot:title>
                <div class="d-flex flex-space-between width-full gap-4">
                    <Icon icon="solar:close-circle-bold" @click="showSettingDialog = !showSettingDialog" width="30"
                        class="text-red-500 cursor-pointer" />
                    <h3>settings</h3>
                </div>
            </template>
            <div class="width-full d-flex flex-column gap-4">
                <div class="d-flex align-center gap-2">
                    <strong>theme:</strong>
                    <div class="d-flex cursor-pointer text-white align-center gap-1">
                        <Icon icon="solar:moon-stars-bold" width="30" />
                        <p>dark</p>
                    </div>
                    <div class="d-flex cursor-pointer text-white align-center gap-1">
                        <Icon class="text-yellow-400" icon="solar:sun-bold" width="30" />
                        <p>light</p>
                    </div>
                </div>
                <div class="d-flex align-center gap-2">
                    <strong>joystick:</strong>
                    <div class="d-flex cursor-pointer text-white align-center gap-1">
                        <Icon icon="bx:joystick" width="40" />
                        <p>ps4</p>
                    </div>
                    <div class="d-flex cursor-pointer text-white align-center gap-1">
                        <Icon icon="icon-park-outline:game-ps" width="30" />
                        <p>ps5</p>
                    </div>
                </div>
                <button class="button-style border-none outline-none text-white text-center px-6 font-size-5 bg-neutral-500 radius-10 py-2
                    font-500">
                    save
                </button>
            </div>
        </Dialog>
        <Dialog :model-value="showInfoDialog" class="text-white" @dialog:close="showInfoDialog = !showInfoDialog">
            <template v-slot:title>
                <div class="d-flex flex-space-between width-full gap-4">
                    <Icon icon="solar:close-circle-bold" @click="showInfoDialog = !showInfoDialog" width="30"
                        class="text-red-500 cursor-pointer" />
                    <h3>info</h3>
                </div>
            </template>
            <div class="d-flex flex-column gap-3">

                <!-- Version -->
                <div class="d-flex flex-column">
                    <h4 class="font-700 text-white">Version</h4>
                    <p class="text-neutral-300 font-size-4">1.0.0</p>
                </div>

                <p class="text-neutral-300 font-size-4">
                    Tinco stands for <strong>Triad Intelligence Nexus Centipede Operation</strong>;
                    a multi‑part project aimed at building an intelligent, controllable, and extensible centipede robot.
                    This robot is designed by combining artificial intelligence, image processing, and modern
                    communication technologies.
                    Its applications can include environmental monitoring, rescue operations, robotics education, and
                    even scientific entertainment.
                    The ultimate goal is to create a platform that is usable and expandable both for researchers and
                    everyday users.
                </p>
            </div>
        </Dialog>
        <Dialog :model-value="showHotSpotDialog" class="text-white"
            @dialog:close="showHotSpotDialog = !showHotSpotDialog">
            <template v-slot:title>
                <div class="d-flex flex-space-between width-full gap-4">
                    <Icon icon="solar:close-circle-bold" @click="showHotSpotDialog = !showHotSpotDialog" width="30"
                        class="text-red-500 cursor-pointer" />
                    <h3>hotspot setting</h3>
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import Dialog from '@/components/ui/dialog.vue';
import { useLanguageStore } from '@/stores/useLanguage';
import { Icon } from '@iconify/vue'
import { ref } from 'vue';
import { RouterLink } from 'vue-router'
const showSettingDialog = ref(false);
const showInfoDialog = ref(false);
const showHotSpotDialog = ref(false);
const useLanguage = useLanguageStore();
</script>

<style lang="scss" scoped>
.top {
    top: 8px;
}

.left {
    left: 8px;
}

.bottom {
    bottom: 16px;
}

.center {
    top: 0;
    bottom: 0;
}

.right {
    right: 5px;
}

.button-style {
    position: relative;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    user-select: none;
    transition: all 0.18s ease;
    transform: translateZ(0);
    box-shadow: 0 0 0 rgba(255, 255, 255, 0);
}

.button-style:hover {
    background-color: rgba(255, 255, 255, 0.12);
    box-shadow: 0 0 3px rgba(255, 255, 255, 0.18);
}


.button-style:active {
    transform: scale(0.94);
    background-color: rgba(255, 255, 255, 0.18);
    box-shadow: 0 0 3px rgba(255, 255, 255, 0.25);
}
</style>
