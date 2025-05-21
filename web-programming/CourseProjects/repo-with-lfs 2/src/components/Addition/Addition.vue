<template>
  <div class="card">
    <div class="card-body">
      <h5 class="text-center">Qayta a'loqa vaqti va Yosh chegarasi</h5>
      <form @submit.prevent="update_contact_date()">
        <div class="row d-flex justify-content-center">
          <div class="col">
            <label class="form-label" for="date">Qayta a'loqa vaqti</label>
            <div class="input-group">
              <input
                type="number"
                min="0"
                step="any"
                id="date"
                class="form-control"
                v-model="recall_hour"
                required
              />
              <span class="input-group-text">soat</span>
            </div>
          </div>
          <div class="col">
            <label class="form-label" for="age_border">Yosh chegarasi</label>
            <div class="input-group">
              <input
                type="number"
                min="0"
                step="any"
                id="age_border"
                class="form-control"
                v-model="age_border"
                required
              />
              <span class="input-group-text">yosh</span>
            </div>
          </div>
          <div class="col-auto d-flex mt-auto">
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
      </form>
    </div>
  </div>
</template>

<script>
import { disabled, settings_get, setting_update, success } from "../Utils/api";
export default {
  name: "Addition",
  data() {
    return {
      recall_hour: null,
      age_border: null,
      loading: false,
    };
  },
  methods: {
    get() {
      this.$store.dispatch("setloading", { loading: true });
      settings_get()
        .then((e) => {
          this.recall_hour = e.data.recall_hour;
          this.age_border = e.data.age_border;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    update_contact_date() {
      disabled(true);
      this.loading = true;
      setting_update({ hour: this.recall_hour, age_border: this.age_border })
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
