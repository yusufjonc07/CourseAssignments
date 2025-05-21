<template>
  <h3 class="text-center fw-normal">Hodimning muolajasi ulushi</h3>
  <hr />
  <div class="row">
    <div class="col-md-4">
      <div class="dropdown">
        <button
          id="services"
          class="btn btn-sm btn-block btn-outline-primary dropdown-toggle"
          data-mdb-toggle="dropdown"
          @click="get_services()"
        >
          {{ service?.name ? service?.name : "Mutahasislikni tanlang" }}
        </button>
        <div class="dropdown-menu w-100 p-1" aria-labelledby="services">
          <ul
            class="list-group p-1 responsive"
            style="max-height: 25vh"
            @scroll="scroll_services($event)"
          >
            <li
              class="list-group-item p-2 cursor-pointer"
              @click="
                service_id = 0;
                service = null;
                get();
              "
            >
              Barchasi
            </li>
            <li
              class="list-group-item p-2 cursor-pointer"
              v-for="item in services.data"
              :key="item"
              @click="
                service = item;
                service_id = item.id;
                get();
              "
            >
              {{ item?.name }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="dropdown">
        <button
          id="users"
          class="btn btn-sm btn-block btn-outline-primary dropdown-toggle"
          data-mdb-toggle="dropdown"
          @click="get_users()"
        >
          {{ user?.name ? user?.name : "Hodimni tanlang" }}
        </button>
        <div class="dropdown-menu w-100 p-1" aria-labelledby="users">
          <input
            class="form-control form-control-sm"
            placeholder="qidiruv"
            v-model="search_users"
            @keyup="get_users()"
          />
          <ul
            class="list-group p-1 responsive"
            style="max-height: 25vh"
            @scroll="scroll_users($event)"
          >
            <li
              class="list-group-item p-2 cursor-pointer"
              @click="
                user_id = 0;
                user = null;
                get();
              "
            >
              Barchasi
            </li>
            <li
              class="list-group-item p-2 cursor-pointer"
              v-for="item in users.data"
              :key="item"
              @click="
                user = item;
                user_id = item.id;
                get();
              "
            >
              {{ item?.name }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="input-group input-group-sm">
        <span
          class="input-group-text border border-primary border-2 border-right-0"
          >sana</span
        >
        <input
          type="month"
          v-model="date"
          class="form-control form-control-sm border-primary border border-2 border-left-0"
          @change="get()"
        />
        <button
          @click="$util.exportToExcel('kpi')"
          class="btn btn-sm btn-success mx-1 rounded px-3"
        >
          <i class="fa-regular fa-file-excel"></i>
        </button>
      </div>
    </div>
  </div>

  <div class="responsive mt-2" style="max-height: 79vh; min-height: 79vh">
    <table
      class="table table-hover table-sm align-middle mb-0 bg-white table-bordered text-center"
      kpi
    >
      <thead>
        <tr>
          <th rowspan="2">№</th>
          <th rowspan="2" style="width: 18%">Bemor FISH</th>
          <th rowspan="2" style="width: 18%">Muolaja Olingan sana</th>
          <th rowspan="2" style="width: 18%">Summasi</th>
          <th rowspan="2" style="width: 18%" v-if="!user">
            Muolaja o'tkazgan mutahassis
          </th>
          <th style="width: 18%" colspan="2">Hodimga</th>
          <th rowspan="2" style="width: 18%">Qoldi</th>
        </tr>
        <tr>
          <th>Foizda</th>
          <th>Summada</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, i) in data" :key="item">
          <td>{{ i + 1 }}</td>
          <td>{{ item.patient_name }}</td>
          <td>{{ item.date }}</td>
          <td>{{ Intl.NumberFormat().format(item.summa) }} so'm</td>
          <td v-if="!user">{{ item.specialist }}</td>
          <td>{{ Intl.NumberFormat().format(item.kpi) }}%</td>
          <td>
            {{ Intl.NumberFormat().format((item.kpi * item.summa) / 100) }} so'm
          </td>
          <td>
            {{ Intl.NumberFormat().format(item.qoldi) }}
            so'm
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!data.length">Ma'lumot topilmadi !</h4>
  </div>
</template>

<script>
import {
  catchError,
  monthly_procedures_get,
  services_get,
  users_get,
} from "@/components/Utils/api";
export default {
  name: "procedures",
  data() {
    return {
      page: 1,
      limit: 25,
      pages: 0,
      date: new Date().toISOString().slice(0, 7),
      data: [],
      users: {
        page: 0,
        count: 1,
        limit: 25,
        data: [],
      },
      services: {
        page: 0,
        count: 1,
        limit: 25,
        data: [],
      },
      search_users: "",
      search_services: "",
      user: null,
      service: null,
      user_id: 0,
      service_id: 0,
    };
  },
  methods: {
    get() {
      this.$store.dispatch("setloading", { loading: true });
      monthly_procedures_get(
        this.date.slice(0, 4),
        this.date.slice(5, 7),
        0,
        this.user_id,
        this.service_id
      )
        .then((e) => {
          e.data.forEach((element) => {
            let kpi = (element.summa * element.kpi) / 100;
            element.qoldi = element.summa - kpi;
          });
          this.data = e.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    get_users() {
      users_get(1, 25, this.search_users)
        .then((res) => {
          this.users = res.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    scroll_users(event) {
      const element = event.target;
      if (element.scrollTop + element.clientHeight >= element.scrollHeight) {
        if (this.users.page < this.users.count) {
          users_get(this.users.page + 1, 25, this.search_users)
            .then((res) => {
              this.users.page = res.data.page;
              this.users.count = res.data.count;
              this.users.data = this.users.data.concat(res.data.data);
            })
            .catch((error) => {
              catchError(error);
            });
        }
      }
    },
    get_services() {
      services_get(1, 25, this.search_services)
        .then((res) => {
          this.services = res.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    scroll_services(event) {
      const element = event.target;
      if (element.scrollTop + element.clientHeight >= element.scrollHeight) {
        if (this.services.page < this.services.count) {
          services_get(this.services.page + 1, 25, this.search_services)
            .then((res) => {
              this.services.page = res.data.page;
              this.services.count = res.data.count;
              this.services.data = this.services.data.concat(res.data.data);
            })
            .catch((error) => {
              catchError(error);
            });
        }
      }
    },
  },
  created() {
    this.get();
  },
};
</script>
