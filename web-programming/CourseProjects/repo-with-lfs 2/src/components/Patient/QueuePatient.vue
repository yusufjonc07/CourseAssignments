<template>
  <div class="card">
    <div class="card-body">
      <div class="responsive" style="max-height: 79vh" v-if="false">
        <table class="table table-hover table-sm align-middle mb-0 bg-white">
          <thead class="bg-blue">
            <tr>
              <th>№</th>
              <th>Navbat</th>
              <th>Vaqt</th>
              <th>Doktor</th>
              <th>Ko'rik</th>
              <th>Davolanish turi</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(queue, i) in queues" :key="queue">
              <td>{{ i + 1 }}</td>
              <td>{{ queue.number }}</td>
              <td>{{ queue.time }}</td>
              <td>{{ queue.doctor.user.name }}</td>
              <td>{{ queue.service.name }}</td>
              <td>{{ queue.treatment }}</td>
              <td>
                <span class="badge" :class="queue.status_color">
                  {{ queue.status }}</span
                >
              </td>
              <td>
                <button
                  class="btn btn-sm btn-danger"
                  @click="cancel_queue(queue.id)"
                  v-show="queue.step == 1"
                >
                  <i class="fa-solid fa-circle-xmark"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <h4 class="text-center m-4" v-if="!queues.length">
          Ma'lumot topilmadi !
        </h4>
        <Pagination :page="page" :pages="pages" :limit="limit" @get="get" />
      </div>
      <queue-info ref="info" :patient_id="Number(patient_id)" />
    </div>
  </div>

  <div class="modal fade" id="add_queue" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Ko'rik qo'shish</h6>
          <button
            class="btn btn-sm btn-secondary"
            @click="
              body.queues.push({
                doctor_id: 0,
                service_id: 0,
                room: null,
                time: '',
                number: '',
                hasConsultation: false,
                procedures_data: [],
                procedures: [], // id
                times: [],
                doctors: [],
              })
            "
          >
            Navbat qo'shish
          </button>
        </div>
        <form @submit.prevent="inspection_add" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="row">
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
                <div class="form-group">
                  <label for="complaint">Shikoyat: </label>
                  <input
                    type="text"
                    id="complaint"
                    class="form-control"
                    v-model="body.complaint"
                    required
                  />
                </div>
              </div>
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
                <div class="form-group">
                  <label for="responsible">Olib kelgan shaxs: </label>
                  <input
                    type="text"
                    id="responsible"
                    class="form-control"
                    v-model="body.responsible"
                    required
                  />
                </div>
              </div>
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
                <div class="form-group">
                  <label for="treatment">Davolanish turi: </label>
                  <select
                    id="treatment"
                    class="form-select"
                    v-model="body.treatment"
                    required
                  >
                    <option value="ambulator">Ambulator</option>
                    <option value="statsionar">Statsionar</option>
                  </select>
                </div>
              </div>
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
                <label for="patient_date">Sana: </label>
                <input
                  type="date"
                  id="patient_date"
                  class="form-control"
                  :min="current_date"
                  v-model="body.date"
                  @change="
                    body.queues = [
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
            <hr />

            <div class="row" v-for="(que, que_index) in body.queues" :key="que">
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_service">Mutahasislik: </label>
                  <select
                    id="patient_service"
                    class="form-select"
                    v-model="que.service_id"
                    @change="
                      get_doctor(que.service_id, que_index);
                      index_que = que_index;
                    "
                    :disabled="!body.date"
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
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
                <div class="form-group">
                  <label for="patient_service">Doktor: </label>
                  <select
                    id="patient_service"
                    class="form-select"
                    v-model="que.doctor_id"
                    :disabled="!que.service_id"
                    @change="
                      get_room(index_que);
                      get_time(que.room, index_que, body.date);
                    "
                    required
                  >
                    <option
                      :value="doctor.id"
                      v-for="doctor in que.doctors"
                      :key="doctor"
                    >
                      {{ doctor.user.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
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
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
                <label for="times">Vaqt: </label>
                <div class="input-group">
                  <select
                    class="form-control"
                    id="times"
                    v-model="que.time"
                    :disabled="!que.room"
                    @change="queue_number(que_index)"
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
                    v-show="que_index || (!que_index && body.queues.length > 1)"
                    @click="body.queues.splice(que_index, 1)"
                  >
                    <i class="fa-solid fa-circle-xmark"></i>
                  </button>
                </div>
              </div>
              <div class="col-md-6 col-lg-3 col-sm-6 col-12">
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
                        : get_procedures(que_index, que.service_id, '')
                      : ''
                  "
                  @keyup="
                    que.service_id
                      ? get_procedures(
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
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-add-inspection
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
  doctors_get,
  queue_possibility,
  services_get,
  service_procedures_get,
  inspection_create,
  disabled,
  success,
} from "../Utils/api";
import Pagination from "../Utils/Pagination.vue";
import QueueInfo from "./QueueInfo.vue";

export default {
  name: "QueuePatient",
  data() {
    return {
      patient_id: this.$route.query.id,
      body: {
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
            doctors: [],
          },
        ],
      },
      index_que: null,
      role: localStorage.getItem("role"),
      current_date: new Date().toISOString().substr(0, 10),
      services: [],
      loading: false,
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
    get_room(index_que) {
      let item = this.body.queues[index_que].doctors.find(
        (item) => item.id == this.body.queues[index_que].doctor_id
      );
      this.body.queues[index_que].room = Number(item.room);
      this.body.queues[index_que].user_id = Number(item.user_id);
    },
    padTo2Digits(num) {
      return String(num).padStart(2, "0");
    },
    get_time(room, index_que, date) {
      queue_possibility(room, date, this.body.queues[index_que].user_id)
        .then((e) => {
          this.body.queues[index_que].times = e.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    queue_number(que_index) {
      let item = this.body.queues[que_index].times.find(
        (item) => item.time == this.body.queues[que_index].time
      );
      this.body.queues[que_index].number = Number(item.queue_number);
    },
    get_procedures(que_index, service_id, search) {
      service_procedures_get(1, 10, service_id, search)
        .then((e) => {
          this.body.queues[que_index].procedures_data = [];
          e.data.data.forEach((element) => {
            this.body.queues[que_index].procedures_data.push({
              value: element.id,
              label: element.name,
            });
          });
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
    get_doctor(e, index_que) {
      doctors_get(1, 1000, 0, e)
        .then((e) => {
          this.body.queues[index_que].doctors = e.data.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    inspection_add() {
      disabled(true);
      this.loading = true;
      inspection_create(this.body, this.patient_id)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-add-inspection").then(() => {
            this.$refs.info.get(1, 25);
            this.body = {
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
                  doctors: [],
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
  },
  created() {},
  components: { Pagination, QueueInfo },
};
</script>
