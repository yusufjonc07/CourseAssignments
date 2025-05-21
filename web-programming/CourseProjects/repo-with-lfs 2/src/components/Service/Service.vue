<template>
  <div class="card">
    <div class="card-body">
      <form @submit.prevent="add_service()">
        <h5 class="text-center">Mutaxasislik qo'shish</h5>
        <div class="row gap-2 d-flex justify-content-center">
          <div class="col-md-10">
            <div
              class="input-group my-2"
              v-for="(body, i) in bodies"
              :key="body"
            >
              <input
                type="text"
                :id="`service_name${i}`"
                class="form-control"
                v-model="body.name"
                placeholder="Mutaxasislik nomi"
                required
              />
              <button
                class="btn btn-danger"
                type="button"
                style="width: 65px"
                v-show="i || (!i && bodies.length > 1)"
                @click="bodies.splice(i, 1)"
              >
                <i class="fa-solid fa-circle-xmark"></i>
              </button>
              <button
                class="btn btn-primary"
                type="button"
                style="width: 65px"
                v-show="i == bodies.length - 1"
                @click="bodies.push({ name: '', disabled: false })"
                @click.passive="form(`service_name${i}`)"
              >
                <i class="fa-solid fa-circle-plus"></i>
              </button>
              <button
                type="submit"
                class="btn btn-secondary"
                style="width: 65px"
                v-show="i == bodies.length - 1"
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
          </div>
        </div>
      </form>
      <div class="row my-2 gap-2 d-flex justify-content-center">
        <div class="col-md-10 responsive-y" style="max-height: 71.8vh">
          <ul class="list-group list-group-light list-group-sm">
            <li
              class="list-group-item list-group-item-action px-3 border-0"
              v-for="service in services"
              :key="service"
              @dblclick="id = service.id"
            >
              <div v-if="id != service.id">
                {{ service.real_name }}
                <button
                  class="btn btn-secondary float-end mx-1"
                  data-mdb-toggle="modal"
                  data-mdb-target="#modal_procedures"
                  @click="
                    $refs.procedure.body.service_id = service.id;
                    $refs.procedure.get(1, 25);
                  "
                >
                  <i class="fa-solid fa-eye"></i>
                </button>
                <button
                  class="btn btn-warning float-end"
                  @click="id = service.id"
                >
                  <i class="fa-solid fa-pen"></i>
                </button>
              </div>
              <div v-else>
                <form @submit.prevent="update_service(service)">
                  <div class="input-group">
                    <input
                      type="text"
                      class="form-control rounded"
                      v-model="service.name"
                    />
                    <button
                      class="btn btn-secondary mx-1 rounded"
                      :disabled="!service.name"
                      type="submit"
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
                    <button
                      class="btn btn-danger rounded"
                      type="button"
                      @click="
                        id = null;
                        service.name = service.real_name;
                      "
                    >
                      <i class="fa-solid fa-circle-xmark"></i>
                    </button>
                  </div>
                </form>
              </div>
            </li>
          </ul>
          <h4 class="text-center m-4" v-if="!services.length">
            Ma'lumot topilmadi !
          </h4>
          <Pagination :page="page" :pages="pages" :limit="limit" @get="get" />
        </div>
      </div>
    </div>
  </div>

  <Procedure ref="procedure" />
</template>

<script>
import {
  catchError,
  disabled,
  services_get,
  service_create,
  service_update,
  success,
} from "../Utils/api";
import Pagination from "../Utils/Pagination.vue";
import Procedure from "./Procedure.vue";
export default {
  name: "ServiceComponent",
  data() {
    return {
      bodies: [
        {
          name: "",
          disabled: false,
        },
      ],
      loading: false,
      services: [],
      page: 1,
      pages: 0,
      limit: 25,
      id: null,
    };
  },
  methods: {
    add_service() {
      disabled(true);
      this.loading = true;
      service_create(this.bodies)
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            this.get(this.page, this.limit);
            this.bodies = [{ name: "", disabled: false }];
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
      services_get(page, limit)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          e.data.data.forEach((element) => {
            element.real_name = element.name;
          });
          this.services = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    update_service(body) {
      disabled(true);
      this.loading = true;
      service_update(body)
        .then(() => {
          disabled(false);
          this.loading = false;
          this.id = null;
          success().then(() => {
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    form(e) {
      document.getElementById(e).focus();
    },
  },
  created() {
    this.get(this.page, this.limit);
  },
  components: { Pagination, Procedure },
};
</script>
