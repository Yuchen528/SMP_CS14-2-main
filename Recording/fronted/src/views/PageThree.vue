<template>
  <div class="page">

    <!-- Form for 'Share My Screen' page -->
    <div class="card-container">
      <div class="permission-card">
        <h2>Screen Sharing</h2>
        <p class="hint" v-if="!screenGranted">Please turn on screen sharing</p>

        <label class="switch">
          <input type="checkbox" v-model="screenOn" @change="handleScreenShare">
          <span class="slider"></span>
          
        </label>

        <video
          v-show="screenGranted && screenOn && screenStream"
          ref="screenVideo"
          autoplay
          playsinline
          muted
          class="screen-preview"
        ></video>
      </div>
    </div>
    <slot name="navigation" />
  </div>
</template>

<script>
export default {
  name: "PageThree",
  props: {
    isDark: Boolean
  },
  data() {
    return {
      screenOn: false,
      screenGranted: false,
      screenStream: null
    };
  },
  methods: {
    async handleScreenShare() {
      if (this.screenOn) {
        try {
          const stream = await navigator.mediaDevices.getDisplayMedia({
            video: true,
            audio: {
              autoGainControl: false,
              echoCancellation: false,
              noiseSuppression: false,
            }
          });
          const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.screenStream = stream;
          this.screenGranted = true;
          const combinedStream = new MediaStream([
            ...stream.getTracks(),
            ...audioStream.getTracks()
          ]);
          this.$emit('set-screen', combinedStream);
          const video = this.$refs.screenVideo;
          if (video) {
            video.srcObject = stream;
            try {
              await video.play();
            } catch (e) {
              console.warn('video.play() failed:', e);
            }
          }
        } catch (err) {
          this.screenOn = false;
          this.screenGranted = false;
          alert("Please turn on screen sharing, otherwise you will not be able to record !");
        }
      } else {
        if (this.screenStream) {
          this.screenStream.getTracks().forEach(track => track.stop());
        }
        this.screenGranted = false;
        this.screenStream = null;
      }
    },
    validateAndNext() {
      if (!this.screenGranted) {
        alert("Please enable screen sharing before continuing");
        return false;
      }
      return true;
    }
  },
  activated() {
    this.screenOn = false;
    this.screenGranted = false;
    this.screenStream = null;
    const video = this.$refs.screenVideo;
    if (video) {
      video.srcObject = null;
    }
  },
  beforeUnmount() {
    if (this.screenStream) {
      this.screenStream.getTracks().forEach(track => track.stop());
    }
  }
};
</script>

<style>
.page {
  min-height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color);
}

.card-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-top: 40px;
  width: 100%;
}

.permission-card {
  background-color: var(--wrap-color);
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  width: 80%;
  max-width: 960px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.hint {
  font-size: 14px;
  margin: 10px 0;
  color: #f44336;
}

.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
  margin-top: 10px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 20px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: #fff;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

.screen-preview {
  width: 100%;
  height: auto;
  margin-top: 20px;
  border-radius: 6px;
  box-shadow: 0 0 5px rgba(0,0,0,0.2);
}

.record-btn {
  margin-top: 20px;
  background-color: #4caf50;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.record-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
