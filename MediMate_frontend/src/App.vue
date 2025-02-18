<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted } from 'vue';

import NavigationBar from './components/NavigationBar.vue';


</script>

<template>
  <NavigationBar />
  <RouterView />
</template>

