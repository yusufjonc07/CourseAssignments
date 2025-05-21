<template>
  <div class="modal fade" id="modal_procedures" tabindex="-1">
    <div class="modal-dialog modal-xl modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <div class="btn-group">
            <button
              class="btn btn-sm"
              :class="
                body.type == 'muolaja' ? 'btn-primary' : 'btn-outline-primary'
              "
              @click="
                body.type = 'muolaja';
                get(1, 25);
              "
            >
              Muolaja
            </button>
            <button
              class="btn btn-sm"
              :class="
                body.type == 'tekshiruv' ? 'btn-primary' : 'btn-outline-primary'
              "
              @click="
                body.type = 'tekshiruv';
                get(1, 25);
              "
            >
              Tekshiruv
            </button>
          </div>
          <button
            type="button"
            class="btn-close"
            data-mdb-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="add_procedure()">
            <div class="row">
              <div class="col-12 col-sm-12 col-md col-lg">
                <label>{{ title }} nomi</label>
                <input
                  type="text"
                  id="procedure_name"
                  class="form-control"
                  v-model="body.name"
                  :placeholder="`${title} nomi`"
                  required
                />
              </div>
              <div class="col-12 col-sm-12 col-md col-lg">
                <label>KPI</label>
                <div class="input-group">
                  <input
                    type="number"
                    class="form-control"
                    v-model="body.kpi"
                    min="0"
                    max="100"
                    placeholder="KPI"
                    required
                  />
                  <span class="input-group-text">%</span>
                </div>
              </div>
              <div class="col-12 col-sm-12 col-md col-lg">
                <label>Kattalar {{ title }}si</label>
                <div
                  class="input-group"
                  :title="Intl.NumberFormat().format(body.price)"
                  currency
                >
                  <input
                    type="number"
                    id="procedure_price"
                    class="form-control"
                    v-model="body.price"
                    min="0"
                    :placeholder="`Kattalar ${title}si`"
                    required
                  />
                  <span class="input-group-text">so'm</span>
                </div>
              </div>
              <div class="col-12 col-sm-12 col-md col-lg">
                <label>Kichiklar {{ title }}si</label>

                <div
                  class="input-group"
                  :title="Intl.NumberFormat().format(body.price_min)"
                  currency
                >
                  <input
                    type="number"
                    id="procedure_price_min"
                    class="form-control"
                    v-model="body.price_min"
                    min="0"
                    :placeholder="`Kichiklar ${title}si`"
                    required
                  />
                  <span class="input-group-text">so'm</span>
                </div>
              </div>
              <div class="col-md-auto col-lg-auto col-12 d-flex mt-auto">
                <button type="submit" class="btn btn-secondary w-100">
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
            </div>
          </form>
          <div class="row my-2 px-2 d-flex justify-content-center">
            <div class="responsive" style="max-height: 74vh">
              <table
                class="table table-hover table-sm align-middle mb-0 bg-white"
              >
                <thead class="bg-blue">
                  <tr>
                    <th>№</th>
                    <th>{{ title }} nomi</th>
                    <th>KPI</th>
                    <th>Kattalar {{ title }}si</th>
                    <th>Kichiklar {{ title }}si</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(procedure, i) in procedures" :key="procedure">
                    <td>{{ i + 1 }}</td>
                    <td>{{ procedure.name }}</td>
                    <td>{{ Intl.NumberFormat().format(procedure.kpi) }}%</td>
                    <td>
                      {{ Intl.NumberFormat().format(procedure.price) }} so'm
                    </td>
                    <td>
                      {{ Intl.NumberFormat().format(procedure.price_min) }} so'm
                    </td>
                    <td>
                      <button
                        class="btn btn-warning float-end"
                        data-mdb-toggle="modal"
                        data-mdb-target="#procedure_edit"
                        @click="
                          item = {
                            id: procedure.id,
                            name: procedure.name,
                            type: procedure.type,
                            price: procedure.price,
                            service_id: procedure.service_id,
                            price_min: procedure.price_min,
                            kpi: procedure.kpi || 0,
                          }
                        "
                      >
                        <i class="fa-solid fa-pen"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>

              <h4 class="text-center m-4" v-if="!procedures.length">
                Ma'lumot topilmadi !
              </h4>
              <Pagination
                :page="page"
                :pages="pages"
                :limit="limit"
                @get="get"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- UPDATE PROCEDURE -->
  <div class="modal fade" id="procedure_edit">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">{{ title }}ni o'zgartirish</h6>
        </div>
        <form @submit.prevent="update_procedure()" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="form-group">
              <label>{{ title }} nomi</label>
              <input
                type="text"
                id="procedure_name"
                class="form-control"
                v-model="item.name"
                :placeholder="`${title} nomi`"
                required
              />
            </div>
            <div class="form-group">
              <label>KPI</label>
              <div class="input-group">
                <input
                  type="number"
                  class="form-control"
                  v-model="item.kpi"
                  min="0"
                  max="100"
                  placeholder="KPI"
                  required
                />
                <span class="input-group-text">%</span>
              </div>
            </div>
            <div class="form-group">
              <label>Kattalar {{ title }}si</label>
              <div
                class="input-group"
                :title="Intl.NumberFormat().format(item.price)"
                currency
              >
                <input
                  type="number"
                  id="procedure_price"
                  class="form-control"
                  v-model="item.price"
                  min="0"
                  :placeholder="`Kattalar ${title}si`"
                  required
                />
                <span class="input-group-text">so'm</span>
              </div>
            </div>
            <div class="form-group">
              <label>Kichiklar {{ title }}si</label>

              <div
                class="input-group"
                :title="Intl.NumberFormat().format(item.price_min)"
                currency
              >
                <input
                  type="number"
                  id="procedure_price_min"
                  class="form-control"
                  v-model="item.price_min"
                  min="0"
                  :placeholder="`Kichiklar ${title}si`"
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
              data-mdb-toggle="modal"
              data-mdb-target="#modal_procedures"
              close-procedure
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!item.name || !item.price || !item.price_min"
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
import {
  catchError,
  disabled,
  service_procedures_get,
  service_procedure_create,
  service_procedure_update,
  success,
} from "../Utils/api";
import Pagination from "../Utils/Pagination.vue";
export default {
  name: "procedure",
  components: { Pagination },
  data() {
    return {
      body: {
        name: "",
        price: 0,
        price_min: 0,
        service_id: 0,
        kpi: 0,
        type: "muolaja",
      },
      loading: false,
      procedures: [],
      page: 1,
      pages: 0,
      limit: 25,
      id: null,
      item: {},
    };
  },
  computed: {
    title() {
      return this.body.type == "muolaja" ? "Muolaja" : "Tekshiruv";
    },
  },
  methods: {
    add_procedure() {
      disabled(true);
      this.loading = true;
      service_procedure_create(this.body)
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            this.get(this.page, this.limit);
            this.body.name = "";
            this.body.price = 0;
            this.body.price_min = 0;
            this.body.type = "muolaja";
            this.body.kpi = 0;
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      service_procedures_get(
        page,
        limit,
        this.body.service_id,
        "",
        this.body.type
      )
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.procedures = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    update_procedure() {
      disabled(true);
      this.loading = true;
      service_procedure_update(this.item)
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            this.get(this.page, this.limit);
            this.item = {};
            document.querySelector("[close-procedure]").click();
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
  },
};
</script>
