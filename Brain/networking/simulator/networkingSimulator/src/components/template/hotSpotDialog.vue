<template>
    <Dialog title="Hotspot" :model-value="modelValue" @dialog:close="emit('update:modelValue', false)">
        <div class="d-flex flex-column gap-4 width-full pa-2" :class="theme.switchPrimaryClass">
            <div v-for="item in 3" :key="item" class="width-full d-flex flex-space-between gap-4 px-2 py-2 radius-2"
                :class="theme.colors === 'black' ? 'bg-neutral-400' : 'bg-neutral-200'">
                <div class="d-flex align-center gap-2">
                    <img src="/images/robot.jpg" class="avatar radius-3" alt="" />
                    <strong :class="theme.switchPrimaryClass">robot {{ item }}</strong>
                </div>
                <div class="d-flex flex-space-between gap-2">
                    <button @click="emit('connect', `r${item}`)"
                        class="px-4 py-2 radius-2 transition-fast d-flex flex-center gap-1 cursor-pointer border-none outline-none"
                        :class="connectedRobots[`r${item}`]
                            ? (theme.colors === 'black' ? 'bg-red-600 text-white' : 'bg-red-400 text-white')
                            : (theme.colors === 'black' ? 'bg-emerald-600 text-white' : 'bg-emerald-400 text-white')">
                        {{ connectedRobots[`r${item}`] ? 'disconnect' : 'connect' }}
                        <Icon icon="solar:bluetooth-wave-bold" width="20" />
                    </button>
                </div>
            </div>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { useThemeStore } from '../../stores/useTheme';
import Dialog from '../dialog.vue'
defineProps<{ modelValue: boolean; connectedRobots: Record<string, boolean> }>()
const emit = defineEmits(['update:modelValue', 'connect'])
const theme = useThemeStore();
</script>

<style scoped>
.connect-btn {
    padding: 6px 12px;
    border-radius: 6px
}


.avatar {
    width: 40px;
    height: 40px;
}

.button-style-success {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    user-select: none;
    transition: all 0.18s ease;
    transform: translateZ(0);
}

body.theme-dark .button-style-success {
    background-color: #016630;
    color: #fff;
}

body.theme-light .button-style-success {
    background-color: #4caf50;
    color: #000;
}

button:hover {
    background-color: rgba(1, 102, 48, 0.9);
    box-shadow: 0 0 3px rgba(0, 0, 0, 0.18);
}

button:active {
    transform: scale(0.94);
    background-color: rgba(3, 46, 21, 0.8);
    box-shadow: 0 0 3px rgba(0, 0, 0, 0.25);
}
</style>
