import { defineStore } from 'pinia'

export const useUserPreferenceStore = defineStore('user-preferences', {
    id: 'user-preferences',
    state: () => ({
        theme: 'light',
    }),
    actions: {
        initStore() {
            console.log('initStore');
            const theme = localStorage.getItem('theme') || 'Light';
            this.theme = theme;
            this.setThemePreference(theme);
            console.log('theme', theme);
        },
        setThemePreference(theme) {
            localStorage.setItem('theme', theme);
            this.theme = theme;
        }
    }

});