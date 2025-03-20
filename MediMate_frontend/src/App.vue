<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted , ref} from 'vue';
import { useUserStore } from '@/stores/user';
import NavigationBar from './components/NavigationBar.vue';
import Alert from './components/Alert.vue';

import { watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const overflow = ref(null);
const height = ref(null)
const userStore = useUserStore();
const alertList = ref([])



const removeAlertFromArray = (id) => {
  alertList.value.splice(id, 1)
}

const handleDiagnosisVerificationEmit = (data) => {
  let dangerColour = '';
  let serverity = '';
  let message = '';
  if (data.label === "LABEL_1") {
    dangerColour = '#43bb2b';
    serverity = '';
    message = 'MediMate System is ' + (data.score * 100).toFixed(5) + '% confident that the diagnosis is correct';
  }
  else {
    dangerColour = '#fc4040';
    serverity = '';
    message = 'MediMate System is ' + (data.score * 100).toFixed(5) + '% confident that the diagnosis is incorrect';
  }
  alertList.value.push({'dangerColour': dangerColour, 'serverity': serverity, 'message': message, 'messageType': 'diagnosis_alert'})
}

onMounted(() => {
  userStore.initStore();
  if (userStore.token) {
    userStore.getUserInfo();
  }
})

// vue watcher function to alter the overflow property of the body tag, depending on url
watch(() => route.path, (newPath) => {
    if (newPath === '/doctors-office') {
      document.body.style.overflow = 'auto'
      height.value = 'auto'
    } else {
      document.body.style.overflow = 'hidden'
      height.value = '100vh';
    }
  },
  { immediate: true }
);



</script>

<template>

  <Alert 
  v-for="item, index in alertList" v-bind:key="item" 
  :dangerColour="item.dangerColour" 
  :serverity="item.serverity" 
  :message="item.message" 
  :messageCount="index"
  :messageType="item.messageType"
  @deleteAlertEmit="removeAlertFromArray"
  />
  <!-- navigation bar component -->
  <NavigationBar />
  <div class="main" :style="`--overflow: ${overflow}; --height: ${height}`">
    <!-- where page contents is rendered after a url change -->
    <RouterView @diagnosisVerification="handleDiagnosisVerificationEmit" />
  </div> 
</template>

