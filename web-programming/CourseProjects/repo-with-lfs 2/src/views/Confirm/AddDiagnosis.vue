<template>
  <h4 class="text-center fw-normal">
    {{ queue?.inspection?.patient.name }}ga qo'yilgan tashxislar
  </h4>
  <div class="row">
    <div class="col-md-4">
      <button
        class="btn btn-sm btn-block btn-secondary"
        data-mdb-toggle="modal"
        data-mdb-target="#add_diagnosis"
        @click="get_illness()"
      >
        <i class="fa-solid fa-user-plus"></i> Tashxis qo'shish
      </button>
    </div>
    <div class="col-md-4 my-1">
      <h5 class="card-title text-center">{{ queue?.queue_count }} - marta</h5>
    </div>
    <div class="col-md-4">
      <router-link
        :to="{
          name: 'patient',
          query: {
            id: $route.query.patient_id,
            name: queue?.inspection?.patient.name,
          },
        }"
        class="btn btn-sm btn-block btn-secondary"
      >
        <i class="fa-solid fa-eye"></i> Bemor haqida
      </router-link>
    </div>
  </div>
  <hr />

  <div class="responsive-y">
    <div class="accordion" id="accordion">
      <div
        class="accordion-item"
        v-for="diagnosis in queue?.diagnosiss"
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
                  class="btn btn-sm btn-warning mx-1 float-end"
                  data-mdb-toggle="modal"
                  data-mdb-target="#update_diagnosis"
                  @click="
                    get_illness();
                    get_templates(diagnosis.illness);
                    item = {
                      id: diagnosis.id,
                      illness: diagnosis.illness,
                      description: diagnosis.description,
                    };
                  "
                >
                  <i class="fa-solid fa-edit"></i>
                </button>
                <button
                  class="badge badge-primary float-end p-2 border-0"
                  data-mdb-toggle="collapse"
                  :data-mdb-target="`#collapse${diagnosis.id}`"
                  aria-expanded="false"
                  :aria-controls="`collapse${diagnosis.id}`"
                  @click="diagnosis_id = diagnosis.id"
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
            <div class="row">
              <div class="col-md-4">
                <button
                  class="btn btn-sm btn-secondary"
                  data-mdb-toggle="modal"
                  data-mdb-target="#add_recipe"
                >
                  <i class="fa fa-user-plus"></i> Retsept qo'shish
                </button>
              </div>
              <div class="col-md-4">
                <h5 class="text-center fw-normal">Retseptlar</h5>
              </div>
              <div class="col-md-4"></div>
            </div>
            <table class="table table-hover table-bordered table-sm mb-0">
              <tbody>
                <tr v-for="(recipe, inc) in diagnosis.recipes" :key="recipe">
                  <td>
                    {{ inc + 1 }}. {{ recipe.drug?.name }}
                    <span v-show="recipe.comment && recipe.drug">-</span>
                    {{ recipe.comment }}
                    <button
                      class="btn btn-sm btn-danger float-end"
                      @click="remove_recipe(recipe.id)"
                    >
                      <i class="fa-solid fa-circle-xmark"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-2" v-if="queue?.diagnosiss.length">
      <div class="col">
        <button class="btn btn-sm btn-block btn-success" @click="finish()">
          <i class="fa-solid fa-flag-checkered"></i> Yakunlash
        </button>
      </div>
    </div>
    <h4 class="text-center m-4" v-if="!queue?.diagnosiss.length">
      Ma'lumot topilmadi !
    </h4>
  </div>

  <DiagnosisModal
    :loading="loading"
    @create_diagnosis="create_diagnosis"
    @update_diagnosis="update_diagnosis"
    @create_recipe="create_recipe"
    :item="item"
    :templates="templates"
    :illnesses="illnesses"
    :queue="queue"
    @get_templates="get_templates"
  />
</template>

