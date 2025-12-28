<template>
    <div class="d-flex flex-column transition width-window position-relative align-center height-window overflow-hidden pa-2 font-us"
        :class="theme.colors === 'black' ? 'bg-neutral-800 text-white' : 'bg-neutral-100 text-black'">
        <!-- Header -->
        <header class="d-flex flex-center width-full text-center py-2 position-relative">
            <h1>robot network simulator</h1>
            <IconButton theme="red" use-absolute direction="top: 2px; left: 2px" icon-size="30"
                icon="solar:shield-warning-bold" />
            <IconButton style="z-index: 100 !important;" theme="blue" use-absolute direction="top: 2px; right: 2px"
                icon-size="30" icon="solar:bluetooth-bold" />
        </header>

        <!-- Main Content -->
        <div class="flex-1 d-flex flex-center width-full height-full position-relative flex-column">
            <!-- Robot Card -->
            <div class="d-flex flex-column width-full align-center transition max-width-500 pa-2 radius-5 gap-4"
                :class="theme.colors === 'black' ? 'bg-neutral-700 text-white' : 'bg-neutral-300 text-black'">
                <div class="d-flex flex-space-between width-full gap-4">
                    <strong class="px-4">
                        {{ selectedRobot == 'r1' ? 'robot 1' : selectedRobot == 'r2' ? 'robot 2' : 'robot 3' }}
                    </strong>
                    <div class="d-flex align-center">
                        <strong>85%</strong>
                        <Icon icon="mingcute:battery-3-line"
                            :class="theme.colors === 'white' ? 'text-green-100' : 'text-green-400'" width="30" />
                    </div>
                </div>
                <img src="/videos/placeholder.gif" class="width-full radius-3" />
                <div class="d-flex flex-space-between width-full px-2 py-4 gap-2">
                    <!-- Arrow Controller -->
                    <div class="arrow-key-controller-container transition">
                        <button style="width: 35px; height: 55px"
                            class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-flex-start justify-center radius-2"
                            :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                            <Icon icon="solar:double-alt-arrow-up-line-duotone" width="30"
                                :class="theme.switchPrimaryClass" />
                        </button>

                        <div class="arrow-key-controller-middle">
                            <button style="width: 55px; height: 35px"
                                class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-center justify-flex-start radius-2"
                                :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                                <Icon icon="solar:double-alt-arrow-left-line-duotone" width="30"
                                    :class="theme.switchPrimaryClass" />
                            </button>
                            <button style="width: 55px; height: 35px"
                                class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-center justify-flex-end radius-2"
                                :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                                <Icon icon="solar:double-alt-arrow-right-line-duotone" width="30"
                                    :class="theme.switchPrimaryClass" />
                            </button>
                        </div>

                        <button style="width: 35px; height: 55px"
                            class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-flex-end justify-center radius-2"
                            :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                            <Icon icon="solar:double-alt-arrow-down-line-duotone" width="30"
                                :class="theme.switchPrimaryClass" />
                        </button>
                    </div>

                    <!-- Functional Controller -->
                    <div class="functional-key-controller-container transition">
                        <button
                            class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                            :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                            <Icon icon="tabler:triangle" width="40" class="text-green-300" />
                        </button>

                        <div class="functional-key-controller-middle">
                            <button
                                class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                                :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                                <Icon icon="tabler:square" width="40" class="text-pink-300" />
                            </button>
                            <button
                                class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                                :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                                <Icon icon="tabler:circle" width="40" class="text-red-300" />
                            </button>
                        </div>

                        <button
                            class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                            :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                            <Icon icon="tabler:letter-x" width="40" class="text-blue-300" />
                        </button>
                    </div>
                </div>
            </div>

            <!-- Side Controls -->
            <div class="d-flex flex-column flex-center height-full gap-6 position-absolute"
                style="bottom: 0; top: 0; left: 2px;">
                <IconButton theme="default" icon-size="30" @click="theme.toggleTheme()"
                    :icon="theme.colors == 'white' ? 'solar:moon-stars-bold' : 'solar:sun-bold'" />
                <IconButton theme="default" icon-size="30" icon="circle-flags:fa" />
            </div>

            <!-- Side Tabs -->
            <div class="side-tab-container">
                <button @click="selectedRobot = 'r1'" class="side-tab"
                    :class="selectedRobot == 'r1' ? 'bg-red-500 font-bold' : (theme.colors === 'black' ? 'bg-neutral-600' : 'bg-neutral-300')">
                    <p>robot 1</p>
                </button>
                <button @click="selectedRobot = 'r2'" class="side-tab"
                    :class="selectedRobot == 'r2' ? 'bg-red-500 font-bold' : (theme.colors === 'black' ? 'bg-neutral-600' : 'bg-neutral-300')">
                    <p>robot 2</p>
                </button>
                <button @click="selectedRobot = 'r3'" class="side-tab"
                    :class="selectedRobot == 'r3' ? 'bg-red-500 font-bold' : (theme.colors === 'black' ? 'bg-neutral-600' : 'bg-neutral-300')">
                    <p>robot 3</p>
                </button>
            </div>
        </div>

        <!-- Footer -->
        <footer class="d-flex flex-center width-full text-center py-2 position-relative">
            <IconButton theme="default" use-absolute direction="bottom: 2px; left: 2px" icon-size="30"
                icon="solar:users-group-two-rounded-bold" />
            <p>{{ new Date().getFullYear() }} &copy; copyright</p>
            <IconButton style="z-index: 100 !important;" theme="blue" use-absolute direction="bottom: 2px; right: 2px"
                icon-size="30" icon="solar:info-circle-bold" />
        </footer>
    </div>
