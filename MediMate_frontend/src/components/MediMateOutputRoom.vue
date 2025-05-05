<template>
    <div class="office__title-container">
        <h2 class="heading heading__h3">MediMate EHR Summary</h2>
        <p class="heading heading__p">Please always consult a qualified doctor, MediMate is prone to making mistakes</p>
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
                <p class="heading heading__p" v-if="Object.keys(summaryObject.encounterSummary.data).length != 0" v-html="summaryObject.encounterSummary.data.summary"></p>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.encounterSummary.data).length == 0 && !encounterLoader">Select a patient and click `summarise past appointments`.</p>
                <div v-if="Object.keys(summaryObject.encounterSummary.data).length != 0" v-for="item in summaryObject.encounterSummary.data.encounters" v-bind:key="item" style="margin-bottom: 10px;">
                    <p style="font-weight: bold;">{{ item.startDate }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
                </div>
            </div>
            <div class="office__output-contents" id="medicationSummary">
                <div class="office__loader" v-if="medicationLoader"></div>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.medicationSummary.data).length != 0">{{summaryObject.medicationSummary.data.summary}}</p>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.medicationSummary.data).length == 0 && !medicationLoader">Select a patient and click `summarise past and current medication`.</p>
                <div v-if="Object.keys(summaryObject.medicationSummary.data).length != 0" v-for="item in summaryObject.medicationSummary.data.medications" v-bind:key="item" style="margin-bottom: 10px;">
                    <p style="font-weight: bold;">{{ item.startDate }} - {{ item.endDate }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
                </div>
            </div>
            <div class="office__output-contents" id="allergySummary">
                <div class="office__loader" v-if="allergyLoader"></div>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.allergySummary.data).length != 0">{{summaryObject.allergySummary.data.summary}}</p>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.allergySummary.data).length == 0 && !allergyLoader">Select a patient and click `summarise allergies`.</p>
                <div v-if="Object.keys(summaryObject.allergySummary.data).length != 0" v-for="item in summaryObject.allergySummary.data.allergy" v-bind:key="item" style="margin-bottom: 10px;">
                    <p style="font-weight: bold;">{{ item.startDate }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
                </div>
            </div>
            <div class="office__output-contents" id="conditionSummary">
                <div class="office__loader" v-if="conditionLoader"></div>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.conditionSummary.data).length != 0">{{summaryObject.conditionSummary.data.summary}}</p>
                <p class="heading heading__p" v-if="Object.keys(summaryObject.conditionSummary.data).length == 0 && !conditionLoader">Select a patient and click `summarise condition`.</p>
                <div v-if="Object.keys(summaryObject.conditionSummary.data).length != 0" v-for="item in summaryObject.conditionSummary.data.conditions" v-bind:key="item" style="margin-bottom: 10px;">
                    <p style="font-weight: bold;">{{ item.startDate }} - {{ item.endDate }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
                </div>
            </div>
            <div class="office__output-contents" id="prescriptionClash">
                <div class="office__loader" v-if="precriptionClashLoader"></div>
                <ul class="office__prescription-list">
                    <li class="office__prescription-line-item" v-if="summaryObject.prescriptionClash.data.length != 0" v-for="item in summaryObject.prescriptionClash.data" v-bind:key="item">
                        <div class="office__prescription-icon-container">
                            <font-awesome-icon class="alert__icon" v-if="item[0].severity === 'Major'" :icon="['fas', 'circle-exclamation']" style="color: #DB4437; width: 30px; height: 30px;"/>
                            <font-awesome-icon class="alert__icon" v-if="item[0].severity === 'Moderate'" :icon="['fas', 'triangle-exclamation']" style="color: #F7BA3E; width: 30px; height: 30px;"/>
                            <font-awesome-icon class="alert__icon" v-if="item[0].severity === 'Minor' || item[0].severity === 'Unknown' " :icon="['fas', 'exclamation']" style="color: #31BFA6; width: 30px; height: 30px;"/>    
                        </div>
                        <p class="heading heading__p">Medimate systems has detected a possible <span style="font-weight: bold; ">{{item[0].severity}}</span> drug drug interaction between the currently prescribed {{item[0].active_medication}} and {{item[0].prescription}}. Score: {{(item[0].score * 100).toFixed(5)}}</p>
                    </li>
                </ul>
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
    conditionSummary: {heading: 'Conditions', data: {}},
    prescriptionClash: {heading: 'Prescription Clashes', data: {}}

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
    patientConditionSummary: Object,
    conditionLoader: Boolean,
    prescriptionClash: Object,
    precriptionClashLoader: Boolean,
})

watch(() => [props.patientEncounterSummary, props.patientMedicationSummary, props.patientAllergySummary, props.patientConditionSummary, props.prescriptionClash],
    ([newEncounterSummary, newMedicationSummary, newAllergySummary, newConditionSummary, newPrescriptionClash]) => {
        summaryObject.value.encounterSummary.data = newEncounterSummary
        summaryObject.value.medicationSummary.data = newMedicationSummary
        summaryObject.value.allergySummary.data = newAllergySummary
        summaryObject.value.conditionSummary.data = newConditionSummary
        summaryObject.value.prescriptionClash.data = newPrescriptionClash
        console.log(summaryObject.value)
    },
    { deep: true }
);

watch(() => props.encounterLoader, (newVal) => {
    toggleActiveSection('encounterSummary')
});

watch(() => props.medicationLoader, (newVal) => {
    toggleActiveSection('medicationSummary')
});

watch(() => props.allergyLoader, (newVal) => {
    toggleActiveSection('allergySummary')
});

watch(() => props.conditionLoader, (newVal) => {
    toggleActiveSection('conditionSummary')
});

watch(() => props.precriptionClashLoader, (newVal) => {
    toggleActiveSection('prescriptionClash')
});


</script>