<template>
  <h3 class="text-center fw-normal">Registratsiya</h3>
  <div class="row">
    <div class="col-md-4">
      <button
        class="btn btn-sm btn-block btn-secondary"
        data-mdb-toggle="collapse"
        data-mdb-target="#registration"
        @click="
          get_services();
          get_source();
          get_region();
        "
      >
        <i class="fa fa-user-plus"></i> Bemor qo'shish
      </button>
    </div>
    <div class="col-md-4 my-1"></div>
    <div class="col-md-4">
      <div class="input-group input-group-sm">
        <input
          type="search"
          id="search_patient"
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

  <div>
    <PatientAdd
      :loading="loading"
      :regions="regions"
      :states="states"
      :sources="sources"
      :services="services"
      :doctors="doctors"
      @get_state="get_state"
      @get_doctor="get_doctor"
      @create_patient="create_patient"
      ref="patient"
    />

    <div class="row justify-content-end">
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
  </div>

  <queue-info ref="info" edit cancel />

  <!-- ADD PARTNER -->
  <div class="modal fade" id="add_partner" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Hamkor qo'shish</h6>
        </div>
        <form @submit.prevent="add_partner()" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                v-model="body_partner.name"
                placeholder="Hamkor"
                required
              />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-partner
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button type="submit" class="btn btn-primary">
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
        </form>
      </div>
    </div>
  </div>

  <!-- ADD PARTNER EMPLOYEE -->
  <div class="modal fade" id="add_partner_employee" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Hamkasb qo'shish</h6>
        </div>
        <form @submit.prevent="add_employee()" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="name">Ism</label>
              <input
                id="name"
                type="text"
                class="form-control"
                v-model="body_employee.name"
                placeholder="Hamkasb"
                required
              />
            </div>
            <div class="form-group">
              <label for="phone">Telefon</label>
              <div class="input-group">
                <span class="input-group-text">+998</span>
                <input
                  id="phone"
                  type="tel"
                  class="form-control"
                  maxlength="9"
                  minlength="9"
                  v-model="body_employee.phone"
                  @keypress="isNumber($event)"
                  required
                />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-employee
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button type="submit" class="btn btn-primary">
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
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import {
  catchError,
  disabled,
  doctors_get,
  partner_create,
  partner_employee_create,
  patient_create,
  queue_possibility,
  regions_get,
  services_get,
  sources_get,
  states_get,
  success,
} from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
import PatientAdd from "@/components/Patient/AddPatient.vue";
import QueueInfo from "@/components/Patient/QueueInfo.vue";
export default {
  name: "RegistrationItem",
  data() {
    return {
      search: "",
      step: 1,
      loading: false,
      states: [],
      regions: [],
      sources: [],
      services: [],
      doctors: [],
      doctors_for_update: [],
      item_queue: {},
      current_date: new Date().toISOString().substr(0, 10),
      body_partner: {
        name: "",
        source_id: 0,
        employees: [],
      },
      body_employee: {
        phone: null,
        name: "",
      },
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
    get_state(e) {
      states_get(1, 1000, e)
        .then((e) => {
          this.states = e.data.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    get_region() {
      regions_get(1, 1000)
        .then((e) => {
          this.regions = e.data.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    get_source() {
      sources_get(1, 1000)
        .then((e) => {
          this.sources = e.data.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    get_services() {
      services_get(1, 1000)
        .then((e) => {
          this.services = e.data.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    get_doctor(e, update) {
      doctors_get(1, 1000, 0, e)
        .then((e) => {
          if (update) {
            this.doctors_for_update = e.data.data;
          } else {
            this.doctors = e.data.data;
          }
        })
        .catch((error) => {
          catchError(error);
        });
    },
    create_patient(e) {
      disabled(true);
      this.loading = true;
      patient_create(e)
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            this.$refs.info.get(this.$refs.info.page, this.$refs.info.limit);
            this.$refs.patient.body = {
              name: "",
              surename: "",
              fathername: "",
              age: "",
              address: "",
              state_id: 0,
              region_id: 0,
              source_id: 0,
              partner_id: 0,
              partner_employee_id: 0,
              phone: null,
              inspections: [
                {
                  date: "",
                  responsible: "",
                  complaint: "",
                  treatment: "ambulator",
                  queues: [
                    {
                      doctor_id: 0,
                      service_id: 0,
                      room: null,
                      time: "",
                      number: "",
                      hasConsultation: false,
                      procedures_data: [],
                      procedures: [], // id
                      times: [],
                    },
                  ],
                },
              ],
            };
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    get_room() {
      let item = this.doctors_for_update.find(
        (item) => item.id == this.item_queue.doctor_id
      );
      this.item_queue.room = Number(item.room);
      this.item_queue.user_id = Number(item.user_id);
    },

    get_time(room, date) {
      queue_possibility(room, date, this.item_queue.user_id)
        .then((e) => {
          this.item_queue.times = e.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    isNumber(evt) {
      evt = evt ? evt : window.event;
      var charCode = evt.which ? evt.which : evt.keyCode;
      if (
        charCode > 31 &&
        (charCode < 48 || charCode > 57) &&
        charCode !== 46
      ) {
        evt.preventDefault();
      } else {
        return true;
      }
    },
    add_partner() {
      this.body_partner.source_id = this.$refs.patient.body.source_id;
      disabled(true);
      this.loading = true;
      partner_create(this.body_partner)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-partner").then(() => {
            this.$refs.patient.get_partners();
            this.body_partner.name = "";
            this.body_partner.source_id = 0;
            this.body_partner.employees = [];
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    add_employee() {
      disabled(true);
      this.loading = true;
      partner_employee_create(
        this.body_employee,
        this.$refs.patient.body.partner_id
      )
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-employee").then(() => {
            this.$refs.patient.get_partners(true);
            this.body_employee.name = "";
            this.body_employee.phone = null;
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
  },
  components: { Pagination, PatientAdd, QueueInfo },
};
</script>
