<template>
  <div class="d-flex flex-column width-full height-full">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useLanguageStore } from './stores/useLanguage'
import { BluetoothLe } from '@capacitor-community/bluetooth-le'
import { CapacitorWifi } from '@capgo/capacitor-wifi'
onMounted(async () => {
  try {
    // ۱. مقداردهی اولیه پلاگین
    await BluetoothLe.initialize()

    // ۲. تحریک نمایش دیالوگ اجازه بلوتوث (مخصوص اندروید ۱۲+)
    // این متد باعث می‌شود سیستم پنجره دسترسی به Bluetooth Connect و Scan را باز کند
    await BluetoothLe.requestLEScan({
      services: [],
    })

    // بلافاصله اسکن را متوقف کنید تا سیستم آزاد شود
    await BluetoothLe.stopLEScan()

    // ۳. درخواست مجوز لوکیشن (برای وای‌فای و بلوتوث در اندروید زیر ۱۲ الزامی است)
    await CapacitorWifi.requestPermissions({
      permissions: ['location'],
    })
    console.log('تمام مجوزها با موفقیت مدیریت شدند.')
  } catch (error) {
    // اگر کاربر 'Deny' را بزند، کد به اینجا منتقل می‌شود
    console.error('کاربر اجازه دسترسی نداد یا خطایی رخ داد:', error)
  }
  document.body.classList.add(`font-${useLanguageStore().language}`)
})
</script>

<style lang="scss" scoped></style>
