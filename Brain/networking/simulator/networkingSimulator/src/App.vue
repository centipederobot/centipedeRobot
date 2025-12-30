<template>
    <div class="d-flex flex-column transition width-window position-relative align-center height-window overflow-hidden pa-2 font-us"
        :class="theme.colors === 'black' ? 'bg-neutral-800 text-white' : 'bg-neutral-100 text-black'">
        <!-- Header -->
        <header class="d-flex flex-center width-full text-center py-2 position-relative">
            <h1>robot network simulator</h1>
            <IconButton @click="showEmergencyDialog = true" theme="red" use-absolute direction="top: 2px; left: 2px"
                icon-size="30" icon="solar:shield-warning-bold" />
            <IconButton style="z-index: 100 !important;" @click="showHotSpotDialog = true" theme="blue" use-absolute
                direction="top: 2px; right: 2px" icon-size="30" icon="solar:bluetooth-bold" />
        </header>

        <!-- Main Content -->
        <div class="flex-1 d-flex flex-center width-full height-full position-relative flex-column">
            <!-- ✅ اگر هیچ رباتی وصل نیست -->
            <div v-if="!anyConnected" class="d-flex flex-column flex-center gap-4">
                <img src="/images/no-connection.png" alt="no connection" style="width:400px; opacity:0.8;" />
                <p class="text-center font-bold">
                    You are not connected to any robot, please connect to one.
                </p>
            </div>

            <!-- ✅ اگر حداقل یک ربات وصل است -->
            <template v-else>
                <!-- Robot Card -->
                <RobotCard :selectedRobot="selectedRobot" />
                <!-- Side Tabs (فقط برای ربات‌های وصل‌شده) -->
                <div class="side-tab-container">
                    <button v-for="r in connectedRobotList" :key="r" @click="selectedRobot = r" class="side-tab" :class="selectedRobot === r
                        ? 'bg-red-500 font-bold'
                        : theme.colors === 'black'
                            ? 'bg-neutral-600'
                            : 'bg-neutral-300'">
                        <p>{{ r.replace('r', 'robot ') }}</p>
                    </button>
                </div>
            </template>
            <!-- Side Controls -->
            <div class="d-flex flex-column flex-center height-full gap-6 position-absolute"
                style="bottom: 0; top: 0; left: 2px">
                <IconButton theme="default" icon-size="30" @click="theme.toggleTheme()"
                    :icon="theme.colors == 'white' ? 'solar:moon-stars-bold' : 'solar:sun-bold'" />
                <IconButton theme="default" icon-size="30" icon="circle-flags:fa" />
            </div>
        </div>

        <!-- Footer -->
        <footer class="d-flex flex-center width-full text-center py-2 position-relative">
            <IconButton @click="showGroupCommandDialog = true" theme="default" use-absolute
                direction="bottom: 2px; left: 2px" icon-size="30" icon="solar:users-group-two-rounded-bold" />
            <p>{{ new Date().getFullYear() }} &copy; copyright</p>
            <IconButton style="z-index: 100 !important;" @click="showLogDialogs = true" theme="blue" use-absolute
                direction="bottom: 2px; right: 2px" icon-size="30" icon="solar:info-circle-bold" />
        </footer>

        <!-- Dialogs -->
        <EmergencyDialog v-model="showEmergencyDialog"
            @emergency="emergencyActive = $event, showEmergencyDialog = false" />
        <LogsDialog v-model="showLogDialogs" :logs="logs" />
        <HotSpotDialog v-if="serviceStatus" v-model="showHotSpotDialog" :connectedRobots="connectedRobots"
            @connect="handleHotspotConnect" @open="fetchLogs" />
        <GroupCommandDialog v-model="showGroupCommandDialog" />
        <div v-if="emergencyActive" class="emergency-overlay">
            <p class="emergency-text font-size-8 font-bold">🚨 Emergency Mode Activated 🚨</p>
            <p class="font-size-5">for deactivating the Emergency mode please press the button</p>
            <IconButton @click="emergencyActive = false" theme="red" icon-size="30" icon="solar:shield-warning-bold" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useThemeStore } from './stores/useTheme'

import IconButton from './components/iconButton.vue'
import RobotCard from './components/template/robotCard.vue'
import EmergencyDialog from './components/template/emergencyDialog.vue'
import GroupCommandDialog from './components/template/GroupCommandDialog.vue'
import HotSpotDialog from './components/template/hotSpotDialog.vue'
import LogsDialog from './components/template/logsDialog.vue'
import { getCommandLogs } from './apis/log'
import { startHotspot, stopHotspot, getHotspotStatus } from './apis/hotspot'
import { Icon } from '@iconify/vue'

const theme = useThemeStore()
const selectedRobot = ref<'r1' | 'r2' | 'r3' | string>('r1')
const emergencyActive = ref(false)
const showEmergencyDialog = ref(false)
const showGroupCommandDialog = ref(false)
const showHotSpotDialog = ref(false)
const showLogDialogs = ref(false)
const serviceStatus = ref(false)

const logs = ref([])

const connectedRobots = ref<Record<string, boolean>>({
    r1: false,
    r2: false,
    r3: false
})

async function handleHotspotConnect(id: string) {
    try {
        if (connectedRobots.value[id]) {
            const res = await stopHotspot(id)
            console.log('Hotspot stopped:', res.data)
            connectedRobots.value[id] = false
        } else {
            const res = await startHotspot(id)
            console.log('Hotspot started:', res.data)
            connectedRobots.value[id] = true
        }
        const status = await getHotspotStatus(id)
        console.log('Hotspot status:', status.data)
    } catch (err) {
        console.error('Hotspot error:', err)
    }
}

const robots = ['r1', 'r2', 'r3']

onMounted(async () => {
    for (const id of robots) {
        const status = await getHotspotStatus(id)
        connectedRobots.value[id] = status.data.connected
    }
    serviceStatus.value = true
    await fetchLogs()
})

async function fetchLogs() {
    try {
        const res = await getCommandLogs()
        logs.value = res.data.logs.map((log: any) => ({
            time: log.time,
            message: typeof log.action === 'string' ? log.action : JSON.stringify(log.action)
        }))
        logs.value.reverse()
    } catch (err) {
        console.error('Error fetching logs:', err)
    }
}

// ✅ محاسبه وضعیت اتصال
const anyConnected = computed(() => Object.values(connectedRobots.value).some(v => v))
const connectedRobotList = computed(() => Object.keys(connectedRobots.value).filter(r => connectedRobots.value[r]))
</script>

<style scoped>
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

.emergency-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(2px);
    z-index: 9998;
    /* پایین‌تر از دکمه اضطراری */
    display: flex;
    flex-direction: column;
    gap: 20px;
    justify-content: center;
    align-items: center;
}

.emergency-text {
    color: oklch(0.637 0.237 25.331);
    font-weight: bold;
}

.emergency-text {
    animation: animationEmergency 2s infinite ease-in-out;
    color: oklch(0.577 0.245 27.325);
    /* قرمز هشدار */
}

/* تغییر رنگ بین قرمز و نارنجی */
@keyframes animationEmergency {
    0% {
        color: oklch(0.577 0.245 27.325);
        /* قرمز */
        text-shadow: 0 0 6px rgba(239, 68, 68, 0.6);
    }

    50% {
        color: oklch(0.646 0.222 41.116);
        /* نارنجی */
        text-shadow: 0 0 12px rgba(249, 115, 22, 0.8);
    }

    100% {
        color: oklch(0.577 0.245 27.325);
        /* دوباره قرمز */
        text-shadow: 0 0 6px rgba(239, 68, 68, 0.6);
    }
}
</style>