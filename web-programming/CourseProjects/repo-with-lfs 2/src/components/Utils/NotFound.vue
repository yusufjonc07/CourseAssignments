<template>
  <div class="d-flex align-items-center justify-content-center vh-100">
    <div class="text-center">
      <h1 class="display-1 fw-bold">404</h1>
      <p class="fs-3">
        <span class="text-danger">Opps!</span> Sahifa topilmadi.
      </p>
      <p class="lead">Siz qidirayotgan sahifa mavjud emas.</p>
      <button @click="$router.go(-1)" class="btn btn-primary" :to="-1">
        <i class="fa-solid fa-left-long"></i> Ortga qaytish
      </button>
    </div>
  </div>
</template>
<script>
export default {
  name: "NotFound",
  created() {
    this.$emit("setloading", false);
  },
};
</script>
