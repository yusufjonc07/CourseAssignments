<template>
  <h4 class="text-center fw-normal">
    {{ $route.query.name }} muolajasi hisoboti
  </h4>
  <hr />
  <div class="row justify-content-end">
    <div class="col-12 col-sm-4 col-md-3 col-lg-3">
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
      </div>
    </div>
  </div>

  <div class="responsive mt-2" style="max-height: 79vh">
    <table
      class="table table-hover table-sm align-middle mb-0 bg-white table-bordered"
    >
      <thead class="bg-blue">
        <tr>
          <th>№</th>
          <th style="width: 25%">Bemor FISH</th>
          <th style="width: 25%">Muolaja Olingan sana</th>
          <th style="width: 25%">Summasi</th>
          <th style="width: 25%">Muolaja o'tkazgan mutahassis</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, i) in data" :key="item">
          <td>{{ i + 1 }}</td>
          <td>{{ item.patient_name }}</td>
          <td>{{ item.date }}</td>
          <td>{{ Intl.NumberFormat().format(item.summa) }} so'm</td>
          <td>{{ item.specialist }}</td>
        </tr>
      </tbody>
    </table>
    <h4 class="text-center m-4" v-if="!data.length">Ma'lumot topilmadi !</h4>
  </div>
</template>

<script>
import { catchError, monthly_procedures_get } from "@/components/Utils/api";
export default {
  name: "procedures",
  data() {
    return {
      page: 1,
      limit: 25,
      pages: 0,
      date: new Date().toISOString().slice(0, 7),
      data: [],
    };
  },
  methods: {
    get() {
      this.$store.dispatch("setloading", { loading: true });
      monthly_procedures_get(
        this.date.slice(0, 4),
        this.date.slice(5, 7),
        this.$route.query.id
      )
        .then((e) => {
          this.data = e.data;
          this.$store.dispatch("setloading", { loading: false });
        })
        .catch((error) => {
          this.$store.dispatch("setloading", { loading: false });
          catchError(error);
        });
    },
  },
  created() {
    this.get();
  },
};
</script>
