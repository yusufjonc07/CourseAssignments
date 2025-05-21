import axios from "axios";
import Swal from "sweetalert2";

export function disabled(bool) {
  document.querySelectorAll('[type="submit"]').forEach((e) => {
    e.disabled = bool;
  });
}

const api = axios.create({
  baseURL: "http://localhost/",
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
  },
});

export function socket(endpoint) {
  var ws = new WebSocket(`ws://localhost/${endpoint}`);

  ws.onerror = (event) => {
    console.log(event);
  };

  ws.onclose = (event) => {
    console.log(event);
    setTimeout(() => {
      socket(endpoint);
    }, 5000);
  };

  return ws;
}

export function success(target) {
  if (target !== undefined) {
    if (typeof target == "number") {
      document.querySelectorAll("[data-dismiss='modal']")[target].click();
    } else if (typeof target == "string") {
      document.querySelector(`[${target}]`).click();
    }
  }
  return Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 800,
    timerProgressBar: true,
  }).fire({
    icon: "success",
    title: "Amaliyot bajarildi",
  });
}

export function catchError(error) {
  if (error.response?.status == 401) {
    console.clear();
    localStorage.removeItem("role");
    localStorage.removeItem("access_token");
    Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 20000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener("mouseenter", Swal.stopTimer);
        toast.addEventListener("mouseleave", Swal.resumeTimer);
      },
    })
      .fire({
        icon: "error",
        title: "Foydalanuvchi nomi yoki parolda xatolik",
      })
      .then(() => {
        if (window.location.pathname == "/") {
          console.log();
        } else {
          window.location.href = "/";
        }
      });
  } else if (error.message == "Network Error") {
    return Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 2000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener("mouseenter", Swal.stopTimer);
        toast.addEventListener("mouseleave", Swal.resumeTimer);
      },
    }).fire({
      icon: "warning",
      title: "Internet bilan a'loqa mavjud emas",
    });
  } else if (error.response?.status == 422) {
    return Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 2000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener("mouseenter", Swal.stopTimer);
        toast.addEventListener("mouseleave", Swal.resumeTimer);
      },
    }).fire({
      icon: "warning",
      title: "Ma'lumot to'liq emas",
    });
  } else if (error.response?.status == 404) {
    return Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 2000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener("mouseenter", Swal.stopTimer);
        toast.addEventListener("mouseleave", Swal.resumeTimer);
      },
    }).fire({
      icon: "error",
      title: "URL manzil notog'ri !",
    });
  } else if (error.response?.status == 400) {
    return Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 2000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener("mouseenter", Swal.stopTimer);
        toast.addEventListener("mouseleave", Swal.resumeTimer);
      },
    }).fire({
      icon: "error",
      title: error.response?.data.detail,
    });
  }
  console.clear();
}

// TOKEN

export function token(data) {
  let params = new URLSearchParams();

  params.append("username", data.username);
  params.append("password", data.password);

  return api.post("token", params);
}

// CURRENT USER

export function current_user() {
  return api.get(`me`);
}

// USERS

export function users_get(page, limit, search, roles = "") {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(
    `users?page=${page}&limit=${limit}&roles=${roles}${search_filter}`
  );
}

export function user_create(body) {
  return api.post(`user/create`, body);
}

export function user_update(body) {
  return api.put(`user/${body.id}/update`, body);
}

// SERVICES

export function services_get(page, limit) {
  return api.get(`services?page=${page}&limit=${limit}`);
}

export function service_create(body) {
  return api.post(`service/create`, body);
}

export function service_update(body) {
  return api.put(`service/${body.id}/update`, body);
}

export function service_procedures_get(page, limit, id, search = "", type) {
  let search_filter = search ? `&search=${search}` : "";
  return api.get(
    `serviceProcedures?page=${page}&limit=${limit}&service_id=${id}${
      type ? `&type=${type}` : ""
    }${search_filter}`
  );
}

export function service_procedure_create(body) {
  return api.post(`serviceProcedure/create`, body);
}

export function service_procedure_update(body) {
  return api.put(`serviceProcedure/${body.id}/update`, body);
}

// DOCTORS

export function doctors_get(page, limit, user_id, service_id) {
  return api.get(
    `doctors?user_id=${user_id}&service_id=${service_id}&page=${page}&limit=${limit}`
  );
}

