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

const changeElementColours = (backgroundColour, colour, transition) => {
    const gridinputs = document.querySelectorAll('.office__grid-input');
    const inputs = document.querySelectorAll('.office__input');
    const textarea = document.querySelector('.office__notes-area');
    const outputArea = document.querySelectorAll('.office__output-inner-container');
    if (gridinputs && inputs && textarea && outputArea) {
        textarea.style.backgroundColor = backgroundColour;
        textarea.style.color = colour;
        textarea.style.transition = transition;
        outputArea.forEach((output) => {
            output.style.backgroundColor = backgroundColour;
            output.style.color = colour;
            output.style.transition = transition;
        })
        gridinputs.forEach((gridinput) => {
            gridinput.style.backgroundColor = backgroundColour;
            gridinput.style.color = colour;
            gridinput.style.transition = transition;
        })
        inputs.forEach((input) => {
            input.style.backgroundColor = backgroundColour;
            input.style.color = colour;
            input.style.transition = transition;
        })
    }
}


const toggleLightDarkMode = () => {
    if (theme.value === 'Dark') {
        theme.value = 'Light';
        userPreferenceStore.setThemePreference(theme.value);
        document.body.style.backgroundColor = 'white';
        document.body.style.color = 'black';
        changeElementColours('white', 'black', 'background-color 0.5s ease, color 0.5s ease');
    } else {
        theme.value = 'Dark';
        userPreferenceStore.setThemePreference(theme.value);
        document.body.style.backgroundColor = 'black';
        document.body.style.color = 'white';
        changeElementColours('black', 'white', 'background-color 0.5s ease, color 0.5s ease');
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
