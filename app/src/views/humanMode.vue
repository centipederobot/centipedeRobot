<script setup lang="ts">
import { useDevicesList, useUserMedia, useFullscreen } from '@vueuse/core'
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
        // if (container.value && !hasEnteredFullscreen.value) {
        //     enter()
        //     hasEnteredFullscreen.value = true
        // }
    }
})
</script>

<template>
    <div ref="container"
        class="d-flex width-window overflow-hidden flex-center height-window flex-column gap-4 text-center">
        <video ref="video" autoplay class="width-full position-relative" />
        <div class="arrow-key-controller-container transition">
            <button style="width: 35px; height: 55px;"
                class="button-style-2 border-none outline-none d-flex align-flex-start radius-2 bg-neutral-700">
                <Icon icon="solar:double-alt-arrow-up-line-duotone" width="30" class="text-white" />
            </button>
            <div class="arrow-key-controller-middle">
                <button style="width: 55px; height: 35px;"
                    class="button-style-2 border-none outline-none d-flex align-center justify-flex-start radius-2 bg-neutral-700">
                    <Icon icon="solar:double-alt-arrow-left-line-duotone" width="30" class="text-white" />
                </button>
                <button style="width: 55px; height: 35px;"
                    class="button-style-2 border-none outline-none d-flex align-center justify-flex-end radius-2 bg-neutral-700">
                    <Icon icon="solar:double-alt-arrow-right-line-duotone" width="30" class="text-white" />
                </button>
            </div>
            <button style="width: 35px; height: 55px;"
                class="button-style-2 border-none outline-none d-flex align-flex-end radius-2 bg-neutral-700">
                <Icon icon="solar:double-alt-arrow-down-line-duotone" width="30" class="text-white" />
            </button>
        </div>
        <div class="functional-key-controller-container transition">
            <button class="button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2 bg-neutral-700">
                <Icon icon="tabler:triangle" width="40" class="text-green-300" />
            </button>
            <div class="functional-key-controller-middle">
                <button
                    class="button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2 bg-neutral-700">
                    <Icon icon="tabler:square" width="40" class="text-pink-300" />
                </button>
                <button
                    class="button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2 bg-neutral-700">
                    <Icon icon="tabler:circle" width="40" class="text-red-300" />
                </button>
            </div>
            <button class="button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2 bg-neutral-700">
                <Icon icon="tabler:letter-x" width="40" class="text-blue-300" />
            </button>
        </div>
        <RouterLink to="/"
            class="button-style-2 position-absolute top left border-none outline-none d-flex align-flex-start radius-2 bg-neutral-700">
            <Icon icon="solar:arrow-left-linear" class="text-white" width="35" />
        </RouterLink>
    </div>
</template>
<style lang="scss" scoped>
.arrow-key-controller-container {
    width: fit-content;
    position: absolute;
    left: 20px;
    bottom: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem; // فاصله بین بالا/پایین و وسط
}

.arrow-key-controller-middle {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem; // فاصله بین چپ و راست
}

.arrow-key-controller-center {
    width: 40px;
    height: 40px;
}

.functional-key-controller-container {
    width: fit-content;
    position: absolute;
    right: 20px;
    bottom: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem; // فاصله بین بالا/پایین و وسط

    button {
        width: 40px !important;
        height: 40px !important;
    }
}

.functional-key-controller-middle {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem; // فاصله بین چپ و راست
}
</style>