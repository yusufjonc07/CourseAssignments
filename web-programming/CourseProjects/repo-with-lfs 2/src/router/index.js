import { createRouter, createWebHistory } from "vue-router";
const role = localStorage.getItem("role");

let routes = [
  {
    path: "/home",
    name: "home",
    meta: { auth: true, title: "Home" },
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/:catchAll(.*)",
    name: "notFound",
    meta: { auth: false, title: "Sahifa Topilmadi" },
    component: () => import("../components/Utils/NotFound.vue"),
  },
  {
    path: "/",
    name: "login",
    meta: { auth: false, title: "Login" },
    component: () => import("../views/Login/Login.vue"),
  },
  {
    path: "/settings",
    name: "settings",
    meta: {
      auth: true,
      title: "Sozlamalar",
      role: [
        "admin",
        "doctor",
        "operator",
        "casher",
        "reception",
        "stationary",
      ],
    },
    component: () => import("../views/Settings/Settings.vue"),
  },
  {
    path: "/users",
    name: "users",
    meta: { auth: true, title: "Hodimlar", role: ["admin"] },
    component: () => import("../views/Users/Users.vue"),
  },
  
  {
    path: "/service",
    name: "service",
    meta: {
      auth: true,
      title: "Hodim",
      last_path: "/users",
      role: ["admin"],
      iscomponent: true,
    },
    component: () => import("../views/Users/Service.vue"),
  },
  {
    path: "/registration",
    name: "registration",
    meta: {
      auth: true,
      title: "Registratsiya",
      last_path: "/registration",
      role: ["reception", "operator"],
    },
    component: () => import("../views/Patient/Registration.vue"),
  },
  
  {
    path: "/doctor_diagnosis",
    name: "doctor_diagnosis",
    meta: {
      auth: true,
      title: "Doktor",
      last_path: "/doctor_diagnosis",
      role: ["doctor"],
    },
    component: () => import("../views/Confirm/DoctorConfirm.vue"),
  },
  {
    path: "/add_diagnosis",
    name: "add_diagnosis",
    meta: {
      auth: true,
      title: "Tashxis",
      last_path: "/doctor_diagnosis",
      role: ["doctor"],
      iscomponent: true,
    },
    component: () => import("../views/Confirm/AddDiagnosis.vue"),
  },
  
  // {
  //   path: "/report",
  //   name: "report",
  //   meta: {
  //     auth: true,
  //     title: "Hisobot",
  //     last_path: "/report",
  //     role: ["admin"],
  //   },
  //   component: () => import("../views/Report/Report.vue"),
  // },
  
  {
    path: "/service_report",
    name: "service_report",
    meta: {
      auth: true,
      title: "Mutahasislik hisobotlari",
      last_path: "/report",
      role: ["admin"],
      iscomponent: true,
    },
    component: () => import("../views/Report/ServiceReport.vue"),
  },
  {
    path: "/contact_date",
    name: "contact_date",
    meta: {
      auth: true,
      title: "Qayta a'loqa",
      last_path: "/contact_date",
      role: ["operator"],
      iscomponent: false,
    },
    component: () => import("../views/ContactDate/ContactDate.vue"),
  },
  {
    path: "/patient",
    name: "patient",
    meta: {
      auth: true,
      title: "Bemor",
      last_path: role == "operator" ? "/contact_date" : "/patients",
      role: ["operator", "admin", "doctor", "reception"],
      iscomponent: true,
    },
    component: () => import("../views/Patient/PatientHistory.vue"),
  },
  {
    path: "/patients",
    name: "patients",
    meta: {
      auth: true,
      title: "Bemorlar",
      last_path: "/patients",
      role: ["operator", "admin", "doctor", "reception"],
      iscomponent: false,
    },
    component: () => import("../views/Patient/Patient.vue"),
  },
  {
    path: "/navbat",
    name: "navbat",
    meta: { auth: false, title: "Navbat", last_path: "/navbat" },
    component: () => import("../views/Queue/Queue.vue"),
  },
  {
    path: "/daily-procedures",
    name: "daily-procedures",
    meta: {
      auth: true,
      title: "Kunlik Muolajalar Hisoboti",
      last_path: "/report",
      role: ["admin"],
    },
    component: () => import("../views/Report/DailyProcedures.vue"),
  },
  {
    path: "/daily-consultant",
    name: "daily-consultant",
    meta: {
      auth: true,
      title: "Kunlik Konsultatsiya Hisoboti",
      last_path: "/report",
      role: ["admin"],
    },
    component: () => import("../views/Report/DailyConsultant.vue"),
  },
  {
    path: "/user-procedures",
    name: "user-procedures",
    meta: {
      auth: true,
      title: "Hodimning muolajasi boyicha hisobot",
      last_path: "/report",
      role: ["admin"],
    },
    component: () => import("../views/Report/UserProcedures.vue"),
  },
  {
    path: "/procedures",
    name: "procedures",
    meta: {
      auth: true,
      title: "Muolaja boyicha hisobot",
      last_path: "/report",
      role: ["admin"],
    },
    component: () => import("../views/Report/Procedures.vue"),
  },
  {
    path: "/report-kpi",
    name: "report-kpi",
    meta: {
      auth: true,
      title: "KPI boyicha hisobot",
      last_path: "/report",
      role: ["admin"],
    },
    component: () => import("../views/Report/Kpi.vue"),
  },
  {
    path: "/monthly-consultations",
    name: "monthly-consultations",
    meta: {
      auth: true,
      title: "Oylik Konsultatsiya hisoboti",
      last_path: "/report",
      role: ["admin"],
    },
    component: () => import("../views/Report/MonthlyConsultation.vue"),
  },
  {
    path: "/user-consultant",
    name: "user-consultant",
    meta: {
      auth: true,
      title: "Hodimning konsultatsiya hisoboti",
      last_path: "/report",
      role: ["admin"],
    },
    component: () => import("../views/Report/UserConsultant.vue"),
  },
  
];

routes = routes.filter((route) => {
  if (route.meta.role) {
    return route.meta.role.includes(role);
  } else {
    return route;
  }
});

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem("access_token") !== null;

  if (to.matched.some((record) => record.meta.auth)) {
    if (!loggedIn) {
      next("/");
    }
  }
  next();
});

export default router;
