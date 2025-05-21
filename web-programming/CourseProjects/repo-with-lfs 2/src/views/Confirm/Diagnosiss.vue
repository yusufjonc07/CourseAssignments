<template>
  <h3 class="text-center fw-normal">Tashxislar</h3>
  <div class="row">
    <div class="col-md-4">
      <input
        type="date"
        v-model="date"
        class="form-control form-control-sm"
        @change="get(1, 25)"
      />
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
          <th>Vaqt</th>
          <th>Bemor</th>
          <th>Doktor</th>
          <th>Ko'rik</th>
          <th>Tashxis</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(queue, i) in queues" :key="queue">
          <td>{{ i + 1 }}</td>
          <td>{{ queue.time }}</td>
          <td>
            {{
              queue.inspection.patient?.name +
              " " +
              queue.inspection.patient?.surename
            }}
          </td>
          <td>{{ queue.doctor.user.name }}</td>
          <td>{{ queue.service.name }}</td>
          <td>
            <button
              class="btn btn-sm btn-primary position-relative"
              data-mdb-toggle="modal"
              data-mdb-target="#diagnosis"
              @click="
                diagnosiss = queue.diagnosiss;
                queue_id = queue.id;
              "
            >
              <i class="fa-solid fa-clipboard-list"></i>
              <span
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill badge-primary"
              >
                {{ queue.diagnosiss.length }}
                <span class="visually-hidden">unread messages</span>
              </span>
            </button>
            <button
              type="button"
              class="btn btn-secondary btn-sm mx-1"
              @click="complete(queue.id)"
            >
              <i class="fa-solid fa-circle-check"></i>
            </button>
            <div id="custom-finish"></div>
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!queues.length">Ma'lumot topilmadi !</h4>
    <Pagination :page="page" :pages="pages" :limit="limit" @get="get" />
  </div>

  <!-- DIAGNOSIS -->
  <div class="modal fade" id="diagnosis" tabindex="-1">
    <div class="modal-dialog modal-xl modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Tashxislar</h6>
        </div>
        <div class="modal-body">
          <div class="responsive-y">
            <div class="accordion" id="accordion">
              <div
                class="accordion-item"
                v-for="diagnosis in diagnosiss"
                :key="diagnosis"
              >
                <h2 class="accordion-header" :id="`heading${diagnosis.id}`">
                  <button
                    class="accordion-button collapsed"
                    type="button"
                    style="cursor: default"
                  >
                    <div class="row w-100">
                      <div class="col-md-4 col-sm-12">
                        <i class="fa-solid fa-virus"></i> Kasallik:
                        {{ diagnosis.illness }}
                      </div>
                      <div class="col-md-4 col-sm-12">
                        <i class="fa-solid fa-comment"></i> Izoh:
                        {{ diagnosis.description }}
                      </div>
                      <div class="col-md-4 col-sm-12">
                        <i class="fa-solid fa-clock"></i> Sana:
                        {{ diagnosis.created_at.replace("T", " ") }}
                        <button
                          class="badge badge-primary float-end p-2 border-0"
                          data-mdb-toggle="collapse"
                          :data-mdb-target="`#collapse${diagnosis.id}`"
                          aria-expanded="false"
                          :aria-controls="`collapse${diagnosis.id}`"
                        >
                          Retsept: {{ diagnosis.recipes.length }}
                        </button>
                      </div>
                    </div>
                  </button>
                </h2>
                <div
                  :id="`collapse${diagnosis.id}`"
                  class="accordion-collapse collapse"
                  :aria-labelledby="`heading${diagnosis.id}`"
                  data-mdb-parent="#accordion"
                >
                  <div class="accordion-body">
                    <table
                      class="table table-hover table-bordered table-sm mb-0"
                    >
                      <tbody>
                        <tr
                          v-for="(recipe, inc) in diagnosis.recipes"
                          :key="recipe"
                        >
                          <td>
                            {{ inc + 1 }}. {{ recipe.drug?.name }}
                            <span v-show="recipe.comment && recipe.drug"
                              >-</span
                            >
                            {{ recipe.comment }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <h4 class="text-center m-4" v-if="!diagnosiss.length">
              Ma'lumot topilmadi !
            </h4>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-mdb-dismiss="modal"
          >
            <i class="fa-solid fa-circle-xmark"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
  <diagnosis-list ref="list" />
</template>

<script>
import {
  catchError,
  queues_all_get,
  queue_complete,
  success,
} from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
import Swal from "sweetalert2";
import DiagnosisList from "./DiagnosisList.vue";
export default {
  name: "Diagnosiss",
  data() {
    return {
      queues: [],
      page: 1,
      pages: 0,
      limit: 25,
      search: "",
      step: 4,
      diagnosiss: [],
      print: {},
      queue_id: null,
      date: new Date().toISOString().slice(0, 10),
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      queues_all_get(page, limit, this.step, this.search, 0, this.date)
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
    complete(id) {
      Swal.fire({
        text: "Yakunlamoqchimisiz !",
        target: "#custom-finish",
        customClass: {
          container: "position-absolute",
        },
        toast: true,
        position: "bottom-right",
        confirmButtonText: "Xa",
        showCancelButton: true,
        cancelButtonColor: "#DC4C64",
        cancelButtonText: "Yo'q",
      }).then((e) => {
        if (e.isConfirmed == true) {
          queue_complete(id)
            .then(() => {
              success().then(() => {
                this.get(this.page, this.limit);
                this.$refs.list.start(id);
              });
            })
            .catch((error) => {
              catchError(error);
            });
        }
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
  },
  created() {
    this.get(this.page, this.limit);
  },
  components: { Pagination, DiagnosisList },
};
</script>
