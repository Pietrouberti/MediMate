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
        <div class="office__filter-container">
            <div class="office__filter-container-item">
                <label for="checkbox">Retrieve Past Patient Summaries:</label>
                <input type="checkbox" class="office__filter-checkbox" v-model="useMediMateCache"/>
            </div>
            <div class="office__filter-container-item">
                <label for="checkbox">Show Evaluation Metrics:</label>
                <input type="checkbox" class="office__filter-checkbox" v-model="showMetrics"/>
            </div>
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
                <label for="notes">Medical Record Type</label>
                <select class="office__notes-area office__notes-area--select" name="" id="" v-model="medicalRecordType">
                    <option value=""></option>
                    <option value="encounters_collection">Encounter</option>
                    <option value="medications_collection">Medication</option>
                    <option value="allergy_collection">Allergy</option>
                    <option value="conditions_collections">Condition</option>
                </select>
            </div>
        </div>
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
            <div class="office__grid-input-item">
                <label for="Diagnosis">Appointment Type</label>
                <select type="text" id="diagnosis" class="office__grid-input" placeholder="" v-model="appointment.encounterType">
                    <option value=""></option>
                    <option v-for="item in encounterTypes" :key="item" :value="`${item}`">{{item}}</option>
                </select>
            </div>
        </div>
        <div class="office__patient-info">
            <div class="office__grid-input-item" v-for="item in selectedMedicalRecordType" :key="item">
                <label>{{item.label}}</label>
                <input :type="`${item.type}`" class="office__grid-input" :placeholder="`${item.placeholder}`" v-model="appointment[item.name]"/>
            </div>
        </div>
        <div class="office__cta">
            <button class="button button--form" @click="verifyDoctorsDiagnosis" :disabled="appointment.diagnosis == null || appointment.symptoms == null || appointment.notes == null || selectedPatient.id == null">Verify diagnosis prediction</button>
            <button class="button button--form" @click="verifyPrescriptionClashes">Check for Prescription Clashes</button>
            <button class="button button--form" @click="generateRecord">Generate New EHR</button>
        </div>
    </div>
</template>
<script setup>
// vue imports
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useMediMateOutputStore } from '@/stores/medimate-output-store';

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
    'emitPrescriptionClashClear',
    'emitEvaluationMetrics',
    'success'
])

const fetchingInformation = ref(false);

const userStore = useUserStore();
const mediMateStore = useMediMateOutputStore();
const useMediMateCache = ref(false);
const showMetrics = ref(false);

const patients = ref([])
const allergyKeys = ref()
const conditionKeys = ref()
const encounterKeys = ref()
const medicationKeys = ref()
const medicalRecordType = ref('')
const encounterTypes = ref()

