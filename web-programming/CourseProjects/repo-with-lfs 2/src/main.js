import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/index";
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";
import "./libraries/MDB5-STANDARD-UI-KIT-Free-6.1.0/js/mdb.min.js";
import util from "./components/Utils/util";

const app = createApp(App);

app.config.globalProperties.$util = util;
app.use(router).use(store).component("multiselect", Multiselect).mount("#app");
