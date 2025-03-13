<template>
    <div class="alert" :style="`background-color: ${props.dangerColour}; --messageCount: ${props.messageCount}`">
        <font-awesome-icon class="alert__icon" v-show="props.serverity === 'Major'" :icon="['fas', 'circle-exclamation']" style="color: #ffffff;" />
        <font-awesome-icon class="alert__icon" v-show="props.serverity === 'Moderate'" :icon="['fas', 'triangle-exclamation']" style="color: #ffffff;" />
        <font-awesome-icon class="alert__icon" v-show="props.serverity === 'Mild'" :icon="['fas', 'exclamation']" style="color: #ffffff;" />
        <p v-if="props.messageType === 'prescription_alert'">{{props.message}} : {{props.serverity}}</p>
        <p v-if="props.messageType === 'diagnosis_alert'">{{props.message}}</p>
        <font-awesome-icon :icon="['fas', 'xmark']" style="color: #ffffff;" @click="deleteAlert(props.messageCount)"/>
    </div>
</template>
<script setup>
import { defineEmits } from 'vue';

const emit = defineEmits(['deleteAlertEmit'])

const deleteAlert = (id) => {
    emit('deleteAlertEmit', id)
}

const props = defineProps({
    dangerColour: String,
    serverity: String,
    message: String,
    messageCount: Number,
    messageType: String,
})

</script>