<script>
import DiagnosisModal from "@/components/Confirm/DiagnosisModal.vue";
import {
  catchError,
  diagnosis_confirm,
  diagnosis_create,
  diagnosis_update,
  disabled,
  illnesses_get,
  queue_cancel,
  queue_get,
  recipe_create,
  recipe_delete,
  recipe_t_get,
  success,
} from "@/components/Utils/api";
import Swal from "sweetalert2";
export default {
  name: "AddDiagnosis",
  data() {
    return {
      search: "",
      loading: false,
      item: {},
      queue: null,
      diagnosis_id: null,
      service_id: this.$route.query.service_id,
      current_date: new Date().toISOString().substr(0, 10),
      templates: [],
      illnesses: [],
      body: {
        queue_id: this.$route.query.queue_id,
        next_date: "none",
      },
    };
  },
  methods: {
    get() {
      this.$store.dispatch("setloading", { loading: true });
      queue_get(this.$route.query.queue_id)
        .then((e) => {
          this.queue = e.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    create_diagnosis(e) {
      disabled(true);
      this.loading = true;
      diagnosis_create(e)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-diagnosis").then(() => {
            this.get(this.page, this.limit);
            e.illness = "";
            e.illness_id = null;
            e.description = "";
            e.recipes = [
              {
                drug_id: null,
                unit: "",
              },
            ];
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    update_diagnosis(e) {
      disabled(true);
      this.loading = true;
      diagnosis_update(e)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-diagnosis-u").then(() => {
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    remove_recipe(id) {
      recipe_delete(id)
        .then(() => {
          success().then(() => {
            this.get();
          });
        })
        .catch((error) => {
          catchError(error);
        });
    },
    create_recipe(e) {
      disabled(true);
      this.loading = true;
      recipe_create(e.recipes, this.diagnosis_id)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-recipe").then(() => {
            this.get();
            e.recipes = [
              {
                unit: "",
                drug_id: null,
              },
            ];
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    finish() {
      Swal.fire({
        title: "Yakunlamoqchimisiz!",
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: "Yakunlash",
        denyButtonText: "Qayta ko'rik sanasi",
        cancelButtonText: "Bekor qilish",
      }).then((result) => {
        if (result.isConfirmed) {
          this.finish_function();
        } else if (result.isDenied) {
          Swal.fire({
            title: "Qayta ko'rik sanasini belgilang!",
            showCancelButton: true,
            html: `<input type="date" min="${this.current_date}" class="form-control" id="date" />`,
            confirmButtonText: "Yakunlash",
            cancelButtonText: "Bekor qilish",
          }).then((res) => {
            if (res.isConfirmed) {
              let value = document.getElementById("date").value;
              this.body.next_date = value;
              this.finish_function();
            }
          });
        }
      });
    },
    cancel(id) {
      Swal.fire({
        text: "Bekor qilmoqchimisiz !",
        target: "#custom-cancel",
        customClass: {
          container: "position-absolute",
        },
        toast: true,
        position: "bottom-left",
        confirmButtonText: "Xa",
        showCancelButton: true,
        cancelButtonColor: "#DC4C64",
        cancelButtonText: "Yo'q",
      }).then((e) => {
        if (e.isConfirmed == true) {
          this.$store.dispatch("setloading", { loading: true });
          queue_cancel(id)
            .then(() => {
              success().then(() => {
                this.$router.go(-1);
              });
            })
            .catch((error) => {
              this.$store.dispatch("setloading", { loading: false });
              catchError(error);
            });
        }
      });
    },
    get_illness() {
      this.$store.dispatch("setloading", { loading: true });
      illnesses_get(1, 1000, "", this.service_id)
        .then((e) => {
          this.illnesses = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    get_templates(e) {
      this.templates = [];
      let item = this.illnesses.find((item) => item.name == e);
      if (item) {
        this.$store.dispatch("setloading", { loading: true });
        recipe_t_get(1, 1000, "", item.id)
          .then((e) => {
            this.templates = e.data.data;
            this.$store.dispatch("setloading", { loading: false });
          })
          .catch((error) => {
            this.$store.dispatch("setloading", { loading: false });
            catchError(error);
          });
      }
    },
    finish_function() {
      this.$store.dispatch("setloading", { loading: true });
      diagnosis_confirm(this.body)
        .then(() => {
          success().then(() => {
            this.$router.go(-1);
          });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
  },
  created() {
    this.get();
  },
  components: { DiagnosisModal },
};
</script>
