<template>
  <h3 class="text-center fw-normal">Navbat</h3>
  <div class="row">
    <div class="col-md-4">
      <button
        class="btn btn-sm btn-secondary btn-block"
        @click="call_patient()"
        v-show="queues.length"
      >
        <i class="fa-solid fa-headset"></i> Navbatdagi bemor
      </button>
    </div>
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
            get(1, limit);
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

  <div class="responsive" style="max-height: 80vh">
    <table class="table table-hover table-sm align-middle mb-0 bg-white">
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th>Navbat</th>
          <th>Vaqt</th>
          <th>Bemor</th>
          <th>Ko'rik</th>
          <th>Status</th>
          <th>Tashxis</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(queue, i) in queues" :key="queue">
          <td>{{ i + 1 }}</td>
          <td>{{ queue.number }}</td>
          <td>{{ queue.time }}</td>
          <td>
            {{
              queue.inspection?.patient.name +
              " " +
              queue.inspection?.patient.surename
            }}
          </td>
          <td>{{ queue.service.name }}</td>
          <td>
            <span
              class="badge"
              :class="queue.in_room ? 'badge-success' : 'badge-warning'"
              >{{ queue.in_room ? "chaqirildi" : "chaqirilmadi" }}</span
            >
          </td>
          <td>
            <router-link
              :to="{
                name: 'add_diagnosis',
                query: {
                  patient_id: queue.inspection?.patient.id,
                  queue_id: queue.id,
                  service_id: queue.service_id,
                },
              }"
              class="btn btn-sm btn-primary position-relative"
            >
              <i class="fa-solid fa-clipboard-list"></i>
              <span
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill badge-primary"
              >
                {{ queue.diagnosiss.length }}
                <span class="visually-hidden">unread messages</span>
              </span>
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!queues.length">Ma'lumot topilmadi !</h4>
    <Pagination :page="page" :pages="pages" :limit="limit" @get="get" />
  </div>
</template>

<script>
import {
  catchError,
  queues_all_get,
  queue_call,
  success,
} from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
export default {
  components: { Pagination },
  name: "DoctorConfirm",
  data() {
    return {
      queues: [],
      page: 1,
      pages: 0,
      limit: 25,
      search: "",
      step: 3,
      loading: false,
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      queues_all_get(page, limit, this.step, this.search, 0)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.queues = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    call_patient() {
      this.$store.dispatch("setloading", { loading: true });
      queue_call(this.queues[0].room)
        .then((e) => {
          this.$store.dispatch("setloading", { loading: false });
          success().then(() => {
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
  },
  created() {
    this.get(this.page, this.limit);
  },
};
</script>
