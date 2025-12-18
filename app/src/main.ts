import { createApp } from 'vue'
import { createPinia } from 'pinia'
// @ts-ignore
import { SplashScreen } from '@capacitor/splash-screen';
import 'mini-k-tailwind/skeleton.css';
import './assets/styles.scss';
SplashScreen.hide();

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
