<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';


const mode = ref(null);
const router = useRouter();

onMounted(() => {
    mode.value = 'Dark';
})

const toggleLightDarkMode = () => {
    if (mode.value === 'Dark') {
        mode.value = 'Light';
        document.body.style.backgroundColor = 'white';
        document.body.style.color = 'black';
    } else {
        mode.value = 'Dark';
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
            <button class="button button--secondary" @click="toggleLightDarkMode">Mode: {{mode}}</button>
            <button class="button button--primary" @click="redirect('/login')">Login</button>
        </div>
    </div>
</template>
