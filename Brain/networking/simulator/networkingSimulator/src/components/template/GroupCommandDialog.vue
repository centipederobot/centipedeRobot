<template>
    <Dialog title="Group Command" :model-value="modelValue" @dialog:close="close">
        <div class="dialog-content">
            <Transition name="step-fade-slide" mode="out-in">

                <!-- STEP 1 -->
                <section v-if="step === 1" class="dialog-section">
                    <div class="d-flex flex-center gap-2 width-full">
                        <Icon icon="svg-spinners:wifi-fade" width="72" class="icon-spin-slow text-blue-400" />
                        <Icon icon="svg-spinners:3-dots-fade" width="72" class="icon-spin-slow text-green-400" />
                        <div class="d-flex flex-column gap-1">
                            <Icon icon="line-md:reddit-loop" width="72" class="icon-spin-slow text-neutral-400" />
                            <p>robot leader</p>
                        </div>
                        <Icon icon="svg-spinners:3-dots-fade" width="72" class="icon-spin-slow text-green-400" />
                        <div class="d-flex flex-column gap-1">
                            <Icon icon="line-md:reddit-loop" width="48" class="icon-spin-slow text-neutral-400" />
                            <Icon icon="line-md:reddit-loop" width="48" class="icon-spin-slow text-neutral-400" />
                        </div>
                    </div>

                    <div class="typing-block">
                        <p v-for="(line, i) in typedGroupLines" :key="i" class="typed-line">
                            {{ line }}
                        </p>
                    </div>

                    <button class="next-btn" @click="step = 2">Next</button>
                </section>

                <!-- STEP 2 -->
                <section v-else class="dialog-section">
                    <h3 class="section-title">Configure Group Command</h3>

                    <div class="form-block">
                        <label class="form-label">Leader Robot:</label>
                        <select v-model="leaderRobot" class="form-select">
                            <option disabled value="">Select a robot</option>
                            <option value="r1">Robot 1</option>
                            <option value="r2">Robot 2</option>
                            <option value="r3">Robot 3</option>
                        </select>
                    </div>

                    <div class="form-block">
                        <label class="form-label">Command:</label>
                        <select v-model="groupCommand" class="form-select">
                            <option disabled value="">Select a command</option>
                            <option value="forward">Forward</option>
                            <option value="backward">Backward</option>
                            <option value="rotate">Rotate</option>
                            <option value="rotate-reverse">Rotate Reverse</option>
                            <option value="turn-left">Turn Left</option>
                            <option value="turn-right">Turn Right</option>
                            <option value="increase-speed">Increase Speed</option>
                            <option value="decrease-speed">Decrease Speed</option>
                        </select>
                    </div>

                    <button class="next-btn" @click="applyGroupCommand">Apply Command</button>
                </section>

            </Transition>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import Dialog from '../dialog.vue'
import { Icon } from '@iconify/vue'
import { ref, watch, onMounted } from 'vue'

defineProps<{ modelValue: boolean }>()
const emit = defineEmits(['update:modelValue'])

const step = ref(1)

const groupLines = [
    'Group Command allows you to control multiple robots at once.',
    'You can assign a leader robot and synchronize commands.',
    'This ensures coordinated movement and efficient execution.'
]

const typedGroupLines = ref<string[]>([])

function typeLines(lines: string[]) {
    typedGroupLines.value = []
    let l = 0, c = 0

    const tick = () => {
        if (!lines[l]) return
        if (!typedGroupLines.value[l]) typedGroupLines.value.push('')
        // @ts-ignore
        typedGroupLines.value[l] = lines[l].slice(0, ++c)
        // @ts-ignore
        if (c >= lines[l].length) { l++; c = 0 }
        setTimeout(tick, 20)
    }
    tick()
}

onMounted(() => typeLines(groupLines))

watch(step, () => {
    if (step.value === 1) typeLines(groupLines)
})

const leaderRobot = ref('')
const groupCommand = ref('')

function applyGroupCommand() {
    console.log('Leader:', leaderRobot.value, 'Command:', groupCommand.value)
}

function close() {
    emit('update:modelValue', false)
    step.value = 1
}
</script>

<style scoped>
.dialog-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.typing-block {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.typed-line {
    max-width: 560px;
}

.next-btn {
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
}

.form-block {
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 100%;
    max-width: 300px;
}

.form-label {
    font-weight: bold;
    text-align: left;
}

.form-select {
    padding: 6px;
    border-radius: 6px;
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
</style>
