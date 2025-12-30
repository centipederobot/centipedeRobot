<template>
    <div class="relative width-full">
        <!-- دکمه اصلی -->
        <button @click="toggleDropdown" class="select-btn flex justify-between items-center"
            :class="theme.colors === 'black' ? 'bg-neutral-800 text-white' : 'bg-neutral-200 text-black'">
            {{ selectedLabel }}
            <Icon icon="solar:alt-arrow-down-linear" width="24"
                :class="theme.colors === 'black' ? 'text-white' : 'text-black'" />
        </button>

        <!-- لیست گزینه‌ها -->
        <ul v-show="isOpen" class="select-list absolute z-10 mt-1 w-full rounded shadow-md max-h-60 overflow-auto"
            :class="theme.colors === 'black' ? 'bg-neutral-900 text-white border border-neutral-700' : 'bg-white text-black border border-gray-300'">
            <li v-for="option in options" :key="option.value" @click="selectOption(option)"
                class="select-item cursor-pointer px-4 py-2"
                :class="theme.colors === 'black' ? 'hover:bg-neutral-700' : 'hover:bg-blue-100'">
                {{ option.label }}
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ref, computed } from 'vue'
import { useThemeStore } from '../stores/useTheme'

export interface selectBoxT {
    option: {
        label: string
        value: string
    }[]
}

const selectBoxValues = defineProps<selectBoxT>()
const emits = defineEmits(['update:model-value'])
const options = ref(selectBoxValues.option)

const selected = ref<{ label: string; value: string } | null>(null)
const isOpen = ref(false)

const theme = useThemeStore()

const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}

const selectOption = (option: { label: string; value: string }) => {
    selected.value = option
    isOpen.value = false
    emits('update:model-value', selected.value.value)
}

const selectedLabel = computed(() => selected.value ? selected.value.label : 'سایر موارد')
</script>

<style scoped>
.relative {
    position: relative;
}

.select-btn {
    width: 100%;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    font-size: 1rem;
    cursor: pointer;
    border: none;
    transition: background-color 0.2s ease;
}

.select-list {
    box-sizing: border-box;
    list-style: none;
}

.select-item {
    transition: background-color 0.2s ease;
}
</style>
