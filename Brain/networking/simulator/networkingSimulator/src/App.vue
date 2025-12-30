<template>
    <div class="d-flex flex-column transition width-window position-relative align-center height-window overflow-hidden pa-2 font-us"
        :class="theme.colors === 'black' ? 'bg-neutral-800 text-white' : 'bg-neutral-100 text-black'">
        <!-- Header -->
        <header class="d-flex flex-center width-full text-center py-2 position-relative">
            <h1>robot network simulator</h1>
            <IconButton @click="showEmergencyDialog = true" theme="red" use-absolute direction="top: 2px; left: 2px"
                icon-size="30" icon="solar:shield-warning-bold" />
            <IconButton @click="showHotSpotDialog = true" style="z-index: 100 !important;" theme="blue" use-absolute
                direction="top: 2px; right: 2px" icon-size="30" icon="solar:bluetooth-bold" />
        </header>

        <!-- Main Content -->
        <div class="flex-1 d-flex flex-center width-full height-full position-relative flex-column">
            <!-- Robot Card -->
            <div class="d-flex flex-column width-full align-center transition max-width-500 pa-2 radius-5 gap-4"
                :class="theme.colors === 'black' ? 'bg-neutral-700 text-white' : 'bg-neutral-300 text-black'">
                <div class="d-flex flex-space-between width-full gap-4">
                    <strong class="px-4">
                        {{ selectedRobot == 'r1' ? 'robot 1' : selectedRobot == 'r2' ? 'robot 2' : 'robot 3' }}
                    </strong>
                    <div class="d-flex align-center">
                        <strong>85%</strong>
                        <Icon icon="mingcute:battery-3-line"
                            :class="theme.colors === 'white' ? 'text-green-100' : 'text-green-400'" width="30" />
                    </div>
                </div>
                <img src="/videos/placeholder.gif" class="width-full radius-3" />
                <div class="d-flex flex-space-between width-full px-2 py-4 gap-2">
                    <!-- Arrow Controller -->
                    <div class="arrow-key-controller-container transition">
                        <button style="width: 35px; height: 55px"
                            class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-flex-start justify-center radius-2"
                            :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                            <Icon icon="solar:double-alt-arrow-up-line-duotone" width="30"
                                :class="theme.switchPrimaryClass" />
                        </button>

                        <div class="arrow-key-controller-middle">
                            <button style="width: 55px; height: 35px"
                                class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-center justify-flex-start radius-2"
                                :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                                <Icon icon="solar:double-alt-arrow-left-line-duotone" width="30"
                                    :class="theme.switchPrimaryClass" />
                            </button>
                            <button style="width: 55px; height: 35px"
                                class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-center justify-flex-end radius-2"
                                :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                                <Icon icon="solar:double-alt-arrow-right-line-duotone" width="30"
                                    :class="theme.switchPrimaryClass" />
                            </button>
                        </div>

                        <button style="width: 35px; height: 55px"
                            class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex align-flex-end justify-center radius-2"
                            :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                            <Icon icon="solar:double-alt-arrow-down-line-duotone" width="30"
                                :class="theme.switchPrimaryClass" />
                        </button>
                    </div>

                    <!-- Functional Controller -->
                    <div class="functional-key-controller-container transition">
                        <button
                            class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                            :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                            <Icon icon="tabler:triangle" width="40" class="text-green-300" />
                        </button>

                        <div class="functional-key-controller-middle">
                            <button
                                class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                                :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                                <Icon icon="tabler:square" width="40" class="text-pink-300" />
                            </button>
                            <button
                                class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                                :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                                <Icon icon="tabler:circle" width="40" class="text-red-300" />
                            </button>
                        </div>

                        <button
                            class="transition-fast cursor-pointer button-style-2 border-none outline-none d-flex flex-center radius-20 pa-2"
                            :class="theme.colors === 'black' ? 'bg-neutral-900' : 'bg-neutral-100'">
                            <Icon icon="tabler:letter-x" width="40" class="text-blue-300" />
                        </button>
                    </div>
                </div>
            </div>

            <!-- Side Controls -->
            <div class="d-flex flex-column flex-center height-full gap-6 position-absolute"
                style="bottom: 0; top: 0; left: 2px;">
                <IconButton theme="default" icon-size="30" @click="theme.toggleTheme()"
                    :icon="theme.colors == 'white' ? 'solar:moon-stars-bold' : 'solar:sun-bold'" />
                <IconButton theme="default" icon-size="30" icon="circle-flags:fa" />
            </div>

            <!-- Side Tabs -->
            <div class="side-tab-container">
                <button @click="selectedRobot = 'r1'" class="side-tab"
                    :class="selectedRobot == 'r1' ? 'bg-red-500 font-bold' : (theme.colors === 'black' ? 'bg-neutral-600' : 'bg-neutral-300')">
                    <p>robot 1</p>
                </button>
                <button @click="selectedRobot = 'r2'" class="side-tab"
                    :class="selectedRobot == 'r2' ? 'bg-red-500 font-bold' : (theme.colors === 'black' ? 'bg-neutral-600' : 'bg-neutral-300')">
                    <p>robot 2</p>
                </button>
                <button @click="selectedRobot = 'r3'" class="side-tab"
                    :class="selectedRobot == 'r3' ? 'bg-red-500 font-bold' : (theme.colors === 'black' ? 'bg-neutral-600' : 'bg-neutral-300')">
                    <p>robot 3</p>
                </button>
            </div>
        </div>

        <!-- Footer -->
        <footer class="d-flex flex-center width-full text-center py-2 position-relative">
            <IconButton theme="default" use-absolute direction="bottom: 2px; left: 2px" icon-size="30"
                icon="solar:users-group-two-rounded-bold" />
            <p>{{ new Date().getFullYear() }} &copy; copyright</p>
            <IconButton @click="showLogDialogs = true" style="z-index: 100 !important;" theme="blue" use-absolute
                direction="bottom: 2px; right: 2px" icon-size="30" icon="solar:info-circle-bold" />
        </footer>
        <!-- dialogs -->
        <Dialog title="Emergency mode" :model-value="showEmergencyDialog"
            @dialog:close="showEmergencyDialog = !showEmergencyDialog">
            <div class="dialog-content">
                <!-- ناوبری بالا (اختیاری) -->
                <div class="dialog-steps-indicator">
                    <span :class="['step-dot', step === 1 ? 'active' : '']"></span>
                    <span :class="['step-dot', step === 2 ? 'active' : '']"></span>
                    <span :class="['step-dot', step === 3 ? 'active' : '']"></span>
                </div>

                <!-- بخش‌ها با ترنزیشن نرم بین جابجایی -->
                <Transition name="step-fade-slide" mode="out-in">
                    <!-- بخش اول: توضیح بک‌اند + آیکون‌های انیمیشن‌دار (بلوتوث + اسپینر) -->
                    <section v-if="step === 1" key="step-1" class="dialog-section">
                        <div class="d-flex flex-center gap-2 width-full">
                            <Icon icon="svg-spinners:wifi-fade" :width="72" class="icon-spin-slow text-white" />
                            <Icon icon="svg-spinners:3-dots-fade" :width="72" class="icon-spin-slow text-white" />
                            <Icon icon="line-md:reddit-loop" :width="72" class="icon-spin-slow text-white" />
                        </div>

                        <div class="typing-block">
                            <p v-for="(line, i) in typedBackendLines" :key="'b-' + i" class="typed-line">
                                {{ line }}
                            </p>
                        </div>
                        <button class="next-btn" @click="goNext">بعدی</button>
                    </section>

                    <!-- بخش دوم: توضیح ظاهر سایت + آیکون‌های انیمیشن‌دار -->
                    <section v-else-if="step === 2" key="step-2" class="dialog-section">
                        <div class="d-flex flex-column flex-center width-full">
                            <Icon icon="line-md:alert-loop" :width="72" class="icon-pulse text-red-500" />
                        </div>

                        <div class="typing-block">
                            <p v-for="(line, i) in typedFrontendLines" :key="'f-' + i" class="typed-line">
                                {{ line }}
                            </p>
                        </div>

                        <button class="next-btn" @click="goNext">بعدی</button>
                    </section>

                    <!-- بخش سوم: عنوان + تصویر + دکمه فعال‌سازی -->
                    <section v-else key="step-3" class="dialog-section">
                        <h3 class="section-title">فعال‌سازی حالت اضطراری</h3>

                        <!-- نام عکس مطابق نام دیالوگ -->
                        <img src="/images/emergency.png" alt="emergency" class="section-image" />

                        <IconButton style="z-index: 100 !important;" :theme="isLocked ? 'red' : 'blue'"
                            :use-absolute="false" direction="top: 2px; right: 2px" icon-size="30"
                            :icon="isLocked ? 'solar:shield-check-bold' : 'solar:shield-keyhole-bold'"
                            @click="toggleEmergency" />
                    </section>
                </Transition>
            </div>
        </Dialog>
        <Dialog title="logs info" :model-value="showLogDialogs" @dialog:close="showLogDialogs = false">
            <div class="logs-dialog-content">
                <!-- متن توضیحی -->
                <p class="logs-description">
                    در این بخش می‌توانید لیست لاگ‌های سیستم را مشاهده کنید. هر لاگ شامل زمان و توضیح مربوطه است.
                </p>

                <!-- جدول لاگ‌ها -->
                <div class="logs-table-container">
                    <table class="logs-table">
                        <thead>
                            <tr>
                                <th>زمان</th>
                                <th>پیام</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(log, index) in logs" :key="index">
                                <td>{{ log.time }}</td>
                                <td>{{ log.message }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </Dialog>
        <!-- Hotspot Dialog -->
        <Dialog title="Hotspot" :model-value="showHotSpotDialog" @dialog:close="showHotSpotDialog = !showHotSpotDialog">
            <div class="d-flex flex-column gap-4 width-full pa-2" :class="theme.switchPrimaryClass">
                <div v-for="item in 3" :key="item" class="width-full d-flex flex-space-between gap-4 px-2 py-2 radius-2"
                    :class="theme.colors === 'black' ? 'bg-neutral-400' : 'bg-neutral-200'">
                    <div class="d-flex align-center gap-2">
                        <img src="/images/robot.jpg" class="avatar radius-3" alt="" />
                        <strong :class="theme.switchPrimaryClass">robot {{ item }}</strong>
                    </div>
                    <div class="d-flex flex-space-between gap-2">
                        <button
                            class="button-style-success px-4 py-2 radius-2 d-flex flex-center gap-1 border-none outline-none"
                            :class="theme.colors === 'black' ? 'bg-emerald-600 text-white' : 'bg-emerald-400 text-white'
                                ">
                            connect
                            <Icon icon="solar:bluetooth-wave-bold" width="15" />
                        </button>
                    </div>
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import Dialog from './components/dialog.vue';
import IconButton from './components/iconButton.vue';
import { useThemeStore } from './stores/useTheme';
import { Icon } from '@iconify/vue';
import { onMounted, ref, watch } from 'vue'
const selectedRobot = ref('r1') // پیش‌فرض ربات 1
const theme = useThemeStore()
const showLogDialogs = ref(false);
const showHotSpotDialog = ref(false);
const showEmergencyDialog = ref(false);
const step = ref(1)
const isLocked = ref(false)
const backendLines = [
    'در بک‌اند، با فعال شدن حالت اضطراری، یک رویداد سراسری منتشر می‌شود.',
    'تمام ربات‌ها فرمان توقف فوری دریافت می‌کنند.',
    'کانال‌های ارتباطی (مثلاً MQTT/WebSocket) در وضعیت محدود قرار می‌گیرند.',
    'وضعیت هر ربات در دیتابیس به حالت emergency تغییر می‌کند.',
    'ثبت لاگ انجام شده و شناسه‌ی عملیات برای ردیابی ذخیره می‌شود.'
]

const frontendLines = [
    'در ظاهر سایت، کارت‌های ربات حالت قرمز و هشدار می‌گیرند.',
    'کنترل‌های حرکتی و دکمه‌ها غیرفعال می‌شوند.',
    'پیغام هشدار در بالای داشبورد نمایش داده می‌شود.',
    'بخش لاگ‌ها یک رویداد اضطراری جدید ثبت و برجسته می‌کند.',
    'امکان خروج از حالت اضطراری فقط از طریق دکمه تأیید مجدد فعال می‌شود.'
]

/* خروجی تایپ‌شده هر بخش */
const typedBackendLines = ref<string[]>([])
const typedFrontendLines = ref<string[]>([])


/* تایپ کردن خط‌به‌خط با افکت (JS) — مناسب برای متن‌های خیلی طولانی */
function typeLines(sourceLines: string[], target: typeof typedBackendLines | typeof typedFrontendLines, speed = 20) {
    target.value = []
    let lineIndex = 0
    let charIndex = 0

    const tick = () => {
        const currentLine = sourceLines[lineIndex] ?? ''
        const currentTyped = (target.value[lineIndex] ?? '')

        // اگر خط جدید شروع شده، آرایه را آماده کن
        if (currentTyped.length === 0 && charIndex === 0) {
            target.value.push('')
        }

        // افزودن کاراکتر بعدی
        if (charIndex < currentLine.length) {
            target.value[lineIndex] = currentLine.slice(0, charIndex + 1)
            charIndex++
        } else {
            // پایان خط فعلی؛ برو خط بعدی
            lineIndex++
            charIndex = 0
            if (lineIndex >= sourceLines.length) {
                // پایان همه خطوط
                return
            }
        }

        // اسکرول به پایین برای نمایش خط بعدی در صورت نیاز
        requestAnimationFrame(() => {
            const container = document.querySelector('.dialog-content') as HTMLElement | null
            if (container) container.scrollTop = container.scrollHeight
        })

        setTimeout(tick, speed) // سرعت تایپ
    }

    setTimeout(tick, speed)
}

/* شروع تایپ هر بخش هنگام ورود */
function startTypingForStep() {
    if (step.value === 1) {
        typeLines(backendLines, typedBackendLines)
    } else if (step.value === 2) {
        typeLines(frontendLines, typedFrontendLines)
    }
}

onMounted(startTypingForStep)
watch(step, () => startTypingForStep())

function goNext() {
    if (step.value < 3) {
        step.value = (step.value + 1) as 1 | 2 | 3
    }
}

function toggleEmergency() {
    isLocked.value = !isLocked.value
}

const logs = ref([
    { time: '2025-12-29 22:10', message: 'سیستم راه‌اندازی شد.' },
    { time: '2025-12-29 22:12', message: 'ارتباط با ربات شماره 1 برقرار شد.' },
    { time: '2025-12-29 22:13', message: 'حالت اضطراری فعال شد.' },
    { time: '2025-12-29 22:14', message: 'ارتباط با دیتابیس بررسی شد.' },
    { time: '2025-12-29 22:15', message: 'کاربر وارد سیستم شد.' },
    // می‌تونی هر تعداد لاگ اضافه کنی
])
</script>

<style scoped>
/* کانتینر اصلی که همه کنترلرها رو نگه می‌داره */
.controller-wrapper {
    display: flex;
    justify-content: space-between;
    /* یکی سمت چپ، یکی سمت راست */
    align-items: flex-end;
    width: 100%;
    padding: 1rem;
    box-sizing: border-box;
}

/* کنترلر جهت‌ها */
.arrow-key-controller-container {
    width: fit-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    gap: 0.2rem;
}

.arrow-key-controller-middle {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
}

/* کنترلر دکمه‌های عملکردی */
.functional-key-controller-container {
    width: fit-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    gap: 0.1rem;
}

.functional-key-controller-container button {
    width: 40px;
    height: 40px;
    cursor: pointer;
    border: none;
    outline: none;
    transition: all 0.2s ease;
}

.functional-key-controller-middle {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
}

/* هاور و اکتیو برای همه دکمه‌ها */
.arrow-key-controller-container button,
.functional-key-controller-container button {
    transition: transform 0.2s ease;
}

.arrow-key-controller-container button:hover,
.functional-key-controller-container button:hover {
    transform: scale(1.1);
}

.arrow-key-controller-container button:active,
.functional-key-controller-container button:active {
    transform: scale(0.9);
}

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

/* محتوای دیالوگ: وسط‌چین + اسکرول رو به پایین */
.dialog-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* وسط‌چین افقی */
    justify-content: center;
    /* وسط‌چین عمودی */
    text-align: center;
    max-height: 520px;
    overflow-y: auto;
    /* اگر متن زیاد بود، اسکرول عمودی */
    padding: 8px 4px;
}

