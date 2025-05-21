<template>
  <nav class="">
    <div class="container-fluid">
      <div class="desktop navbar-nav">
        <router-link
          class="link"
          :class="
            route.path == $route.meta.last_path
              ? 'router-link-exact-active'
              : ''
          "
          :to="route.path"
          v-for="route in routes.filter((item) => {
            return item.role.find((roleItem) => {
              return roleItem == role;
            });
          })"
          :key="route"
          >{{ route.title }}</router-link
        >
        <button
          class="btn btn-sm float-start shadow-sm d-none mobile"
          type="button"
          data-mdb-toggle="offcanvas"
          data-mdb-target="#offcanvasExample"
          aria-controls="offcanvasExample"
        >
          <i class="fa fa-bars" />
        </button>
        <div class="btn-group shadow-none float-end">
          <i
            @click="$router.push('/')"
            class="fa fa-sign-out mx-2 my-1"
            style="font-size: 20px; cursor: pointer"
          >
          </i>
        </div>
      </div>
    </div>
  </nav>

  <div
    class="offcanvas offcanvas-start"
    tabindex="-1"
    id="offcanvasExample"
    aria-labelledby="offcanvasExampleLabel"
    data-mdb-dismiss="offcanvas"
  >
    <div class="offcanvas-header justify-content-end">
      <button
        type="button"
        class="btn btn-sm"
        data-mdb-dismiss="offcanvas"
        aria-label="Close"
      >
        <i class="fa fa-lg fa-xmark" />
      </button>
    </div>
    <div class="offcanvas-body">
      <ul class="list-group list-group-light list-group-small">
        <router-link
          class="list-group-item list-group-item-action px-3 border-0"
          :to="route.path"
          :class="
            $route.path == route.path
              ? 'active'
              : route.path == $route.meta.last_path
              ? 'active'
              : ''
          "
          v-for="route in routes.filter((item) => {
            return item.role.find((roleItem) => {
              return roleItem == role;
            });
          })"
          :key="route"
          >{{ route.title }}</router-link
        >
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavbarItem",
  data() {
    return {
      role: localStorage.getItem("role"),
      routes: [
        {
          title: "Hodimlar",
          path: "/users",
          role: ["admin"],
        },
        {
          title: "Registratsiya",
          path: "/registration",
          role: ["reception", "operator"],
        },
        {
          title: "Kassa",
          path: "/cashreg_confirm",
          role: ["casher"],
        },
        {
          title: "Doktor",
          path: "/doctor_diagnosis",
          role: ["doctor"],
        },
        {
          title: "Tashxislar",
          path: "/diagnosiss",
          role: ["reception", "doctor"],
        },
        {
          title: "Chiqimlar",
          path: "/expence",
          role: ["admin"],
        },
        {
          title: "Hisobot",
          path: "/report",
          role: ["admin"],
        },
        {
          title: "Operator",
          path: "/contact_date",
          role: ["operator"],
        },
        {
          title: "Bemorlar",
          path: "/patients",
          role: ["operator", "admin", "doctor", "reception"],
        },
        {
          title: "Statsionar",
          path: "/stationary",
          role: ["admin", "stationary", "casher"],
        },
        {
          title: "Sozlamalar",
          path: "/settings",
          role: [
            "admin",
            "doctor",
            "operator",
            "casher",
            "reception",
            "stationary",
          ],
        },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.desktop {
  display: block;
}
nav {
  padding: 5px;
  text-align: left;
  box-shadow: 0 1px 20px -10px rgb(50, 55, 65);
  height: 36px;

  a.link {
    position: relative;
    padding: 5px;
    font-size: 15px;
    font-weight: bold;
    color: #2c3e50;
    text-decoration: none;
    transition: 0.2s all;
    border-radius: 5px;

    &:hover {
      background: rgb(50, 55, 65, 0.2);
    }

    &::after {
      content: "";
      display: block;
      position: absolute;
      bottom: 5%;
      left: 50%;
      right: 50%;
      width: 0;
      height: 2px;
      background: rgb(50, 55, 65);
      transition: 0.2s all;
    }

    &:hover::after {
      left: 5%;
      right: 5%;
      width: 90%;
    }

    &.router-link-exact-active {
      color: whitesmoke;
      background: rgb(50, 55, 65);
    }

    &.router-link-exact-active::after {
      background: rgb(245, 245, 245);
    }

    &.router-link-exact-active:hover {
      color: whitesmoke;
      background: rgb(50, 55, 65);
    }

    &.router-link-exact-active:hover::after {
      left: 50%;
      right: 50%;
      width: 0;
    }
  }
}

@media (max-width: 768px) {
  .mobile {
    display: block !important;
  }

  .link {
    display: none;
  }
}
</style>
