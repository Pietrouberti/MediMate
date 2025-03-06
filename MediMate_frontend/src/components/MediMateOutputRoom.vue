<template>
    <div class="office__title-container">
        <h2 class="heading heading__h3">MediMate EHR Summary</h2>
    </div>
    <div class="office__output-container">
        <div class="office__output-headers">
            <ul class="office__output-header-list">
                <li class="office__output-header-item" v-for="item, key in summaryObject" v-bind:key="item" :id="`${key}`" @click="toggleActiveSection(key)">{{item.heading}}</li>
            </ul>
        </div>
        <div class="office__output-inner-container">
            <div class="office__output-contents" id="encounterSummary">
                <div class="office__loader" v-if="encounterLoader"></div>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.encounterSummary.data).length != 0">{{summaryObject.encounterSummary.data.summary}}</p>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.encounterSummary.data).length == 0 && !encounterLoader">Select a patient and click `summarise past appointments`.</p>
                <div v-if="Object.keys(summaryObject.encounterSummary.data).length != 0" v-for="item in summaryObject.encounterSummary.data.encounters" v-bind:key="item">
                    <p style="font-weight: bold;">{{ item.date }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
                </div>
            </div>
            <div class="office__output-contents" id="medicationSummary">
                <div class="office__loader" v-if="medicationLoader"></div>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.medicationSummary.data).length != 0">{{summaryObject.medicationSummary.data.summary}}</p>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.medicationSummary.data).length == 0 && !medicationLoader">Select a patient and click `summarise past and current medication`.</p>
                <div v-if="Object.keys(summaryObject.medicationSummary.data).length != 0" v-for="item in summaryObject.medicationSummary.data.medications" v-bind:key="item">
                    <p style="font-weight: bold;">{{ item.startDate }} - {{ item.endDate }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
                </div>
            </div>
            <div class="office__output-contents" id="allergySummary">
                <div class="office__loader" v-if="allergyLoader"></div>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.allergySummary.data).length != 0">{{summaryObject.allergySummary.data.summary}}</p>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.allergySummary.data).length == 0 && !allergySummary">Select a patient and click `summarise allergies`.</p>
                <div v-if="Object.keys(summaryObject.allergySummary.data).length != 0" v-for="item in summaryObject.allergySummary.data.allergy" v-bind:key="item">
                    <p style="font-weight: bold;">{{ item.date }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, watch, onMounted } from 'vue';


onMounted(() => {
    toggleActiveSection('encounterSummary')
})


const summaryObject = ref({
    encounterSummary: {heading: 'Appointments', data: {}},
    medicationSummary: {heading: 'Medications', data: {}},
    allergySummary: {heading: 'Allergies', data: {}},

})


const toggleActiveSection = (key) => {
    const summarySections = document.querySelectorAll('.office__output-contents');
    const summaryHeader = document.querySelectorAll('.office__output-header-item');
    summaryHeader.forEach((header) => {
        if (header.id != key) {
            header.classList.remove('office__output-header-item--active');
        }
        else {
            header.classList.add('office__output-header-item--active')
        }
    })
    summarySections.forEach((section) => {
        if (section.id != key) {
            section.style.display = 'none';
        }
        else {
            section.style.display = 'block';
        }
    });

}


const props = defineProps({
    patientEncounterSummary: Object,
    encounterLoader: Boolean, 
    patientMedicationSummary: Object,
    medicationLoader: Boolean,
    patientAllergySummary: Object,
    allergyLoader: Boolean,
})

watch(() => [props.patientEncounterSummary, props.patientMedicationSummary, props.patientAllergySummary],
    ([newEncounterSummary, newMedicationSummary, newAllergySummary]) => {
        summaryObject.value.encounterSummary.data = newEncounterSummary
        summaryObject.value.medicationSummary.data = newMedicationSummary
        summaryObject.value.allergySummary.data = newAllergySummary
        console.log(summaryObject.value)
    },
    { deep: true }
);


</script>