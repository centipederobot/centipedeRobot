<template>
    <Dialog title="Logs info" :model-value="modelValue" @dialog:close="emit('update:modelValue', false)"
        @dialog:open="emit('open')">
        <div class="logs-dialog-content">
            <p class="logs-description">System logs</p>
            <table class="logs-table">
                <tr v-for="(log, i) in logs" :key="i">
                    <td>{{ log.message.replace('_', ' ') }}</td>
                    <td>{{ log.time.replace('T', ' / ').split('.')[0] }}</td>
                </tr>
            </table>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import Dialog from '../dialog.vue'
defineProps<{ modelValue: boolean; logs: { message: string, time: string }[] }>()
const emit = defineEmits(['update:modelValue', 'open'])
</script>

<style scoped>
.logs-table {
    width: 100%;
    border-collapse: collapse
}

.logs-table tr:nth-child(even) {
    background: #3a3a3a
}

.logs-table td {
    padding: 8px
}
</style>
