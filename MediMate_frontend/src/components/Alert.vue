<template>
    <div class="alert" :style="`background-color: ${props.dangerColour}; --messageCount: ${props.messageCount}`" v-if="props.messageType='diagnosis_alert'">
        <font-awesome-icon class="alert__icon" v-show="props.serverity === 'Major'" :icon="['fas', 'circle-exclamation']" style="color: #ffffff;" />
        <font-awesome-icon class="alert__icon" v-show="props.serverity === 'Moderate'" :icon="['fas', 'triangle-exclamation']" style="color: #ffffff;" />
        <font-awesome-icon class="alert__icon" v-show="props.serverity === 'Mild' || props.serverity === 'Minor'" :icon="['fas', 'exclamation']" style="color: #ffffff;" />
        <p>{{props.message}}</p>
        <font-awesome-icon :icon="['fas', 'xmark']" style="color: #ffffff;" @click="deleteAlert(props.messageCount)"/>
    </div>
    <div class="alert" :style="`background-color: ${props.dangerColour}; --messageCount: ${props.messageCount}; flex-direction: column; align-center: flex-start;`" v-if="props.messageType === 'evaluation'">
        <p style="text-align: center; font-weight: bold;">Summary Evaluation Metrics Scores  <font-awesome-icon :icon="['fas', 'xmark']" style="color: #ffffff;" @click="deleteAlert(props.messageCount)"/></p>
        <p v-if="props?.evaluation?.conciseness?.compression_ratio">Compression Ratio: {{props.evaluation.conciseness.compression_ratio}}</p>
        <p v-if="props?.evaluation?.conciseness?.avg_sentence_length">Avg. Sentence Length: {{props.evaluation.conciseness.avg_sentence_length}}</p>
        <p v-if="props?.evaluation?.conciseness?.stopword_ratio">Stopword Ratio: {{props.evaluation.conciseness.stopword_ratio}}</p>
        <p v-if="props?.evaluation?.faithfulness">Faithfulness: {{props.evaluation.faithfulness}}</p>
        <p v-if="props?.evaluation?.coverage">Coverage: {{ props.evaluation.coverage }}</p>
        <p v-if="props?.evaluation?.fluency">Fluency: {{ props.evaluation.fluency }}</p>
        <p v-if="props?.evaluation?.redundancy">Redundancy: {{props.evaluation.redundancy}}</p>
        <p v-else>No evaluation metrics available.</p>
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
    evaluation: Object,
})

</script>

