<template></template>

<script>
export default {
  name: "Home",
  mounted() {
    this.$store.dispatch("setloading", { loading: false });
  },
};
</script>
