<template>
  <!-- ADD DIAGNOSIS -->
  <div class="modal fade" id="add_diagnosis">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Yangi Tashxis qo'shish</h6>
        </div>
        <form
          @submit.prevent="$emit('create_diagnosis', body)"
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2 diagnosis_create">
            <div class="row">
              <div class="col-md-6 col-sm-6">
                <div class="form-group">
                  <label for="illness">Kasallik nomi:</label>
                  <input
                    list="illnesses"
                    class="form-control"
                    id="illness"
                    v-model="body.illness"
                    autocomplete="off"
                    @keyup="$emit('get_templates', body.illness)"
                    @change="$emit('get_templates', body.illness)"
                  />
                  <datalist id="illnesses">
                    <option v-for="illness in illnesses" :key="illness">
                      {{ illness.name }}
                    </option>
                  </datalist>
                </div>
              </div>
              <div class="col-md-6 col-sm-6">
                <div class="form-group">
                  <label for="comment">Shikoyat:</label>
                  <textarea
                    v-model="body.description"
                    class="form-control"
                    required
                  ></textarea>
                </div>
              </div>
            </div>
            <hr />
            <h6 class="text-center mb-0">Retsept</h6>
            <div class="row" v-for="(recipe, i) in body.recipes" :key="recipe">
              <div class="col-lg-6 col-md-6 col-sm-12 drop">
                <div class="form-group">
                  <label>Dorilar</label>
                  <div class="dropdown row">
                    <div class="col">
                      <button
                        class="form-control dropdown-toggle"
                        type="button"
                        id="auto_complete"
                        data-mdb-toggle="dropdown"
                        @click="!drugs.length ? get() : ''"
                      >
                        {{
                          recipe.item
                            ? recipe.item.slice(0, 25)
                            : "Dori tanlash"
                        }}
                      </button>
                      <ul
                        class="dropdown-menu w-100 drugs-scroll"
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
                          v-for="drug in drugs"
                          :key="drug"
                          class="dropdown-item"
                          @click="
                            recipe.drug_id = drug.id;
                            recipe.item = drug.name;
                          "
                          :class="drug.id == recipe.drug_id ? 'active' : ''"
                        >
                          {{ drug.name }}
                        </li>
                        <li v-show="!drugs.length" class="dropdown-item">
                          Ma'lumot topilmadi !
                        </li>
                      </ul>
                    </div>
                    <div class="col-auto">
                      <button
                        class="btn btn-primary"
                        type="button"
                        data-mdb-toggle="modal"
                        data-mdb-target="#add_drug"
                        @click="recipe_index = i"
                      >
                        <i class="fas fa-circle-plus"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-lg-6 col-md-6 col-sm-12">
                <div class="form-group">
                  <label for="recipe_unit">Izoh: </label>
                  <div class="row">
                    <div :class="body.recipes.length > 1 ? 'col-10' : 'col-12'">
                      <textarea
                        id="recipe_unit"
                        v-model="recipe.unit"
                        class="form-control"
                        required
                      ></textarea>
                    </div>
                    <div
                      class="col-2"
                      v-show="i || (!i && body.recipes.length > 1)"
                    >
                      <button
                        class="btn btn-danger mx-1"
                        type="button"
                        @click="body.recipes.splice(i, 1)"
                      >
                        <i class="fa-solid fa-circle-xmark"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <hr class="my-2" v-show="body.recipes.length - 1" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              class="btn btn-primary"
              type="button"
              style="width: 65px"
              @click="
                body.recipes.push({
                  drug_id: null,
                  unit: '',
                })
              "
            >
              <i class="fa-solid fa-circle-plus"></i>
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-diagnosis
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!body.description || !body.illness"
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
  <!-- UPDATE DIAGNOSIS -->
  <div class="modal fade" id="update_diagnosis">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Tashxisni o'zgartirish</h6>
        </div>
        <form
          @submit.prevent="$emit('update_diagnosis', item)"
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="illness2">Kasallik nomi:</label>
              <input
                list="illnesses2"
                class="form-control"
                id="illness2"
                v-model="item.illness"
                autocomplete="off"
                @change="$emit('get_templates', item.illness)"
              />
              <datalist id="illnesses2">
                <option v-for="illness in illnesses" :key="illness">
                  {{ illness.name }}
                </option>
              </datalist>
            </div>

            <div class="form-group">
              <label for="comment2">Izoh:</label>
              <textarea
                v-model="item.description"
                class="form-control"
                required
              ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-diagnosis-u
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!item.illness || !item.description"
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

  <!-- ADD RECEPT -->
  <div class="modal fade" id="add_recipe">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Yangi retsept qo'shish</h6>
        </div>
        <form
          @submit.prevent="$emit('create_recipe', retsept)"
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2">
            <div
              class="row"
              v-for="(recipe, i) in retsept.recipes"
              :key="recipe"
            >
              <div class="col-md-6 col-sm-12">
                <div class="form-group">
                  <label>Dorilar</label>
                  <div class="dropdown w-100">
                    <button
                      class="form-control dropdown-toggle"
                      type="button"
                      id="auto_complete2"
                      data-mdb-toggle="dropdown"
                      @click="!drugs.length ? get() : ''"
                    >
                      {{ recipe.item ? recipe.item : "Dorilar" }}
                    </button>
                    <ul
                      class="dropdown-menu w-100 drugs-scroll"
                      aria-labelledby="auto_complete2"
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
                        v-for="drug in drugs"
                        :key="drug"
                        class="dropdown-item"
                        @click="
                          recipe.drug_id = drug.id;
                          recipe.item = drug.name;
                        "
                        :class="drug.id == recipe.drug_id ? 'active' : ''"
                      >
                        {{ drug.name }}
                      </li>
                      <li v-show="!drugs.length" class="dropdown-item">
                        Ma'lumot topilmadi !
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="col-md-6 col-sm-12">
                <div class="form-group">
                  <label for="recipe_unit">Izoh: </label>
                  <div class="row">
                    <div
                      :class="retsept.recipes.length > 1 ? 'col-10' : 'col-12'"
                    >
                      <textarea
                        id="recipe_unit"
                        v-model="recipe.unit"
                        class="form-control"
                        required
                      ></textarea>
                    </div>
                    <div
                      class="col-2"
                      v-show="i || (!i && retsept.recipes.length > 1)"
                    >
                      <button
                        class="btn btn-danger mx-1"
                        type="button"
                        @click="retsept.recipes.splice(i, 1)"
                      >
                        <i class="fa-solid fa-circle-xmark"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <hr class="my-2" v-show="retsept.recipes.length - 1" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              class="btn btn-primary"
              type="button"
              style="width: 65px"
              @click="
                retsept.recipes.push({
                  drug_id: null,
                  unit: '',
                })
              "
            >
              <i class="fa-solid fa-circle-plus"></i>
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-recipe
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

  <!-- ADD DRUG -->
  <div class="modal fade" id="add_drug">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Yangi dori qo'shish</h6>
        </div>
        <form @submit.prevent="create_drug" class="p-4 pt-0 pb-0">
          <div class="modal-body mb-2">
            <div class="form-group">
              <label>Dori nomi: </label>
              <input
                type="text"
                class="form-control"
                v-model="drug_body.name"
                required
              />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-toggle="modal"
              data-mdb-target="#add_diagnosis"
              close-add-drug
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button type="submit" class="btn btn-primary">
              <i class="fa-solid fa-circle-check" v-if="!loading_drug"></i>
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
  drugs_get,
  drug_create,
  success,
} from "../Utils/api";
export default {
  name: "DiagnosisModal",
  emits: [
    "create_diagnosis",
    "update_diagnosis",
    "create_recipe",
    "get_templates",
  ],
  props: ["loading", "item", "illnesses", "templates", "queue"],
  data() {
    return {
      body: {
        illness_id: null,
        illness: "",
        description: "",
        queue_id: this.$route.query.queue_id,
        recipes: [
          {
            drug_id: null,
            unit: "",
          },
        ],
      },
      retsept: {
        recipes: [
          {
            drug_id: null,
            unit: "",
          },
        ],
      },
      page: 1,
      pages: 0,
      search: "",
      drugs: [],
      drug_body: {
        name: "",
      },
      recipe_index: 0,
      loading_drug: false,
    };
  },
  watch: {
    queue(e) {
      this.body.description = e.complaint;
    },
    templates(e) {
      if (e.length) {
        this.body.recipes = [];
        e.forEach((element) => {
          this.body.recipes.push({
            item: element.drug.name,
            drug_id: element.drug_id,
            unit: element.comment,
          });
        });
      } else {
        this.body.recipes = [{ drug_id: null, unit: "" }];
      }
    },
  },
  methods: {
    get() {
      this.$store.dispatch("setloading", { loading: true });
      drugs_get(this.page, 10, this.search)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.drugs = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    scroll() {
      let div = document.querySelector(".drugs-scroll");
      if (div.scrollTop + div.clientHeight >= div.scrollHeight - 10) {
        if (this.page < this.pages) {
          drugs_get(this.page + 1, 10)
            .then((e) => {
              this.page = e.data.page;
              this.drugs = this.drugs.concat(e.data.data);
            })
            .catch((error) => {
              catchError(error);
            });
        }
      }
    },
    create_drug() {
      disabled(true);
      this.loading_drug = true;
      drug_create(this.drug_body)
        .then((id) => {
          disabled(false);
          this.loading_drug = false;
          this.body.recipes[this.recipe_index].drug_id = id;
          this.body.recipes[this.recipe_index].item = this.drug_body.name;
          success("close-add-drug").then(() => {
            this.get();
            this.drug_body.name = "";
            this.recipe_index = 0;
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading_drug = false;
          catchError(error);
        });
    },
  },
};
</script>

<style scoped>
.diagnosis_create {
  zoom: 85%;
}

.comments {
  cursor: pointer;
  padding: 1px 1px;
  border-radius: 2px;
  transition: all 0.3s;
}

.comments:hover,
.comments.active {
  background: rgb(220, 220, 220, 0.5);
}
</style>
