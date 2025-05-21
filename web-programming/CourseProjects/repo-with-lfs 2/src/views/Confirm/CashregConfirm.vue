<template>
  <h3 class="text-center fw-normal">Navbat</h3>
  <div class="row">
    <div class="col-md-4"></div>
    <div class="col-md-4 my-1"></div>
    <div class="col-md-4">
      <div class="input-group input-group-sm">
        <input
          type="search"
          id="search_queue"
          class="form-control form-control-sm"
          v-model="search"
          placeholder="Qidiruv"
          @keyup="
            $refs.info.search = search;
            $refs.info.get(1, 25);
            $store.dispatch('setloading', { loading: false });
          "
        />

        <div class="input-group-text bg-white">
          <i class="fa fa-search"></i>
        </div>
      </div>
    </div>
  </div>
  <hr />

  <div class="row">
    <div class="col"></div>
    <div class="col"></div>
    <div class="col"></div>
    <div class="col">
      <div class="input-group shadow-0">
        <input
          type="date"
          v-model="date"
          class="form-control border-primary border border-2"
          @change="
            $refs.info.date = date;
            $refs.info.get(1, 25);
          "
        />
        <button
          type="button"
          class="btn"
          :class="step == 1 ? 'btn-primary' : 'btn-outline-primary'"
          data-mdb-color="dark"
          @click="
            step = 1;
            $refs.info.step = step;
            $refs.info.get(1, 25);
          "
        >
          Kassa
        </button>
        <button
          type="button"
          class="btn"
          :class="step == 3 ? 'btn-primary' : 'btn-outline-primary'"
          data-mdb-color="dark"
          @click="
            step = 3;
            $refs.info.step = step;
            $refs.info.get(1, 25);
          "
        >
          Navbat
        </button>
      </div>
    </div>
  </div>

  <queue-info ref="info" cancel confirm print />
</template>

<script>
import QueueInfo from "@/components/Patient/QueueInfo.vue";
export default {
  components: { QueueInfo },
  name: "CashregConfirm",
  data() {
    return {
      search: "",
      step: 1,
      date: new Date().toISOString().slice(0, 10),
    };
  },
  methods: {
    format(number) {
      return String(
        "(" +
          String(number).substr(0, 2) +
          ") " +
          String(number).substr(2, 3) +
          " " +
          String(number).substr(5, 2) +
          " " +
          String(number).substr(7, 2)
      );
    },
  },
};
</script>
