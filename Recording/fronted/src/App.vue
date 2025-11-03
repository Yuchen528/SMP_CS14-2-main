<template>
  <div id="app">
    <!-- Red frame during the recording status -->
    <div v-if="isRecording" class="global-recording-border"></div>
    <!-- dark mode -->
    <router-view :is-dark="isDarkMode" @toggle-mode="toggleMode" />
    <!-- main body content -->
    <main style="min-height: 300px; padding: 1rem;">
    </main>
    <!-- footer -->
    <FooterDecoration />
  </div>
  
</template>

<script>
import FooterDecoration from "@/components/FooterDecoration.vue";

export default {
  name: "App",
  components: {
    FooterDecoration,
  },
  data() {
    return {
      isRecording: false,
      isDarkMode: false
    };
  },
  provide() {
    return {
      isRecording: () => this.isRecording,
      setRecording: this.setRecording
    };
  },
  mounted() {
   // Read user preferences and set the mode
   const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
   this.toggleMode(prefersDark);
  },
  methods: {
    setRecording(value) {
      this.isRecording = value;
    },
    toggleMode(val) {
      this.isDarkMode = val;

      document.body.classList.remove('dark-mode', 'light-mode');

      document.body.classList.add(val ? 'dark-mode' : 'light-mode');


    }
  }
};
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    background-color: var(--bg-color);
    min-height: 100vh;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
  }

  /* Light color mode variable */
  body.light-mode {
    --bg-color: #ffffff;
    --text-color: #000000;
    --header-bg: #f5f5f5;
    --wrap-color:#eef4f4
  }

  /* Dark color mode variable */
  body.dark-mode {
    --bg-color: #1e1e1e;
    --text-color: #ffffff;
    --header-bg: #333333;
    --wrap-color:#006666
  }

  body, html, #app {
    margin: 0;
    padding: 0;
    background-color: var(--bg-color);
    color: var(--text-color);
    font-family: sans-serif;
    transition: background-color 0.3s, color 0.3s;
  }


  .global-recording-border {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    z-index: 9999;
    border: 4px solid red;
    border-radius: 20px;
    box-sizing: border-box;
    background: linear-gradient(135deg, rgba(255,0,0,0.1), rgba(255,0,0,0.05));
    animation: pulse-border 1.2s ease-in-out infinite;
    box-shadow: 0 0 16px 6px rgba(255, 0, 0, 0.5);
  }

  @keyframes pulse-border {
    0%, 100% {
      border-color: red;
      opacity: 1;
    }
    50% {
      border-color: rgba(255, 0, 0, 0.3);
      opacity: 0.5;
    }
  }

</style>
