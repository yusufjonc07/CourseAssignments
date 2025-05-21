<template>
  <div class="card">
    <div class="card-body">
      <form @submit.prevent="add_source()">
        <h5 class="text-center">Manba qo'shish</h5>
        <div class="row gap-2 d-flex justify-content-center">
          <div class="col-md-10">
            <div
              class="input-group my-2"
              v-for="(body, i) in bodies"
              :key="body"
            >
              <input
                type="text"
                :id="`source_name${i}`"
                class="form-control"
                v-model="body.name"
                placeholder="Manba nomi"
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
                @click="bodies.push({ name: '' })"
                @click.passive="form(`source_name${i + 1}`)"
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
              v-for="source in sources"
              :key="source"
              @dblclick="id = source.id"
            >
              <div v-if="id != source.id">
                {{ source.real_name }}
                <button
                  class="btn btn-warning float-end"
                  @click="id = source.id"
                >
                  <i class="fa-solid fa-pen"></i>
                </button>
              </div>
              <div v-else>
                <form @submit.prevent="update_source(source)">
                  <div class="input-group">
                    <input
                      type="text"
                      class="form-control rounded"
                      v-model="source.name"
                    />
                    <button
                      class="btn btn-secondary mx-1 rounded"
                      :disabled="!source.name"
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
                        source.name = source.real_name;
                      "
                    >
                      <i class="fa-solid fa-circle-xmark"></i>
                    </button>
                  </div>
                </form>
              </div>
            </li>
          </ul>
          <h4 class="text-center m-4" v-if="!sources.length">
            Ma'lumot topilmadi !
          </h4>
          <Pagination :page="page" :pages="pages" :limit="limit" @get="get" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  catchError,
  disabled,
  sources_get,
  source_create,
  source_update,
  success,
} from "../Utils/api";
import Pagination from "../Utils/Pagination.vue";
export default {
  name: "SourceComponent",
  data() {
    return {
      bodies: [
        {
          name: "",
        },
      ],
      loading: false,
      sources: [],
      page: 1,
      pages: 0,
      limit: 25,
      id: null,
    };
  },
  methods: {
    add_source() {
      disabled(true);
      this.loading = true;
      source_create(this.bodies)
        .then(() => {
          disabled(false);
          this.loading = false;
          success().then(() => {
            this.get(this.page, this.limit);
            this.bodies = [{ name: "" }];
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
      sources_get(page, limit)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          e.data.data.forEach((element) => {
            element.real_name = element.name;
          });
          this.sources = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    update_source(body) {
      disabled(true);
      this.loading = true;
      source_update(body)
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
  components: { Pagination },
};
</script>
