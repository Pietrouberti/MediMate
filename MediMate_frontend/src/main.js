import './assets/main.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";

library.add(fas);
axios.defaults.baseURL = "http://127.0.0.1:8000";

const app = createApp(App)
app.component("font-awesome-icon", FontAwesomeIcon);
app.use(createPinia())
app.use(router)

app.mount('#app')
