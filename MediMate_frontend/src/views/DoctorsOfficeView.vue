<template>
    <div class="office">
        <div class="office__col">
           <DoctorAppointment />
        </div>
        <div class="office__col">
            <MediChatOutputRoom />
        </div>
    </div> 
</template>

<script setup>
import MediChatOutputRoom from '@/components/MediMateOutputRoom.vue';
import DoctorAppointment from '@/components/DoctorAppointment.vue';
import { useUserPreferenceStore } from '@/stores/user-preferences';
import { onMounted } from 'vue';

const userPreferenceStore = useUserPreferenceStore();

onMounted(() => {
    if (userPreferenceStore.theme == 'Dark') {
        changeElementColours('black', 'white', 'background-color 0.5s ease, color 0.5s ease');
    } else {
        changeElementColours('white', 'black', 'background-color 0.5s ease, color 0.5s ease');
    }
});


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
