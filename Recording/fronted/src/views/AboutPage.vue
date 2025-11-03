<template>
  <HeaderDecoration :is-dark="isDark" @toggle-mode="toggleMode" />

  <div class="step-uploader">
    <h2>🖊 ProjectTask Form Creation</h2>

    <!-- Project Name -->
    <div class="input-section">
      <label>Project Name:</label>
      <input type="text" v-model="projectName" placeholder="Please Enter The Project Name" />
    </div>

    <!-- Task Number -->
    <div class="input-section">
      <label>Task Number:</label>
      <input type="number" v-model.number="taskNumber" min="1" placeholder="Please Enter The Task Number"/>
      <button @click="generateForm">New Form</button>
    </div>

    <!-- Form for Each Task -->
    <div v-if="tasks.length > 0" class="steps-container">
      <div v-for="(task, index) in tasks" :key="index" class="step-block">
        <h3>Task {{ index + 1 }}</h3>

        <div class="input-section">
          <label>Task Title:</label>
          <input
            type="text"
            v-model="task.taskTitle"
            placeholder="Please Enter The Task Title"
          />
        </div>

        <div class="input-section">
          <label>Task Instructions:</label>
          <textarea
            v-model="task.taskInstructions"
            placeholder="Please Enter The Task Instructions"
            rows="2"
          ></textarea>
        </div>

        <div class="input-section">
          <label>Task Upload:</label>
          <input
            type="text"
            v-model="task.taskUpload"
            placeholder="Please Enter The Task Upload"
          />
        </div>

        <div class="input-section">
          <label>Time guide:</label>
          <input
            type="number"
            v-model="task.timeguide"
            placeholder="Please Enter The Time Guide (min)"
          />
        </div>

        <div class="input-section">
          <label>URL for Instructions:</label>
          <input
            type="text"
            v-model="task.urlForInstructions"
            placeholder="Enter Detailed Instructions URL"
          />
        </div>

        <div class="input-section">
          <label>Icon for This Step:</label>
          <input
            type="text"
            v-model="task.iconForThisStep"
            placeholder="Enter Icon URL or Asset ID"
          />
        </div>

        <div class="input-section">
          <label>Component Type:</label>
          <input
            type="text"
            v-model="task.componenttype"
            placeholder="Enter Component Type Symbol"
          />
        </div>

        <div class="input-section">
          <label>Task Tip:</label>
          <textarea
            v-model="task.taskTip"
            placeholder="Enter a Short Tip or Help Text"
            rows="2"
          ></textarea>
        </div>

        <!-- Button to remove current task form -->
        <button @click="removeTask(index)">Remove Task</button>

      </div>
    </div>

    <!-- Button to add a task, button to upload form -->
    <div class="action-bar" v-if="tasks.length > 0">
        <button
          @click="increaseTaskNum"
        >
          Add Task
        </button>
        <button
          @click="uploadForm"
        >
          Upload ProjectTask
        </button>
    </div>

    <!-- List of uploaded files -->
    <div>
    <h2 style="margin-top: 40px;">📂 Uploaded ProjectTask List</h2>
    <ul>
      <li
        v-for="(file, index) in uploadedFiles"
        :key="index"
        style="margin-bottom: 8px;"
      >
        <span>Project Name: {{ file.name }}  🔗Link:</span>
        <span class="link-text" style="margin-left: 12px;">
          <a
            :href="getFileLink(file)"
            target="_blank"
          >
            {{ getFileLink(file) }}
          </a>
        </span>
        <button
          @click="copyLink(getFileLink(file))"
          style="margin-left: 8px; padding: 2px 8px; cursor: pointer;"
        >
          Copy
        </button>
      </li>
    </ul>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
