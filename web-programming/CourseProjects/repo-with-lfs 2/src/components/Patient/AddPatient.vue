<template>
  <div class="collapse my-3" id="registration">
    <form @submit.prevent="$emit('create_patient', body)" class="px-1">
      <div class="mb-2">
        <div class="row">
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_name">Ism: </label>
              <input
                type="text"
                id="patient_name"
                class="form-control"
                v-model="body.name"
                required
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_surename">Familiya: </label>
              <input
                type="text"
                id="patient_surename"
                class="form-control"
                v-model="body.surename"
                required
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_dadname">Otasining ismi: </label>
              <input
                type="text"
                id="patient_dadname"
                class="form-control"
                v-model="body.fathername"
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_age">Tug'ulgan sana: </label>
              <input
                type="date"
                id="patient_age"
                class="form-control"
                v-model="body.age"
                required
              />
            </div>
          </div>
          <div class="col-md-4">
            <label for="patient_phone">Telefon: </label>
            <div class="input-group">
              <span class="input-group-text">+998</span>
              <input
                type="tel"
                id="patient_phone"
                class="form-control"
                maxlength="9"
                minlength="9"
                v-model="body.phone"
                @keypress="isNumber($event)"
                @keyup="exist_phone($event)"
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_region">Viloyat: </label>
              <select
                id="patient_region"
                class="form-select"
                v-model="body.region_id"
                @change="$emit('get_state', body.region_id)"
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
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_state">Tuman: </label>
              <select
                id="patient_state"
                class="form-select"
                v-model="body.state_id"
                :disabled="!body.region_id"
                required
              >
                <option :value="state.id" v-for="state in states" :key="state">
                  {{ state.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_address">Manzil: </label>
              <input
                type="text"
                id="patient_address"
                class="form-control"
                v-model="body.address"
              />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_source">Manba: </label>
              <select
                id="patient_source"
                class="form-select"
                v-model="body.source_id"
                @change="
                  get_partners();
                  partner_employees = [];
                  body.partner_id = null;
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
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_partner">Hamkor: </label>
              <div class="input-group">
                <select
                  id="patient_partner"
                  class="form-select"
                  v-model="body.partner_id"
                  :disabled="!body.source_id"
                  @change="
                    partner_employees = [];
                    body.partner_employee_id = null;
                    partner_employees = partners.find(
                      (e) => e.id == body.partner_id
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
                <button
                  class="btn btn-primary"
                  type="button"
                  :disabled="!body.source_id"
                  data-mdb-toggle="modal"
                  data-mdb-target="#add_partner"
                >
                  <i
                    class="fas fa-circle-plus"
                    style="pointer-events: none"
                  ></i>
                </button>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label for="patient_employee">Hamkor/Hamkasb: </label>
              <div class="input-group">
                <select
                  id="patient_employee"
                  class="form-select"
                  v-model="body.partner_employee_id"
                  :disabled="!body.partner_id"
                >
                  <option
                    :value="employee.id"
                    v-for="employee in partner_employees"
                    :key="employee"
                  >
                    {{ employee.name }}
                  </option>
                </select>
                <button
                  class="btn btn-primary"
                  type="button"
                  :disabled="!body.partner_id"
                  data-mdb-toggle="modal"
                  data-mdb-target="#add_partner_employee"
                >
                  <i
                    class="fas fa-circle-plus"
                    style="pointer-events: none"
                  ></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div
          class="border border-2 p-2 mt-2 rounded-5"
          v-for="(inspection, index) in body.inspections"
          :key="inspection"
        >
          <div class="row">
            <div class="col">
              <h5 class="text-center text-primary">Ko'rik - {{ index + 1 }}</h5>
            </div>
            <div class="col-auto">
              <button
                class="btn btn-danger btn-sm"
                type="button"
                v-show="index || (!index && body.inspections.length > 1)"
                @click="body.inspections.splice(index, 1)"
              >
                <i class="fa-solid fa-circle-xmark"></i>
              </button>
            </div>
          </div>
          <div class="row">
            <div class="col-md-3">
              <div class="form-group">
                <label for="complaint">Shikoyat: </label>
                <input
                  type="text"
                  id="complaint"
                  class="form-control"
                  v-model="inspection.complaint"
                  required
                />
              </div>
            </div>
            <div class="col-md-3">
              <div class="form-group">
                <label for="responsible">Olib kelgan shaxs: </label>
                <input
                  type="text"
                  id="responsible"
                  class="form-control"
                  v-model="inspection.responsible"
                  required
                />
              </div>
            </div>
            <div class="col-md-3">
              <div class="form-group">
                <label for="treatment">Davolanish turi: </label>
                <select
                  id="treatment"
                  class="form-select"
                  v-model="inspection.treatment"
                  required
                >
                  <option value="ambulator">Ambulator</option>
                  <option value="statsionar">Statsionar</option>
                </select>
              </div>
            </div>
            <div class="col-md-3">
              <label for="patient_date">Sana: </label>
              <input
                type="date"
                id="patient_date"
                class="form-control"
                :min="current_date"
                v-model="inspection.date"
                @change="
                  inspection.queues = [
                    {
                      doctor_id: 0,
                      service_id: 0,
                      room: null,
                      time: '',
                      number: '',
                      hasConsultation: false,
                      procedures_data: [],
                      procedures: [], // id
                      times: [],
                    },
                  ]
                "
                required
              />
            </div>
          </div>

          <div class="row my-2">
            <div class="col">
              <h5 class="text-primary">Navbat</h5>
            </div>
            <div class="col-auto">
              <button
                class="btn btn-primary btn-sm"
                type="button"
                @click="
                  body.inspections[index].queues.push({
                    doctor_id: 0,
                    service_id: 0,
                    room: null,
                    time: '',
                    number: '',
                    hasConsultation: false,
                    procedures_data: [],
                    procedures: [], // id
                    times: [],
                  })
                "
              >
                <i class="fa-solid fa-circle-plus"></i> Navbat qo'shish
              </button>
            </div>
          </div>
          <div
            class="card shadow mb-2"
            v-for="(que, que_index) in inspection.queues"
            :key="que"
          >
            <div class="card-body">
              <div class="row">
                <div class="col-md-3">
                  <div class="form-group">
                    <label for="patient_service">Mutahasislik: </label>
                    <select
                      id="patient_service"
                      class="form-select"
                      v-model="que.service_id"
                      @change="
                        $emit('get_doctor', que.service_id);
                        index_que = que_index;
                        index_inspection = index;
                      "
                      :disabled="!inspection.date"
                      required
                    >
                      <option
                        :value="service.id"
                        v-for="service in services"
                        :key="service"
                      >
                        {{ service.name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="form-group">
                    <label for="patient_service">Doktor: </label>
                    <select
                      id="patient_service"
                      class="form-select"
                      v-model="que.doctor_id"
                      :disabled="!que.service_id"
                      @change="
                        get_room(index, index_que);
                        get_time(que.room, index, index_que, inspection.date);
                      "
                      required
                    >
                      <option
                        :value="doctor.id"
                        v-for="doctor in que.doctor"
                        :key="doctor"
                      >
                        {{ doctor.user.name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-3">
                  <label for="patient_room">Xona: </label>
                  <div class="input-group">
                    <input
                      type="number"
                      min="0"
                      id="patient_room"
                      class="form-control"
                      v-model="que.room"
                      :disabled="!que.doctor_id"
                      required
                    />
                    <span class="input-group-text">xona</span>
                  </div>
                </div>
                <div class="col-md-3">
                  <label for="times">Vaqt: </label>
                  <div class="input-group">
                    <select
                      class="form-control"
                      id="times"
                      v-model="que.time"
                      :disabled="!que.room"
                      @change="queue_number(index, que_index)"
                      required
                    >
                      <option
                        :value="time.time"
                        v-for="time in que.times"
                        :key="time"
                        :disabled="!time.possible"
                      >
                        {{ time.queue_number + " - navbat " + time.time }}
                      </option>
                    </select>
                    <button
                      class="btn btn-danger"
                      type="button"
                      style="width: 65px"
                      v-show="
                        que_index ||
                        (!que_index &&
                          body.inspections[index].queues.length > 1)
                      "
                      @click="
                        body.inspections[index].queues.splice(que_index, 1)
                      "
                    >
                      <i class="fa-solid fa-circle-xmark"></i>
                    </button>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="form-check py-4">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      id="hasconsultation"
                      v-model="que.hasConsultation"
                    />
                    <label class="form-check-label" for="hasconsultation"
                      >Konsultatsiya</label
                    >
                  </div>
                </div>
                <div class="col-12">
                  <multiselect
                    v-model="que.procedures"
                    mode="tags"
                    placeholder="Muolaja tanlash"
                    :options="que.procedures_data"
                    :searchable="true"
                    @click="
                      que.service_id
                        ? $event.target.value
                          ? ''
                          : get_procedures(index, que_index, que.service_id, '')
                        : ''
                    "
                    @keyup="
                      que.service_id
                        ? get_procedures(
                            index,
                            que_index,
                            que.service_id,
                            $event.target.value
                          )
                        : ''
                    "
                  ></multiselect>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-2">
        <div class="col justify-content-end d-flex">
          <button
            class="btn btn-sm btn-primary mx-1"
            type="button"
            style="width: 65px"
            @click="
              body.inspections.push({
                date: '',
                responsible: '',
                complaint: '',
                treatment: 'ambulator',
                queues: [
                  {
                    doctor_id: 0,
                    service_id: 0,
                    room: null,
                    time: '',
                    number: '',
                    hasConsultation: false,
                    procedures_data: [],
                    procedures: [], // id
                    times: [],
                  },
                ],
              })
            "
          >
            <i class="fa-solid fa-circle-plus"></i>
          </button>
          <button
            type="button"
            class="btn btn-sm btn-danger"
            @click="
              body = {
                name: '',
                surename: '',
                fathername: '',
                age: '',
                address: '',
                state_id: 0,
                region_id: 0,
                source_id: 0,
                partner_id: 0,
                partner_employee_id: 0,
                phone: null,
                inspections: [
                  {
                    date: '',
                    responsible: '',
                    complaint: '',
                    treatment: 'ambulator',
                    queues: [
                      {
                        doctor_id: 0,
                        service_id: 0,
                        room: null,
                        time: '',
                        number: '',
                        hasConsultation: false,
                        procedures_data: [],
                        procedures: [], // id
                        times: [],
                      },
                    ],
                  },
                ],
              }
            "
          >
            <i class="fa-solid fa-trash"></i> Bekor qilish
          </button>
          <button type="submit" class="btn btn-sm btn-success mx-1">
            <div v-if="!loading">
              <i class="fa-solid fa-circle-check"></i> qo'shish
            </div>
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
</template>

<script>
import Swal from "sweetalert2";
import {
  catchError,
  partners_get,
  patient_exist,
  queue_possibility,
  service_procedures_get,
} from "../Utils/api";
export default {
  name: "AddPatient",
  emits: ["create_patient", "update_patient", "get_state", "get_doctor"],
  props: ["loading", "sources", "states", "regions", "services", "doctors"],
  watch: {
    doctors(e) {
      this.body.inspections[this.index_inspection].queues[
        this.index_que
      ].doctor = e;
    },
  },
  data() {
    return {
      body: {
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
      },
      index_inspection: null,
      index_que: null,
      role: localStorage.getItem("role"),
      current_date: new Date().toISOString().substr(0, 10),
      partners: [],
      partner_employees: [],
    };
  },
  methods: {
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
    get_room(index, index_que) {
      let item = this.doctors.find(
        (item) =>
          item.id == this.body.inspections[index].queues[index_que].doctor_id
      );
      this.body.inspections[index].queues[index_que].room = Number(item.room);
      this.body.inspections[index].queues[index_que].user_id = Number(
        item.user_id
      );
    },
    exist_phone(e) {
      if (e.target.value.length == 9) {
        e.target.disabled = true;
        patient_exist({ phone: e.target.value })
          .then((res) => {
            if (res.data) {
              e.target.disabled = true;
              Swal.fire({
                title: "Bunday telefon taqamli bemor mavjud !",
                html: `<h3>${res.data.name} ${res.data.surename} ${res.data.fathername}<h3>`,
                showCancelButton: true,
                showConfirmButton: true,
                cancelButtonText: "<i class='fa-solid fa-circle-xmark'></i>",
                confirmButtonText: "<i class='fa-solid fa-eye'></i>",
              }).then((result) => {
                if (result.isConfirmed == true) {
                  this.$router.push({
                    name: "patient",
                    query: {
                      id: res.data.id,
                      name: res.data.name,
                    },
                  });
                } else {
                  e.target.disabled = false;
                }
              });
            } else {
              e.target.disabled = false;
            }
          })
          .catch((error) => {
            e.target.disabled = false;
            catchError(error);
          });
      }
    },
    padTo2Digits(num) {
      return String(num).padStart(2, "0");
    },
    get_time(room, index, index_que, date) {
      queue_possibility(
        room,
        date,
        this.body.inspections[index].queues[index_que].user_id
      )
        .then((e) => {
          this.body.inspections[index].queues[index_que].times = e.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    queue_number(index, que_index) {
      let item = this.body.inspections[index].queues[que_index].times.find(
        (item) =>
          item.time == this.body.inspections[index].queues[que_index].time
      );
      this.body.inspections[index].queues[que_index].number = Number(
        item.queue_number
      );
    },
    get_partners(bool) {
      partners_get(1, 1000, this.body.source_id)
        .then((e) => {
          this.partners = e.data.data;
          if (bool) {
            this.partner_employees = this.partners.find(
              (e) => e.id == this.body.partner_id
            ).employees;
          }
        })
        .catch((error) => {
          catchError(error);
        });
    },
    get_procedures(index, que_index, service_id, search) {
      service_procedures_get(1, 10, service_id, search)
        .then((e) => {
          this.body.inspections[index].queues[que_index].procedures_data = [];
          e.data.data.forEach((element) => {
            this.body.inspections[index].queues[que_index].procedures_data.push(
              { value: element.id, label: element.name }
            );
          });
        })
        .catch((error) => {
          catchError(error);
        });
    },
  },
};
</script>