export function doctor_create(body) {
  return api.post(`doctor/create`, body);
}

export function doctor_update(body) {
  return api.put(`doctor/${body.id}/update`, body);
}

// CASHERS

export function cashers_get(page, limit, user_id) {
  return api.get(`cashers?user_id=${user_id}&page=${page}&limit=${limit}`);
}

export function casher_create(body) {
  return api.post(`casher/create`, body);
}

export function casher_update(body) {
  return api.put(`casher/${body.id}/update`, body);
}

// CASHREGS

export function cashregs_get(page, limit) {
  return api.get(`cashregs?page=${page}&limit=${limit}`);
}

export function get_one_cashreg(page, limit, id, search) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(
    `get_one_cashreg?id=${id}&page=${page}&limit=${limit}${search_filter}`
  );
}

export function get_cashregs_money() {
  return api.get(`get_cashregs_money`);
}

export function cashreg_create(body) {
  return api.post(`cashreg/create`, body);
}

export function income_accept(body) {
  return api.post(`income/accept`, body);
}

export function cashreg_update(body) {
  return api.put(`cashreg/${body.id}/update`, body);
}

// PATIENTS

export function patients_get(page, limit, search) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(`patients?${search_filter}&page=${page}&limit=${limit}`);
}

export function patient_create(body) {
  return api.post(`patient/create`, body);
}

export function patient_exist(body) {
  return api.post(`patient/exist`, body);
}

export function patient_update(body) {
  return api.put(`patient/${body.id}/update`, body);
}

// SOURCES

export function sources_get(page, limit) {
  return api.get(`sources?page=${page}&limit=${limit}`);
}

export function source_create(body) {
  return api.post(`source/create`, body);
}

export function source_update(body) {
  return api.put(`source/${body.id}/update`, body);
}

// DIAGNOSIS

export function diagnosiss_get(page, limit, id) {
  return api.get(`diagnosiss?page=${page}&limit=${limit}&patient_id=${id}`);
}

export function diagnosis_create(body) {
  return api.post(`diagnosis/create`, body);
}

export function diagnosis_confirm(body) {
  return api.post(`diagnosises/confirm`, body);
}

export function diagnosis_update(body) {
  return api.put(`diagnosis/${body.id}/update`, body);
}

export function queue_cancel(id) {
  return api.put(`queue/${id}/cancel`);
}

// QUEUES

export function queues_get(page, limit, step, search, id, date) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(
    `queues?page=${page}&limit=${limit}&step=${step}${search_filter}&patient_id=${id}${
      date ? `&_date=${date}` : ""
    }`
  );
}

export function queues_all_get(
  page,
  limit,
  step,
  search,
  id,
  date = new Date().toISOString().slice(0, 10)
) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(
    `queues_all?page=${page}&limit=${limit}&step=${step}${search_filter}&patient_id=${id}${
      date ? `&_date=${date}` : ""
    }`
  );
}

export function queue_get(id) {
  return api.get(`get_one_queue?id=${id}`);
}

export function diagnosis_paper(id) {
  return api.get(`diagnosis_paper?id=${id}`);
}

export function queue_possibility(room, date, user_id) {
  return api.get(
    `queue_possibility?date=${date}&room=${room}&user_id=${user_id}`
  );
}

export function queue_call(room) {
  return api.get(`queue/call?room=${room}`);
}

export function queue_goout(id) {
  return api.get(`queue/goout?id=${id}`);
}

export function queue_create(body, id) {
  return api.post(`queue/create?inspectionId=${id}`, body);
}

export function queue_complete(id) {
  return api.post(`queue/complete?queue_id=${id}`);
}

export function cashreg_confirm(body) {
  return api.post(`cashreg/confirm`, body);
}

export function queue_update(body) {
  return api.put(`queue/${body.id}/update`, body);
}

// REGIONS

export function regions_get(page, limit) {
  return api.get(`regions?page=${page}&limit=${limit}`);
}

export function region_create(body) {
  return api.post(`region/create`, body);
}

export function region_update(body) {
  return api.put(`region/${body.id}/update`, body);
}

// STATES

