<template>
    <div v-if="modelValue" class="dialog-backdrop" @click="close">
        <div class="dialog-container" :class="theme.colors === 'black' ? 'dialog-dark' : 'dialog-light'" @click.stop>
            <header class="dialog-header">
                <slot name="title" />
            </header>

            <section class="dialog-body">
                <slot />
            </section>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import { useThemeStore } from "@/stores/useTheme";

const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits(["dialog:close"]);
const theme = useThemeStore();

const close = () => {
    emit("dialog:close", false);
};

// بستن با ESC
const handleKey = (e: KeyboardEvent) => {
    if (e.key === "Escape") close();
};

onMounted(() => window.addEventListener("keydown", handleKey));
onUnmounted(() => window.removeEventListener("keydown", handleKey));
</script>

<style lang="scss" scoped>
.dialog-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(1px);
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.2s ease;
    z-index: 9999;
}

.dialog-container {
    overflow-y: auto;
    width: fit-content;
    min-width: 400px;
    max-width: 600px;
    height: fit-content;
    max-height: 280px !important;
    border-radius: 14px;
    padding: 18px;
    animation: scaleIn 0.2s ease;
}

/* حالت تاریک */
.dialog-dark {
    background: #1f1f1f;
    color: #fff;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}

/* حالت روشن */
.dialog-light {
    background: #f5f5f5;
    color: #000;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.dialog-header {
    margin-bottom: 10px;
}

.dialog-title {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
}

.dialog-body {
    font-size: 15px;
    margin-bottom: 18px;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.dialog-btn {
    padding: 8px 16px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: 0.15s ease;
}

.dialog-dark .dialog-btn {
    background: #3a3a3a;
    color: white;
}

.dialog-dark .dialog-btn:hover {
    background: #4a4a4a;
}

.dialog-light .dialog-btn {
    background: #e0e0e0;
    color: black;
}

.dialog-light .dialog-btn:hover {
    background: #d0d0d0;
}

.dialog-btn:active {
    transform: scale(0.95);
}

/* انیمیشن‌ها */
@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes scaleIn {
    from {
        transform: scale(0.85);
        opacity: 0;
    }

    to {
        transform: scale(1);
        opacity: 1;
    }
}
</style>
