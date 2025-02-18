<script setup>
    import { useRouter } from 'vue-router';
    import { ref } from 'vue';
    const form = ref({
        email: '',
        password: ''
    })
    const errors = ref([]);

    async function submitForm() {
        errors.value = []
        if(form.value.email === "") {
            errors.value.push('Missing email')
        }
        if(form.value.password === "") {
            errors.value.push("Missing password")
        }

        if(errors.value.length === 0) {
            //axios request
            console.log("Submitted Form", form.value)
        }
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