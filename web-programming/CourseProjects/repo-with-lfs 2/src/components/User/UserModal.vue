<template>
  <!-- ADD USER -->
  <div class="modal fade" id="add_user" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Yangi Hodim qo'shish</h6>
        </div>
        <form
          @submit.prevent="
            $emit(
              'create_user',
              body,
              body.role == 'doctor'
                ? doctor_body
                : body.role == 'casher'
                ? casher_body
                : ''
            )
          "
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="user_name">Ism: </label>
              <input
                type="text"
                id="user_name"
                class="form-control"
                v-model="body.name"
                required
              />
            </div>
            <div class="form-group">
              <label for="user_phone">Telefon: </label>
              <div class="input-group">
                <span class="input-group-text">+998</span>
                <input
                  type="tel"
                  id="user_phone"
                  class="form-control"
                  maxlength="9"
                  minlength="9"
                  v-model="body.phone"
                  @keypress="isNumber($event)"
                  required
                />
              </div>
            </div>
            <div class="form-group">
              <label for="user_role">Role: </label>
              <select
                id="user_role"
                class="form-select"
                v-model="body.role"
                @change="get(body.role)"
                required
              >
                <option value="admin">Admin</option>
                <option value="operator">Operator</option>
                <option value="reception">Qabulxona Hodimi</option>
                <option value="doctor">Doktor</option>
                <option value="casher">Kassachi</option>
                <option value="stationary">Statsionar Hodimi</option>
              </select>
            </div>
            <div class="form-group">
              <label for="username">Login: </label>
              <input
                type="text"
                id="username"
                class="form-control"
                v-model="body.username"
                minlength="5"
                required
              />
            </div>
            <div class="form-group">
              <label for="password">Parol: </label>
              <input
                type="password"
                id="password"
                class="form-control"
                v-model="body.password_hash"
                minlength="8"
                required
              />
            </div>
            <div v-if="body.role == 'doctor'">
              <div class="form-group">
                <label for="service_service">Mutahasislik: </label>
                <select
                  id="service_service"
                  class="form-select"
                  v-model="doctor_body.service_id"
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
              <div class="form-group">
                <label>KPI</label>
                <div class="input-group">
                  <input
                    type="number"
                    class="form-control"
                    v-model="doctor_body.kpi"
                    min="0"
                    max="100"
                    placeholder="KPI"
                    required
                  />
                  <span class="input-group-text">%</span>
                </div>
              </div>
              <div class="form-group">
                <label for="service_cost">Kattalar konsultatsiyasi: </label>
                <div
                  class="input-group"
                  :title="Intl.NumberFormat().format(doctor_body.cost)"
                  currency
                >
                  <input
                    type="number"
                    min="0"
                    id="service_cost"
                    class="form-control"
                    v-model="doctor_body.cost"
                    required
                  />
                  <span class="input-group-text">so'm</span>
                </div>
              </div>
              <div class="form-group">
                <label for="service_cost_min"
                  >Kichiklar konsultatsiyasi:
                </label>
                <div
                  class="input-group"
                  :title="Intl.NumberFormat().format(doctor_body.cost_min)"
                  currency
                >
                  <input
                    type="number"
                    min="0"
                    id="service_cost_min"
                    class="form-control"
                    v-model="doctor_body.cost_min"
                    required
                  />
                  <span class="input-group-text">so'm</span>
                </div>
              </div>
              <div class="form-group">
                <label for="service_room">Xona raqami: </label>
                <input
                  type="number"
                  min="0"
                  id="service_room"
                  class="form-control"
                  v-model="doctor_body.room"
                  required
                />
              </div>
            </div>
            <div v-else-if="body.role == 'casher'">
              <div class="form-group">
                <label for="user_casher">Kassa: </label>
                <select
                  id="user_service"
                  class="form-select"
                  v-model="casher_body.cashreg_id"
                  required
                >
                  <option
                    :value="cashreg.id"
                    v-for="cashreg in cashregs"
                    :key="cashreg"
                  >
                    {{ cashreg.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-user
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="
                body.role == 'doctor'
                  ? !body.name ||
                    !body.password_hash ||
                    !body.phone ||
                    !body.role ||
                    !body.username ||
                    !doctor_body.service_id ||
                    !doctor_body.room ||
                    !doctor_body.kpi ||
                    !doctor_body.cost_min ||
                    !doctor_body.cost
                  : body.role == 'casher'
                  ? !body.name ||
                    !body.password_hash ||
                    !body.phone ||
                    !body.role ||
                    !body.username ||
                    !casher_body.cashreg_id
                  : !body.name ||
                    !body.password_hash ||
                    !body.phone ||
                    !body.role ||
                    !body.username
              "
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

  <!-- UPDATE USER -->
  <div class="modal fade" id="update_user" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Hodim ma'lumotlarini o'zgartirish</h6>
        </div>
        <form
          @submit.prevent="$emit('update_user', item)"
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="user_name_update">Ism: </label>
              <input
                type="text"
                id="user_name_update"
                class="form-control"
                v-model="item.name"
                required
              />
            </div>
            <div class="form-group">
              <label for="user_phone_update">Telefon: </label>
              <div class="input-group">
                <span class="input-group-text">+998</span>
                <input
                  type="tel"
                  id="user_phone_update"
                  class="form-control"
                  maxlength="9"
                  minlength="9"
                  v-model="item.phone"
                  @keypress="isNumber($event)"
                  required
                />
              </div>
            </div>
            <div class="form-group">
              <label for="user_role_update">Role: </label>
              <select
                id="user_role_update"
                class="form-select"
                v-model="item.role"
                required
              >
                <option value="admin">Admin</option>
                <option value="operator">Operator</option>
                <option value="reception">Qabulxona Hodimi</option>
                <option value="doctor">Doktor</option>
                <option value="casher">Kassachi</option>
                <option value="stationary">Statsionar Hodimi</option>
              </select>
            </div>
            <div class="form-group">
              <label for="user_status_update">Status: </label>
              <select
                id="user_status_update"
                class="form-select"
                v-model="item.disabled"
                required
              >
                <option value="false">faol</option>
                <option value="true">nofaol</option>
              </select>
            </div>
            <div class="form-group">
              <label for="username_update">Login: </label>
              <input
                type="text"
                id="username_update"
                class="form-control"
                v-model="item.username"
                minlength="5"
                required
              />
            </div>
            <div class="form-group">
              <label for="password_update">Parol: </label>
              <input
                type="password"
                id="password_update"
                class="form-control"
                v-model="item.password_hash"
                minlength="8"
              />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-user-update
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
</template>

<script>
import { cashregs_get, catchError, services_get } from "../Utils/api";
export default {
  name: "UserModal",
  emits: ["create_user", "update_user"],
  props: ["loading", "item"],
  data() {
    return {
      body: {
        name: "",
        role: "",
        phone: null,
        username: "",
        password_hash: "",
        disabled: false,
      },
      doctor_body: {
        service_id: null,
        room: null,
        cost: 0,
        cost_min: 0,
        user_id: null,
        kpi: 0,
      },
      casher_body: {
        user_id: null,
        cashreg_id: null,
        disabled: false,
      },
      services: [],
      cashregs: [],
    };
  },
  methods: {
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
    get(e) {
      if (e == "doctor") {
        services_get(1, 1000)
          .then((e) => {
            this.services = e.data.data;
          })
          .catch((error) => {
            catchError(error);
          });
      } else if (e == "casher") {
        cashregs_get(1, 1000)
          .then((e) => {
            this.cashregs = e.data.data;
          })
          .catch((error) => {
            catchError(error);
          });
      }
    },
  },
};
</script>