import HeaderDecoration from '@/components/HeaderDecoration.vue';
export default {
  data() {
    return {
      projectName: '',
      taskNumber: null,
      stepCount: 0,

      tasks: [],

      uploadedFiles: [],
      generatedLinks: {},

    };
  },
  mounted() {
    this.fetchUploadedFiles();
  },
  components: { HeaderDecoration },
  methods: {
    // Generate the link for tester
    getFileLink(file) {
      return `${process.env.VUE_APP_HOME_URL}/home?file=${file.filename}`;
    },
    generateForm() {
      if (!this.projectName.trim()) {
        return alert('Please enter the project name!');
      }
      if (this.taskNumber > 0) {
        this.tasks = Array.from(
          { length: this.taskNumber },
          () => ({
            taskTitle: '',
            taskInstructions: '',
            taskUpload: '',
            timeguide: '',
            urlForInstructions: '',
            iconForThisStep: '',
            componenttype: '',
            taskTip: ''
          })
        );
      }else{
        return alert('Task Number should be at least 1!');
      }
    },
    increaseTaskNum() {
      if (!this.taskNumber) this.taskNumber = 1;
      this.taskNumber++;
      this.tasks.push({
        taskTitle: '',
        taskInstructions: '',
        taskUpload: '',
        timeguide: '',
        urlForInstructions: '',
        iconForThisStep: '',
        componenttype: '',
        taskTip: ''
      });
    },
    removeTask(idx) {
      this.tasks.splice(idx, 1);
      this.taskNumber = this.tasks.length;
    },
    async uploadForm() {
      for (const [i, task] of this.tasks.entries()) {
        if (
          !task.taskTitle.trim() ||
          !task.taskInstructions.trim() ||
          !task.taskUpload.trim() ||
          !task.timeguide==null ||
          !task.urlForInstructions.trim() ||
          !task.iconForThisStep.trim() ||
          !task.componenttype.trim() ||
          !task.taskTip.trim()
        ) {
          alert(`Some Fields of Task ${i + 1} are empty`);
          return;
        }
      }

      const payload = {
          projectName: this.projectName,
          taskNumber: this.taskNumber,
          tasks: this.tasks.map((task, idx) => ({
          taskIndex: idx + 1,
          taskTitle: task.taskTitle,
          taskInstructions: task.taskInstructions,
          taskUpload: task.taskUpload,
          timeguide: task.timeguide,
          urlForInstructions: task.urlForInstructions,
          iconForThisStep: task.iconForThisStep,
          componenttype: task.componenttype,
          taskTip: task.taskTip
        }))
      };

      const blob = new Blob([
        JSON.stringify(payload, null, 2)
      ], { type: 'application/json' });
      //const fileName = `projectTask-${Date.now()}.json`;
      const now = new Date();
      const yyyy = now.getFullYear();
      const MM   = String(now.getMonth() + 1).padStart(2, '0');
      const dd   = String(now.getDate()).padStart(2, '0');
      const hh   = String(now.getHours()).padStart(2, '0');
      const mm   = String(now.getMinutes()).padStart(2, '0');
      const timestamp = `${yyyy}${MM}${dd}${hh}${mm}`;
      const safeName = this.projectName
        .trim()
        .replace(/\s+/g, '_')
        .replace(/[^\w]/g, '');
      const fileName = `projectTask-${safeName}-${timestamp}.json`;
      const formData = new FormData();
      formData.append('file', blob, fileName);

      try {
        await axios.post(`/api/projectTask/upload`, formData,{ 
          headers: { 'Content-Type': 'multipart/form-data' } }
        );
        alert('Submit Successfully!');
         // reset form and refreash link list
         this.projectName = '';
         this.taskNumber = null;
         this.tasks = [];
         this.fetchUploadedFiles();
       } catch (err) {
         const msg = err.response?.data?.message || err.message;
         alert('Submit failed:' + msg);
       }

    },
    async fetchUploadedFiles() {
      try {
        const res = await axios.get(`/api/projectTask/get_projectTask_list`);
        this.uploadedFiles = res.data;
      } catch (err) {
        console.error('Failed to get Projecttask List：', err);
      }
    },
    copyLink(url) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url)
          .then(() => {
            alert('Link copied to clipboard');
          })
          .catch(err => {
            console.error('Failed to copy: ', err);
          });
      } else {
        const textarea = document.createElement('textarea');
        textarea.value = url;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'absolute';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand('copy');
          alert('Link Copied to Clipboard!');
        } catch (err) {
          console.error('Copy failed:', err);
        }
        document.body.removeChild(textarea);
      }
    }
  }
};
</script>

<style scoped>
.step-uploader {
  max-width: 800px;
  margin: 40px auto;
  padding: 24px;
  background-color: #76adad;
  border-radius: 16px;
  box-shadow: 0 6px 12px rgba(0,0,0,0.05);
  font-family: 'Segoe UI', sans-serif;
}

h2, h3 {
  color: #333;
}

.steps-container {
  margin-bottom: 20px;
}

.step-block {
  background: #fff;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 16px;
  border: 1px solid #ddd;
}

.input-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.input-section label {
  min-width: 140px;
  font-weight: bold;
}

.input-section input,
.input-section textarea {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.action-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

button {
  padding: 8px 16px;
  background-color: #006666;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #005555;
}

.link-text a {
  color: #007bff;
}
</style>
