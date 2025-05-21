<template>
  <div class="card">
    <div class="card-body">
      <div class="responsive-y" style="max-height: 79vh">
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
                <table class="table table-hover table-bordered table-sm mb-0">
                  <tbody>
                    <tr
                      v-for="(recipe, inc) in diagnosis.recipes"
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
          </div>
        </div>
        <h4 class="text-center m-4" v-if="!diagnosiss.length">
          Ma'lumot topilmadi !
        </h4>
      </div>
    </div>
  </div>
</template>

<script>
import { catchError, diagnosiss_get } from "../Utils/api";
import Pagination from "../Utils/Pagination.vue";

export default {
  name: "DiagnosisPatient",
  data() {
    return {
      diagnosiss: [],
      page: 1,
      pages: 0,
      limit: 25,
      id: this.$route.query.id,
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      diagnosiss_get(page, limit, this.id)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.diagnosiss = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
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
  components: { Pagination },
};
</script>

<style>
</style>