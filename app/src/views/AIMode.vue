<script setup lang="ts">
import { useDevicesList, useUserMedia, useFullscreen, useToggle, useSpeechRecognition, useScroll } from '@vueuse/core'
import { reactive, shallowRef, useTemplateRef, watchEffect, ref } from 'vue'
import { Icon } from '@iconify/vue';
import { RouterLink } from 'vue-router';

const currentCamera = shallowRef<string>()

const { videoInputs: cameras } = useDevicesList({
    requestPermissions: true,
    onUpdated() {
        if (!cameras.value.find(i => i.deviceId === currentCamera.value))
            currentCamera.value = cameras.value[0]?.deviceId
    },
})

const video = useTemplateRef('video')
const container = useTemplateRef('container')
const { enter } = useFullscreen(container)
const hasEnteredFullscreen = ref(false)

const { stream, enabled } = useUserMedia({
    constraints: reactive({ video: { deviceId: { exact: currentCamera } } }),
})
enabled.value = true

watchEffect(() => {
    if (video.value && stream.value) {
        video.value.srcObject = stream.value
    }
})


// 🎤 Speech Recognition از VueUse
const {
    isSupported,
    isListening,
    result,
    start,
    stop,
} = useSpeechRecognition({ lang: 'fa-IR' }) // می‌تونی 'en-US' بذاری برای انگلیسی

// وضعیت رکورد
const toggleVoice = () => {
    if (isListening.value) {
        stop()
        console.log("🛑 Voice recording stopped.")
    } else {
        start()
        console.log("🎤 Voice recording started...")
    }
}

// متن گفته‌شده را در UI هم نشان بدهیم
const transcript = ref('')
watchEffect(() => {
    if (result.value) {
        transcript.value = result.value
        console.log("🗣️ You said:", result.value)
    }
})

// رفرنس به کانتینر اسکرول
const scrollContainer = ref<HTMLDivElement | null>(null)

// گرفتن وضعیت اسکرول با VueUse
const { x, arrivedState } = useScroll(scrollContainer)
</script>

<template>
    <div ref="container"
        class="d-flex width-window overflow-hidden flex-center height-window flex-column gap-4 text-center">
        <video ref="video" autoplay class="width-full position-relative" />

        <!-- Back Button -->
        <RouterLink to="/"
            class="button-style-2 position-absolute top left border-none outline-none d-flex align-flex-start radius-2 bg-neutral-700">
            <Icon icon="solar:arrow-left-linear" class="text-white" width="35" />
        </RouterLink>

        <!-- Bottom Controls -->
        <div class="bottom position-absolute d-flex flex-center gap-1 flex-column width-full">
            <div class="scroll-wrapper" style="z-index: 1000 !important;">
                <div ref="scrollContainer" class="d-flex align-center gap-4 pa-2 overflow-x-auto scroll-container"
                    style="width: 100%; z-index: 1000 !important;">
                    <button style="width: fit-content; text-wrap: nowrap;"
                        class="button-style-2 d-flex pa-2 text-white flex-center radius-20 bg-neutral-700 border-none outline-none">
                        go forward
                    </button>
                    <button style="width: fit-content; text-wrap: nowrap;"
                        class="button-style-2 d-flex pa-2 text-white flex-center radius-20 bg-neutral-700 border-none outline-none">
                        go backward
                    </button>
                    <button style="width: fit-content; text-wrap: nowrap;"
                        class="button-style-2 d-flex pa-2 text-white flex-center radius-20 bg-neutral-700 border-none outline-none">
                        turn 90deg
                    </button>
                    <button style="width: fit-content; text-wrap: nowrap;"
                        class="button-style-2 d-flex pa-2 text-white flex-center radius-20 bg-neutral-700 border-none outline-none">
                        go forward and turn 90deg
                    </button>
                    <button style="width: fit-content; text-wrap: nowrap;"
                        class="button-style-2 d-flex pa-2 text-white flex-center radius-20 bg-neutral-700 border-none outline-none">
                        jump
                    </button>
                </div>
                <div v-if="!arrivedState.left" class="fade-left"></div>
                <div v-if="!arrivedState.right" class="fade-right"></div>
            </div>
            <!-- Voice Button -->
            <button @click="toggleVoice"
                :class="['button-style-2 d-flex pa-2 text-white flex-center radius-20 bg-neutral-700 border-none outline-none voice-btn', { 'recording': isListening }]"
                style="width: fit-content;">
                <Icon icon="solar:microphone-3-bold" width="35" />
            </button>
        </div>
    </div>
</template>

<style lang="scss" scoped>
/* 🎤 Voice Button Pulse Effect */
.voice-btn.recording {
    position: relative;
    animation: pulse 1.2s infinite;
    background-color: oklch(0.145 0 0) !important;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba($color: #a1a1a1, $alpha: 0.7);
    }

    70% {
        box-shadow: 0 0 0 15px rgba(255, 0, 0, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(255, 0, 0, 0);
    }
}

.scroll-wrapper {
    position: relative;
}

/* افکت fade */
.fade-left,
.fade-right {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 30px;
    pointer-events: none;
}
</style>
