<template>
  <!-- UPDATE DATE -->
  <div class="modal fade" id="update_date" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Qayta a'loqa vaqtini o'zgartirish</h6>
        </div>
        <form
          @submit.prevent="$emit('update_date', item)"
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="update_date">Qayta a'loqa vaqti: </label>
              <input
                type="datetime-local"
                id="update_date"
                class="form-control"
                v-model="item.plan_date"
                required
              />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-date-update
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!item.plan_date"
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
  <!-- ADD DATE -->
  <div class="modal fade" id="add_date" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Qayta a'loqa vaqtini qo'shish</h6>
        </div>
        <form
          @submit.prevent="$emit('create_date', body)"
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2">
            <div class="form-group">
              <div class="dropdown w-100">
                <button
                  class="form-control dropdown-toggle"
                  type="button"
                  id="auto_complete"
                  data-mdb-toggle="dropdown"
                  @click="!patients.length ? get() : ''"
                >
                  {{ body.item ? body.item : "Bemorlar" }}
                </button>
                <ul
                  class="dropdown-menu w-100 patients-scroll"
                  aria-labelledby="auto_complete"
                  @scroll="scroll()"
                >
                  <li>
                    <input
                      type="search"
                      class="form-control form-control-sm"
                      placeholder="Qidiruv"
                      v-model="search"
                      @keyup="
                        page = 1;
                        get();
                        $store.dispatch('setloading', { loading: false });
                      "
                    />
                  </li>
                  <li
                    v-for="patient in patients"
                    :key="patient"
                    class="dropdown-item"
                    @click="
                      body.patient_id = patient.id;
                      body.item = patient.name + ' ' + patient.surename;
                    "
                    :class="patient.id == body.patient_id ? 'active' : ''"
                  >
                    {{ patient.name }} {{ patient.surename }}
                  </li>
                  <li v-show="!patients.length" class="dropdown-item">
                    Ma'lumot topilmadi !
                  </li>
                </ul>
              </div>
            </div>
            <div class="form-group">
              <label for="add_date">Qayta a'loqa vaqti: </label>
              <input
                type="datetime-local"
                id="add_date"
                class="form-control"
                v-model="body.plan_date"
                required
              />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-date
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!body.patient_id || !body.plan_date"
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
  <!-- TALKED -->
  <div class="modal fade" id="talked" tabindex="-1">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">A'loqaga chiqish</h6>
        </div>
        <form @submit.prevent="$emit('talked', talk)" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="row" v-if="queue.queue">
              <div class="col-12">
                <div class="row">
                  <div class="col-6">
                    <h6>
                      <b> Bemor: </b>
                      {{
                        queue.patient.name +
                        " " +
                        queue.patient.surename +
                        " " +
                        queue.patient.fathername
                      }}
                    </h6>
                    <h6>
                      <b> Manzil: </b>
                      {{
                        queue.patient.region.name +
                        " " +
                        queue.patient.state.name +
                        " " +
                        queue.patient.address
                      }}
                    </h6>
                    <h6>
                      <b> Telefon raqam: </b>
                      <a
                        :href="`tel:+998${queue.patient.phone}`"
                        class="text-dark"
                      >
                        +998 {{ format(queue.patient.phone) }}
                      </a>
                    </h6>
                  </div>
                  <div class="col-6">
                    <h6><b> Doktor: </b>{{ queue.queue.doctor.user.name }}</h6>
                    <h6><b> Ko'rik:</b> {{ queue.queue.service.name }}</h6>
                    <h6>
                      <b> Olib kelgan shaxs:</b> {{ queue.queue.responsible }}
                    </h6>
                  </div>
                </div>
                <hr />
              </div>
              <div class="col-12">
                <h5 class="text-center">Tashxislar</h5>
                <table class="table table-hover table-sm mb-0">
                  <thead>
                    <tr>
                      <th>№</th>
                      <th>Kasallik</th>
                      <th>Shikoyat</th>
                      <th>Sana</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(diagnosis, inc) in queue.queue.diagnosiss"
                      :key="diagnosis"
                    >
                      <td>{{ inc + 1 }}</td>
                      <td>{{ diagnosis.illness }}</td>
                      <td>{{ diagnosis.description }}</td>
                      <td>{{ diagnosis.created_at.replace("T", " ") }}</td>
                    </tr>
                  </tbody>
                </table>
                <hr />
              </div>
              <div class="col-12">
                <h5 class="text-center">Retseptlar</h5>
                <table class="table table-hover table-sm mb-0">
                  <tbody>
                    <tr
                      v-for="(recipe, inc) in queue.queue.recipes"
                      :key="recipe"
                    >
                      <td>
                        {{ inc + 1 }}. {{ recipe.drug?.name }}
                        <span v-show="recipe.comment && recipe.drug">-</span>
                        {{ recipe.comment }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <hr v-show="queue.queue" />
            <div class="row">
              <div class="col">
                <div class="form-group">
                  <label for="type">Qo'ng'iroq turi: </label>
                  <select
                    id="type"
                    class="form-control"
                    v-model="talk.talk_type"
                    required
                  >
                    <option value="ijobiy">ijobiy</option>
                    <option value="salbiy">salbiy</option>
                    <option value="etiroz">e'tiroz</option>
                  </select>
                </div>
              </div>
              <div class="col">
                <div class="form-group">
                  <label for="comment">Izoh: </label>
                  <textarea
                    id="comment"
                    class="form-control"
                    v-model="talk.comment"
                    required
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-talked
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!talk.comment || !talk.talk_type"
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
</template>

<script>
import { catchError, patients_get } from "../Utils/api";
export default {
  name: "ContactModal",
  emits: ["update_date", "create_date", "talked"],
  props: ["item", "loading", "recall_id", "queue"],
  data() {
    return {
      body: {
        item: "",
        patient_id: null,
        plan_date: "",
      },
      talk: {
        id: null,
        comment: "",
        talk_type: "ijobiy",
      },
      page: 1,
      pages: 0,
      search: "",
      patients: [],
    };
  },
  methods: {
    get() {
      this.$store.dispatch("setloading", { loading: true });
      patients_get(this.page, 10, this.search)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.patients = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    scroll() {
      let div = document.querySelector(".patients-scroll");
      if (div.scrollTop + div.clientHeight >= div.scrollHeight - 10) {
        if (this.page < this.pages) {
          patients_get(this.page + 1, 10)
            .then((e) => {
              this.page = e.data.page;
              this.patients = this.patients.concat(e.data.data);
            })
            .catch((error) => {
              catchError(error);
            });
        }
      }
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
  },
  watch: {
    recall_id(e) {
      this.talk.id = e;
    },
  },
};
</script>
