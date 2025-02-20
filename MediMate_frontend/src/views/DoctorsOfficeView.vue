<template>
    <div class="office">
        <!--Line Puesdo element-->
        <div class="office__puesdo1"></div>
        <!--Glowing orbs puesdo element -->
        <div class="office__puesdo2"></div>
        <div class="office__puesdo3"></div>
        <div class="office__puesdo4"></div>
        <div class="office__puesdo5"></div>

        <div class="office__col">
            <!-- Doctors Appointment Panel Component -->
           <DoctorAppointment />
        </div>
        <div class="office__col">
            <!-- MediChat Output Panel Component -->
            <MediChatOutputRoom />
        </div>
    </div> 
</template>

<script setup>
// import view components
import MediChatOutputRoom from '@/components/MediMateOutputRoom.vue';
import DoctorAppointment from '@/components/DoctorAppointment.vue';
// import userpreference store for dynamic theming
import { useUserPreferenceStore } from '@/stores/user-preferences';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

//vue imports 
import { onMounted } from 'vue';

//use user preference store
const userPreferenceStore = useUserPreferenceStore();
const userStore = useUserStore();
const router = useRouter();

// on page load check what theme is set and change the colours accordingly
onMounted(() => {
    if (!userStore.user.isAuthenticated) {
        router.push({ path: '/login' });
    }
    if (userPreferenceStore.theme == 'Dark') {
        changeElementColours('black', 'white', 'background-color 0.5s ease, color 0.5s ease');
    } else {
        changeElementColours('white', 'black', 'background-color 0.5s ease, color 0.5s ease');
    }
});


window.scrollTo(0, 64);
// helper fuction to change medichat form elements to match the theme
const changeElementColours = (backgroundColour, colour, transition) => {
    const gridinputs = document.querySelectorAll('.office__grid-input');
    const inputs = document.querySelectorAll('.office__input');
    const textarea = document.querySelector('.office__notes-area');
    const output = document.querySelectorAll('.office__output-inner-container');
    if (gridinputs && inputs && textarea) {
        textarea.style.backgroundColor = backgroundColour;
        textarea.style.color = colour;
        textarea.style.transition = transition;
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
        output.forEach((output) => {
            output.style.color = colour
        })
    }
}

</script>
