<template>
  <Login
    v-if="$route.name == 'login'"
    @contextmenu="(e) => e.preventDefault()"
  />
  <div v-if="$route.name !== 'login'" @contextmenu="(e) => e.preventDefault()">
    <Navbar v-if="$route.name != 'notFound' && $route.name != 'navbat'" />
    <div
      id="main-container"
      :style="
        $route.name == 'notFound' || $route.name == 'navbat'
          ? 'height: 100vh'
          : ''
      "
      class="container-fluid p-2 responsive-y"
    >
      <div
        id="main-card"
        class="p-1 responsive-y"
        :class="
          $route.name != 'settings' &&
          $route.name != 'navbat' &&
          $route.name != 'patient'
            ? 'card shadow'
            : ''
        "
      >
        <button
          @click="back()"
          class="btn btn-sm btn-outline-secondary btn-back"
          v-if="$route.meta.iscomponent"
        >
          <i class="fa fa-arrow-left"></i>
        </button>
        <Router-view />
      </div>
    </div>
  </div>
  <Loading v-if="loading" key="0" />
</template>

<script>
import Loading from "@/components/Utils/Loading.vue";
import Navbar from "@/components/Utils/Header.vue";
import Login from "./views/Login/Login.vue";
export default {
  name: "App",
  components: { Login, Navbar, Loading, Navbar, Loading },
  data() {
    return {
      nightMode: localStorage.getItem("nightMode"),
    };
  },
  watch: {
    $route(to) {
      document.title = `Klinika - ${to.meta.title}`;
    },
  },
  created() {
    this.nightMode = JSON.parse(localStorage.getItem("nightMode"));
    if (this.nightMode == true) {
      localStorage.setItem("nightMode", this.nightMode);
      document.querySelector("#app").classList.remove("dark");
    } else if (this.nightMode == false) {
      localStorage.setItem("nightMode", this.nightMode);
      document.querySelector("#app").classList.add("dark");
    }
  },
  methods: {
    back() {
      this.$router.go(-1);
    },
  },
  computed: {
    loading() {
      return this.$store.state.loading.loading;
    },
  },
};
</script>

<style>
@import url("./components/Style/main.css");
</style>
