<template>
    <div class="office__title-container">
        <h2 class="heading heading__h3">Appointment Notepad</h2>
    </div>
    <div class="office__input-item">
        <label for="patient_search">Find Patient</label>
        <input type="text" class="office__input" v-model="searchQuery" placeholder="Search for a patient" @focus="showDropdown = true" @blur="hideDropdown" />
        <ul v-if="showDropdown && filteredPatients.length" class="office__dropdown">
            <li v-for="patient in filteredPatients" :key="patient.id" @mousedown.prevent="selectPatient(patient)">
                {{ patient.firstName }} {{ patient.lastName }}
            </li>
        </ul>
    </div>
    <div class="office__title-container">
        <h2 class="heading heading__h4">Patient Information</h2>
    </div>
    <div class="office__patient-info">
        <div class="office__grid-input-item">
            <label for="firstName">First Name</label>
            <input type="text" id="firstName" class="office__grid-input" v-model="selectedPatient.firstName" placeholder="First Name" />
        </div>
        <div class="office__grid-input-item">
            <label for="lastName">Last Name</label>
            <input type="text" id="lastName" class="office__grid-input" v-model="selectedPatient.lastName" placeholder="Last Name" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="age">Age</label>
            <input type="text" id="age" class="office__grid-input" v-model="selectedPatient.age" placeholder="Age" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="gender">Gender</label>
            <input type="text" id="gender" class="office__grid-input" v-model="selectedPatient.gender" placeholder="Gender" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="ethnicity">Ethnicity</label>
            <input type="text" id="ethnicity" class="office__grid-input" v-model="selectedPatient.ethnicity" placeholder="Ethnicity" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="NHSID">NHS ID</label>
            <input type="text" id="NHSID" class="office__grid-input" v-model="selectedPatient.NHSID" placeholder="NHS ID" />
        </div>
        
        <div class="office__grid-input-item">
            <label for="address">Address</label>
            <input type="text" id="address" class="office__grid-input" v-model="selectedPatient.address" placeholder="Address" />
        </div>
    </div>
    <div class="office__title-container">
        <h4 class="heading heading__h4">Appointment Notes</h4>
    </div>
    <div class="office__appointment-notes">
        <div class="office__patient-info">
            <div class="office__grid-input-item">
                <label for="notes">Appointment Notes</label>
                <textarea class="office__notes-area" name="notes" id="notes" placeholder="Appointment Notes"></textarea>
            </div>
        </div>
        <div class="office__patient-info">
            <div class="office__grid-input-item">
                <label for="Symptoms">Symptoms</label>
                <input type="text" id="symptoms" class="office__grid-input" placeholder="Patient symptoms" />
            </div>
            <div class="office__grid-input-item">
                <label for="Diagnosis">Diagnosis</label>
                <input type="text" id="diagnosis" class="office__grid-input" placeholder="Diagnosis prediction" />
            </div>
        </div>
        <div class="office__patient-info">
            <div class="office__grid-input-item">
                <label for="prescription-name">Prescription Name</label>
                <input type="text" id="prescription-name" class="office__grid-input" placeholder="Name of prescription" />
            </div>
            <div class="office__grid-input-item">
                <label for="prescription-dosage">Prescription Dosage</label>
                <input type="text" id="prescription-dosage" class="office__grid-input" placeholder="Prescription dosage" />
            </div>
        </div>
        <div class="office__patient-info">
            <div class="office__grid-input-item">
                <label for="prescription-start">Prescription Start Date</label>
                <input type="date" id="prescription-start" class="office__grid-input"/>
            </div>
            <div class="office__grid-input-item">
                <label for="prescription-start">Prescription End Date</label>
                <input type="date" id="prescription-start" class="office__grid-input"/>
            </div>
        </div>
        <div class="office__cta">
            <button class="button button--form">Generate Medical Record</button>
            <button class="button button--form">Check for prescription clash</button>
            <button class="button button--form">Update Medical Record</button>
        </div>
    </div>
</template>
<script setup>
// vue imports
import { ref, computed } from 'vue';


