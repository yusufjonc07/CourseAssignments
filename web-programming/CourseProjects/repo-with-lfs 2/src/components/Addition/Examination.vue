<template>
  <div class="card">
    <div class="card-body">
      <h5 class="text-center">Ko'rik vaqti</h5>
      <form @submit.prevent="update_minute(time)">
        <div class="row gap-6 d-flex justify-content-center">
          <div class="col-md-6">
            <label class="form-label" for="time">Ko'rik vaqti</label>
            <div class="input-group">
              <input
                type="number"
                min="0"
                step="any"
                id="time"
                class="form-control"
                v-model="time"
                required
              />
              <span class="input-group-text">minut</span>
              <button type="submit" class="btn btn-secondary">
                <i class="fa-solid fa-circle-check" v-if="!loading"></i>
                <div
                  class="spinner-border spinner-border-sm mx-1"
                  role="status"
                  v-else
                >
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import {
  catchError,
  current_user,
  disabled,
  minute_update,
  success,
} from "../Utils/api";
export default {
  name: "Examination",
  data() {
    return {
      time: null,
      loading: false,
    };
  },
  methods: {
    get() {
      this.$store.dispatch("setloading", { loading: true });
      current_user()
        .then((e) => {
          this.time = e.data.queue_time;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    update_minute(e) {
      disabled(true);
      this.loading = true;
      minute_update({ minute: e })
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
  },
  created() {
    this.get();
  },
};
</script>
