<template>
    <div class="d-flex flex-column width-full align-center transition max-width-500 pa-2 radius-5 gap-4"
        :class="theme.colors === 'black' ? 'bg-neutral-700 text-white' : 'bg-neutral-300 text-black'">
        <!-- Header -->
        <div class="d-flex flex-space-between width-full gap-4">
            <strong class="px-4">
                {{ robotTitle }}
            </strong>
            <div class="d-flex align-center">
                <strong>85%</strong>
                <Icon icon="mingcute:battery-3-line"
                    :class="theme.colors === 'white' ? 'text-green-100' : 'text-green-400'" width="30" />
            </div>
        </div>

        <!-- Image -->
        <img src="/videos/placeholder.gif" class="width-full radius-3" />

        <!-- Controllers -->
        <div class="d-flex flex-space-between width-full px-2 py-4 gap-2">
            <!-- Arrow Controller -->
            <div class="arrow-key-controller-container transition">
                <button style="width: 35px; height: 55px"
                    class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-flex-start justify-center radius-2"
                    :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                    <Icon icon="solar:double-alt-arrow-up-line-duotone" width="30" :class="theme.switchPrimaryClass" />
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
                    <Icon icon="tabler:triangle" width="30" class="text-green-300" />
                </button>

                <div class="functional-key-controller-middle">
                    <button
                        class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                        :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                        <Icon icon="tabler:square" width="30" class="text-pink-300" />
                    </button>

                    <button
                        class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                        :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                        <Icon icon="tabler:circle" width="30" class="text-red-300" />
                    </button>
                </div>

                <button
                    class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                    :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                    <Icon icon="tabler:letter-x" width="30" class="text-blue-300" />
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '@iconify/vue'
import { useThemeStore } from '../../stores/useTheme';

const props = defineProps<{
    selectedRobot: 'r1' | 'r2' | 'r3' | string
}>()

const theme = useThemeStore()

const robotTitle = computed(() => {
    if (props.selectedRobot === 'r1') return 'robot 1'
    if (props.selectedRobot === 'r2') return 'robot 2'
    return 'robot 3'
})
</script>

<style scoped>
/* 👇 فقط استایل‌های مربوط به Robot Card */

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
    gap: 2rem;
}

.functional-key-controller-container {
    width: fit-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.1rem;
}

.functional-key-controller-middle {
    display: flex;
    gap: 2rem;
}

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
</style>
