<template>
    <div class="office">
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

//vue imports 
import { onMounted } from 'vue';

//use user preference store
const userPreferenceStore = useUserPreferenceStore();

// on page load check what theme is set and change the colours accordingly
onMounted(() => {
    if (userPreferenceStore.theme == 'Dark') {
        changeElementColours('black', 'white', 'background-color 0.5s ease, color 0.5s ease');
    } else {
        changeElementColours('white', 'black', 'background-color 0.5s ease, color 0.5s ease');
    }
});

// helper fuction to change medichat form elements to match the theme
const changeElementColours = (backgroundColour, colour, transition) => {
    const gridinputs = document.querySelectorAll('.office__grid-input');
    const inputs = document.querySelectorAll('.office__input');
    const textarea = document.querySelector('.office__notes-area');
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
    }
}

</script>
