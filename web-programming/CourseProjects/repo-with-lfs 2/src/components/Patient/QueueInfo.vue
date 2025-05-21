<template>
  <div class="responsive mt-2" style="min-height: 74vh; max-height: 74vh">
    <table class="table table-hover table-sm align-middle mb-0 bg-white">
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th>Bemor</th>
          <th>Shikoyat</th>
          <th>Davolanish turi</th>
          <th>Olib kelgan shaxs</th>
          <th>Jami summa</th>
          <th>Chegirma summa</th>
          <th>To'lov summa</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(queue, i) in queues" :key="queue">
          <td>{{ i + 1 }}</td>
          <td>{{ queue.patient.name + " " + queue.patient.surename }}</td>
          <td>{{ queue.complaint }}</td>
          <td>{{ queue.treatment }}</td>
          <td>{{ queue.responsible }}</td>
          <td>{{ Intl.NumberFormat().format(queue.total_price) }} so'm</td>
          <td>{{ Intl.NumberFormat().format(queue.discount) }} so'm</td>
          <td>
            {{ Intl.NumberFormat().format(queue.total_price - queue.discount) }}
            so'm
          </td>
          <td>
            <button
              class="btn btn-sm btn-info ms-1"
              @click="queues_info = queue"
              data-mdb-toggle="modal"
              data-mdb-target="#queue_info"
            >
              <i class="fa-solid fa-circle-info"></i>
            </button>
            <button
              class="btn btn-sm btn-warning mx-1"
              v-if="!queue.cancel_user_id ? step == 1 : false"
              data-mdb-toggle="modal"
              data-mdb-target="#update_inspection"
              @click="
                item_inspection = {
                  id: queue.id,
                  responsible: queue.responsible,
                  complaint: queue.complaint,
                  treatment: queue.treatment,
                  discount: queue.discount,
                  total_price: queue.total_price,
                }
              "
            >
              <i class="fa-solid fa-pen"></i>
            </button>
            <button
              class="btn btn-sm btn-danger"
              v-if="!queue.cancel_user_id ? step == 1 : false"
              @click="cancel_inspcetion(queue.id)"
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              class="btn btn-sm btn-success ms-1"
              v-if="!queue.cancel_user_id ? step == 1 && confirm : false"
              data-mdb-toggle="modal"
              data-mdb-target="#cashreg_confirm"
              @click="
                confirm_body.cost = queue.total_price;
                confirm_body.discount = queue.discount;
                confirm_body.inspection_id = queue.id;
              "
            >
              <i class="fa-solid fa-circle-check"></i>
            </button>
            <button
              class="btn btn-sm btn-primary ms-1"
              v-if="step == 3 && print"
              @click="$refs.check.start(queue.id)"
            >
              <i class="fa-solid fa-print"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!queues.length">Ma'lumot topilmadi !</h4>
    <pagination :page="page" :pages="pages" :limit="limit" @get="get" />
  </div>

  <div class="modal fade" id="queue_info" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">
            {{
              queues_info?.patient?.name + " " + queues_info?.patient?.surename
            }}
            navbatlari
          </h6>
        </div>
        <div class="modal-body mb-2">
          <div class="responsive mt-2" style="max-height: 60vh">
            <table
              class="table table-hover table-sm align-middle mb-0 bg-white"
            >
              <thead class="bg-blue">
                <tr>
                  <td>Navbat</td>
                  <td>Vaqt</td>
                  <td>Xizmat turi</td>
                  <td>Xona</td>
                  <td>Doktor</td>
                  <td>Jami</td>
                  <td></td>
                </tr>
              </thead>
              <tbody v-for="queue in queues_info?.queues || []" :key="queue">
                <tr>
                  <td>{{ queue.number }}</td>
                  <td>{{ queue.time }}</td>
                  <td>{{ queue.service?.name }}</td>
                  <td>{{ queue.room }}-xona</td>
                  <td>{{ queue.doctor?.user?.name }}</td>
                  <td>
                    {{
                      Intl.NumberFormat().format(
                        queue.consultationPrice +
                          queue.queue_procedures?.reduce(
                            (acc, item) => acc + item.price,
                            0
                          )
                      )
                    }}
                    so'm
                  </td>
                  <td>
                    <button
                      class="btn btn-sm btn-warning mx-1"
                      data-mdb-toggle="modal"
                      data-mdb-target="#update_queue"
                      @click="
                        get_procedures(queue.service_id, '', false);
                        get_services();
                        get_doctor(queue.service_id, false);
                        values(queue);
                        get_time(queue.room, queues_info?.date, false);
                      "
                      v-if="!queue.cancel_user_id ? step == 1 && edit : false"
                    >
                      <i class="fa-solid fa-pen"></i>
                    </button>
                    <button
                      class="btn btn-sm btn-danger"
                      @click="cancel_queue(queue.id)"
                      v-if="
                        role == 'reception'
                          ? step == 1 && cancel
                          : step == 3 && cancel
                      "
                    >
                      <i class="fa-solid fa-circle-xmark"></i>
                    </button>
                    <button
                      class="btn btn-sm btn-primary"
                      @click="$refs.list.start(queue.id)"
                      v-if="queue.step == 4 || queue.step == 5"
                    >
                      <i class="fa-solid fa-print"></i>
                    </button>
                  </td>
                </tr>
                <tr>
                  <td colspan="7">
                    <span
                      class="badge bg-secondary me-1"
                      v-if="queue.consultationPrice"
                      >Konsultatsiya:
                      {{ Intl.NumberFormat().format(queue.consultationPrice) }}
                      so'm
                    </span>
                    <span
                      class="badge bg-primary me-1"
                      v-for="procedure in queue.queue_procedures"
                      :key="procedure"
                    >
                      {{ procedure.service_procedure?.name }}:
                      {{ Intl.NumberFormat().format(procedure.price) }} so'm
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
            <h4 class="text-center m-4" v-if="!queues_info?.queues?.length">
              Ma'lumot topilmadi !
            </h4>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-primary"
            data-mdb-toggle="modal"
            data-mdb-target="#create_queue"
            @click="
              body = [
                {
                  doctor_id: 0,
                  service_id: 0,
                  room: null,
                  time: '',
                  number: '',
                  user_id: 0,
                  hasConsultation: false,
                  procedures_data: [],
                  procedures: [], // id
                  times: [],
                  doctors: [],
                },
              ];
              get_services();
            "
          >
            <i class="fa-solid fa-circle-plus"></i>
          </button>
          <button
            type="button"
            class="btn btn-secondary"
            data-mdb-dismiss="modal"
            close-que-info
          >
            <i class="fa-solid fa-circle-xmark"></i>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- UPDATE QUEUE -->
  <div class="modal fade" id="update_queue" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Navbatni o'zgartirish</h6>
        </div>
        <form @submit.prevent="update_queue" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label for="patient_service">Mutahasislik: </label>
                  <select
                    id="patient_service"
                    class="form-select"
                    v-model="item_queue.service_id"
                    @change="get_doctor(item_queue.service_id, false)"
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
              <div class="col-md-6">
                <div class="form-group">
                  <label for="patient_service">Doktor: </label>
                  <select
                    id="patient_service"
                    class="form-select"
                    v-model="item_queue.doctor_id"
                    :disabled="!item_queue.service_id"
                    @change="get_room(false, index)"
                    required
                  >
                    <option
                      :value="doctor.id"
                      v-for="doctor in doctors"
                      :key="doctor"
                    >
                      {{ doctor.user.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <label for="patient_room">Xona: </label>
                <div class="input-group">
                  <input
                    type="number"
                    min="0"
                    id="patient_room"
                    class="form-control"
                    v-model="item_queue.room"
                    :disabled="!item_queue.doctor_id"
                    required
                  />
                  <span class="input-group-text">xona</span>
                </div>
              </div>
              <div class="col-md-6">
                <label for="times">Vaqt: </label>
                <select
                  class="form-control"
                  id="times"
                  v-model="item_queue.time"
                  :disabled="!queues_info.date"
                  required
                >
                  <option
                    :value="time.time"
                    v-for="time in item_queue.times"
                    :key="time"
                    :disabled="!time.possible"
                  >
                    {{ time.queue_number + " - navbat " + time.time }}
                  </option>
                </select>
              </div>
              <div class="col-md-12">
                <div class="form-check py-4">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="hasconsultation2"
                    v-model="item_queue.hasConsultation"
                  />
                  <label class="form-check-label" for="hasconsultation2"
                    >Konsultatsiya</label
                  >
                </div>
              </div>

              <div class="col-12">
                <multiselect
                  v-model="item_queue.procedures"
                  mode="tags"
                  placeholder="Muolaja tanlash"
                  :options="procedures_data"
                  :searchable="true"
                  @click="
                    item_queue.service_id
                      ? $event.target.value
                        ? ''
                        : get_procedures(item_queue.service_id, '', false)
                      : ''
                  "
                  @keyup="
                    item_queue.service_id
                      ? get_procedures(
                          item_queue.service_id,
                          $event.target.value,
                          false
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
              close-que-edit
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

  <!-- CREATE QUEUE -->
  <div class="modal fade" id="create_queue" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Navbat qo'shish</h6>
        </div>
        <form @submit.prevent="create_queue" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="row" v-for="(queue, index) in body" :key="queue">
              <div class="col-md-6">
                <div class="form-group">
                  <label for="patient_service">Mutahasislik: </label>
                  <select
                    id="patient_service"
                    class="form-select"
                    v-model="queue.service_id"
                    @change="
                      get_doctor(queue.service_id, true, index);
                      get_procedures(queue.service_id, '', true, index);
                    "
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
              <div class="col-md-6">
                <div class="form-group">
                  <label for="patient_service">Doktor: </label>
                  <select
                    id="patient_service"
                    class="form-select"
                    v-model="queue.doctor_id"
                    :disabled="!queue.service_id"
                    @change="get_room(true, index)"
                    required
                  >
                    <option
                      :value="doctor.id"
                      v-for="doctor in queue.doctors"
                      :key="doctor"
                    >
                      {{ doctor.user.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <label for="patient_room">Xona: </label>
                <div class="input-group">
                  <input
                    type="number"
                    min="0"
                    id="patient_room"
                    class="form-control"
                    v-model="queue.room"
                    :disabled="!queue.doctor_id"
                    required
                  />
                  <span class="input-group-text">xona</span>
                </div>
              </div>
              <div class="col-md-6">
                <label for="times">Vaqt: </label>
                <select
                  class="form-control"
                  id="times"
                  v-model="queue.time"
                  :disabled="!queues_info.date"
                  @change="
                    queue.number = queue.times.find(
                      (e) => e.time == queue.time
                    )?.queue_number
                  "
                  required
                >
                  <option
                    :value="time.time"
                    v-for="time in queue.times"
                    :key="time"
                    :disabled="!time.possible"
                  >
                    {{ time.queue_number + " - navbat " + time.time }}
                  </option>
                </select>
              </div>
              <div class="col-md-12">
                <div class="form-check py-4">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :id="`hasconsultation-add${index}`"
                    v-model="queue.hasConsultation"
                  />
                  <label
                    class="form-check-label"
                    :for="`hasconsultation-add${index}`"
                    >Konsultatsiya</label
                  >
                </div>
              </div>
              <div class="col-12">
                <multiselect
                  v-model="queue.procedures"
                  mode="tags"
                  placeholder="Muolaja tanlash"
                  :options="queue.procedures_data"
                  :searchable="true"
                  @click="
                    queue.service_id
                      ? $event.target.value
                        ? ''
                        : get_procedures(queue.service_id, '', true, index)
                      : ''
                  "
                  @keyup="
                    queue.service_id
                      ? get_procedures(
                          queue.service_id,
                          $event.target.value,
                          true,
                          index
                        )
                      : ''
                  "
                ></multiselect>
              </div>
              <hr class="mx-0 my-2" v-if="index < body.length - 1" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-que-add
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="
                body.push({
                  doctor_id: 0,
                  service_id: 0,
                  room: null,
                  time: '',
                  number: '',
                  user_id: 0,
                  hasConsultation: false,
                  procedures_data: [],
                  procedures: [], // id
                  times: [],
                  doctors: [],
                })
              "
            >
              <i class="fa-solid fa-circle-plus"></i>
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

  <!-- UPDATE INCPECTION -->
  <div class="modal fade" id="update_inspection" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Ko'rikni o'zgartirish</h6>
        </div>
        <form @submit.prevent="update_inspection" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="complaint">Shikoyat: </label>
              <input
                type="text"
                id="complaint"
                class="form-control"
                v-model="item_inspection.complaint"
                required
              />
            </div>

            <div class="form-group">
              <label for="responsible">Olib kelgan shaxs: </label>
              <input
                type="text"
                id="responsible"
                class="form-control"
                v-model="item_inspection.responsible"
                required
              />
            </div>

            <div class="form-group">
              <label for="treatment">Davolanish turi: </label>
              <select
                id="treatment"
                class="form-select"
                v-model="item_inspection.treatment"
                required
              >
                <option value="ambulator">Ambulator</option>
                <option value="statsionar">Statsionar</option>
              </select>
            </div>

            <div class="row">
              <div class="col-6">
                <div class="form-group">
                  <label>Jami summa: </label>
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control"
                      :value="item_inspection.total_price"
                      disabled
                    />
                    <span class="input-group-text">so'm</span>
                  </div>
                </div>
              </div>
              <div class="col-6">
                <div class="form-group">
                  <label>To'lov summa: </label>
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control"
                      :value="
                        item_inspection.total_price - item_inspection.discount
                      "
                      disabled
                    />
                    <span class="input-group-text">so'm</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="discount">Chegirma narx: </label>
              <div class="input-group">
                <input
                  type="number"
                  id="discount"
                  class="form-control"
                  v-model="item_inspection.discount"
                  min="0"
                  required
                />
                <span class="input-group-text">so'm</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-inspection-edit
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

  <div class="modal fade" id="cashreg_confirm" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Tasdiqlash</h6>
        </div>
        <form @submit.prevent="confirm_inspection" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="confrim_cost">Narx: </label>
              <div class="input-group">
                <input
                  type="number"
                  id="confrim_cost"
                  class="form-control"
                  v-model="confirm_body.cost"
                  min="1"
                  required
                />
                <span class="input-group-text">so'm</span>
              </div>
            </div>
            <div class="form-group">
              <label for="confrim_discount">Chegirma narx: </label>
              <div class="input-group">
                <input
                  type="number"
                  id="confrim_discount"
                  class="form-control"
                  v-model="confirm_body.discount"
                  min="0"
                  required
                />
                <span class="input-group-text">so'm</span>
              </div>
            </div>
            <div class="form-group">
              <label>To'lov summa: </label>
              <div class="input-group">
                <input
                  type="number"
                  class="form-control"
                  :value="confirm_body.cost - confirm_body.discount"
                  disabled
                />
                <span class="input-group-text">so'm</span>
              </div>
            </div>
            <div class="form-group">
              <label for="confrim_cost">To'lov turi: </label>
              <select
                class="form-control"
                v-model="confirm_body.method"
                required
              >
                <option value="naqd">naqd</option>
                <option value="plastik">plastik</option>
                <option value="otkazma">otkazma</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-confirm
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!confirm_body.method"
            >
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

  <check ref="check" />
  <diagnosis-list ref="list" />
</template>

<script>
import DiagnosisList from "@/views/Confirm/DiagnosisList.vue";
import {
  cashreg_confirm,
  catchError,
  disabled,
  doctors_get,
  inspcetion_cancel,
  inspcetion_update,
  queues_get,
  queue_cancel,
  queue_create,
  queue_possibility,
  queue_update,
  services_get,
  service_procedures_get,
  success,
} from "../Utils/api";
import Pagination from "../Utils/Pagination.vue";
import Check from "./Check.vue";
export default {
  components: { Pagination, Check, DiagnosisList },
  name: "queue-info",
  props: {
    edit: { default: false, type: Boolean },
    cancel: { default: false, type: Boolean },
    confirm: { default: false, type: Boolean },
    print: { default: false, type: Boolean },
    patient_id: { default: 0, type: Number },
  },
  data() {
    return {
      queues_info: {},
      queues: [],
      page: 1,
      pages: 0,
      limit: 25,
      search: "",
      step: 1,
      loading: false,
      date: new Date().toISOString().slice(0, 10),
      current_date: new Date().toISOString().substr(0, 10),
      item_queue: {
        id: null,
        doctor_id: null,
        user_id: null,
        service_id: null,
        room: null,
        time: "",
        number: null,
        hasConsultation: false,
        procedures: [],
      },
      services: [],
      doctors: [],
      procedures_data: [],
      item_inspection: {},
      role: localStorage.getItem("role"),
      confirm_body: {
        inspection_id: null,
        method: "naqd",
        cost: null,
        discount: 0,
      },
      body: [
        {
          doctor_id: 0,
          service_id: 0,
          room: null,
          time: "",
          number: "",
          user_id: 0,
          hasConsultation: false,
          procedures_data: [],
          procedures: [], // id
          times: [],
          doctors: [],
        },
      ],
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      queues_get(
        page,
        limit,
        this.step,
        this.search,
        this.patient_id,
        this.date
      )
        .then((e) => {
          e.data.data.forEach((element) => {
            let total_price = null;
            element.queues.forEach((que) => {
              total_price += que.consultationPrice;
              que.queue_procedures.forEach((procedure) => {
                total_price += procedure.price;
              });
            });
            element.total_price = total_price;
          });
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
    cancel_queue(id) {
      this.$store.dispatch("setloading", { loading: true });
      queue_cancel(id)
        .then(() => {
          success().then(() => {
            this.get(this.page, this.limit);
            document.querySelector("[close-que-info]").click();
          });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
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
    get_doctor(e, bool, index) {
      doctors_get(1, 1000, 0, e)
        .then((e) => {
          if (bool) this.body[index].doctors = e.data.data;
          else this.doctors = e.data.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    get_room(bool, index) {
      let item = null;
      if (bool)
        item = this.body[index].doctors.find(
          (item) => item.id == this.body[index].doctor_id
        );
      else
        item = this.doctors.find(
          (item) => item.id == this.item_queue.doctor_id
        );

      if (bool) {
        this.body[index].room = Number(item.room);
        this.body[index].user_id = Number(item.user_id);
        this.get_time(
          this.body[index].room,
          this.queues_info?.date,
          true,
          index
        );
      } else {
        this.item_queue.room = Number(item.room);
        this.item_queue.user_id = Number(item.user_id);
      }
    },
    get_time(room, date, bool, index) {
      queue_possibility(
        room,
        date,
        bool ? this.body[index].user_id : this.item_queue.user_id
      )
        .then((e) => {
          bool
            ? (this.body[index].times = e.data)
            : (this.item_queue.times = e.data);
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
    update_queue() {
      disabled(true);
      this.loading = true;
      queue_update(this.item_queue)
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            document.querySelector("[close-que-edit]").click();
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    create_queue() {
      disabled(true);
      this.loading = true;
      queue_create(this.body, this.queues_info?.id)
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            this.body = [
              {
                doctor_id: 0,
                service_id: 0,
                room: null,
                time: "",
                number: "",
                user_id: 0,
                hasConsultation: false,
                procedures_data: [],
                procedures: [], // id
                times: [],
                doctors: [],
              },
            ];
            document.querySelector("[close-que-add]").click();
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    get_procedures(service_id, search, bool, index) {
      service_procedures_get(1, 10, service_id, search)
        .then((e) => {
          bool
            ? (this.body[index].procedures_data = [])
            : (this.procedures_data = []);
          e.data.data.forEach((element) => {
            if (bool)
              this.body[index].procedures_data.push({
                value: element.id,
                label: element.name,
              });
            else
              this.procedures_data.push({
                value: element.id,
                label: element.name,
              });
          });
        })
        .catch((error) => {
          catchError(error);
        });
    },
    values(queue) {
      let procedures = [];
      queue.queue_procedures.forEach((element) => {
        procedures.push(element.service_procedure.id);
      });
      this.item_queue = {
        id: queue.id,
        doctor_id: queue.doctor_id,
        user_id: queue.doctor.user_id,
        service_id: queue.service_id,
        room: queue.room,
        time: queue.time.slice(0, 5),
        number: queue.number,
        hasConsultation: queue.hasConsultation,
        procedures: procedures,
      };
    },
    cancel_inspcetion(id) {
      this.$store.dispatch("setloading", { loading: true });
      inspcetion_cancel(id)
        .then(() => {
          success().then(() => {
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    update_inspection() {
      disabled(true);
      this.loading = true;
      inspcetion_update(this.item_inspection)
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            this.get(this.page, this.limit);
            document.querySelector("[close-inspection-edit]").click();
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    confirm_inspection() {
      disabled(true);
      this.loading = true;
      cashreg_confirm(this.confirm_body)
        .then((response) => {
          disabled(false);
          this.loading = false;
          success("close-confirm").then(() => {
            this.get(this.page, this.limit);
            if (response.data == "done") {
              this.$refs.check.start(this.confirm_body.inspection_id);
            }
            this.confirm_body = {
              method: "naqd",
              inspection_id: null,
              cost: null,
              discount: 0,
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
  created() {
    this.get(this.page, this.limit);
  },
};
</script>