export function states_get(page, limit, id) {
  return api.get(`states?region_id=${id}&page=${page}&limit=${limit}`);
}

export function state_create(body) {
  return api.post(`state/create`, body);
}

export function state_update(body) {
  return api.put(`state/${body.id}/update`, body);
}

// DRUGS

export function drugs_get(page, limit, search) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(`drugs?page=${page}&limit=${limit}${search_filter}`);
}

export function drug_create(body) {
  return api.post(`drug/create`, body);
}

export function drug_update(body) {
  return api.put(`drug/${body.id}/update`, body);
}

// RECIPE

export function recipes_get(page, limit) {
  return api.get(`recipes?page=${page}&limit=${limit}`);
}

export function recipe_create(body, id) {
  return api.post(`recipe/create?diagnosis_id=${id}`, body);
}

export function recipe_update(body) {
  return api.put(`recipe/${body.id}/update`, body);
}

export function recipe_delete(id) {
  return api.delete(`recipe_delete/${id}`);
}

// NAVBAT

export function queues_waiting() {
  return api.get(`queues/waiting`);
}

export function queues_inroom() {
  return api.get(`queues/inroom`);
}

export function queues_skipped() {
  return api.get(`queues/skipped`);
}

// EXPENSE

export function expences_get(page, limit, from_date, to_date, search) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }

  let date_filter = "";
  if (from_date && to_date) {
    date_filter = `from_date=${from_date}&to_date=${to_date}&`;
  } else {
    date_filter = "";
  }

  return api.get(
    `expences?${date_filter}page=${page}&limit=${limit}${search_filter}`
  );
}

export function expence_create(body) {
  return api.post(`expence/create`, body);
}

export function expence_update(body) {
  return api.put(`expence/${body.id}/update`, body);
}

// REPORT

export function reports_get(from_date, to_date) {
  let date_filter = "";
  if (from_date && to_date) {
    date_filter = `?from_date=${from_date}&to_date=${to_date}&`;
  } else {
    date_filter = "";
  }

  return api.get(`reports${date_filter}`);
}

export function state_reports_get(page, limit, from_date, to_date, state_id) {
  let date_filter = "";
  if (from_date && to_date) {
    date_filter = `from_date=${from_date}&to_date=${to_date}&`;
  } else {
    date_filter = "";
  }

  return api.get(
    `state_reports?state_id=${state_id}&${date_filter}page=${page}&limit=${limit}`
  );
}

export function service_reports_get(
  page,
  limit,
  from_date,
  to_date,
  service_id
) {
  let date_filter = "";
  if (from_date && to_date) {
    date_filter = `from_date=${from_date}&to_date=${to_date}&`;
  } else {
    date_filter = "";
  }

  return api.get(
    `service_reports?service_id=${service_id}&${date_filter}page=${page}&limit=${limit}`
  );
}

export function service_procedures_reports_get(page, limit, date) {
  return api.get(
    `service_procedures_reports?page=${page}&limit=${limit}&date=${date}`
  );
}

export function daily_consultations_get(page, limit, date) {
  return api.get(
    `daily_consultations?page=${page}&limit=${limit}&date=${date}`
  );
}

export function monthly_procedures_get(
  year,
  month,
  id = 0,
  user_id = 0,
  service_id = 0
) {
  return api.get(
    `monthly_procedures?id=${id}&year=${year}&month=${month}&user_id=${user_id}&service_id=${service_id}`
  );
}

export function monthly_consultations_get(
  year,
  month,
  id = 0,
  user_id = 0,
  service_id = 0
) {
  return api.get(
    `monthly_consultations?id=${id}&year=${year}&month=${month}&user_id=${user_id}&service_id=${service_id}`
  );
}
// INCOME

export function incomes_get(page, limit, from_date, to_date, search) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }

  let date_filter = "";
  if (from_date && to_date) {
    date_filter = `from_date=${from_date}&to_date=${to_date}&`;
  } else {
    date_filter = "";
  }

  return api.get(
    `incomes?${date_filter}page=${page}${search_filter}&limit=${limit}`
  );
}

// RECALL

export function settings_get() {
  return api.get(`settings`);
}

export function setting_update(body) {
  return api.put(`setting_update`, body);
}

export function counts_get() {
  return api.get(`count_of_calls`);
}

