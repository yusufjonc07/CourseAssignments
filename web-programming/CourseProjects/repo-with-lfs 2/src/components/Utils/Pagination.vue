<template>
  <nav>
    <ul class="pagination my-1 justify-content-center align-items-center">
      <li class="page-item">
        <button class="page-link" @click="get(page, limited)">
          <i class="fa-solid fa-rotate"></i>
        </button>
      </li>
      <li class="page-item">
        <button
          class="page-link"
          :disabled="page == 1"
          @click="get(1, limited)"
        >
          <i class="fa-solid fa-angle-double-left"></i>
        </button>
      </li>
      <li class="page-item">
        <button
          class="page-link"
          :disabled="page == 1"
          @click="get(page - 1, limited)"
        >
          <i class="fa-solid fa-angle-left"></i>
        </button>
      </li>
      <li class="page-item" v-if="page - 2 > 0" @click="get(page - 2, limited)">
        <button class="page-link">
          {{ page - 2 }}
        </button>
      </li>
      <li class="page-item" v-if="page - 1 > 0" @click="get(page - 1, limited)">
        <button class="page-link">
          {{ page - 1 }}
        </button>
      </li>
      <li class="page-item active">
        <button class="page-link">
          {{ page }}
        </button>
      </li>
      <li class="page-item">
        <button
          class="page-link"
          v-if="page + 1 <= pages"
          @click="get(page + 1, limited)"
        >
          {{ page + 1 }}
        </button>
      </li>
      <li class="page-item">
        <button
          class="page-link"
          v-if="page + 2 <= pages"
          @click="get(page + 2, limited)"
        >
          {{ page + 2 }}
        </button>
      </li>
      <li class="page-item">
        <button
          class="page-link"
          :disabled="page == pages || !pages"
          @click="get(page + 1, limited)"
        >
          <i class="fa-solid fa-angle-right"></i>
        </button>
      </li>
      <li class="page-item">
        <button
          class="page-link"
          :disabled="page == pages || !pages"
          @click="get(pages, limited)"
        >
          <i class="fa-solid fa-angle-double-right"></i>
        </button>
      </li>
      <li class="page-item mx-1">
        <select
          class="form-select form-select-sm"
          v-model="limited"
          @change="get(1, limited)"
        >
          <option disabled value="">limit</option>
          <option value="25">25</option>
          <option value="50">50</option>
          <option value="100">100</option>
          <option value="10000">barchasi</option>
        </select>
      </li>
      <li class="page-item" v-if="$props.attr">
        <button
          @click="$util.exportToExcel(attr)"
          class="btn btn-sm btn-success"
        >
          <i class="fa-regular fa-file-excel"></i>
        </button>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "Pagination",
  props: ["page", "pages", "limit", "attr"],
  emits: ["get"],
  data() {
    return {
      limited: this.limit,
    };
  },
  methods: {
    get(page, limit) {
      this.$emit("get", page, limit);
    },
  },
};
</script>

<style scoped>
@media (max-width: 456px) {
  nav {
    zoom: 75%;
  }
}
</style>
