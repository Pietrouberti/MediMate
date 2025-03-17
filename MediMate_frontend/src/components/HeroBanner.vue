<template>
    <div class="hero-banner">
        <div class="hero-banner__content">
          <div class="hero-banner__heading">
            <h2 class="heading heading__h1" v-if="!userStore.user.isAuthenticated">Welcome to <span style="color: rgba(0, 123, 255, 0.8); font-weight: 600">MediMate</span></h2>
            <h2 class="heading heading__h1" v-if="userStore.user.isAuthenticated">Welcome <span style="color: rgba(0, 123, 255, 0.8); font-weight: 600">{{userStore.user.name}},</span></h2>
            <p class="heading heading__h3">Get Started with MediMate</p>
          </div>
          <div class="hero-banner__subheading">
            <p class="heading heading__h4" v-if="!userStore.user.isAuthenticated">Agent for EHR Summarisation, Prescription Clash Detection <br> and Diagnosis Validation
            </p>
            <p class="heading heading__p" v-if="userStore.user.isAuthenticated">Enter your doctor's office</p>
            <button class="button button--primary" v-if="!userStore.user.isAuthenticated" @click="redirect('/doctors-office')">Get Started</button>
            <button class="button button--primary" v-if="userStore.user.isAuthenticated" @click="redirect('/doctors-office')">Doctors Office</button>
          </div>
          <!-- <img src="/public/static/vectors.png" alt="" class="hero-banner__vector"> -->
        </div>
        <img src="/static/hero-banner-image.png" class="hero-banner__image">
      </div>
</template>
<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

// initialise vue router
const router = useRouter();

// initialise user store
const userStore = useUserStore();

// redirect helper function 
const redirect = (path) => {
    router.push(path);
}
</script>