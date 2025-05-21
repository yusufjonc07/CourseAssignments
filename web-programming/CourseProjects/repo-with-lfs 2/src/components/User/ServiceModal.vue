<template>
  <!-- ADD USER -->
  <div class="modal fade" id="add_service" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Yangi Mutahasislik qo'shish</h6>
        </div>
        <form
          @submit.prevent="$emit('create_service', body)"
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="service_service">Mutahasislik: </label>
              <select
                id="service_service"
                class="form-select"
                v-model="body.service_id"
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
                  v-model="body.kpi"
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
                :title="Intl.NumberFormat().format(body.cost)"
                currency
              >
                <input
                  type="number"
                  min="0"
                  id="service_cost"
                  class="form-control"
                  v-model="body.cost"
                  required
                />
                <span class="input-group-text">so'm</span>
              </div>
            </div>
            <div class="form-group">
              <label for="service_cost_min">Kichiklar konsultatsiyasi: </label>
              <div
                class="input-group"
                :title="Intl.NumberFormat().format(body.cost_min)"
                currency
              >
                <input
                  type="number"
                  min="0"
                  id="service_cost_min"
                  class="form-control"
                  v-model="body.cost_min"
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
                v-model="body.room"
                required
              />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-service
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="
                !body.service_id || !body.room || !body.cost || !body.cost_min
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
  <div class="modal fade" id="update_service" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title">Mutahasislik ma'lumotlarini o'zgartirish</h6>
        </div>
        <form
          @submit.prevent="$emit('update_service', item)"
          class="p-4 pt-0 pb-0"
        >
          <div class="modal-body mb-2">
            <div class="form-group">
              <label for="service_service">Mutahasislik: </label>
              <select
                id="service_service"
                class="form-select"
                v-model="item.service_id"
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
              <label for="service_cost">Kattalar konsultatsiyasi: </label>
              <div
                class="input-group"
                :title="Intl.NumberFormat().format(item.cost)"
                currency
              >
                <input
                  type="number"
                  min="0"
                  id="service_cost"
                  class="form-control"
                  v-model="item.cost"
                  required
                />
                <span class="input-group-text">so'm</span>
              </div>
            </div>
            <div class="form-group">
              <label for="service_cost_min">Kichiklar konsultatsiyasi: </label>
              <div
                class="input-group"
                :title="Intl.NumberFormat().format(item.cost_min)"
                currency
              >
                <input
                  type="number"
                  min="0"
                  id="service_cost_min"
                  class="form-control"
                  v-model="item.cost_min"
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
                v-model="item.room"
                required
              />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-mdb-dismiss="modal"
              close-service-update
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="!item.service_id"
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
export default {
  name: "ServiceModal",
  emits: ["create_service", "update_service"],
  props: ["loading", "item", "services"],
  data() {
    return {
      body: {
        service_id: null,
        room: null,
        cost: null,
        cost_min: null,
        user_id: Number(this.$route.query.id),
        kpi: 0,
      },
    };
  },
};
</script>