// dummy patients object just to test proxy varible functionality
const patients = ref([
    {
        firstName: 'John',
        lastName: 'Doe',
        id: '123456',
        age: 45,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS123456',
        address: '123 Main St, Anytown, AT 12345'
    },
    {
        firstName: 'Jane',
        lastName: 'Doe',
        id: '654321',
        age: 38,
        gender: 'Female',
        ethnicity: 'Caucasian',
        NHSID: 'NHS654321',
        address: '456 Elm St, Othertown, OT 65432'
    },
    { 
        firstName: 'John',
        lastName: 'Smith',
        id: '987654',
        age: 50,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS987654',
        address: '789 Oak St, Sometown, ST 98765'
    },
    {
        firstName: 'Jane',
        lastName: 'Smith',
        id: '456789',
        age: 42,
        gender: 'Female',
        ethnicity: 'Caucasian',
        NHSID: 'NHS456789',
        address: '321 Pine St, Anycity, AC 45678'
    },
    {
        firstName: 'Alice',
        lastName: 'Johnson',
        id: '112233',
        age: 30,
        gender: 'Female',
        ethnicity: 'African American',
        NHSID: 'NHS112233',
        address: '654 Maple St, Newtown, NT 11223'
    },
    {
        firstName: 'Bob',
        lastName: 'Brown',
        id: '223344',
        age: 55,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS223344',
        address: '987 Birch St, Oldtown, OT 22334'
    },
    {
        firstName: 'Charlie',
        lastName: 'Davis',
        id: '334455',
        age: 28,
        gender: 'Male',
        ethnicity: 'Hispanic',
        NHSID: 'NHS334455',
        address: '123 Cedar St, Smalltown, ST 33445'
    },
    {
        firstName: 'Diana',
        lastName: 'Evans',
        id: '445566',
        age: 35,
        gender: 'Female',
        ethnicity: 'Asian',
        NHSID: 'NHS445566',
        address: '456 Spruce St, Bigcity, BC 44556'
    },
    {
        firstName: 'Eve',
        lastName: 'Foster',
        id: '556677',
        age: 40,
        gender: 'Female',
        ethnicity: 'Caucasian',
        NHSID: 'NHS556677',
        address: '789 Willow St, Uptown, UT 55667'
    },
    {
        firstName: 'Frank',
        lastName: 'Green',
        id: '667788',
        age: 60,
        gender: 'Male',
        ethnicity: 'African American',
        NHSID: 'NHS667788',
        address: '321 Ash St, Downtown, DT 66778'
    },
    {
        firstName: 'Grace',
        lastName: 'Harris',
        id: '778899',
        age: 25,
        gender: 'Female',
        ethnicity: 'Hispanic',
        NHSID: 'NHS778899',
        address: '654 Fir St, Midtown, MT 77889'
    },
    {
        firstName: 'Hank',
        lastName: 'Irving',
        id: '889900',
        age: 48,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS889900',
        address: '987 Poplar St, Suburbia, SB 88990'
    },
    {
        firstName: 'Ivy',
        lastName: 'Johnson',
        id: '990011',
        age: 32,
        gender: 'Female',
        ethnicity: 'African American',
        NHSID: 'NHS990011',
        address: '123 Redwood St, Countryside, CS 99001'
    },
    {
        firstName: 'Jack',
        lastName: 'King',
        id: '101112',
        age: 29,
        gender: 'Male',
        ethnicity: 'Asian',
        NHSID: 'NHS101112',
        address: '456 Sequoia St, Metropolis, MP 10111'
    },
    {
        firstName: 'Karen',
        lastName: 'Lee',
        id: '121314',
        age: 36,
        gender: 'Female',
        ethnicity: 'Asian',
        NHSID: 'NHS121314',
        address: '789 Cypress St, Village, VG 12131'
    },
    {
        firstName: 'Leo',
        lastName: 'Martin',
        id: '141516',
        age: 52,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS141516',
        address: '321 Palm St, Hamlet, HT 14151'
    },
    {
        firstName: 'Mona',
        lastName: 'Nelson',
        id: '161718',
        age: 27,
        gender: 'Female',
        ethnicity: 'Hispanic',
        NHSID: 'NHS161718',
        address: '654 Bamboo St, Borough, BR 16171'
    },
    {
        firstName: 'Nina',
        lastName: 'Owens',
        id: '181920',
        age: 33,
        gender: 'Female',
        ethnicity: 'Caucasian',
        NHSID: 'NHS181920',
        address: '987 Pineapple St, District, DT 18191'
    },
    {
        firstName: 'Oscar',
        lastName: 'Perez',
        id: '202122',
        age: 41,
        gender: 'Male',
        ethnicity: 'Hispanic',
        NHSID: 'NHS202122',
        address: '123 Coconut St, Region, RG 20212'
    },
    {
        firstName: 'Paul',
        lastName: 'Quinn',
        id: '222324',
        age: 39,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS222324',
        address: '456 Mango St, Province, PV 22232'
    },
    {
        firstName: 'Quincy',
        lastName: 'Roberts',
        id: '242526',
        age: 47,
        gender: 'Male',
        ethnicity: 'African American',
        NHSID: 'NHS242526',
        address: '789 Papaya St, Territory, TY 24252'
    },
    {
        firstName: 'Rachel',
        lastName: 'Smith',
        id: '262728',
        age: 34,
        gender: 'Female',
        ethnicity: 'Caucasian',
        NHSID: 'NHS262728',
        address: '321 Guava St, Zone, ZN 26272'
    },
    {
        firstName: 'Sam',
        lastName: 'Taylor',
        id: '282930',
        age: 43,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS282930',
        address: '654 Kiwi St, Sector, SC 28293'
    },
    {
        firstName: 'Tina',
        lastName: 'Underwood',
        id: '303132',
        age: 37,
        gender: 'Female',
        ethnicity: 'Asian',
        NHSID: 'NHS303132',
        address: '987 Lychee St, Division, DV 30313'
    },
    {
        firstName: 'Uma',
        lastName: 'Vance',
        id: '323334',
        age: 31,
        gender: 'Female',
        ethnicity: 'African American',
        NHSID: 'NHS323334',
        address: '123 Durian St, Area, AR 32333'
    },
    {
        firstName: 'Victor',
        lastName: 'White',
        id: '343536',
        age: 49,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS343536',
        address: '456 Rambutan St, Locale, LC 34353'
    },
    {
        firstName: 'Wendy',
        lastName: 'Xander',
        id: '363738',
        age: 26,
        gender: 'Female',
        ethnicity: 'Hispanic',
        NHSID: 'NHS363738',
        address: '789 Mangosteen St, Quarter, QT 36373'
    },
    {
        firstName: 'Xander',
        lastName: 'Young',
        id: '383940',
        age: 44,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS383940',
        address: '321 Jackfruit St, Sector, SC 38393'
    },
    {
        firstName: 'Yara',
        lastName: 'Zane',
        id: '404142',
        age: 29,
        gender: 'Female',
        ethnicity: 'African American',
        NHSID: 'NHS404142',
        address: '654 Longan St, Region, RG 40414'
    },
    {
        firstName: 'Zane',
        lastName: 'Adams',
        id: '424344',
        age: 53,
        gender: 'Male',
        ethnicity: 'Caucasian',
        NHSID: 'NHS424344',
        address: '987 Lychee St, Division, DV 42434'
    }
]);


// selected patient object
const selectedPatient = ref({
    firstName: null,
    lastName: null,
    age: null,
    gender: null,
    ethnicity: null,
    NHSID: null,
    address: null,
});


// search patient v-model proxy varible
const searchQuery = ref('');

// boolean to show/hide dropdown
const showDropdown = ref(false);


// filter patient list based on search query
const filteredPatients = computed(() => {
    console.log(searchQuery.value);
    return patients.value.filter(patient => 
        patient.firstName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        patient.lastName.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});


// select patient from dropdown
const selectPatient = (patient) => {
    searchQuery.value = patient.firstName + ' ' + patient.lastName;
    selectedPatient.value = patient;
    console.log("Test time",selectedPatient.value);
    showDropdown.value = false;
};

// hide dropdown after 200ms for smoother transition and silky UX
const hideDropdown = () => {
    setTimeout(() => {
        showDropdown.value = false;
    }, 200);
};
</script>