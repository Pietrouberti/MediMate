<script setup>
    import { useUserStore } from '@/stores/user';
    import { useRouter } from 'vue-router';
    import { ref, onMounted } from 'vue';
    import axios from 'axios';


    // form object 
    const form = ref({
        email: '',
        password: ''
    })

    // initialise userStore
    const userStore = useUserStore();

    // errors array that gets populated during fronted validation 
    const errors = ref([]);
    const router = useRouter();

    onMounted(() => {
        // don't let authenticated users access the login page
        if(userStore.user.isAuthenticated) {
            router.push({path: '/'})
        }

    });

    // frontend simple form validation function, async added but pending for backend endpoint setup
    async function submitForm() {
        errors.value = []
        if(form.value.email === "") {
            errors.value.push('Missing email')
        }
        if(form.value.password === "") {
            errors.value.push("Missing password")
        }

        if(errors.value.length === 0) {
            await axios.post('api/doctor/login/', form.value).then((response) => {
                userStore.setToken(response.data)
                axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
                getUserDetails()
            })
            console.log("Submitted Form", form.value)
        }
    }
    async function getUserDetails() {
        await axios.get('api/doctor/get_user/').then((response) => {
            userStore.setUserInfo(response.data)
            router.push({path: '/'})
        })
    }

</script>

<template>
    <div class="form-page">
        <div class="form-container">
            <div class="form-container__text-content">
                <div class="form-container__main-content">
                    <h1 class="form-container__form-title">Login</h1>
                </div>
            </div>
            <div class="form-container__form-container">
                <form class="form-container__form" v-on:submit.prevent="submitForm">
                    <div class="form-container__form-item">
                        <label for="">Email</label><br>
                        <input type="text" placeholder="Email" class="" v-model="form.email">
                    </div>
                    <div class="form-container__form-item">
                        <label for="">Password</label><br>
                        <input type="password" placeholder="Password" class="" v-model="form.password">
                    </div>
                    <div class="form-container__error-container" v-if="errors.length > 0">
                        <p v-for="error in errors" v-bind:key="error">
                            {{error}}
                        </p>
                    </div>
                    <div class="form-container__form-item">
                        <button class="button button--primary">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>