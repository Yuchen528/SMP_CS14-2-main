<template>
  <div class="page">

    <!-- Form for 'My Cam & Mic' page -->
    <div class="card-container">
      <!-- Camera Authorization -->
      <div class="Camera-permission-card">
        <h2>Camera Access</h2>
        <p v-if="cameraGranted">Granted Successfully !</p>
        <p v-else> Not Granted</p>
        <label class="switch">
          <input type="checkbox" v-model="cameraOn" @change="handleCameraToggle" />
          <span class="slider"></span>
        </label>
        <video
          v-show="cameraGranted && cameraOn"
          ref="cameraVideo"
          autoplay
          playsinline
          muted
          class="camera-preview"
        ></video>
      </div>

      <!-- Microphone Authorization -->
      <div class="Mico-permission-card">
        <h2>Microphone Access</h2>
        <p v-if="microphoneGranted">Granted Successfully !</p>
        <p v-else> Not Granted.</p>
        <label class="switch">
          <input type="checkbox" v-model="microphoneOn" @change="handleMicrophoneToggle" />
          <span class="slider"></span>
        </label>
        <canvas
          v-show="microphoneGranted && microphoneOn"
          ref="micCanvas"
          class="mic-visual"
        ></canvas>
      </div>
    </div>

    <slot name="navigation" />
  </div>
</template>

<script>
export default {
  name: "PageTwo",
  props: {
    isDark: Boolean
  },
  data() {
    return {
      cameraGranted: false,
      cameraOn: false,
      microphoneGranted: false,
      microphoneOn: false,
      cameraStream: null,
      micStream: null,
      audioContext: null,
      analyser: null,
      animationFrameId: null
    };
  },
  methods: {
    async handleCameraToggle() {
      if (this.cameraOn) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ video: true });
          this.cameraGranted = true;
          this.cameraStream = stream;
            const video = this.$refs.cameraVideo;
          if (video) {
            video.srcObject = stream;
          }
        } catch (err) {
          this.cameraGranted = false;
          this.cameraOn = false;
          alert("Unable to access camera.");
        }
      } else {
        if (this.cameraStream) {
          this.cameraStream.getTracks().forEach(track => track.stop());
        }
        this.cameraGranted = false;
        this.cameraStream = null;
      }
    },
    async handleMicrophoneToggle() {
      if (this.microphoneOn) {
        try {
          this.micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.microphoneGranted = true;
          this.startMicVisualization();
        } catch (err) {
          this.microphoneGranted = false;
          this.microphoneOn = false;
          alert("Unable to access microphone.");
        }
      } else {
        this.stopMicVisualization();
        this.microphoneGranted = false;
      }
    },
    startMicVisualization() {
      const canvas = this.$refs.micCanvas;
      const ctx = canvas.getContext("2d");
      canvas.width = 260;
      canvas.height = 100;

      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const source = this.audioContext.createMediaStreamSource(this.micStream);
      this.analyser = this.audioContext.createAnalyser();
      source.connect(this.analyser);
      this.analyser.fftSize = 256;

      const bufferLength = this.analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const draw = () => {
        this.animationFrameId = requestAnimationFrame(draw);
        this.analyser.getByteFrequencyData(dataArray);

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const barWidth = (canvas.width / bufferLength) * 1.5;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
          const barHeight = dataArray[i];
          const r = 50 + barHeight;
          const g = 100;
          const b = 200;
          ctx.fillStyle = `rgb(${r},${g},${b})`;

          ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
          x += barWidth + 1;
        }
      };
      draw();
    },
    stopMicVisualization() {
      if (this.audioContext) {
        this.audioContext.close();
        this.audioContext = null;
      }
      if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId);
        this.animationFrameId = null;
      }
      if (this.micStream) {
        this.micStream.getTracks().forEach(track => track.stop());
        this.micStream = null;
      }
    },
    validateAndNext() {
      // send the permission status of camera and microphone to recordWizard.vue
      this.$emit('set-device-status', {
        camera: this.cameraGranted,
        mic: this.microphoneGranted
      });
      return true;
    },


  },
  activated() {
    if (this.cameraStream && this.cameraGranted) {
    this.cameraOn = true;
    const video = this.$refs.cameraVideo;
    if (video) {
      video.srcObject = this.cameraStream;
    }
    }

  if (this.micStream && this.microphoneGranted) {
    this.microphoneOn = true;
    this.startMicVisualization();
  }
    },
  deactivated() {
    const video = this.$refs.cameraVideo;
    if (video) {
      video.srcObject = null; // Stop previewing when redirecting to another page
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
  align-items: flex-start; 
  gap: 40px;
  margin-top: 150px;
  justify-content: center;
  flex-wrap: wrap;
  width: 100%;
}

.Camera-permission-card {
  background-color: var(--wrap-color);
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  width: 280px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  
}

.Mico-permission-card {
  background-color: var(--wrap-color);
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  width: 280px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.camera-preview {
  width: 100%;
  height: auto;
  margin-top: 10px;
  border-radius: 6px;
  box-shadow: 0 0 5px rgba(0,0,0,0.2);
}

.mic-visual {
  width: 100%;
  height: 100px;
  margin-top: 10px;
  border-radius: 6px;
  background: #eee;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
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

</style>