<template>
  <h3 class="text-center fw-normal">Kunlik konsultatsiyalar</h3>
  <hr />
  <div class="row justify-content-end">
    <div class="col-12 col-sm-4 col-md-3 col-lg-3">
      <div class="input-group input-group-sm">
        <span
          class="input-group-text border border-primary border-2 border-right-0"
          >sana</span
        >
        <input
          type="date"
          v-model="date"
          class="form-control form-control-sm border-primary border border-2 border-left-0"
          @change="get(1, 25)"
        />
      </div>
    </div>
  </div>

  <div class="responsive mt-2" style="max-height: 79vh">
    <table
      class="table table-hover table-sm align-middle mb-0 bg-white table-bordered"
      kunlik-konsultatsiyalar
    >
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th style="width: 25%">Vrach ismi</th>
          <th style="width: 25%">Lavozimi</th>
          <th style="width: 25%">Konsultatsiya soni</th>
          <th style="width: 25%">Jami summa</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, i) in data" :key="item">
          <td>{{ i + 1 }}</td>
          <td>{{ item.fullname }}</td>
          <td>{{ item.services }}</td>
          <td>{{ item.consultation_count }}</td>
          <td>{{ Intl.NumberFormat().format(item.total_sum) }} so'm</td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!data.length">Ma'lumot topilmadi !</h4>
    <pagination
      :page="page"
      :pages="pages"
      :limit="limit"
      @get="get"
      attr="kunlik-konsultatsiyalar"
    />
  </div>
</template>

<script>
import { catchError, daily_consultations_get } from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
export default {
  components: { Pagination },
  name: "daily-consultant",
  data() {
    return {
      page: 1,
      limit: 25,
      pages: 0,
      date: new Date().toISOString().slice(0, 10),
      data: [],
    };
  },
  methods: {
    get(page, limit) {
      this.$store.dispatch("setloading", { loading: true });
      daily_consultations_get(page, limit, this.date)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          this.data = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
  },
  created() {
    this.get(1, 25);
  },
};
</script>
