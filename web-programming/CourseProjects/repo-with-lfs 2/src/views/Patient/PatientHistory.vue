<template>
  <div class="row">
    <div class="col-md-4"></div>
    <div class="col-md-4">
      <h3 class="text-center fw-normal">{{ $route.query.name }}</h3>
    </div>
    <div class="col-md-4">
      <button
        class="btn btn-secondary btn-sm w-100"
        v-show="content == 'queue' && role != 'casher'"
        data-mdb-toggle="modal"
        data-mdb-target="#add_queue"
        @click="$refs.queue_patient.get_services()"
      >
        <i class="fa-solid fa-circle-plus"></i> Ko'rik qo'shish
      </button>
    </div>
  </div>

  <div class="main">
    <div class="d-flex align-items-start">
      <div
        class="nav flex-column nav-pills text-center w-25"
        id="v-pills-tab"
        role="tablist"
        aria-orientation="vertical"
      >
        <a
          class="nav-link mb-0 mt-1"
          :class="content == tab.content ? 'active' : ''"
          id="v-pills-link1-tab"
          data-mdb-toggle="pill"
          href="#v-pills-link1"
          role="tab"
          aria-controls="v-pills-link1"
          aria-selected="true"
          v-for="tab in tabs.filter((item) => {
            return item.role.find((roleItem) => {
              return roleItem == role;
            });
          })"
          :key="tab"
          @click="content = ''"
          @click.passive="content = tab.content"
          >{{ tab.title }}</a
        >
      </div>

      <div class="tab-content w-100 mt-1" id="v-pills-tabContent">
        <div
          class="tab-pane fade show active"
          id="v-pills-link1"
          role="tabpanel"
          aria-labelledby="v-pills-link1-tab"
        >
          <div v-if="content == 'contact'">
            <div class="card">
              <div class="card-body">
                <div class="responsive" style="max-height: 79vh">
                  <table
                    class="table table-hover table-sm align-middle mb-0 bg-white"
                  >
                    <thead class="bg-blue">
                      <tr>
                        <th>№</th>
                        <th>Sana</th>
                        <th>Muddat</th>
                        <th>Qo'ng'iroq turi</th>
                        <th>Izoh</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(contact, i) in contacts" :key="contact">
                        <td>{{ i + 1 }}</td>
                        <td>{{ contact.created_at.replace("T", " ") }}</td>
                        <td>{{ contact.plan_date.replace("T", " ") }}</td>
                        <td>{{ contact.talk_type }}</td>
                        <td>{{ contact.comment }}</td>
                      </tr>
                    </tbody>
                  </table>
                  <h4 class="text-center m-4" v-if="!contacts.length">
                    Ma'lumot topilmadi !
                  </h4>
                  <Pagination
                    :page="page"
                    :pages="pages"
                    :limit="limit"
                    @get="get"
                  />
                </div>
              </div>
            </div>
          </div>
          <QueuePatient ref="queue_patient" v-else-if="content == 'queue'" />

          <DiagnosisPatient v-else-if="content == 'diagnosis'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DiagnosisPatient from "@/components/Patient/DiagnosisPatient.vue";
import QueuePatient from "@/components/Patient/QueuePatient.vue";
import { catchError, recalls_get } from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
export default {
  name: "PatientHistory",
  data() {
    return {
      contacts: [],
      page: 1,
      pages: 0,
      limit: 25,
      patient_id: this.$route.query.id,
      from: "",
      to: "",
      queue: true,
      completed: true,
      content:
        localStorage.getItem("role") == "operator" ||
        localStorage.getItem("role") == "admin"
          ? "contact"
          : "queue",
      tabs: [
        {
          title: "Qayta a'loqa",
          content: "contact",
          role: ["operator", "admin"],
        },
        {
          title: "Navbat",
          content: "queue",
          role: ["operator", "admin", "doctor", "reception"],
        },
        {
          title: "Tashxis",
          content: "diagnosis",
          role: ["operator", "admin", "doctor", "reception"],
        },
      ],
      role: localStorage.getItem("role"),
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      recalls_get(
        page,
        limit,
        this.from,
        this.to,
        this.patient_id,
        this.queue,
        this.completed
      )
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.contacts = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
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
    if (this.role == "admin" || this.role == "operator") {
      this.get(this.page, this.limit);
    }
  },
  components: { Pagination, QueuePatient, DiagnosisPatient },
};
</script>

<style>
@media (max-width: 500px) {
  div.nav {
    zoom: 75%;
  }
}
</style>
