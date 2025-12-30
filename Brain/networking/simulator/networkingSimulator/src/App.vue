<template>
    <div class="d-flex flex-column transition width-window position-relative align-center height-window overflow-hidden pa-2 font-us"
        :class="theme.colors === 'black' ? 'bg-neutral-800 text-white' : 'bg-neutral-100 text-black'">
        <!-- Header -->
        <header class="d-flex flex-center width-full text-center py-2 position-relative">
            <h1>robot network simulator</h1>
            <IconButton @click="showEmergencyDialog = true" theme="red" use-absolute direction="top: 2px; left: 2px"
                icon-size="30" icon="solar:shield-warning-bold" />
            <IconButton @click="showHotSpotDialog = true" theme="blue" use-absolute direction="top: 2px; right: 2px"
                icon-size="30" icon="solar:bluetooth-bold" />
        </header>

        <!-- Main Content -->
        <div class="flex-1 d-flex flex-center width-full height-full position-relative flex-column">
            <!-- ✅ Robot Card Component -->
            <RobotCard :selectedRobot="selectedRobot" />

            <!-- Side Controls -->
            <div class="d-flex flex-column flex-center height-full gap-6 position-absolute"
                style="bottom: 0; top: 0; left: 2px">
                <IconButton theme="default" icon-size="30" @click="theme.toggleTheme()"
                    :icon="theme.colors == 'white' ? 'solar:moon-stars-bold' : 'solar:sun-bold'" />
                <IconButton theme="default" icon-size="30" icon="circle-flags:fa" />
            </div>

            <!-- Side Tabs -->
            <div class="side-tab-container">
                <button v-for="(r) in ['r1', 'r2', 'r3']" :key="r" @click="selectedRobot = r" class="side-tab"
                    :class="selectedRobot === r ? 'bg-red-500 font-bold' : (theme.colors === 'black' ? 'bg-neutral-600' : 'bg-neutral-300')">
                    <p>{{ r.replace('r', 'robot ') }}</p>
                </button>
            </div>
        </div>

        <!-- Footer -->
        <footer class="d-flex flex-center width-full text-center py-2 position-relative">
            <IconButton @click="showGroupCommandDialog = true" theme="default" use-absolute
                direction="bottom: 2px; left: 2px" icon-size="30" icon="solar:users-group-two-rounded-bold" />
            <p>{{ new Date().getFullYear() }} &copy; copyright</p>
            <IconButton @click="showLogDialogs = true" theme="blue" use-absolute direction="bottom: 2px; right: 2px"
                icon-size="30" icon="solar:info-circle-bold" />
        </footer>

        <!-- Dialogs -->
        <EmergencyDialog v-model="showEmergencyDialog" />
        <LogsDialog v-model="showLogDialogs" :logs="logs" />
        <HotSpotDialog v-model="showHotSpotDialog" />
        <GroupCommandDialog v-model="showGroupCommandDialog" />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useThemeStore } from './stores/useTheme'

import IconButton from './components/iconButton.vue'
import RobotCard from './components/template/robotCard.vue'
import EmergencyDialog from './components/template/emergencyDialog.vue'
import GroupCommandDialog from './components/template/GroupCommandDialog.vue'
import HotSpotDialog from './components/template/hotSpotDialog.vue'
import LogsDialog from './components/template/logsDialog.vue'

const theme = useThemeStore()
const selectedRobot = ref<'r1' | 'r2' | 'r3' | string>('r1')

const showEmergencyDialog = ref(false)
const showGroupCommandDialog = ref(false)
const showHotSpotDialog = ref(false)
const showLogDialogs = ref(false)

const logs = ref([
    { time: '2025-12-29 22:10', message: 'System started.' },
    { time: '2025-12-29 22:12', message: 'Connection established with robot 1.' },
    { time: '2025-12-29 22:13', message: 'Emergency mode activated.' },
    { time: '2025-12-29 22:14', message: 'Database connection checked.' },
    { time: '2025-12-29 22:15', message: 'User logged in.' }
])
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
</style>