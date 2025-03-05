<template>
    <div class="office__title-container">
        <h2 class="heading heading__h3">MediMate Chat</h2>
    </div>
    <div class="office__output-container">
        <p class="heading heading__p">Patient Past Appointments</p>
        <div class="office__output-inner-container">
            <div class="office__loader" v-if="props.encounterLoader"></div>
            <p class="heading heading__p" v-if="props.patientEncounterSummary" >{{props.patientEncounterSummary.summary}}</p>
            <p class="heading heading__p" v-if="props.patientEncounterSummary" v-for="item in props.patientEncounterSummary.encounters" v-bind:key="item">
                <p style="font-weight: bold;">{{ item.date }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
            </p>
            <p class="heading heading__p" v-if="Object.keys(props.patientEncounterSummary).length == 0 && !props.encounterLoader">Nothing to see here</p>
        </div>
    </div>
    <div class="office__output-container">
        <p class="heading heading__p">Medication</p>
        <div class="office__output-inner-container">
            <div class="office__loader" v-if="props.medicationLoader"></div>
            <p class="heading heading__p" v-if="props.patientMedicationSummary">{{props.patientMedicationSummary.summary}}</p>
            <p class="heading heading__p" v-if="props.patientMedicationSummary" v-for="item in props.patientMedicationSummary.currentMedication" v-bind:key="item">
                <p style="font-weight: bold;">{{ item.startDate }} - Present <span style="font-weight: normal;">{{ item.details }}</span></p> 
            </p>
            <p class="heading heading__p" v-if="props.patientMedicationSummary" v-for="item in props.patientMedicationSummary.oldMedication" v-bind:key="item">
                <p style="font-weight: bold;">{{ item.startDate }} - {{ item.endDate }} <span style="font-weight: normal;">{{ item.details }}</span></p> 
            </p>
            <p class="heading heading__p" v-if="Object.keys(props.patientMedicationSummary).length == 0 && !props.medicationLoader">Nothing see here...</p>
        </div>
    </div>
    <div class="office__output-container">
        <p class="heading heading__p">Allergies</p>
        <div class="office__output-inner-container">
            <div class="office__loader" v-if="props.allergyLoader"></div>
            <p class="heading heading__p" v-if="props.patientAllergySummary">{{props.patientAllergySummary.summary}}</p>
            <p class="heading heading__p" v-if="props.patientAllergySummary" v-for="item in props.patientAllergySummary.allergy" v-bind:key="item">
                <p style="font-weight: bold;">{{item.date}} <span style="font-weight:normal">{{item.details}}</span></p>
            </p>
            <p class="heading heading__p" v-if="Object.keys(props.patientAllergySummary).length == 0 && !props.allergyLoader">Nothing see here...</p>
        </div>
    </div>
    <div class="office__output-container">
        <p class="heading heading__p">Adverse drug effect alerts</p>
        <div class="office__output-inner-container">
            <p class="heading heading__p">Nothing see here...</p>
        </div>
    </div>
    <div class="office__output-container">
        <p class="heading heading__p">Medical record Export and Download</p>
        <div class="office__output-inner-container office__output-inner-container--export">
            <p class="heading heading__p">Nothing see here...</p>
        </div>
    </div>
</template>
<script setup>
const props = defineProps({
    patientEncounterSummary: Object,
    encounterLoader: Boolean, 
    patientMedicationSummary: Object,
    medicationLoader: Boolean,
    patientAllergySummary: Object,
    allergyLoader: Boolean,
})

console.log(props)
</script>