onMounted(async() => {
    await getPatientList();
    await getVectorDBKeys();
    mediMateStore.initStore();
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

const getVectorDBKeys = async() => {
    await axios.get('api/llm_generation/get_vectordb_keys', {
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}`
        }
    }).then((response) => {
        if (response.data.success == true) {
            allergyKeys.value = response.data.allergy
            conditionKeys.value = response.data.conditions
            encounterKeys.value = response.data.encounters
            medicationKeys.value = response.data.medications
            encounterTypes.value = response.data.encounters_class
        }
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
    encounterType: null,
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

const selectedMedicalRecordType = computed(() => {
    appointment.value = {
        notes: null,
        symptoms: null,
        diagnosis: null,
        encounterType: null,
    }

    if (medicalRecordType.value == "allergy_collection") {
        return allergyKeys.value
    } 
    if (medicalRecordType.value == "conditions_collections") {
        return conditionKeys.value
    }
    if (medicalRecordType.value == "encounters_collection") {
        return encounterKeys.value
    }
    if (medicalRecordType.value == "medications_collection") {
        return medicationKeys.value
    }

})

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

const emitSummaryEvaluationMetrics = (data) => {
    emit('emitEvaluationMetrics', data)
}

// get a summary of patient medication
const getMedicationSummary = async() => {
    // clear previous repsonses
    emit('clearMedicationResponse')
    emit('medicationSummaryLoader', true)
    // start the loading animation
    const isPatientCached = mediMateStore.doesPatientExist(selectedPatient.value.id, 'medications');
    if(useMediMateCache.value && isPatientCached) {
        const response = mediMateStore.fetchPatientRecord(selectedPatient.value.id, 'medications')
        setTimeout(() => {
            emit('medicationSummary', response.output);
            emit('medicationSummaryLoader', false);
            if (showMetrics.value) {
                emitSummaryEvaluationMetrics(response.output.metric)
            }
        }, 3000);    
    }
    if(!useMediMateCache.value || !isPatientCached) {
        fetchingInformation.value = true;
        await axios.get('api/llm_generation/get_summary/medication/' + selectedPatient.value.id + '/' + showMetrics.value, {
            headers: {
                'Authorization': `Bearer ${userStore.user.accessToken}`
            }
        }).then((response) => {
            if (response.data.success) {
                fetchingInformation.value = false;
                console.log(response.data);
                // emit value of the medication summary to the parent component
                mediMateStore.createMediMateSessionOutput(selectedPatient.value.id,'medications', response.data.summary);
                emit('medicationSummary', response.data.summary)
                if(showMetrics.value) {
                    emitSummaryEvaluationMetrics(response.data.evaluation)
                }
                // notify parent component to stop loading animation
                emit('medicationSummaryLoader', false)
            }
        }).catch((error) => {
            console.error(error)
            emit('medicationSummaryLoader', false)
        })
    }
}

const getAllergySummary = async() => {
    // clear previous repsonses
    emit('clearAllergyResponse')
    // start loading animation to provide user feedback
    emit('allergySummaryLoader', true)

    const isPatientCached = mediMateStore.doesPatientExist(selectedPatient.value.id, 'allergy')
    if(useMediMateCache.value && isPatientCached) {
        const response = mediMateStore.fetchPatientRecord(selectedPatient.value.id, 'allergy')
        setTimeout(() => {
            emit('allergySummary', response.output);
            emit('allergySummaryLoader', false);
            if (showMetrics.value) {
                emitSummaryEvaluationMetrics(response.output.metric)
            }
        }, 3000);
    }
    if(!useMediMateCache.value || !isPatientCached) {
        fetchingInformation.value = true;
        await axios.get('api/llm_generation/get_summary/allergy/' + selectedPatient.value.id + '/' + showMetrics.value, {
            headers: {
                'Authorization': `Bearer ${userStore.user.accessToken}` 
            }
        }).then((response) => {
            if(response.data.success) {
                fetchingInformation.value = false;
                // emit summary to parent component
                console.log(response.data.summary);
                mediMateStore.createMediMateSessionOutput(selectedPatient.value.id,'allergy', response.data.summary);
                emit('allergySummary', response.data.summary);
                if(showMetrics.value) {
                    emitSummaryEvaluationMetrics(response.data.evaluation)
                }
                // stop the loading animation
                emit('allergySummaryLoader', false);
            }
        }).catch((error) => {
            console.error(error)
            emit('allergySummaryLoader', false);
        })
    }
}

// get a summary of patient previous encounters
const getEncounterSummary = async() => {
    emit('clearEncounterResponse')
    // start the loading animation
    emit('encounterSummaryLoader', true)
    const isPatientCached = mediMateStore.doesPatientExist(selectedPatient.value.id, 'encounters')
    // clear previous repsonses
    console.log(isPatientCached)
    if(useMediMateCache.value && isPatientCached) {
        const response = mediMateStore.fetchPatientRecord(selectedPatient.value.id, 'encounters')
        setTimeout(() => {
            emit('encounterSummary', response.output);
            emit('encounterSummaryLoader', false);
            if (showMetrics.value) {
                emitSummaryEvaluationMetrics(response.output.metric)
            }
        }, 3000);
    }
    if (!useMediMateCache.value || !isPatientCached) {
        fetchingInformation.value = true;
        await axios.get('api/llm_generation/get_summary/encounters/' + selectedPatient.value.id + '/' + showMetrics.value,{
            headers: {
                'Authorization': `Bearer ${userStore.user.accessToken}`
            }
        }).then((response) => {
            if(response.data.success) {
                fetchingInformation.value = false;
                // emit value to parent component
                console.log(response.data);
                mediMateStore.createMediMateSessionOutput(selectedPatient.value.id,'encounters', response.data.summary);
                emit('encounterSummary', response.data.summary)
                if(showMetrics.value) {
                    emitSummaryEvaluationMetrics(response.data.evaluation)
                }
                // stop loading animation
                emit('encounterSummaryLoader', false)
            }
        }).catch((error) => {
            console.error(error)
            emit('encounterSummaryLoader', false)
        })
    }



}

const getConditionSummary = async() => {
    // clear previous response
    emit('clearConditionResponse')
    // start the loading animation
    emit('conditionSummaryLoader', true)
    const isPatientCached = mediMateStore.doesPatientExist(selectedPatient.value.id, 'conditions')
    if(useMediMateCache.value && isPatientCached) {
        const response = mediMateStore.fetchPatientRecord(selectedPatient.value.id, 'conditions')
        setTimeout(() => {
            emit('conditionSummary', response.output);
            emit('conditionSummaryLoader', false);
            if (showMetrics.value) {
                emitSummaryEvaluationMetrics(response.output.metric)
            }
        }, 3000);
    }
    if(!useMediMateCache.value || !isPatientCached) {
        fetchingInformation.value = true;
        await axios.get('api/llm_generation/get_summary/conditions/' + selectedPatient.value.id + '/' + showMetrics.value, {
            headers: {
                'Authorization': `Bearer ${userStore.user.accessToken}`
            }
        }).then((response) => {
            if (response.data.success) {
                fetchingInformation.value = false;
                // emit value to parent component
                console.log(response.data.summary);
                mediMateStore.createMediMateSessionOutput(selectedPatient.value.id,'conditions', response.data.summary);
                emit('conditionSummary', response.data.summary)
                if(showMetrics.value) {
                    emitSummaryEvaluationMetrics(response.data.evaluation)
                }
                //stop loading animation
                emit('conditionSummaryLoader', false)
            }
        }).catch((error) => {
            console.error(error)
            emit('conditionSummaryLoader', false)
        })
    }
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
        'prescription': appointment.value.PRESCRIPTION_NAME,
    }).then((response) => {
        fetchingInformation.value = false;
        console.log(response)
        emit('emitPrescriptionClash', response.data.result)
        emit('emitPrescriptionClashLoader', false)
    }).catch((error) => {
        fetchingInformation.value = false;
        emit('emitPrescriptionClashLoader', false)
        console.error(error)
    })
}

const generateRecord = async() => {
    console.log(appointment.value)
    fetchingInformation.value = true;
    await axios.post('api/llm_generation/create_record/'+ selectedPatient.value.id + '/' + medicalRecordType.value, {
        headers: {
            'Authorization': `Bearer ${userStore.user.accessToken}`
        },
        'body': appointment.value,
    }).then((response) => {
        console.log(response)
        fetchingInformation.value = false;
        emit('success', 'Record has been added to ' +selectedPatient.value.first_name+ ' EHR')
    }).catch((error) => {
        console.error(error)
        fetchingInformation.value = false;
        emit('success', 'Record has been added to ' +selectedPatient.first_name+ ' EHR')
    })
    console.log(appointment.value)
}
</script>