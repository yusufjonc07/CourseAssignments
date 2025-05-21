<!-- <template>
  <div class="row">
    <div class="col"></div>
    <div class="col">
      <h3 class="text-center fw-normal">Hisobotlar</h3>
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
  <div class="row text-center mt-1">
    <div class="col-md-4 col-sm-4 col-lg-4 col-xl-4 mb-2">
      <router-link to="/income_history">
        <div
          class="card shadow-sm p-2 border border-2 border-success text-success"
        >
          <h3 class="card-title m-0">
            <b>
              <i class="fa-solid fa-down-long"></i>
              {{ Intl.NumberFormat().format(reports.income) }} so'm</b
            >
          </h3>
          <h6 class="mb-0">kirim</h6>
        </div>
      </router-link>
    </div>
    <div class="col-md-4 col-sm-4 col-lg-4 col-xl-4 mb-2">
      <div>
        <div
          class="card shadow-sm p-2 border border-2 border-primary text-primary"
        >
          <h3 class="card-title m-0">
            <b>
              <i class="fa-solid fa-percent"></i>
              {{ Intl.NumberFormat().format(reports.discount) }} so'm</b
            >
          </h3>
          <h6 class="mb-0">chegirma</h6>
        </div>
      </div>
    </div>
    <div class="col-md-4 col-sm-4 col-lg-4 col-xl-4 mb-2">
      <router-link to="/expence">
        <div
          class="card shadow-sm p-2 border border-2 border-danger text-danger"
        >
          <h3 class="card-title m-0">
            <b>
              <i class="fa-solid fa-up-long"></i>
              {{ Intl.NumberFormat().format(reports.expence) }} so'm</b
            >
          </h3>
          <h6 class="mb-0">chiqim</h6>
        </div>
      </router-link>
    </div>
  </div>

  <div class="row">
    <div class="col-12 col-sm-6 col-md-6 col-lg-3 my-1">
      <router-link
        class="card border border-2 border-primary"
        to="/daily-consultant"
      >
        <div class="card-body">
          <h5 class="card-title mb-0 text-center text-primary">
            Kunlik konsultatsiya hisoboti
          </h5>
        </div>
      </router-link>
    </div>
    <div class="col-12 col-sm-6 col-md-6 col-lg-3 my-1">
      <router-link
        class="card border border-2 border-primary"
        to="/daily-procedures"
      >
        <div class="card-body">
          <h5 class="card-title mb-0 text-center text-primary">
            Kunlik muolaja hisoboti
          </h5>
        </div>
      </router-link>
    </div>
    <div class="col-12 col-sm-6 col-md-6 col-lg-3 my-1">
      <router-link class="card border border-2 border-primary" to="/report-kpi">
        <div class="card-body">
          <h5 class="card-title mb-0 text-center text-primary">KPI hisoboti</h5>
        </div>
      </router-link>
    </div>
    <div class="col-12 col-sm-6 col-md-6 col-lg-3 my-1">
      <div class="card border border-2 border-primary">
        <div class="card-body">
          <h5 class="card-title mb-0 text-center text-primary">
            Statsionar hisoboti
          </h5>
        </div>
      </div>
    </div> 
    <div class="col-12 col-sm-6 col-md-6 col-lg-3 my-1">
      <router-link
        class="card border border-2 border-primary"
        to="/monthly-consultations"
      >
        <div class="card-body">
          <h5 class="card-title mb-0 text-center text-primary">
            Oylik konsultatsiya hisoboti
          </h5>
        </div>
      </router-link>
    </div>
  </div>

  <div class="row">
    <div class="col-md-12 col-sm-12 col-lg-6 col-xl-6 mb-3" id="content_state">
      <canvas id="state"></canvas>
    </div>
    <div
      class="col-md-12 col-sm-12 col-lg-6 col-xl-6 mb-3"
      id="content_service"
    >
      <canvas id="service"></canvas>
    </div>
    <div class="col-md-12 col-sm-12 col-lg-6 col-xl-6 mb-3" id="content_source">
      <canvas id="source"></canvas>
    </div>
    <div class="col-md-12 col-sm-12 col-lg-6 col-xl-6 mb-3" id="content_doctor">
      <canvas id="doctor"></canvas>
    </div>
    <div
      class="col-md-12 col-sm-12 col-lg-6 col-xl-6 mb-3"
      id="content_partner"
    >
      <canvas id="partner"></canvas>
    </div>
    <div
      class="col-md-12 col-sm-12 col-lg-6 col-xl-6 mb-3"
      id="content_partner_employee"
    >
      <canvas id="partner_employee"></canvas>
    </div>
  </div>
</template> 

