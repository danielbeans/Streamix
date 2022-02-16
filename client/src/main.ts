import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
<<<<<<< HEAD
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "./index.css";

createApp(App).use(store).use(router).use(ElementPlus).mount("#app");
=======

createApp(App).use(store).use(router).mount("#app");
>>>>>>> a5ee137... Scaffold Vue 3.0 and Django Streamix project.
