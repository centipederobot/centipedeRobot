<template>
    <div class="d-flex flex-column width-window height-window overflow-hidden bg-neutral-800">

        <!-- لوگو بالا -->
        <div class="position-absolute top left">
            <h1 class="font-size-12 font-700 text-white">tinco</h1>
        </div>

        <!-- منوی وسط -->
        <div class="d-flex flex-column flex-center gap-4 position-absolute center right">
            <RouterLink style="width: 160px;"
                class="button-style text-white text-center px-6 font-size-5 bg-neutral-500 radius-10 py-2 font-500"
                to="/">
                AI mode
            </RouterLink>

            <RouterLink style="width: 160px;"
                class="button-style text-white text-center px-6 font-size-5 bg-neutral-500 radius-10 py-2 font-500"
                to="/">
                joystick
            </RouterLink>

            <RouterLink style="width: 160px;"
                class="button-style text-white text-center px-6 font-size-5 bg-neutral-500 radius-10 py-2 font-500"
                to="/">
                emergency
            </RouterLink>
        </div>

        <!-- نوار پایین -->
        <div class="bottom position-absolute width-full px-4 d-flex flex-space-between">

            <!-- دکمه‌های سمت چپ -->
            <div class="d-flex flex-1 align-center gap-2">
                <button
                    class="button-style border-none outline-none d-flex flex-column flex-center radius-20 bg-neutral-400"
                    style="width: 40px; height: 40px;">
                    <Icon icon="circle-flags:fa" width="30" class="text-white" />
                </button>
                <button
                    class="button-style border-none outline-none d-flex flex-column flex-center radius-20 bg-neutral-400"
                    style="width: 40px; height: 40px;">
                    <Icon icon="solar:settings-bold" width="30" class="text-white" />
                </button>

                <button
                    class="button-style border-none outline-none d-flex flex-column flex-center radius-20 bg-neutral-400"
                    style="width: 40px; height: 40px;">
                    <Icon icon="solar:info-circle-bold" width="30" class="text-white" />
                </button>

                <button
                    class="button-style border-none outline-none d-flex flex-column flex-center radius-20 bg-neutral-400"
                    style="width: 40px; height: 40px;">
                    <Icon icon="solar:bluetooth-wave-bold" width="30" class="text-white" />
                </button>
            </div>

            <!-- متن وسط -->
            <div class="d-flex flex-1 flex-center text-white gap-2">
                <p>&copy; {{ new Date().getFullYear() }} copyright</p>
            </div>

            <div class="d-flex flex-1 text-neutral-800 align-center gap-2">
                <p></p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { RouterLink } from 'vue-router'
</script>

<style lang="scss" scoped>
/* پوزیشن‌ها */
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

/* 🎨 افکت حرفه‌ای برای همه دکمه‌ها و لینک‌ها */
.button-style {
    position: relative;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    user-select: none;
    transition: all 0.18s ease;
    transform: translateZ(0);

    /* نور subtle */
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
