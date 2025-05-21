<template>
  <div class="row">
    <div class="col"></div>
    <div class="col">
      <h3 class="text-center fw-normal">Kirim tarixi</h3>
    </div>
    <div class="col">
      <button
        class="btn btn-secondary float-end"
        id="date"
        @click="date_filter()"
      >
        <i class="fa-solid fa-calendar"></i>
      </button>
    </div>
  </div>
  <div class="row">
    <div class="col-md-4"></div>
    <div class="col-md-4 my-1"></div>
    <div class="col-md-4">
      <div class="input-group input-group-sm">
        <input
          type="search"
          id="search_incomes"
          class="form-control form-control-sm"
          v-model="search"
          placeholder="Qidiruv"
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
    <table
      class="table table-hover table-sm align-middle mb-0 bg-white"
      kirim-tarixi
    >
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th>Sana</th>
          <th>Bemor turi</th>
          <th>Summa</th>
          <th>Bemor</th>
          <th>Ko'rik</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(income, i) in incomes" :key="income">
          <td>{{ i + 1 }}</td>
          <td>{{ income.created_at.replace("T", " ") }}</td>
          <td>{{ income.inspection ? "Ambulator" : "Statsionar" }}</td>
          <td>{{ Intl.NumberFormat().format(income.value) }} so'm</td>
          <td>{{ income.patient.name + " " + income.patient.surename }}</td>
          <td>
            <button
              class="btn btn-sm btn-primary ms-1"
              @click="
                income.inspection
                  ? $refs.patient.start(income.inspection_id)
                  : $refs.stationary.start(income.inpatient_id)
              "
            >
              <i class="fa-solid fa-print"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!incomes.length">Ma'lumot topilmadi !</h4>
    <Pagination
      :page="page"
      :pages="pages"
      :limit="limit"
      @get="get"
      attr="kirim-tarixi"
    />
  </div>

  <Stationary ref="stationary" />
  <Patient ref="patient" />
</template>

<script>
import { catchError, incomes_get } from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
import Swal from "sweetalert2";
import Stationary from "../Stationary/Check.vue";
import Patient from "@/components/Patient/Check.vue";
export default {
  name: "Income",
  data() {
    return {
      incomes: [],
      page: 1,
      pages: 0,
      limit: 25,
      search: "",
      from: "",
      to: "",
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      incomes_get(page, limit, this.from, this.to, this.search)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.incomes = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    date_filter() {
      Swal.fire({
        title: "Sana tanlang !",
        html:
          '<input id="from" type="date" class="form-control">' +
          '<input id="to" type="date" class="form-control mt-2">',
        showCancelButton: true,
        confirmButtonText: "Saqlash",
        cancelButtonText: "Bekor qilish",
        preConfirm: () => {
          return {
            from: document.getElementById("from").value,
            to: document.getElementById("to").value,
          };
        },
      }).then((result) => {
        if (result.isConfirmed) {
          if (result.value.from && result.value.to) {
            this.from = result.value.from;
            this.to = result.value.to;
            this.get(this.page, this.limit);
          } else {
            Swal.fire("Sanani kiriting !").then(() => {
              document.getElementById("date").click();
            });
          }
        }
      });
    },
  },
  created() {
    this.get(this.page, this.limit);
  },
  components: { Pagination, Stationary, Patient },
};
</script>
