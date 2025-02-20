<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted , ref} from 'vue';
import { useUserStore } from '@/stores/user';
import NavigationBar from './components/NavigationBar.vue';

import { watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const overflow = ref(null);
const height = ref(null)
const userStore = useUserStore();


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
  <!-- navigation bar component -->
  <NavigationBar />
  <div class="main" :style="`--overflow: ${overflow}; --height: ${height}`">
    <!-- where page contents is rendered after a url change -->
    <RouterView />
  </div> 
</template>