/* اندیکاتور مراحل */
.dialog-steps-indicator {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
}

.step-dot {
    width: 10px;
    height: 10px;
    border-radius: 9999px;
    background: #ccc;
    transition: all 0.2s ease;
}

.step-dot.active {
    background: #ef4444;
    /* قرمز */
    transform: scale(1.2);
}

/* ترنزیشن نرم بین جابجایی بخش‌ها */
.step-fade-slide-enter-active,
.step-fade-slide-leave-active {
    transition: all 250ms ease;
}

.step-fade-slide-enter-from {
    opacity: 0;
    transform: translateY(8px);
}

.step-fade-slide-enter-to {
    opacity: 1;
    transform: translateY(0);
}

.step-fade-slide-leave-from {
    opacity: 1;
    transform: translateY(0);
}

.step-fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}

/* بخش */
.dialog-section {
    width: 100%;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    align-items: center;
    /* وسط‌چین */
    justify-content: center;
    gap: 16px;
    padding: 8px 0;
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

/* عنوان بخش سوم و تصویر */
.section-title {
    font-weight: 700;
    font-size: 18px;
    margin: 4px 0 2px;
}

.section-image {
    max-width: 300px;
    border-radius: 8px;
    display: block;
}

.logs-dialog-content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-height: 400px;
    overflow-y: auto;
    /* اسکرول عمودی */
}

