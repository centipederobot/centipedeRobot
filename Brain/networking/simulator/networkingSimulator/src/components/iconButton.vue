<template>
    <button :style="direction"
        :class="[theme == 'red' ? 'bg-red-500 text-white' : theme == 'blue' ? 'bg-blue-500 text-white' : 'bg-neutral-400 text-white', useAbsolute ? 'position-absolute' : 'position-relative']"
        class="pa-2 radius-20 border-none transition-fast outline-none d-flex flex-center cursor-pointer">
        <Icon v-if="icon" :icon :width="iconSize" />
        <slot v-if="!icon"></slot>
    </button>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue';
interface iconButtonT {
    theme: 'default' | 'red' | 'blue'
    direction?: string;
    icon?: string;
    iconSize?: string;
    useAbsolute?: boolean;
}
const props = defineProps<iconButtonT>()
</script>

<style scoped>
button:hover {
    transform: scale(1.1);
}

button:active {
    transform: scale(0.9);
}
</style>