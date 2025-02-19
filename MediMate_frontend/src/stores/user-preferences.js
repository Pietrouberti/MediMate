import { defineStore } from 'pinia'

// user store to save and manage user customisability preference

export const useUserPreferenceStore = defineStore('user-preferences', {
    id: 'user-preferences',
    state: () => ({
        theme: 'light',
    }),
    actions: {
        // initialise the store
        initStore() {
            console.log('initStore');
            const theme = localStorage.getItem('theme') || 'Light';
            this.theme = theme;
            this.setThemePreference(theme);
            console.log('theme', theme);
        },
        // set the theme preference into the local storage so information survives refresh
        setThemePreference(theme) {
            localStorage.setItem('theme', theme);
            this.theme = theme;
        }
    }

});