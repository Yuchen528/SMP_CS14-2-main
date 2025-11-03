<template>
  <!-- HomePage control the display of 1-4 page, and transfer data and stream -->
  <div class="wizard-page">
    <HeaderDecoration :is-dark="isDark" @toggle-mode="toggleMode" />

    <!-- Process Bar -->
    <div class="steps-indicator">
      <div
        v-for="(step, index) in steps"
        :key="index"
        :class="['step-item', { active: currentStep === index }]"
      >
        {{ step.label }}
      </div>
    </div>

    <!-- context switch -->
    <transition name="slide-fade" mode="out-in">

        <keep-alive>
          <component
            v-if="steps.length > 0 && steps[currentStep]"
            ref="stepComponent"
            :is="steps[currentStep].component"
            v-bind="steps[currentStep].props || {}"
            :is-dark="isDark"
            :screen-stream="sharedScreenStream"
            :camera-enabled="cameraEnabled"
            :mic-enabled="micEnabled"

            @toggle-mode="toggleMode"
            @next="nextStep"
            @set-screen="setScreenStream"
            @set-device-status="setDeviceStatus"
            @user-info="handleUserInfo"
            :key="currentStep"
            :user-info="userInfo"
          >
        
            <template #navigation>
              <div class="navigation-buttons">
                <button v-if="currentStep > 0" class="back-btn" @click="prevStep">Back</button>
                <button v-if="currentStep < steps.length - 1" class="next-btn" @click="nextStep">Next</button>
              </div>
            </template>

          </component>

        </keep-alive>

    </transition>

  </div>
</template>



<script>
  import HeaderDecoration from '@/components/HeaderDecoration.vue';

  import PageOne from './PageOne.vue';
  import PageTwo from './PageTwo.vue';
  import PageThree from './PageThree.vue';
  import PageFour from './PageFour.vue';

  import { markRaw } from 'vue';
  import axios from 'axios';

  export default {
    name: 'RecordWizard',
    props: {
      isDark: Boolean
    },
    components: {
      HeaderDecoration,
    },
    data() {
      return {
        currentStep: 0,
        sharedScreenStream: null,
        cameraEnabled: false,
        micEnabled: false,
        taskData: null, //data of instruction
        userInfo: null, //data of user in page one
        steps: []  
      };
    },
    async mounted() {
      const fileName = this.$route.query.file
      if (fileName) {
        try {
          const res = await axios.get('/api/projectTask/get_projectTask', { params: { file: fileName } })
          // console.log('✅ File Acquisition Successful:', res.data)
          this.taskData = res.data
        } catch (err) {
          console.error('❌ File Acquisition Failed:', err)
        }
      }

      // Initialize the authorization process form
      // Transfer data among each page
      this.steps = [
        { label: 'About Me',        component: markRaw(PageOne) },
        { label: 'My Cam & Mic',    component: markRaw(PageTwo) },
        { label: 'Share My Screen', component: markRaw(PageThree) },
        { label: 'Finish Setup',    component: markRaw(PageFour),
          props: {
            uploadFile:   this.taskData,
            userInfoFile: this.userInfo
          }
        }
      ]
    },
    methods: {
      nextStep() {
        const currentComponent = this.$refs.stepComponent;
        if (currentComponent?.validateAndNext && !currentComponent.validateAndNext()) {
          return;
        }

        if (this.currentStep < this.steps.length - 1) {
          this.currentStep++;
        }
      },
      prevStep() {
        if (this.currentStep > 0) {
          this.currentStep--;
        }
      },
      toggleMode(val) {
        this.$emit('toggle-mode', val);
      },
      setScreenStream(stream) {
        this.sharedScreenStream = stream;
      },
      setDeviceStatus({ camera, mic }) {
        this.cameraEnabled = camera;
        this.micEnabled = mic;
      },
      handleUserInfo(userInfo) {
        this.userInfo = userInfo;
        this.steps[3].props.userInfoFile = userInfo;
      }
    }
  };
</script>

<style>
.wizard-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color);
}

.steps-indicator {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  gap: 20px;
}
.step-item {
  padding: 10px 20px;
  border-bottom: 2px solid transparent;
  color: var(--text-color);
  font-size: 16px;
  transition: all 0.3s ease;
}
.step-item.active {
  font-weight: bold;
  border-color: #2196F3;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(200px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-200px);
}

.navigation-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 16px;
}
.back-btn,
.next-btn {
  background-color: #2196F3;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}
</style>
