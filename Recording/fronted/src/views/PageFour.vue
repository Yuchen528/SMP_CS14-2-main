<template>
  <div class="page">

    <!-- Form for 'Finish Setup' page -->
    <div class="container">
      <h2>Record Task</h2>

      <div>
        <button @click="openRecordingPopup" id="startSessionBtn">Start Session</button>
      </div>

      <div v-if="showPopupMessage && !tasksComplete">
        <p>Please follow the pop-up window</p>
      </div>
      <div v-if="tasksComplete">
        <p>🎉 Congratulations! All the tasks have been completed!</p>
        <button @click="handleQuit">Quit</button>
      </div>


      <div  id="backBtn">
        <slot name="navigation" />
      </div>
    </div>
    
  </div>
</template>
    
<script>
  import axios from 'axios'
  export default {
    name: 'PageFour',
    inject: ['setRecording'],
    // data and stream from HomePage
    props: {
      screenStream: Object,
      cameraEnabled: Boolean,
      micEnabled: Boolean,
      // data for popup window content
      uploadFile: {
        type: Object,
        default: () => ({ projectName: '', tasks: [] })
      },
      // data from PageOne
      userInfoFile: {
        type:    Object,
        default: () => ({
          uuid: '',
          firstName: '',
          lastName: '',
          email: ''
        })
      }
    },
    data() {
      return {
        internalScreenStream: null,
        cameraStream: null,
        audioStream: null,
        cameraRecorder: null,
        screenRecorder: null,
        micRecorder: null,
        cameraChunks: [],
        screenChunks: [],
        micChunks: [],
        recordedCameraUrl: null,
        recordedScreenUrl: null,
        recordedMicUrl: null,
        isRecording: false,
        currentTaskIndex: 0,
        recordingPopup: null,
        timerInterval: null,
        showPopupMessage: false, 
        tasksComplete: false
      };
    },
    watch: {
      screenStream(newStream) {
        this.internalScreenStream = newStream;
      }
    },
    created() {
      this.resetState();
      this.internalScreenStream = this.screenStream;
    },
    methods: {        
      handleQuit() {
        if (this.recordingPopup && !this.recordingPopup.closed) {
          this.recordingPopup.close();
        }
        window.close();
      },   
      taskShow(index) {
        const startSessionBtn = document.getElementById("startSessionBtn");
        startSessionBtn.style.display = 'none';
        const backBtn = document.getElementById("backBtn");
        backBtn.style.display = 'none';
        const tasks = this.uploadFile.tasks;
        const popup = this.recordingPopup;
        if (!popup || !popup.document) return;

        // 👉 For the last task
        const task = tasks[index];
        if (!task || index >= tasks.length) {
          this.tasksComplete = true;
          popup.document.getElementById('taskContainer').innerHTML = `
            <p>🎉 All Task Complete！</p>
            <button id="quitBtn">Quit</button>
          `;

          const startBtn = popup.document.getElementById("startBtn");
          if (startBtn) startBtn.style.display = 'none';
          if (startBtn) startBtn.remove();
          popup.document.body.addEventListener('click', (event) => {
            if (event.target && event.target.id === 'quitBtn') {
              popup.close();
              window.close();
            }
          });
          return;
        }

        // 👉 For the other task
        popup.document.getElementById("projectName").textContent =
          "Project Name: " + (this.uploadFile.projectName || "(Unnamed)");
        popup.document.getElementById("taskContainer").innerHTML = `
          <h3>Task ${task.taskIndex}: ${task.taskTitle}</h3>
          <p><strong>Instructions:</strong></p>
          ${task.taskInstructions
            .split(/\r?\n/)
            .map(
              (line) => `<div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${line}</div>`
            )
            .join("")}
          <p><strong>Upload:</strong> ${task.taskUpload}</p>
          <p><strong>Instructions URL:</strong> <a href="${task.urlForInstructions}" target="_blank">${task.urlForInstructions}</a></p>
          <p><strong>Icon:</strong> <img src="${task.iconForThisStep}" style="width:24px;height:24px;"></p>
          <p><strong>Component Type:</strong> ${task.componenttype}</p>
          <p><strong>Tips for this task:</strong></p>
          ${task.taskTip
            .split(/\r?\n/)
            .map(
              (line) => `<div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${line}</div>`
            )
            .join("")}
          <p><strong>Suggested time:</strong> ${task.timeguide} min</p>
        `;
        const startBtn = popup.document.getElementById('startBtn');
        if (startBtn) {
          startBtn.style.display = 'inline-block';
        }
      },
      openRecordingPopup() {
        this.showPopupMessage = true;
        const left = screen.width - 500;
        // Open the popup window
        this.recordingPopup = window.open(
          "",
          "recordingStatusWindow",
          `width=380,height=600,top=150,left=${left},resizable=no,scrollbars=yes`
        );
        if (!this.recordingPopup || this.recordingPopup.closed || typeof this.recordingPopup.closed === 'undefined') {
          alert("🔒 Pop-up window was blocked. Please allow pop-ups for this site.");
          return;
        }

        // Render the content in the popup window
        const doc = this.recordingPopup.document;
        doc.open();
        doc.write(`
          <html>
            <body>
              <div id="timer" style="font-size:16px; font-weight:bold; top:10px; right:10px;">Time: 00:00</div>
              <p id="recordingStatus" style="font-size:18px; display: none;">🔴 Recording...</p>
              <div id="loadingSpinner" style="display:none;text-align:center;margin-top:10px;">
              <div style="width:24px;height:24px;border:4px solid #ccc;border-top:4px solid #333;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto;"></div>
              <p style="font-size:14px; margin-top:8px; color:#555;">Submitting... Please wait a second</p>
              </div>
              <hr/>
              <h2 id="projectName"></h2>
              <div style="display:flex; gap: 10px; justify-content: center;">
                <button id="startBtn" class="task-btn">Start Task</button>
                <button id="completeBtn" class="task-btn" style="display: none;">Finish Task</button>
                <button id="nextBtn" class="task-btn" style="display: none;">Next Task</button>
              </div>
              <div id="taskContainer"></div>




              <style>
                @keyframes spin {
                  0% { transform: rotate(0deg); }
                  100% { transform: rotate(360deg); }
                }
                  
                .task-btn {
                  padding: 10px 20px;
                  font-size: 16px;
                  border: none;
                  border-radius: 8px;
                  background-color: #2196f3;
                  color: white;
                  cursor: pointer;
                  transition: background 0.3s ease, transform 0.2s ease;
                }

                .task-btn:hover {
                  background-color: #1976d2;
                  transform: scale(1.05);
                }

                .task-btn:disabled {
                  background-color: #ccc;
                  cursor: not-allowed;
                }
              </style>
              
              
            </body>
          </html>
        `);
        doc.close();

        // Bind Event with buttons on the popup window
        const waitAndBind = () => {
          try {
            const startBtn = this.recordingPopup.document.getElementById("startBtn");
            const completeBtn = this.recordingPopup.document.getElementById("completeBtn");
            const nextBtn     = this.recordingPopup.document.getElementById("nextBtn");
            const timerEl     = this.recordingPopup.document.getElementById("timer");
            if (!startBtn || !completeBtn || !nextBtn || !timerEl) throw new Error("wait DOM");

            let seconds = 0;

            // Start Task
            startBtn.onclick = async () => {
              startBtn.style.display = "none";
              completeBtn.style.display = "inline-block";

              clearInterval(this.timerInterval);
              seconds = 0;
              this.timerInterval = setInterval(() => {
                seconds++;
                const min = String(Math.floor(seconds / 60)).padStart(2, '0');
                const sec = String(seconds % 60).padStart(2, '0');
                timerEl.textContent = `Time: ${min}:${sec}`;
              }, 1000);

              await this.startRecording(true);
            };

            // Complete Task
            completeBtn.onclick = async () => {
              this.stopRecording();

              clearInterval(this.timerInterval);
              this.timerInterval = null;

              const doc = this.recordingPopup.document;
              const spinner = doc.getElementById("loadingSpinner");
              const nextBtn = doc.getElementById("nextBtn");

              const isLastTask = this.currentTaskIndex === this.uploadFile.tasks.length - 1;

              if (isLastTask) {
                // ✅ last task
                if (spinner) spinner.style.display = "block";
                if (nextBtn) nextBtn.style.display = "none";
                completeBtn.style.display = "none";
              } else {
                // ✅ other tasks
                completeBtn.style.display = "none";
                if (nextBtn) nextBtn.style.display = "inline-block";
              }
            };


            // Next Task
            nextBtn.onclick = async () => {
              nextBtn.style.display = "none";
              startBtn.style.display = "inline-block";

              clearInterval(this.timerInterval);
              seconds = 0;
              timerEl.textContent = "Time: 00:00";

              this.currentTaskIndex++;
              this.taskShow(this.currentTaskIndex);
            };

            // initialize the first task
            this.currentTaskIndex = 0;
            this.taskShow(this.currentTaskIndex);

          } catch (e) {
            setTimeout(waitAndBind, 50);
          }
        };
        waitAndBind();
      },

      async uploadVideo() {
        const formData = new FormData();
        let isLastTaskfinish = false;
        if(this.currentTaskIndex === this.uploadFile.tasks.length - 1) {
          isLastTaskfinish = true;
        }

        if(this.currentTaskIndex==0){
          formData.append('firstName', this.userInfoFile.firstName);
          formData.append('lastName', this.userInfoFile.lastName);
          formData.append('email', this.userInfoFile.email);
        }
        formData.append('projectName', this.uploadFile.projectName);
        formData.append('uuid', this.userInfoFile.uuid);
        formData.append('taskIndex', this.currentTaskIndex+1);
        formData.append('taskTile', this.uploadFile.tasks[this.currentTaskIndex].taskTitle);

        async function appendBlob(url, fieldName, filename) {
          if (!url) return;
          try {
            const response = await fetch(url);
            const blob = await response.blob();
            formData.append(fieldName, blob, filename);
          } catch (error) {
            console.error(`Error fetching blob from ${url}:`, error);
          }
        }
        await appendBlob(
          this.recordedScreenUrl,
          'recordedScreen',
          `screen.webm`
        );
        await appendBlob(
          this.recordedCameraUrl,
          'recordedCamera',
          `camera.webm`
        );
        await appendBlob(
          this.recordedMicUrl,
          'recordedAudio',
          `audio.webm`
        );
        axios.post('/api/recording/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          if (isLastTaskfinish) {
              const doc = this.recordingPopup.document;
              const spinner = doc.getElementById("loadingSpinner");
              const nextBtn = doc.getElementById("nextBtn");
              if (spinner) spinner.style.display = "none";
              if (nextBtn) nextBtn.style.display = "block";
          }
          console.log("Submission Successful:", response.data);
        })
        .catch(error => {
          console.error("Submission Error:", error);
          alert("Submission Failed. Please try again later.");
        });
      },

      async startRecording(isRestart = false) {
        if (!this.internalScreenStream) {
          alert("Screen sharing stream not being received!");
          return;
        }

        if (!isRestart) {
          this.showPopupMessage = true;
          this.openRecordingPopup();
        }

        this.setRecording(true);

        try {
            this.cameraChunks = [];
            this.screenChunks = [];
            this.micChunks = [];


          // 🟢 Screen capture
          if (!isRestart || !this.screenRecorder) {
            this.screenRecorder = new MediaRecorder(this.internalScreenStream);
            this.screenRecorder.ondataavailable = e => {
              if (e.data.size > 0) {
                this.screenChunks.push(e.data);
              }
            };
          }

          this.screenRecorder.onstop = () => {
            if (this.screenChunks.length > 0) {
              const blob = new Blob(this.screenChunks, { type: 'video/webm' });
              this.recordedScreenUrl = URL.createObjectURL(blob);
            } else {
              console.warn("⚠️ There is no data in the screen recording");
            }
          };
          this.screenRecorder.start();

          // 🟢 Camera capture
          if (this.cameraEnabled) {
            if (!isRestart || !this.cameraRecorder) {
              this.cameraStream = await navigator.mediaDevices.getUserMedia({ video: true });
              this.cameraRecorder = new MediaRecorder(this.cameraStream);
              this.cameraRecorder.ondataavailable = e => {
                if (e.data.size > 0) {
                  this.cameraChunks.push(e.data);
                }
              };
            }
            this.cameraRecorder.onstop = () => {
              if (this.cameraChunks.length > 0) {
                const blob = new Blob(this.cameraChunks, { type: 'video/webm' });
                this.recordedCameraUrl = URL.createObjectURL(blob);
              } else {
                console.warn("⚠️ There is no data recorded by the camera");
              }
            };
            this.cameraRecorder.start();
          }


          // 🟢 Microphone capture
          if (this.micEnabled) {
            if (!isRestart || !this.micRecorder) {
              this.audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
              this.micRecorder = new MediaRecorder(this.audioStream);
              this.micRecorder.ondataavailable = e => {
                if (e.data.size > 0) {
                  this.micChunks.push(e.data);
                }
              };
            }
            this.micRecorder.onstop = () => {
              if (this.micChunks.length > 0) {
                const blob = new Blob(this.micChunks, { type: 'audio/webm' });
                this.recordedMicUrl = URL.createObjectURL(blob);
              } else {
                console.warn("⚠️ There is no data recorded by the microphone");
              }
            };
            this.micRecorder.start();
          }


          this.isRecording = true;

          const statusEl = this.recordingPopup?.document?.getElementById('recordingStatus');
          if (statusEl) statusEl.style.display = 'block';

        } catch (e) {
          alert("Failed to start recording：" + e.message);
        }
      },


      stopRecording() {

        this.setRecording(false);

        if (this.isRecording) {
          const screenPromise = new Promise((resolve) => {
            if (this.screenRecorder) {
              this.screenRecorder.onstop = () => {
                if (this.screenChunks.length > 0) {
                  const blob = new Blob(this.screenChunks, { type: 'video/webm' });
                  this.recordedScreenUrl = URL.createObjectURL(blob);
                } else {
                  console.warn("⚠️ There is no data recorded by the screen");
                }
                resolve();
              };
              this.screenRecorder.stop();
            } else {
              resolve();
            }
          });

          const cameraPromise = new Promise((resolve) => {
            if (this.cameraRecorder) {
              this.cameraRecorder.onstop = () => {
                if (this.cameraChunks.length > 0) {
                  const blob = new Blob(this.cameraChunks, { type: 'video/webm' });
                  this.recordedCameraUrl = URL.createObjectURL(blob);
                } else {
                  console.warn("⚠️ There is no data recorded by the camera");
                }
                resolve();
              };
              this.cameraRecorder.stop();
            } else {
              resolve();
            }
          });

          const micPromise = new Promise((resolve) => {
            if (this.micRecorder) {
              this.micRecorder.onstop = () => {
                if (this.micChunks.length > 0) {
                  const blob = new Blob(this.micChunks, { type: 'audio/webm' });
                  this.recordedMicUrl = URL.createObjectURL(blob);
                } else {
                  console.warn("⚠️ There is no data recorded by the microphone");
                }
                resolve();
              };
              this.micRecorder.stop();
            } else {
              resolve();
            }
          });

          // ⬆️ Stop all then execute "uploadVideo"
          Promise.all([screenPromise, cameraPromise, micPromise])
            .then(() => {
              console.log("🛑 All MediaRecorders have been stopped");
              this.uploadVideo();
            });
          this.isRecording = false;
        }

        if (this.timerInterval) {
          clearInterval(this.timerInterval);
          this.timerInterval = null;
        }

        const statusEl = this.recordingPopup?.document?.getElementById('recordingStatus');
        if (statusEl) statusEl.style.display = 'none';

      },  
      resetState() {
        this.setRecording(false);
        this.cameraRecorder = null;
        this.screenRecorder = null;
        this.micRecorder = null;
        this.cameraStream = null;
        this.audioStream = null;
        this.internalScreenStream = null;
        this.cameraChunks = [];
        this.screenChunks = [];
        this.micChunks = [];

        if (this.recordedCameraUrl) {
          URL.revokeObjectURL(this.recordedCameraUrl);
          this.recordedCameraUrl = null;
        }
        if (this.recordedScreenUrl) {
          URL.revokeObjectURL(this.recordedScreenUrl);
          this.recordedScreenUrl = null;
        }
        if (this.recordedMicUrl) {
          URL.revokeObjectURL(this.recordedMicUrl);
          this.recordedMicUrl = null;
        }
        this.isRecording = false;
      }
    },
    deactivated() {
      this.stopRecording();
      this.resetState();
    }
  };
</script>
  
<style>
  .page {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 50vh;
    background-color: var(--bg-color);
    color: var(--text-color);
    }

  .container {
    margin-top: 100px; 
    text-align: center;
    padding: 20px;
    background-color: var(--wrap-color);
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 400px;
  }

  h2 {
    font-size: 28px;
    margin-bottom: 20px;
  }

  button {
    background-color: #2196f3;
    border: none;
    color: white;
    padding: 12px 24px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #006666;
  }

  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  p {
    font-size: 20px;
    margin-bottom: 20px;
  }

  .page p.success {
    color: #4CAF50;
    font-size: 24px;
    font-weight: bold;
  }

  .page p.follow-instructions {
    color: #ff9800;
    font-size: 18px;
  }
</style>
  