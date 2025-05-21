<template>
  <div class="content login">
    <div class="container">
      <div class="row">
        <div
          class="col-md-6 col-lg-6 col-xl-6 col-xxl-6 d-none d-sm-none d-md-none d-lg-block d-flex d-xl-block d-xxl-block justify-content-center"
        >
          <img
            src="../../assets/clinic.gif"
            draggable="false"
            alt="Image"
            class="img-fluid"
            style="display: block; margin: auto"
            loop="1"
          />
        </div>
        <div class="col-md-12 col-lg-6 col-xl-6 col-xxl-6 col-sm-12 contents">
          <div class="row justify-content-center">
            <div class="col-md-8">
              <div class="mb-4 text-center">
                <img src="../../assets/logo.png" width="200" alt="" />
                <h3>Xush kelibsiz !</h3>
                <p class="mb-4">Kirish uchun ushbu formani to'ldiring.</p>
              </div>
              <form @submit.prevent="signin">
                <div class="form-group first field--not-empty">
                  <label for="username">Login</label>
                  <div class="input-group flex-nowrap">
                    <input
                      type="text"
                      class="form-control"
                      id="username"
                      placeholder="Login"
                      v-model="data.username"
                      autocomplete="off"
                      required
                    />
                    <div class="input-group-text">
                      <i class="fa-solid fa-at"></i>
                    </div>
                  </div>
                </div>
                <div class="form-group last mb-4 field--not-empty">
                  <label for="password">Parol</label>
                  <div class="input-group flex-nowrap">
                    <input
                      :type="type ? 'password' : 'text'"
                      class="form-control"
                      id="password"
                      placeholder="Parol"
                      v-model="data.password"
                      autocomplete="off"
                      required
                    />
                    <div class="input-group-text" @click="type = !type">
                      <i :class="`fa-regular fa-eye${type ? '-slash' : ''}`" />
                    </div>
                  </div>
                </div>
                <button
                  type="submit"
                  id="login_button"
                  class="btn btn-block text-white"
                  style="background: #005a5a"
                  :disabled="!data.username || !data.password"
                >
                  <i class="fa-solid fa-arrow-right-to-bracket"></i>
                  Кириш
                  <div
                    class="spinner-border spinner-border-sm mx-1"
                    role="status"
                    v-if="loading"
                  >
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { catchError, token } from "@/components/Utils/api";
export default {
  name: "Login",
  data() {
    return {
      data: {
        username: "",
        password: "",
      },
      type: true,
      loading: false,
      icon: "fa-regular fa-eye",
    };
  },
  methods: {
    signin() {
      this.loading = true;
      document.getElementById("login_button").disabled = true;
      token(this.data)
        .then((response) => {
          this.require(response.data);
        })
        .catch((error) => {
          this.loading = false;
          document.getElementById("login_button").disabled = false;
          catchError(error);
        });
    },
    require(data) {
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("role", data.user.role);
      localStorage.setItem("id", data.user.id);
      this.loading = false;
      document.getElementById("login_button").disabled = false;
      if (data.user.role == "admin") {
        window.location.href = "/users";
      } else if (data.user.role == "reception") {
        window.location.href = "/registration";
      } else if (data.user.role == "doctor") {
        window.location.href = "/doctor_diagnosis";
      } else if (data.user.role == "casher") {
        window.location.href = "/cashreg_confirm";
      } else if (data.user.role == "operator") {
        window.location.href = "/contact_date";
      } else if (data.user.role == "stationary") {
        window.location.href = "/stationary";
      } else {
        window.location.href = "/home";
      }
    },
  },
  created() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    localStorage.removeItem("id");
  },
  mounted() {
    document.querySelector("[type=text]").focus();
  },
};
</script>

<style lang="scss" scoped>
.content {
  overflow-y: auto;
  height: 100vh;
  user-select: none;
  .container {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  .row {
    margin: 4rem 0;
  }
  .input-group-text {
    width: 45px;
    background: #fff;
    cursor: pointer;
  }
}
@media (max-width: 768px) {
  .contents .row {
    margin: 0 0;
  }
}
</style>
