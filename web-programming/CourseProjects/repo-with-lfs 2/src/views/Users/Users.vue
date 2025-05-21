<template>
  <h3 class="text-center fw-normal">Hodimlar</h3>
  <div class="row">
    <div class="col-md-4">
      <button
        class="btn btn-sm btn-block btn-secondary"
        data-mdb-toggle="modal"
        data-mdb-target="#add_user"
      >
        <i class="fa fa-user-plus"></i> Hodim qo'shish
      </button>
    </div>
    <div class="col-md-4 my-1"></div>
    <div class="col-md-4">
      <div class="input-group input-group-sm">
        <input
          type="search"
          id="search_users"
          class="form-control form-control-sm"
          placeholder="Qidiruv"
          v-model="search"
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
          <th>Nomi</th>
          <th>Telefon raqam</th>
          <th>Login</th>
          <th>Role</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, i) in users" :key="user">
          <td>{{ i + 1 }}</td>
          <td>{{ user.name }}</td>
          <td>
            <a :href="`tel:+998${user.phone}`" class="text-dark">
              +998 {{ format(user.phone) }}
            </a>
          </td>
          <td>{{ user.username }}</td>
          <td>{{ user.role }}</td>
          <td>
            <span
              class="badge rounded-pill d-inline"
              :class="!user.disabled ? 'badge-success' : 'badge-danger'"
              >{{ !user.disabled ? "faol" : "nofaol" }}</span
            >
          </td>
          <td>
            <div class="d-flex">
              <button
                class="btn btn-sm btn-warning mx-1"
                data-mdb-toggle="modal"
                data-mdb-target="#update_user"
                @click="
                  item = {
                    id: user.id,
                    name: user.name,
                    role: user.role,
                    phone: user.phone,
                    username: user.username,
                    password_hash: '',
                    disabled: user.disabled,
                  }
                "
              >
                <i class="fa-solid fa-pen"></i>
              </button>
              <router-link
                v-if="user.role == 'doctor' || user.role == 'casher'"
                :to="{
                  name: user.role == 'doctor' ? 'service' : 'cashreg',
                  query: { id: user.id, name: user.name },
                }"
                class="btn btn-sm btn-secondary"
              >
                <i class="fa-solid fa-eye"></i>
              </router-link>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!users.length">Ma'lumot topilmadi !</h4>
    <Pagination :page="page" :pages="pages" :limit="limit" @get="get" />
  </div>
  <UserModal
    @create_user="create_user"
    :loading="loading"
    :item="item"
    @update_user="update_user"
  />
</template>

<script>
import Pagination from "@/components/Utils/Pagination.vue";
import {
  casher_create,
  catchError,
  disabled,
  doctor_create,
  success,
  users_get,
  user_create,
  user_update,
} from "@/components/Utils/api";
import UserModal from "@/components/User/UserModal.vue";

export default {
  name: "UsersPage",
  data() {
    return {
      users: [],
      page: 1,
      pages: 0,
      limit: 25,
      loading: false,
      search: "",
      item: {},
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      users_get(page, limit, this.search)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.users = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    create_user(body, body2) {
      disabled(true);
      this.loading = true;
      user_create(body)
        .then((e) => {
          if (body.role == "casher" || body.role == "doctor") {
            body2.user_id = e.data;
            if (body.role == "casher") {
              casher_create(body2)
                .finally(() => {
                  disabled(false);
                  this.loading = false;
                  success("close-user").then(() => {
                    this.get(this.page, this.limit);
                  });
                  body2.cashreg_id = null;
                  body2.user_id = null;
                  body.name = "";
                  body.role = "";
                  body.phone = null;
                  body.username = "";
                  body.password_hash = "";
                  body.disabled = false;
                })
                .catch((error) => {
                  catchError(error);
                });
            } else {
              doctor_create(body2)
                .finally(() => {
                  disabled(false);
                  this.loading = false;
                  success("close-user").then(() => {
                    this.get(this.page, this.limit);
                  });
                  body2.service_id = null;
                  body2.room = null;
                  body2.kpi = 0;
                  body2.cost_min = 0;
                  body2.cost = 0;
                  body2.user_id = null;
                  body.name = "";
                  body.role = "";
                  body.phone = null;
                  body.username = "";
                  body.password_hash = "";
                  body.disabled = false;
                })
                .catch((error) => {
                  catchError(error);
                });
            }
          } else {
            disabled(false);
            this.loading = false;
            success("close-user").then(() => {
              this.get(this.page, this.limit);
              body.name = "";
              body.role = "";
              body.phone = null;
              body.username = "";
              body.password_hash = "";
              body.disabled = false;
            });
          }
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    update_user(body) {
      disabled(true);
      this.loading = true;
      user_update(body)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-user-update").then(() => {
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
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
  components: { Pagination, UserModal },
};
</script>