export function recalls_get(
  page,
  limit,
  from_date,
  to_date,
  patient_id,
  queue,
  completed
) {
  let date_filter = "";
  if (from_date && to_date) {
    date_filter = `&from_date=${from_date}&to_date=${to_date}`;
  } else {
    date_filter = "";
  }

  return api.get(
    `recalls?queue=${queue}&completed=${completed}&page=${page}&limit=${limit}&patient_id=${patient_id}${date_filter}`
  );
}

export function recall_create(body) {
  return api.post(`recall/create`, body);
}

export function recall_talked(body) {
  return api.put(`recall/${body.id}/talked`, body);
}

export function recall_update(body) {
  return api.put(`recall/${body.id}/update`, body);
}

export function recall_delete(id) {
  return api.delete(`recall/${id}/delete`);
}

// ILLNESS

export function illnesses_get(page, limit, search, id) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(
    `illnesses?service_id=${id}&page=${page}&limit=${limit}${search_filter}`
  );
}

export function illness_create(body) {
  return api.post(`illness/create`, body);
}

export function illness_update(body) {
  return api.put(`illness/${body.id}/update`, body);
}

// RECIPE TEMPLATES

export function recipe_t_get(page, limit, search, id) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(
    `recipe_templates?illness_id=${id}&page=${page}&limit=${limit}${search_filter}`
  );
}

export function recipe_t_create(body) {
  return api.post(`recipe_template/create`, body);
}

export function recipe_t_update(body) {
  return api.put(`recipe_template/${body.id}/update`, body);
}

// QUEUE TIME

export function minute_update(body) {
  return api.put(`minute_update`, body);
}

// PARTNERS
export function partners_get(page, limit, id) {
  return api.get(`partners?source_id=${id}&page=${page}&limit=${limit}`);
}

export function partner_create(body) {
  return api.post(`partner/create`, body);
}

export function partner_update(body) {
  return api.put(`partner/${body.id}/update`, body);
}

export function partner_employee_create(body, id) {
  return api.post(`partner_employee/create?partner_id=${id}`, body);
}

export function partner_employee_update(body, id) {
  return api.put(`partner_employee/${id}/update`, body);
}

// INSPECTIONS

export function inspcetion_update(body) {
  return api.put(`inspection/${body.id}/update`, body);
}

export function inspcetion_cancel(id) {
  return api.put(`inspection/${id}/cancel`);
}

export function inspection_get(id) {
  return api.get(`inspection/${id}`);
}

export function inspection_create(body, id) {
  return api.post(`inspection/create?patient_id=${id}`, body);
}

// STATIONARY

export function inpatients_get(page, limit, search) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(`inpatients?${search_filter}&page=${page}&limit=${limit}`);
}

export function inpatient_create(body) {
  return api.post(`inpatient/create`, body);
}

export function inpatient_update(body) {
  return api.put(`inpatient/${body.id}/update`, body);
}

// STATIONARY PROCEDURES

export function inpatient_procedures_get(page, limit, search) {
  let search_filter = "";
  if (search) {
    search_filter = `&search=${search}`;
  } else {
    search_filter = "";
  }
  return api.get(
    `inpatient_procedures?${search_filter}&page=${page}&limit=${limit}`
  );
}

export function inpatient_get(id) {
  return api.get(`inpatient/${id}/one`);
}

export function inpatient_procedure_create(body, date) {
  return api.post(`inpatient_procedure/create?date=${date}`, body);
}

export function inpatient_procedure_update(body) {
  return api.put(`inpatient_procedure/${body.id}/update`, body);
}

export function inpatient_procedure_delete(id) {
  return api.delete(`inpatient_procedure/${id}/delete`);
}

export function inpatient_procedure_modify(body) {
  return api.put(`inpatient_procedure_item/${body.id}/modify`, body);
}

export function inpatient_payment_create(body) {
  return api.post(`inpatient/${body.id}/payment`, body);
}

export function inpatient_left_date(body) {
  return api.put(`inpatient/${body.id}/left?Date=${body.date}`);
}

// SOUND

export function audio_play(number, room) {
  return api.get(`audio/${number}/${room}`);
}

export function audio_delete(filename) {
  return api.delete(`audio/${filename}`);
}