<script>
import { catchError, reports_get } from "@/components/Utils/api";
import Chart from "chart.js";
import Swal from "sweetalert2";
export default {
  name: "Report",
  data() {
    return {
      from: "",
      to: "",
      reports: {},
    };
  },
  methods: {
    get(from, to) {
      this.$store.dispatch("setloading", { loading: true });
      reports_get(from, to)
        .then((e) => {
          this.reports = e.data;
          this.create_element(e);
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    create_element(e) {
      // REMOVE ELEMENT
      document.getElementById("state").remove();
      document.getElementById("service").remove();
      document.getElementById("source").remove();
      document.getElementById("doctor").remove();
      document.getElementById("partner").remove();
      document.getElementById("partner_employee").remove();

      // CREATE ELEMENT
      let canvas_state = document.createElement("canvas");
      let canvas_service = document.createElement("canvas");
      let canvas_source = document.createElement("canvas");
      let canvas_doctor = document.createElement("canvas");
      let canvas_partner = document.createElement("canvas");
      let canvas_partner_employee = document.createElement("canvas");

      canvas_state.id = "state";
      canvas_service.id = "service";
      canvas_source.id = "source";
      canvas_doctor.id = "doctor";
      canvas_partner.id = "partner";
      canvas_partner_employee.id = "partner_employee";

      // APPEND

      document.getElementById("content_state").append(canvas_state);
      document.getElementById("content_service").append(canvas_service);
      document.getElementById("content_source").append(canvas_source);
      document.getElementById("content_doctor").append(canvas_doctor);
      document.getElementById("content_partner").append(canvas_partner);
      document
        .getElementById("content_partner_employee")
        .append(canvas_partner_employee);
      this.create_chart(e);
    },
    create_chart(e) {
      let state = document.getElementById("state");
      let service = document.getElementById("service");
      let source = document.getElementById("source");
      let doctor = document.getElementById("doctor");
      let partner = document.getElementById("partner");
      let partner_employee = document.getElementById("partner_employee");
      // state
      let states = [];
      let state_count = [];
      // service
      let services = [];
      let service_count = [];
      // source
      let sources = [];
      let source_count = [];
      // doctor
      let doctors = [];
      let doctor_summa = [];
      // partner
      let partners = [];
      let partner_count = [];
      // partner employee
      let partner_employees = [];
      let partner_employee_count = [];

      let backgroundcolors = [];
      let bordercolors = [];
      e.data.states.forEach((element) => {
        states.push(element.name);
        state_count.push(element.count);
      });
      e.data.services.forEach((element) => {
        services.push(element.name);
        service_count.push(element.count);
      });
      e.data.sources.forEach((element) => {
        sources.push(element.name);
        source_count.push(element.count);
      });
      e.data.doctors.forEach((element) => {
        doctors.push(element.name);
        doctor_summa.push(element.summa);
      });
      e.data.partners.forEach((element) => {
        partners.push(element.name);
        partner_count.push(element.count);
      });
      e.data.partner_employees.forEach((element) => {
        partner_employees.push(element.name);
        partner_employee_count.push(element.count);
      });
      for (let i = 0; i < states.length; i++) {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        backgroundcolors.push(`rgba(${r}, ${g}, ${b}, 0.5)`);
        bordercolors.push(`rgba(${r}, ${g}, ${b}, 1)`);
      }
      // state
      var stateChart = new Chart(state, {
        type: "bar",
        data: {
          labels: states,
          datasets: [
            {
              label: "Mijozlar tashrifi",
              data: state_count,
              backgroundColor: backgroundcolors,
              borderColor: bordercolors,
              hoverOffset: 4,
            },
          ],
        },
      });
      // service
      var serviceChart = new Chart(service, {
        type: "bar",
        data: {
          labels: services,
          datasets: [
            {
              label: "Mutahasislik ko'rsatkichlari",
              data: service_count,
              backgroundColor: backgroundcolors,
              borderColor: bordercolors,
              hoverOffset: 4,
            },
          ],
        },
      });
      // source
      new Chart(source, {
        type: "bar",
        data: {
          labels: sources,
          datasets: [
            {
              label: "Reklama ko'rsatkichlari",
              data: source_count,
              backgroundColor: backgroundcolors,
              borderColor: bordercolors,
              hoverOffset: 4,
            },
          ],
        },
      });
      // doctor
      new Chart(doctor, {
        type: "bar",
        data: {
          labels: doctors,
          datasets: [
            {
              label: "Doktor keltirgan foydasi",
              data: doctor_summa,
              backgroundColor: backgroundcolors,
              borderColor: bordercolors,
              hoverOffset: 4,
            },
          ],
        },
      });
      // partner
      new Chart(partner, {
        type: "bar",
        data: {
          labels: partners,
          datasets: [
            {
              label: "Hamkorlar ko'rsatkichlari",
              data: partner_count,
              backgroundColor: backgroundcolors,
              borderColor: bordercolors,
              hoverOffset: 4,
            },
          ],
        },
      });
      // partner employee
      new Chart(partner_employee, {
        type: "bar",
        data: {
          labels: partner_employees,
          datasets: [
            {
              label: "Hamkorlarning hodimlari ko'rsatkichlari",
              data: partner_employee_count,
              backgroundColor: backgroundcolors,
              borderColor: bordercolors,
              hoverOffset: 4,
            },
          ],
        },
      });
      this.$store.dispatch("setloading", { loading: false });
      state.onclick = (e) => {
        var slice = stateChart.getElementAtEvent(e);
        if (!slice.length) return; // return if not clicked on slice
        var label = slice[0]._model.label;
        let item = this.reports.states.find((item) => item.name == label);
        this.$router.push({
          name: "state_report",
          query: { id: item.id, name: item.name },
        });
      };
      service.onclick = (e) => {
        var slice = serviceChart.getElementAtEvent(e);
        if (!slice.length) return; // return if not clicked on slice
        var label = slice[0]._model.label;
        let item = this.reports.services.find((item) => item.name == label);
        this.$router.push({
          name: "service_report",
          query: { id: item.id, name: item.name },
        });
      };
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
    this.get(this.from, this.to);
  },
};
</script>

<style scoped>
.card {
  cursor: pointer;
}
</style>
-->
