<template>
    <div class="office__title-container">
        <h2 class="heading heading__h3">Appointment Notepad</h2>
    </div>
    <div class="office__input-item">
        <label for="patient_search">Find Patient</label>
        <div class="office__input-container">
            <input type="text" class="office__input" v-model="searchQuery" placeholder="Search for a patient" @focus="showDropdown = true" @blur="hideDropdown" />
            <p class="office__clear-patient heading heading__p" v-if="selectedPatient.id != null" @click="removeSelectedPatient()">X</p>
        </div>
        <ul v-if="showDropdown && filteredPatients.length" class="office__dropdown">
            <li v-for="patient in filteredPatients" :key="patient.id" @mousedown.prevent="selectPatient(patient)">
                {{ patient.first_name }} {{ patient.last_name }}
            </li>
        </ul>
    </div>
    <div class="office__title-container">
        <h2 class="heading heading__h4">Patient Information</h2>
    </div>
    <div class="office__patient-info">
        <div class="office__grid-input-item">
            <label for="first_name">First Name</label>
            <input type="text" id="first_name" class="office__grid-input" disabled v-model="selectedPatient.first_name" placeholder="First Name" />
        </div>
        <div class="office__grid-input-item">
            <label for="last_name">Last Name</label>
            <input type="text" id="last_name" class="office__grid-input" disabled v-model="selectedPatient.last_name" placeholder="Last Name" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="age">Age</label>
            <input type="text" id="age" class="office__grid-input" disabled v-model="selectedPatient.age" placeholder="Age" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="gender">Gender</label>
            <input type="text" id="gender" class="office__grid-input" disabled v-model="selectedPatient.gender" placeholder="Gender" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="ethnicity">Ethnicity</label>
            <input type="text" id="ethnicity" class="office__grid-input" disabled v-model="selectedPatient.ethnicity" placeholder="Ethnicity" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="NHSID">NHS ID</label>
            <input type="text" id="NHSID" class="office__grid-input" disabled v-model="selectedPatient.id" placeholder="NHS ID" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="address">Address</label>
            <input type="text" id="address" class="office__grid-input" disabled v-model="selectedPatient.address" placeholder="Address" />
        </div>
        <div class="office__cta1">
            <button class="button button--form" @click="getEncounterSummary()" :disabled="selectedPatient.id == null || fetchingInformation">Summaries past appointments</button>
            <button class="button button--form" @click="getMedicationSummary()" :disabled="selectedPatient.id == null || fetchingInformation">Summaries current active medication</button>
            <button class="button button--form" @click="getAllergySummary()" :disabled="selectedPatient.id == null || fetchingInformation">Summaries allergies</button>
            <button class="button button--form" @click="getConditionSummary()" :disabled="selectedPatient.id == null || fetchingInformation">Summaries Conditions</button>
        </div>
    </div>
    <div class="office__title-container">
        <h4 class="heading heading__h4">Appointment Notes</h4>
    </div>
    <div class="office__appointment-notes">
        <div class="office__patient-info">
            <div class="office__grid-input-item">
                <label for="notes">Observations</label>
                <textarea class="office__notes-area" name="notes" id="notes" placeholder="Appointment Notes" v-model="appointment.notes"></textarea>
            </div>
        </div>
        <div class="office__patient-info">
            <div class="office__grid-input-item">
                <label for="Symptoms">Symptoms</label>
                <input type="text" id="symptoms" class="office__grid-input" placeholder="Patient symptoms" v-model="appointment.symptoms" />
            </div>
            <div class="office__grid-input-item">
                <label for="Diagnosis">Diagnosis</label>
                <input type="text" id="diagnosis" class="office__grid-input" placeholder="Diagnosis prediction" v-model="appointment.diagnosis" />
            </div>
        </div>
        <div class="office__patient-info">
            <div class="office__grid-input-item">
                <label for="prescription-name">Prescription Name</label>
                <input type="text" id="prescription-name" class="office__grid-input" placeholder="Name of prescription" v-model="appointment.prescription"/>
            </div>
            <div class="office__grid-input-item">
                <label for="prescription-dosage">Prescription Dosage</label>
                <input type="text" id="prescription-dosage" class="office__grid-input" placeholder="Prescription dosage" v-model="appointment.dosage"/>
            </div>
        </div>
        <div class="office__patient-info">
            <div class="office__grid-input-item">
                <label for="prescription-start">Prescription Start Date</label>
                <input type="date" id="prescription-start" class="office__grid-input" v-model="appointment.prescription_start"/>
            </div>
            <div class="office__grid-input-item">
                <label for="prescription-start">Prescription End Date</label>
                <input type="date" id="prescription-start" class="office__grid-input" v-model="appointment.prescription_end"/>
            </div>
        </div>
        <div class="office__cta">
            <button class="button button--form" @click="verifyDoctorsDiagnosis" :disabled="appointment.diagnosis == null || appointment.symptoms == null || appointment.notes == null || selectedPatient.id == null">Verify diagnosis prediction</button>
            <button class="button button--form" @click="verifyPrescriptionClashes">Check for Prescription Clashes</button>
            <button class="button button--form">Download EHR Record</button>
        </div>
    </div>
