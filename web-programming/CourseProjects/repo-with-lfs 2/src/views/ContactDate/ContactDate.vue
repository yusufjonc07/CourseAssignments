<template>
  <div class="row">
    <div class="col"></div>
    <div class="col">
      <h3 class="text-center fw-normal">Qayta a'loqa</h3>
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
  <div class="row">
    <div class="col d-flex justify-content-center">
      <div class="btn-group btn-group-sm shadow-0 float-end">
        <button
          type="button"
          class="btn"
          :class="
            queue == true && completed == false
              ? 'btn-primary'
              : 'btn-outline-primary'
          "
          data-mdb-color="dark"
          @click="
            queue = true;
            completed = false;
            get_counts();
            get(page, limit);
          "
        >
          Qayta a'loqalar
          <span class="badge badge-danger ms-2" v-show="counts.recall > 0">{{
            counts.recall
          }}</span>
        </button>
        <button
          type="button"
          class="btn"
          :class="
            queue == false && completed == false
              ? 'btn-primary'
              : 'btn-outline-primary'
          "
          data-mdb-color="dark"
          @click="
            queue = false;
            completed = false;
            get_counts();
            get(page, limit);
          "
        >
          Rejadagilar
          <span class="badge badge-danger ms-2" v-show="counts.planning > 0">{{
            counts.planning
          }}</span>
        </button>
        <button
          type="button"
          class="btn"
          :class="
            queue == false && completed == true
              ? 'btn-primary'
              : 'btn-outline-primary'
          "
          data-mdb-color="dark"
          @click="
            queue = false;
            completed = true;
            get_counts();
            get(page, limit);
          "
        >
          Qong'iroqlar tarixi
        </button>
        <button
          class="btn btn-sm btn-secondary"
          data-mdb-toggle="modal"
          data-mdb-target="#add_date"
        >
          <i class="fa fa-circle-plus"></i>
        </button>
      </div>
    </div>
  </div>

  <div class="responsive mt-2" style="max-height: 80vh">
    <table class="table table-hover table-sm align-middle mb-0 bg-white">
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th>Bemor</th>
          <th>Telefon</th>
          <th>Sana</th>
          <th>Muddat</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(contact, i) in contacts" :key="contact">
          <td>{{ i + 1 }}</td>
          <td>{{ contact.patient.name + " " + contact.patient.surename }}</td>
          <td>
            <a :href="`tel:+998${contact.patient.phone}`" class="text-dark">
              +998 {{ format(contact.patient.phone) }}
            </a>
          </td>
          <td>{{ contact.created_at.replace("T", " ") }}</td>
          <td>{{ contact.plan_date.replace("T", " ") }}</td>
          <td>
            <div class="d-flex">
              <router-link
                :to="{
                  name: 'patient',
                  query: {
                    id: contact.patient.id,
                    name: contact.patient.name,
                  },
                }"
                class="btn btn-sm btn-secondary mx-1"
              >
                <i class="fa-solid fa-eye"></i>
              </router-link>
              <button
                class="btn btn-sm btn-secondary"
                data-mdb-toggle="modal"
                data-mdb-target="#talked"
                v-show="completed != true"
                @click="
                  recall_id = contact.id;
                  que = contact;
                "
              >
                <i class="fa-solid fa-phone"></i>
              </button>
              <button
                class="btn btn-sm btn-warning mx-1"
                data-mdb-toggle="modal"
                data-mdb-target="#update_date"
                @click="
                  item = {
                    id: contact.id,
                    plan_date: contact.plan_date,
                  }
                "
                v-show="completed != true"
              >
                <i class="fa-solid fa-edit"></i>
              </button>
              <button
                class="btn btn-sm btn-danger"
                @click="remove(contact.id)"
                v-show="completed != true"
              >
                <i class="fa-solid fa-circle-xmark"></i>
              </button>
              <div id="custom-cancel"></div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!contacts.length">
      Ma'lumot topilmadi !
    </h4>
    <Pagination :page="page" :pages="pages" :limit="limit" @get="get" />
  </div>

  <ContactModal
    :item="item"
    @update_date="update_date"
    @create_date="create_date"
    @talked="talked"
    :loading="loading"
    :recall_id="recall_id"
    :queue="que"
  />
</template>

<script>
import ContactModal from "@/components/Contact/ContactModal.vue";
import {
  catchError,
  counts_get,
  disabled,
  recalls_get,
  recall_create,
  recall_delete,
  recall_talked,
  recall_update,
  success,
} from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
import Swal from "sweetalert2";
export default {
  name: "ContactDate",
  data() {
    return {
      contacts: [],
      page: 1,
      pages: 0,
      limit: 25,
      from: "",
      to: "",
      queue: true,
      completed: false,
      counts: {},
      loading: false,
      item: {},
      recall_id: null,
      que: {},
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
        0,
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
    get_counts() {
      counts_get()
        .then((e) => {
          this.counts = [];
          this.counts = e.data;
        })
        .catch((error) => {
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
            this.get_counts();
            this.get(this.page, this.limit);
          } else {
            Swal.fire("Sanani kiriting !").then(() => {
              document.getElementById("date").click();
            });
          }
        }
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
    update_date(e) {
      disabled(true);
      this.loading = true;
      recall_update(e)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-date-update").then(() => {
            this.get_counts();
            this.get(this.page, this.limit);
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    create_date(e) {
      disabled(true);
      this.loading = true;
      recall_create(e)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-date").then(() => {
            this.get_counts();
            this.get(this.page, this.limit);
            e.patient_id = null;
            e.plan_date = "";
            e.item = "";
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
    remove(id) {
      Swal.fire({
        text: "O'chirmoqchimisiz !",
        target: "#custom-cancel",
        customClass: {
          container: "position-absolute",
        },
        toast: true,
        position: "bottom-right",
        confirmButtonText: "Xa",
        showCancelButton: true,
        cancelButtonColor: "#DC4C64",
        cancelButtonText: "Yo'q",
      }).then((e) => {
        if (e.isConfirmed == true) {
          this.$store.dispatch("setloading", { loading: true });
          recall_delete(id)
            .then(() => {
              success().then(() => {
                this.get_counts();
                this.get(this.page, this.limit);
              });
            })
            .catch((error) => {
              this.$store.dispatch("setloading", { loading: false });
              catchError(error);
            });
        }
      });
    },
    talked(e) {
      disabled(true);
      this.loading = true;
      recall_talked(e)
        .then(() => {
          disabled(false);
          this.loading = false;
          success("close-talked").then(() => {
            this.get_counts();
            this.get(this.page, this.limit);
            e.comment = "";
            e.talk_type = "ijobiy";
          });
        })
        .catch((error) => {
          disabled(false);
          this.loading = false;
          catchError(error);
        });
    },
  },
  created() {
    this.get_counts();
    this.get(this.page, this.limit);
    setInterval(() => {
      this.get_counts();
    }, 5000);
  },
  components: { Pagination, ContactModal },
};
</script>
