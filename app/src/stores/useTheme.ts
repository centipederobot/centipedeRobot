import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useThemeStore = defineStore("useThemeStore", () => {
    const colors = ref<'white' | 'black'>(
        (localStorage.getItem("theme") as 'white' | 'black') || 'black'
    );
    const toggleTheme = () => {
        colors.value = colors.value === "black" ? "white" : "black";
        localStorage.setItem("theme", colors.value);
    };
    const switchPrimaryClass = computed(() => {
        return colors.value === "black"
            ? "text-white"
            : "text-black";
    });
    const backgroundClass = computed(() => {
        return colors.value === "black"
            ? "bg-neutral-900"
            : "bg-neutral-100";
    });
    return {
        colors,
        toggleTheme,
        switchPrimaryClass,
        backgroundClass,
    };
});
