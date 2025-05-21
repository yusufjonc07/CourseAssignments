<template>
  <div class="row">
    <div class="col"></div>
    <div class="col">
      <h3 class="text-center fw-normal">{{ $route.query.name }}</h3>
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
  <hr />
  <div class="responsive" style="max-height: 84vh">
    <table
      class="table table-hover table-sm align-middle mb-0 bg-white"
      mutahasislik-korsatkichlari
    >
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th>Sana</th>
          <th>Doktor</th>
          <th>Bemor</th>
          <th>Ko'rik narxi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(report, i) in reports" :key="report">
          <td>{{ i + 1 }}</td>
          <td>{{ report.created_at.replace("T", " ") }}</td>
          <td>{{ report.doctor.user.name }}</td>
          <td>
            {{
              report.inspection?.patient.name +
              " " +
              report.inspection?.patient.surename
            }}
          </td>
          <td>{{ Intl.NumberFormat().format(report.doctor.cost) }} so'm</td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!reports.length">Ma'lumot topilmadi !</h4>
    <Pagination
      :page="page"
      :pages="pages"
      :limit="limit"
      @get="get"
      attr="mutahasislik-korsatkichlari"
    />
  </div>
</template>

<script>
import { catchError, service_reports_get } from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
import Swal from "sweetalert2";
export default {
  name: "ServiceReport",
  data() {
    return {
      reports: [],
      page: 1,
      pages: 0,
      limit: 25,
      id: this.$route.query.id,
      from: "",
      to: "",
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      service_reports_get(page, limit, this.from, this.to, this.id)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.reports = e.data.data;
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
  components: { Pagination },
};
</script>
