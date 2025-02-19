<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted , ref} from 'vue';
import { useUserPreferenceStore } from './stores/user-preferences';
import NavigationBar from './components/NavigationBar.vue';

import { watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const overflow = ref(null);
const height = ref(null)
watch(
  () => route.path,
  (newPath) => {
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
  <NavigationBar />
  <div class="main" :style="`--overflow: ${overflow}; --height: ${height}`">
    <RouterView />
  </div> 
</template>

