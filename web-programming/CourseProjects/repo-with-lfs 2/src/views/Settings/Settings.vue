<template>
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
          id="settings-tab"
          data-mdb-toggle="pill"
          href="#settings"
          role="tab"
          aria-controls="settings"
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
          id="settings"
          role="tabpanel"
          aria-labelledby="settings-tab"
        >
          <div v-if="content == 'all'">
            <div class="card">
              <div class="card-body">
                <h5>Tungi rejim</h5>
                <hr class="mx-0" />
                <span>Tizim uchun tunggi yoki tonggi rejim</span>
                <DarkMode class="float-end" />
              </div>
            </div>
          </div>
          <Cashreg v-else-if="content == 'cashreg'" />
          <Source v-else-if="content == 'source'" />
          <Region v-else-if="content == 'region'" />
          <Drug v-else-if="content == 'drug'" />
          <Service v-else-if="content == 'service'" />
          <Addition v-else-if="content == 'addition'" />
          <Illness v-else-if="content == 'illness'" />
          <Examination v-else-if="content == 'examination'" />
          <Instruction v-else-if="content == 'instruction'" />
          <Partner v-else-if="content == 'partner'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DarkMode from "@/components/Utils/DarkMode.vue";
import Service from "@/components/Service/Service.vue";
import Addition from "@/components/Addition/Addition.vue";
import Examination from "@/components/Addition/Examination.vue";

export default {
  name: "SettingsPage",
  data() {
    return {
      content: "",
      tabs: [
        // { title: "Umumiy", content: "all" },
        { title: "Mutaxasislik", content: "service", role: ["admin"] },
        { title: "Qo'shimcha", content: "addition", role: ["admin"] },
        { title: "Ko'rik vaqti", content: "examination", role: ["doctor"] },
      ],
      role: localStorage.getItem("role"),
    };
  },
  components: {
    DarkMode,
    Service,
    Addition,
    Examination,
  },
  created() {
    if (this.role == "admin") {
      this.content = "cashreg";
    } else if (this.role == "doctor") {
      this.content = "illness";
    } else {
      this.content = "instruction";
    }
  },
};
</script>

<style>
@media (max-width: 500px) {
  .main {
    zoom: 75%;
  }
}

@media (max-width: 700px) {
  .nav.flex-column {
    width: auto !important;
  }
}
</style>
