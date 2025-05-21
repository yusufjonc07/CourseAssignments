<template>
  <button
    type="button"
    class="btn btn_dark btn-floating"
    @click="nightMode = !nightMode"
  >
    <i class="fa-solid fa-moon text-white" id="icon"></i>
  </button>
</template>

<script>
export default {
  name: "DarkMode",
  data() {
    return {
      nightMode: localStorage.getItem("nightMode"),
    };
  },
  watch: {
    nightMode() {
      if (this.nightMode == true) {
        localStorage.setItem("nightMode", JSON.stringify(this.nightMode));
        document.querySelector("#app").classList.remove("dark");
        document.querySelector("#icon").classList.remove("fa-sun");
        document.querySelector("#icon").classList.add("fa-moon");
        document.querySelector("#icon").classList.remove("text-warning");
        document.querySelector("#icon").classList.add("text-white");
      } else if (this.nightMode == false) {
        localStorage.setItem("nightMode", JSON.stringify(this.nightMode));
        document.querySelector("#app").classList.add("dark");
        document.querySelector("#icon").classList.remove("fa-moon");
        document.querySelector("#icon").classList.add("fa-sun");
        document.querySelector("#icon").classList.remove("text-white");
        document.querySelector("#icon").classList.add("text-warning");
      }
    },
  },
  created() {
    this.nightMode = JSON.parse(localStorage.getItem("nightMode"));
  },
  mounted() {
    if (this.nightMode == true) {
      document.querySelector("#icon").classList.remove("fa-sun");
      document.querySelector("#icon").classList.add("fa-moon");
      document.querySelector("#icon").classList.remove("text-warning");
      document.querySelector("#icon").classList.add("text-white");
    } else if (this.nightMode == false) {
      document.querySelector("#icon").classList.remove("fa-moon");
      document.querySelector("#icon").classList.add("fa-sun");
      document.querySelector("#icon").classList.remove("text-white");
      document.querySelector("#icon").classList.add("text-warning");
    }
  },
};
</script>

<!-- <style lang="scss" scoped>
</style> -->