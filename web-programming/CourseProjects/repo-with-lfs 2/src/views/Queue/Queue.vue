<template>
  <div class="btn-group zoom-buttons">
    <button class="btn btn-sm btn-light" @click="change_zoom(true)">
      <i class="fas fa-plus"></i>
    </button>
    <button class="btn btn-sm btn-light" @click="change_zoom(false)">
      <i class="fas fa-minus"></i>
    </button>
  </div>
  <div class="queue text-dark">
    <div class="row">
      <div class="col-md-6">
        <h6 class="card-title text-center">Qabuldagilar</h6>
        <div class="container responsive-y" id="data" style="height: 87vh">
          <div class="card my-2 py-0 success" v-for="que in inroom" :key="que">
            <div class="card-body">
              <div class="row">
                <div class="col">
                  <h1 class="card-title fw-bolder mb-0">
                    {{ que.number }}-navbat
                  </h1>
                </div>
                <div class="col">
                  <h1 class="card-title fw-bolder mb-0 float-end">
                    {{ que.room }}-xona
                  </h1>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <h6 class="card-title text-center">Navbatdagilar</h6>
        <div class="container responsive-y" id="data2" style="height: 87vh">
          <div
            class="card my-2 py-0 warning"
            v-for="que in waitings"
            :key="que"
          >
            <div class="card-body">
              <div class="row">
                <div class="col">
                  <h1 class="card-title fw-bolder mb-0">
                    {{ que.number }}-navbat
                  </h1>
                </div>
                <div class="col">
                  <h1 class="card-title fw-bolder mb-0 float-end">
                    {{ que.room }}-xona
                  </h1>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  audio_delete,
  audio_play,
  catchError,
  queues_inroom,
  queues_waiting,
  socket,
} from "@/components/Utils/api";
import Swal from "sweetalert2";

export default {
  name: "Queue",
  data() {
    return {
      waitings: [],
      inroom: [],
      queue: [],
      zoom: parseInt(localStorage["zoom"]) || 100,
    };
  },
  methods: {
    pageScroll() {
      var div = document.getElementById("data");
      if (div.clientHeight < div.scrollHeight) {
        if (div.scrollTop + div.clientHeight >= div.scrollHeight - 5) {
          div.scrollTop = 0;
          this.get_queue_in_room();
        } else {
          div.scrollTop = div.scrollTop + 1;
        }
      }
    },
    pageScroll2() {
      var div = document.getElementById("data2");
      if (div.clientHeight < div.scrollHeight) {
        if (div.scrollTop + div.clientHeight >= div.scrollHeight - 5) {
          div.scrollTop = 0;
          this.get_queue();
        } else {
          div.scrollTop = div.scrollTop + 1;
        }
      }
    },
    get_queue_in_room() {
      queues_inroom()
        .then((e) => {
          this.inroom = e.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    get_queue() {
      queues_waiting()
        .then((e) => {
          this.waitings = e.data;
        })
        .catch((error) => {
          catchError(error);
        });
    },
    get_current_que() {
      socket("ws_navbat").onmessage = (event) => {
        if (event.data != "Connected!") {
          this.get_queue();
          this.get_queue_in_room();
          let res = JSON.parse(event.data);
          this.PlaySound(res);
          Swal.fire({
            showConfirmButton: false,
            title: res.number,
            text: `${res.room}-xona`,
            timer: 8000,
          });
        }
      };
    },
    PlaySound(e) {
      audio_play(e.number, e.room).then((res) => {
        const audioData = `https://api.taskinmed.uz/tmp/${res.data}`;
        const ctx = new AudioContext();
        fetch(audioData)
          .then((data) => data.arrayBuffer())
          .then((arrayBuffer) => ctx.decodeAudioData(arrayBuffer))
          .then((decodedAudio) => {
            let audio = decodedAudio;
            const playSound = ctx.createBufferSource();
            playSound.buffer = audio;
            playSound.connect(ctx.destination);
            playSound.start(ctx.currentTime);
            playSound.onended = () => {
              audio_delete(res.data);
            };
          });
      });
    },
    change_zoom(e) {
      if (e) {
        this.zoom += 5;
      } else {
        this.zoom -= 5;
      }
      document.body.style.zoom = `${this.zoom}%`;
      localStorage["zoom"] = this.zoom;
    },
  },
  mounted() {
    document.body.style.zoom = `${this.zoom}%`;
    this.get_queue();
    this.get_queue_in_room();
    this.get_current_que();
    setInterval(() => {
      this.pageScroll();
    }, 40);
    setInterval(() => {
      this.pageScroll2();
    }, 40);
    setInterval(() => {
      this.get_queue_in_room();
      this.get_queue();
    }, 5000);
  },
};
</script>

<style>
#main-container {
  background-image: url(../../assets/bg_que.svg);
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

.queue * {
  font-family: calibri;
  color: black;
}

#data::-webkit-scrollbar {
  display: none;
}

.queue h6.card-title {
  font-size: 60px;
  font-weight: 600;
  text-shadow: 4px 4px 2px rgba(255, 255, 255, 0.9);
}

.queue .card {
  background: rgba(255, 255, 255, 0.8) !important;
  border-radius: 16px;
  border: 3px solid #fff;
}

h2.swal2-title {
  font-size: 200px;
  padding: 0;
}

.swal2-html-container {
  font-size: 70px;
  margin: 0;
}

.success {
  border: 5px solid lightgreen !important;
}

.warning {
  border: 5px solid orange !important;
}

.zoom-buttons {
  position: fixed;
  right: 50%;
  transform: translate(50%);
}

.swal2-html-container {
  font-size: 50px !important;
}
</style>