</template>

<script setup lang="ts">
import IconButton from './components/iconButton.vue';
import { useThemeStore } from './stores/useTheme';
import { Icon } from '@iconify/vue';
import { ref } from 'vue'
const selectedRobot = ref('r1') // پیش‌فرض ربات 1
const theme = useThemeStore()
</script>

<style scoped>
/* کانتینر اصلی که همه کنترلرها رو نگه می‌داره */
.controller-wrapper {
    display: flex;
    justify-content: space-between;
    /* یکی سمت چپ، یکی سمت راست */
    align-items: flex-end;
    width: 100%;
    padding: 1rem;
    box-sizing: border-box;
}

/* کنترلر جهت‌ها */
.arrow-key-controller-container {
    width: fit-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    gap: 0.2rem;
}

.arrow-key-controller-middle {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
}

/* کنترلر دکمه‌های عملکردی */
.functional-key-controller-container {
    width: fit-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    gap: 0.1rem;
}

.functional-key-controller-container button {
    width: 40px;
    height: 40px;
    cursor: pointer;
    border: none;
    outline: none;
    transition: all 0.2s ease;
}

.functional-key-controller-middle {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
}

/* هاور و اکتیو برای همه دکمه‌ها */
.arrow-key-controller-container button,
.functional-key-controller-container button {
    transition: transform 0.2s ease;
}

.arrow-key-controller-container button:hover,
.functional-key-controller-container button:hover {
    transform: scale(1.1);
}

.arrow-key-controller-container button:active,
.functional-key-controller-container button:active {
    transform: scale(0.9);
}

/* تب‌های کناری */
.side-tab-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 3.5rem;
    /* width: 100vw; */
    /* height: 100vh; */
    position: fixed;
    right: -36px;
    top: 0;
    bottom: 0;
    padding: 1rem 0.5rem;
    z-index: 10;
}

.side-tab {
    width: 100px;
    height: 50px;
    border-radius: 0 0 10px 10px;
    transform: rotate(90deg);
    color: white;
    border: none;
    outline: none;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.side-tab:hover {
    transform: rotate(90deg) scale(1.05);
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.25);
}

.side-tab:active {
    transform: rotate(90deg) scale(0.95);
}
</style>