</template>
<script setup>
// vue imports
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';

const emit = defineEmits([
    'encounterSummary', 
    'encounterSummaryLoader', 
    'clearEncounterResponse',
    'medicationSummary', 
    'medicationSummaryLoader',
    'clearMedicationResponse',
    'allergySummary', 
    'allergySummaryLoader',
    'clearAllergyResponse',
    'conditionSummary',
    'conditionSummaryLoader',
    'clearConditionResponse',
    'emitDiagnosisVerification',
    'emitPrescriptionClash',
    'emitPrescriptionClashLoader',
    'emitPrescriptionClashClear'
])

const fetchingInformation = ref(false);

const userStore = useUserStore();

const patients = ref([])


onMounted(async() => {
    await getPatientList()
});

const getPatientList = async() => {
    await axios.get('api/patients/get_patients/', {
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}`
        }
    }).then((response) => {
        if (response.data.success == true) {
            patients.value = response.data.patients 
        }
    }).catch((error) => {
        console.error(error)
    })
}

// selected patient object
const selectedPatient = ref({
    id: null,
    first_name: null,
    last_name: null,
    age: null,
    gender: null,
    ethnicity: null,
    address: null,
});

// appointment object
const appointment = ref({
    notes: null,
    symptoms: null,
    diagnosis: null,
    prescription_start: null,
    prescription_end: null,
    prescription: null,
    prescription_dosage: null,
})


// search patient v-model proxy varible
const searchQuery = ref('');

// boolean to show/hide dropdown
const showDropdown = ref(false);


// filter patient list based on search query
const filteredPatients = computed(() => {
    if (!patients.value || patients.value.length === 0) return[];
    return patients.value
        .filter(patient => 
            patient.first_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            patient.last_name.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
        .sort((a, b) => {
            const query = searchQuery.value.toLowerCase();
            const aFirstNameMatch = a.first_name.toLowerCase().startsWith(query);
            const bFirstNameMatch = b.first_name.toLowerCase().startsWith(query);
            if (aFirstNameMatch && !bFirstNameMatch) return -1;
            if (!aFirstNameMatch && bFirstNameMatch) return 1;
            return a.first_name.localeCompare(b.first_name);
        });
});


// select patient from dropdown
const selectPatient = (patient) => {
    searchQuery.value = patient.first_name + ' ' + patient.last_name;
    selectedPatient.value = patient;
    showDropdown.value = false;
};

const removeSelectedPatient = () => {
    searchQuery.value = "";
    selectedPatient.value = {
        id: null,
        first_name: null,
        last_name: null,
        age: null,
        gender: null,
        ethnicity: null,
        address: null,
    }

    // clear the contents of the summary tabs and prescription clash when a user deselects a patient
    emit('clearAllergyResponse')
    emit('clearConditionResponse')
    emit('clearMedicationResponse')
    emit('clearEncounterResponse')
    emit('emitPrescriptionClashClear')
}

// hide dropdown after 200ms for smoother transition and silky UX
const hideDropdown = () => {
    setTimeout(() => {
        showDropdown.value = false;
    }, 200);
};

// get a summary of patient medication
const getMedicationSummary = async() => {
    // clear previous repsonses
    fetchingInformation.value = true;
    emit('clearMedicationResponse')
    emit('medicationSummaryLoader', true)
    // start the loading animation
    await axios.get('api/llm_generation/get_summary/medication/' + selectedPatient.value.id, {
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}`
        }
    }).then((response) => {
        if (response.data.success) {
            fetchingInformation.value = false;
            // emit value of the medication summary to the parent component
            emit('medicationSummary', response.data.summary)
            // notify parent component to stop loading animation
            emit('medicationSummaryLoader', false)
        }
    }).catch((error) => {
        console.error(error)
        emit('medicationSummaryLoader', false)
    })
}

