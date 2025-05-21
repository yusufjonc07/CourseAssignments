<template>
  <h3 class="text-center fw-normal">Bemorlar</h3>
  <div class="row">
    <div class="col-md-4"></div>
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
          <th>Bemor</th>
          <th>Telefon</th>
          <th>Manzil</th>
          <th>Manba</th>
          <th>Hamkor</th>
          <th>Hamkor/Hamkasb</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(patient, i) in patients" :key="patient">
          <td>{{ i + 1 }}</td>
          <td>
            {{ patient.name }} {{ patient.surename }} {{ patient.fathername }}
          </td>
          <td>
            <a :href="`tel:+998${patient.phone}`" class="text-dark">
              +998 {{ format(patient.phone) }}
            </a>
          </td>
          <td>
            {{ patient.region.name }}, {{ patient.state.name }},
            {{ patient.address }}
          </td>
          <td>{{ patient.source.name }}</td>
          <td>{{ patient.partner?.name }}</td>
          <td>{{ patient.partner_employee?.name }}</td>
          <td>
            <div class="d-flex">
              <router-link
                :to="{
                  name: 'patient',
                  query: {
                    id: patient.id,
                    name: patient.name,
                  },
                }"
                class="btn btn-sm btn-secondary mx-1"
              >
                <i class="fa-solid fa-eye"></i>
              </router-link>
              <button
                class="btn btn-sm btn-warning"
                data-mdb-toggle="modal"
                data-mdb-target="#update_patient"
                v-show="role == 'admin' || role == 'reception'"
                @click="
                  get_region();
                  get_source();
                  get_state(patient.region_id);
                  item = {
                    id: patient.id,
                    name: patient.name,
                    surename: patient.surename,
                    fathername: patient.fathername,
                    age: patient.age,
                    address: patient.address,
                    partner_id: patient.partner_id,
                    partner_employee_id: patient.partner_employee_id,
                    state_id: patient.state_id,
                    region_id: patient.region_id,
                    source_id: patient.source_id,
                    phone: patient.phone,
                  };
                  get_partners();
                "
              >
                <i class="fa-solid fa-pen"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!patients.length">
      Ma'lumot topilmadi !
    </h4>
    <Pagination :page="page" :pages="pages" :limit="limit" @get="get" />
  </div>

  <!-- UPDATE PATIENT -->
  <div
    class="modal fade"
    id="update_patient"
    tabindex="-1"
    v-show="role == 'admin' || role == 'reception'"
  >
    <div class="modal-dialog modal-dialog-scrollable modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Bemor ma'lumotlarini o'zgartirish</h6>
        </div>
        <form @submit.prevent="update_patient(item)" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="row">
              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_name">Ism: </label>
                  <input
                    type="text"
                    id="patient_name"
                    class="form-control"
                    v-model="item.name"
                    required
                  />
                </div>
              </div>
              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_surename">Familiya: </label>
                  <input
                    type="text"
                    id="patient_surename"
                    class="form-control"
                    v-model="item.surename"
                    required
                  />
                </div>
              </div>
              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_dadname">Otasining ismi: </label>
                  <input
                    type="text"
                    id="patient_dadname"
                    class="form-control"
                    v-model="item.fathername"
                  />
                </div>
              </div>
              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_age">Tug'ulgan sana: </label>
                  <input
                    type="date"
                    id="patient_age"
                    class="form-control"
                    v-model="item.age"
                    required
                  />
                </div>
              </div>
              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <label for="patient_phone">Telefon: </label>
                <div class="input-group">
                  <span class="input-group-text">+998</span>
                  <input
                    type="tel"
                    id="patient_phone"
                    class="form-control"
                    maxlength="9"
                    minlength="9"
                    v-model="item.phone"
                    @keypress="isNumber($event)"
                  />
                </div>
              </div>

              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_region">Viloyat: </label>
                  <select
                    id="patient_region"
                    class="form-select"
                    v-model="item.region_id"
                    @change="
                      item.state_id = null;
                      get_state(item.region_id);
                    "
                    required
                  >
                    <option
                      :value="region.id"
                      v-for="region in regions"
                      :key="region"
                    >
                      {{ region.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_state">Tuman: </label>
                  <select
                    id="patient_state"
                    class="form-select"
                    v-model="item.state_id"
                    :disabled="!item.region_id"
                    required
                  >
                    <option
                      :value="state.id"
                      v-for="state in states"
                      :key="state"
                    >
                      {{ state.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_address">Manzil: </label>
                  <input
                    type="text"
                    id="patient_address"
                    class="form-control"
                    v-model="item.address"
                  />
                </div>
              </div>
              <div class="col-lg-6 col-md-6 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_source">Manba: </label>
                  <select
                    id="patient_source"
                    class="form-select"
                    v-model="item.source_id"
                    @change="
                      get_partners();
                      partner_employees = [];
                      item.partner_id = null;
                    "
                    required
                  >
                    <option
                      :value="source.id"
                      v-for="source in sources"
                      :key="source"
                    >
                      {{ source.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label for="patient_partner">Hamkor: </label>
                  <select
                    id="patient_partner"
                    class="form-select"
                    v-model="item.partner_id"
                    :disabled="!item.source_id"
                    @change="
                      partner_employees = [];
                      item.partner_employee_id = null;
                      partner_employees = partners.find(
                        (e) => e.id == item.partner_id
                      ).employees;
                    "
                  >
                    <option
                      :value="partner.id"
                      v-for="partner in partners"
                      :key="partner"
                    >
                      {{ partner.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label for="patient_employee">Hamkor/Hamkasb: </label>
                  <select
                    id="patient_employee"
                    class="form-select"
                    v-model="item.partner_employee_id"
                    :disabled="!item.partner_id"
                  >
                    <option
                      :value="employee.id"
                      v-for="employee in partner_employees"
                      :key="employee"
                    >
                      {{ employee.name }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-patient-update
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
  partners_get,
  patients_get,
  patient_update,
  regions_get,
  sources_get,
  states_get,
  success,
} from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
export default {
  name: "Patient",
  data() {
    return {
      patients: [],
      page: 1,
      pages: 0,
      limit: 25,
      search: "",
      item: {},
      loading: false,
      states: [],
      regions: [],
      sources: [],
      role: localStorage.getItem("role"),
      partners: [],
      partner_employees: [],
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      patients_get(page, limit, this.search)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.patients = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
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
    update_patient(body) {
      disabled(true);
      this.loading = true;
      patient_update(body)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-patient-update").then(() => {
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    get_partners() {
      partners_get(1, 1000, this.item.source_id)
        .then((e) => {
          this.partners = e.data.data;
          if (this.partners.length) {
            this.partner_employees = this.partners.find(
              (e) => e.id == this.item.partner_id
            ).employees;
          }
        })
        .catch((error) => {
          catchError(error);
        });
    },
  },
  created() {
    this.get(this.page, this.limit);
  },
  components: { Pagination },
};
</script>
