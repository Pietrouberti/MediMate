<template>
    <div class="hero-banner">
        <div class="hero-banner__content">
          <div class="hero-banner__heading">
            <h2 class="heading heading__h1">Welcome to MediMate</h2>
            <p class="heading heading__h3">Your personal AI medical assistant</p>
          </div>
          <div class="hero-banner__subheading">
            <p class="heading heading__p">I streamline patient care by gathering medical records,<br> providing intelligent prescription suggestions, <br> and alerting you to potential prescription clashes. <br> I analyze patient history, appointment notes, <br> and other critical data to help you make informed decisions <br> faster and accurately. <br>

            </p>
            <button class="button button--primary" @click="redirect('/doctors-office')">Get Started</button>
          </div>
          <!-- <img src="/public/static/vectors.png" alt="" class="hero-banner__vector"> -->
        </div>
        <img src="/public/static/hero-banner-image.png" class="hero-banner__image">
      </div>
</template>
<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const redirect = (path) => {
    router.push(path);
}
</script>