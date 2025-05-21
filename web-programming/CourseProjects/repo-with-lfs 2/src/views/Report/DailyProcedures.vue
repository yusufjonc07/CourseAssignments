<template>
  <h3 class="text-center fw-normal">Tekshiruvlar</h3>
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
      tekshiruvlar
    >
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th style="width: 25%">Tekshiruv turlari</th>
          <th style="width: 25%">Ma'sul hodim</th>
          <th style="width: 25%">Konsultatsiya soni</th>
          <th style="width: 25%">Jami summa</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, i) in data" :key="item">
          <td>{{ i + 1 }}</td>
          <td
            @click="$router.push(`procedures?id=${item.id}&name=${item.name}`)"
            class="cursor-pointer"
          >
            {{ item.name }}
          </td>
          <td>
            <span
              class="d-block"
              v-for="user in item.responsible_employees.filter((e) => {
                return e !== ' ';
              })"
              :key="user"
            >
              {{ user }}
            </span>
          </td>
          <td>{{ item.quantity }}</td>
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
      attr="tekshiruvlar"
    />
  </div>
</template>

<script>
import {
  catchError,
  service_procedures_reports_get,
} from "@/components/Utils/api";
import Pagination from "@/components/Utils/Pagination.vue";
export default {
  components: { Pagination },
  name: "daily-procedures",
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
      service_procedures_reports_get(page, limit, this.date)
        .then((e) => {
          this.page = e.data.page;
          this.pages = e.data.count;
          this.limit = e.data.limit;
          e.data.data.forEach((element) => {
            element.responsible_employees = this.removeDuplicates(
              element.responsible_employees.split(",")
            );
          });
          this.data = e.data.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
    removeDuplicates(arr) {
      return arr.filter((item, index) => arr.indexOf(item) === index);
    },
  },
  created() {
    this.get(1, 25);
  },
};
</script>
