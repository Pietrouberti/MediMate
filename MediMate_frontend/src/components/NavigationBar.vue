<script setup>
import { ref, onMounted } from 'vue';
import { useUserPreferenceStore } from '@/stores/user-preferences';
import { useRouter } from 'vue-router';

const theme = ref(null);
const router = useRouter();
const userPreferenceStore = useUserPreferenceStore();


onMounted(() => {
    userPreferenceStore.initStore();
    theme.value = userPreferenceStore.theme;
    if (userPreferenceStore.theme == 'Dark') {

        document.body.style.backgroundColor = 'black';
        document.body.style.color = 'white';
    } else {
        document.body.style.backgroundColor = 'white';
        document.body.style.color = 'black';
    }
})


const toggleLightDarkMode = () => {
    if (theme.value === 'Dark') {
        theme.value = 'Light';
        userPreferenceStore.setThemePreference(theme.value);
        document.body.style.backgroundColor = 'white';
        document.body.style.color = 'black';
    } else {
        theme.value = 'Dark';
        userPreferenceStore.setThemePreference(theme.value);
        document.body.style.backgroundColor = 'black';
        document.body.style.color = 'white';
    }
}

const redirect = (path) => {
    router.push(path);
}  
</script>

<template>
    <div class="navbar">
        <div class="navbar__logo">
            <h1 class="heading heading__h1" @click="redirect('/')">MediMate</h1>
        </div>
        <div class="navbar__cta">
            <button class="button button--secondary" @click="toggleLightDarkMode">Mode: {{theme}}</button>
            <button class="button button--primary" @click="redirect('/login')">Login</button>
        </div>
    </div>
</template>
