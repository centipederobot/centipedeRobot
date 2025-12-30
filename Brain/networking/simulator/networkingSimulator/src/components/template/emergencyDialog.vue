<template>
    <Dialog title="Emergency mode" :model-value="modelValue" @dialog:close="emit('update:modelValue', false)">
        <div class="dialog-content">
            <!-- steps -->
            <div class="dialog-steps-indicator">
                <span :class="['step-dot', step === 1 && 'active']"></span>
                <span :class="['step-dot', step === 2 && 'active']"></span>
                <span :class="['step-dot', step === 3 && 'active']"></span>
            </div>

            <Transition name="step-fade-slide" mode="out-in">
                <!-- STEP 1 -->
                <section v-if="step === 1" class="dialog-section">
                    <div class="d-flex flex-center gap-2">
                        <Icon icon="svg-spinners:wifi-fade" width="72" />
                        <Icon icon="svg-spinners:3-dots-fade" width="72" />
                        <Icon icon="line-md:reddit-loop" width="72" />
                    </div>

                    <div class="typing-block">
                        <p v-for="(line, i) in typedBackendLines" :key="i" class="typed-line">{{ line }}</p>
                    </div>

                    <button class="next-btn" @click="goNext">Next</button>
                </section>

                <!-- STEP 2 -->
                <section v-else-if="step === 2" class="dialog-section">
                    <Icon icon="line-md:alert-loop" width="72" class="text-red-500" />

                    <div class="typing-block">
                        <p v-for="(line, i) in typedFrontendLines" :key="i" class="typed-line">{{ line }}</p>
                    </div>

                    <button class="next-btn" @click="goNext">Next</button>
                </section>

                <!-- STEP 3 -->
                <section v-else class="dialog-section">
                    <h3>Activate Emergency Mode</h3>
                    <img src="/images/emergency.png" class="section-image" />

                    <IconButton :theme="isLocked ? 'red' : 'blue'"
                        :icon="isLocked ? 'solar:shield-check-bold' : 'solar:shield-keyhole-bold'"
                        @click="isLocked = !isLocked" icon-size="35" />
                </section>
            </Transition>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import Dialog from '../dialog.vue'
import IconButton from '../iconButton.vue'
import { Icon } from '@iconify/vue'
import { ref, watch, onMounted } from 'vue'

defineProps<{ modelValue: boolean }>()
const emit = defineEmits(['update:modelValue'])

const step = ref(1)
const isLocked = ref(false)

// Emergency dialog lines
const backendLines = [
    'In the backend, when emergency mode is activated, a global event is published.',
    'All robots receive an immediate stop command.',
    'Communication channels (e.g., MQTT/WebSocket) are restricted.',
    'Each robot status in the database changes to emergency.',
    'Logs are recorded and an operation ID is stored for tracking.'
]

const frontendLines = [
    'On the frontend, robot cards turn red with a warning state.',
    'Movement controls and buttons are disabled.',
    'A warning message is displayed at the top of the dashboard.',
    'The logs section records and highlights a new emergency event.',
    'Exiting emergency mode is only possible via a confirmation button.'
]

const typedBackendLines = ref<string[]>([])
const typedFrontendLines = ref<string[]>([])

function typeLines(src: string[], target: typeof typedBackendLines) {
    target.value = []
    let l = 0, c = 0
    const tick = () => {
        if (!src[l]) return
        if (!target.value[l]) target.value.push('')
        // @ts-ignore
        target.value[l] = src[l].slice(0, ++c)
        // @ts-ignore
        if (c >= src[l].length) { l++; c = 0 }
        setTimeout(tick, 20)
    }
    tick()
}

watch(step, () => {
    if (step.value === 1) typeLines(backendLines, typedBackendLines)
    if (step.value === 2) typeLines(frontendLines, typedFrontendLines)
})

onMounted(() => typeLines(backendLines, typedBackendLines))

function goNext() {
    if (step.value < 3) step.value++
}
</script>

<style scoped>
.step-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #ccc
}

.step-dot.active {
    background: #ef4444
}

.dialog-section {
    display: flex;
    flex-direction: column;
    gap: 16px;
    align-items: center
}

.typed-line {
    max-width: 560px
}

.next-btn {
    padding: 8px 16px;
    border-radius: 8px
}

.section-image {
    max-width: 300px;
    border-radius: 8px
}

/* دکمه بعدی */
.next-btn {
    padding: 8px 16px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    background: #3a3a3a;
    color: white;
    transition: 0.2s ease;
}

.next-btn:hover {
    background: #4a4a4a;
}

.next-btn:active {
    transform: scale(0.96);
}

/* بلوک تایپینگ چندخطی (نه تک‌خطی) */
.typing-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* وسط‌چین خطوط */
    gap: 8px;
    width: 100%;
}

/* هر خط تایپ‌شونده */
.typed-line {
    display: block;
    white-space: pre-wrap;
    /* چندخطی و حفظ فاصله‌ها */
    word-break: break-word;
    /* اگر کلمات طولانی شد، بشکنه */
    max-width: 560px;
    text-align: center;
}
</style>
