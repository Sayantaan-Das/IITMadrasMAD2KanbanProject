import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'



const front=createApp(App);
front.use(router);
front.mount('#app');