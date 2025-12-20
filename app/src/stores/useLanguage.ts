import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";
import i18n from "../lang/i18n"; // مسیر i18n که ساختی

export const useLanguageStore = defineStore("useLanguageStore", () => {
    const language = ref<"fa" | "us">(
        (localStorage.getItem("app-language") as "fa" | "us") || "us"
    );

    const toggleLanguage = () => {
        document.body.classList.remove(`font-${language.value}`);
        language.value = language.value === "us" ? "fa" : "us";
        saveToLocalStorage();
        document.body.classList.add(`font-${language.value}`);
    };

    const languageIcon = computed(() => {
        return language.value === "us"
            ? "circle-flags:fa" // وقتی زبان انگلیسی است، آیکون فارسی نشان داده شود
            : "circle-flags:us"; // وقتی زبان فارسی است، آیکون انگلیسی نشان داده شود
    });

    const saveToLocalStorage = () => {
        localStorage.setItem("app-language", language.value);
    };

    // هر بار زبان تغییر کند، locale هم تغییر کند
    watch(language, (newLang) => {
        i18n.global.locale.value = newLang;
    }, { immediate: true });

    return {
        language,
        toggleLanguage,
        languageIcon,
        saveToLocalStorage,
    };
});