<template>
    <div class="hero-banner">
        <div class="hero-banner__content">
          <div class="hero-banner__heading">
            <h2 class="heading heading__h1" v-if="!userStore.user.isAuthenticated">Welcome to MediMate</h2>
            <h2 class="heading heading__h1" v-if="userStore.user.isAuthenticated">Welcome {{userStore.user.name}},</h2>
            <p class="heading heading__h3">Your personal AI medical assistant</p>
          </div>
          <div class="hero-banner__subheading">
            <p class="heading heading__p" v-if="!userStore.user.isAuthenticated">I streamline patient care by gathering medical records,<br> providing intelligent prescription suggestions, <br> and alerting you to potential prescription clashes. <br> I analyze patient history, appointment notes, <br> and other critical data to help you make informed decisions <br> faster and accurately. <br>
            </p>
            <p class="heading heading__p" v-if="userStore.user.isAuthenticated">Enter your doctors office to get started with MediMate</p>
            <button class="button button--primary" v-if="!userStore.user.isAuthenticated" @click="redirect('/doctors-office')">Get Started</button>
            <button class="button button--primary" v-if="userStore.user.isAuthenticated" @click="redirect('/doctors-office')">Doctors Office</button>
          </div>
          <!-- <img src="/public/static/vectors.png" alt="" class="hero-banner__vector"> -->
        </div>
        <img src="/public/static/hero-banner-image.png" class="hero-banner__image">
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