const getAllergySummary = async() => {
    // clear previous repsonses
    fetchingInformation.value = true;
    emit('clearAllergyResponse')
    // start loading animation to provide user feedback
    emit('allergySummaryLoader', true)
    await axios.get('api/llm_generation/get_summary/allergy/' + selectedPatient.value.id, {
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}` 
        }
    }).then((response) => {
        if(response.data.success) {
            fetchingInformation.value = false;
            // emit summary to parent component
            emit('allergySummary', response.data.summary);
            // stop the loading animation
            emit('allergySummaryLoader', false);
        }
    }).catch((error) => {
        console.error(error)
        emit('allergySummaryLoader', false);
    })
}


// get a summary of patient previous encounters
const getEncounterSummary = async() => {
    // clear previous repsonses
    fetchingInformation.value = true;
    emit('clearEncounterResponse')
    // start the loading animation
    emit('encounterSummaryLoader', true)
    await axios.get('api/llm_generation/get_summary/encounters/' + selectedPatient.value.id,{
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}`
        }
    }).then((response) => {
        if(response.data.success) {
            fetchingInformation.value = false;
            // emit value to parent component
            emit('encounterSummary', response.data.summary)
            // stop loading animation
            emit('encounterSummaryLoader', false)
        }
    }).catch((error) => {
        console.error(error)
        emit('encounterSummaryLoader', false)
    })
}

const getConditionSummary = async() => {
    fetchingInformation.value = true;
    // clear previous response
    emit('clearConditionResponse')
    // start the loading animation
    emit('conditionSummaryLoader', true)
    await axios.get('api/llm_generation/get_summary/conditions/' + selectedPatient.value.id, {
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}`
        }
    }).then((response) => {
        if (response.data.success) {
            fetchingInformation.value = false;
            // emit value to parent component
            emit('conditionSummary', response.data.summary)
            //stop loading animation
            emit('conditionSummaryLoader', false)
        }
    }).catch((error) => {
        console.error(error)
        emit('conditionSummaryLoader', false)
    })
}

const verifyDoctorsDiagnosis = async() => {
    fetchingInformation.value = true;
    await axios.post('api/llm_generation/verify_diagnosis/', {
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}`
        },
        'patient' : {
            'first_name': selectedPatient.value.first_name,
            'age': selectedPatient.value.age,
            'gender': selectedPatient.value.gender,
            'ethnicity': selectedPatient.value.ethnicity,
        },
        'notes': appointment.value.notes,
        'symptoms': appointment.value.symptoms,
        'diagnosis': appointment.value.diagnosis,
    }).then((response) => {
        emit('emitDiagnosisVerification', response.data.result[0])
        fetchingInformation.value = false;
    }).catch((error) => {
        console.log(error)
    })
}

const verifyPrescriptionClashes = async() => {
    fetchingInformation.value = true;
    emit('emitPrescriptionClashLoader', true)
    emit('emitPrescriptionClashClear')
    await axios.post('api/llm_generation/check_ddi/', {
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}`
        },
        'patient' : selectedPatient.value.id,
        'prescription': appointment.value.prescription,
    }).then((response) => {
        console.log(response)
        emit('emitPrescriptionClash', response.data.result)
        emit('emitPrescriptionClashLoader', false)
    }).catch((error) => {
        emit('emitPrescriptionClashLoader', false)
        console.error(error)
    })
}
</script>