.logs-description {
    font-size: 14px;
    text-align: center;
    color: #666;
}

.logs-table-container {
    width: 100%;
}

.logs-table {
    width: 100%;
    border-collapse: collapse;
}

.logs-table thead tr {
    background-color: #4a4a4a;
    color: #f5f5f5;
}

.logs-table tr:nth-child(even) {
    background-color: #3a3a3a;
    color: #f5f5f5;
}

.logs-table th,
.logs-table td {
    padding: 8px;
    text-align: left;
    font-size: 14px;
}

/* بدون حاشیه */
.logs-table th {
    font-weight: bold;
    background: transparent;
}

.logs-table td {
    border: none;
}

.avatar {
    width: 40px;
    height: 40px;
}

.button-style-success {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    user-select: none;
    transition: all 0.18s ease;
    transform: translateZ(0);
}

body.theme-dark .button-style-success {
    background-color: #016630;
    color: #fff;
}

body.theme-light .button-style-success {
    background-color: #4caf50;
    color: #000;
}

.button-style-success:hover {
    background-color: rgba(1, 102, 48, 0.9);
    box-shadow: 0 0 3px rgba(0, 0, 0, 0.18);
}

.button-style-success:active {
    transform: scale(0.94);
    background-color: rgba(3, 46, 21, 0.8);
    box-shadow: 0 0 3px rgba(0, 0, 0, 0.25);
}
</style>