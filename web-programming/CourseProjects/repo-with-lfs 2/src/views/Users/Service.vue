<template>
  <h4 class="text-center fw-normal">{{ name }} mutahasisliklari</h4>
  <div class="row">
    <div class="col-md-4">
      <button
        class="btn btn-sm btn-block btn-secondary"
        data-mdb-toggle="modal"
        data-mdb-target="#add_service"
        @click="get_services()"
      >
        <i class="fa fa-user-plus"></i> Mutahasislik qo'shish
      </button>
    </div>
    <div class="col-md-4 my-1"></div>
    <div class="col-md-4"></div>
  </div>
  <hr />

  <div class="responsive" style="max-height: 80vh">
    <table class="table table-hover table-sm align-middle mb-0 bg-white">
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th>Mutahasislik</th>
          <th>KPI</th>
          <th>Kattalar konsultatsiyasi</th>
          <th>Kichiklar konsultatsiyasi</th>
          <th>Xona</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(service, i) in services" :key="service">
          <td>{{ i + 1 }}</td>
          <td>{{ service.service.name }}</td>
          <td>{{ Intl.NumberFormat().format(service.kpi) }}%</td>
          <td>{{ Intl.NumberFormat().format(service.cost) }} so'm</td>
          <td>{{ Intl.NumberFormat().format(service.cost_min) }} so'm</td>
          <td>{{ service.room }}-xona</td>
          <td>
            <button
              class="btn btn-sm btn-warning"
              data-mdb-toggle="modal"
              data-mdb-target="#update_service"
              @click="
                get_services();
                item = {
                  id: service.id,
                  service_id: service.service_id,
                  cost: service.cost,
                  cost_min: service.cost_min,
                  room: service.room,
                  user_id: service.user_id,
                  kpi: service.kpi || 0,
                };
              "
            >
              <i class="fa-solid fa-pen"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!services.length">
      Ma'lumot topilmadi !
    </h4>
  </div>
  <ServiceModal
    @create_service="create_service"
    :loading="loading"
    :item="item"
    @update_service="update_service"
    :services="service_category"
  />
</template>

<script>
import ServiceModal from "@/components/User/ServiceModal.vue";
import {
  catchError,
  disabled,
  doctors_get,
  doctor_create,
  doctor_update,
  services_get,
  success,
} from "@/components/Utils/api";
export default {
  name: "ServiceItem",
  data() {
    return {
      name: this.$route.query.name,
      id: this.$route.query.id,
      services: [],
      service_category: [],
      loading: false,
      item: {},
    };
  },
  methods: {
    get() {
      this.$store.dispatch("setloading", { loading: true });
      doctors_get(1, 1000, this.id, 0)
        .then((e) => {
          this.services = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    create_service(e) {
      disabled(true);
      this.loading = true;
      doctor_create(e)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-service").then(() => {
            this.get(this.page, this.limit);
            e.service_id = null;
            e.room = null;
            e.cost = null;
            e.cost_min = null;
            e.kpi = 0;
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    update_service(body) {
      disabled(true);
      this.loading = true;
      doctor_update(body)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-service-update").then(() => {
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    get_services() {
      services_get(1, 1000)
        .then((e) => {
          this.service_category = e.data.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
  },
  created() {
    this.get();
  },
  components: { ServiceModal },
};
</script>
