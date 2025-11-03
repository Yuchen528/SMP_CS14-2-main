<template>
  <HeaderDecoration :is-dark="isDark" @toggle-mode="toggleMode" />

  <div class="project-gallery">
    <h2>Project Gallery</h2>

        <!-- 全局加载动画 -->
    <div v-if="globalLoading" class="global-loader">
      <div class="spinner"></div>
      <p>Loading ...</p>
    </div>

    <div class="project-list">
      <div
        v-for="(project, index) in projects"
        :key="index"
        class="project-item"
      >
        <div @click="toggleProject(project)" class="project-header">
          {{ project }}
          <span v-if="loadingProject === project" class="spinner-small"></span>
        </div>

        <transition name="slide-fade">
          <div v-if="expandedProject === project" class="image-grid">
            <div
              v-for="(image, imgIndex) in images[project]"
              :key="imgIndex"
              class="image-item-container"
            >
              <img
                :src="image.url"
                class="image-item"
                @click="openPreview(project, imgIndex)"
              />
              <p class="image-name">{{ image.name }}</p>
            </div>
          </div>
        </transition>

        <p v-if="errorMessage && expandedProject === project" class="error-message">
          {{ errorMessage }}
        </p>
      </div>
    </div>

    <!-- 全屏预览 -->
    <div v-if="isPreview" class="fullscreen-overlay" @click.self="closePreview">
      <img :src="currentImage.url" class="fullscreen-image" />
      <p class="fullscreen-name">{{ currentImage.name }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import HeaderDecoration from '@/components/HeaderDecoration.vue';

export default {
  emits: ['toggleMode'],
  components: { HeaderDecoration },
  data() {
    return {
      projects: [],
      images: {},
      expandedProject: null,
      isPreview: false,
      currentImage: null,
      currentIndex: 0,
      currentProject: null,
      loadingProject: null,// 当前加载中的项目
      globalLoading: true,    // 是否在全局加载中
      errorMessage: "",       // 错误信息
      isDark: false           // 主题模式
    };
  },
  mounted() {
    axios.get(`/api/visualization/get_project_list`)
      .then(response => {
        this.projects = response.data;
      })
      .catch(error => {
        console.error('Failed to fetch projects:', error);
        this.errorMessage = 'Failed to fetch projects';
      })

      .finally(() => {
        this.globalLoading = false;  // 加载结束
      });
    
  },
  methods: {
    toggleProject(project) {
      if (this.expandedProject === project) {
        this.expandedProject = null;
        this.errorMessage = "";
        return;
      }

      if (!this.images[project]) {
        this.loadingProject = project; // 开始加载
        axios.get(`/api/visualization/get_heatmap_list/${project}`)
          .then(response => {
            // 假设返回数据是这样的格式：[{ url: 'https://...', name: 'p1.jpg' }, ...]
            this.images[project] = response.data;
            this.expandedProject = project;
            this.errorMessage = "";
          })
          .catch(error => {
            console.error(`Failed to fetch images for ${project}:`, error);
            this.errorMessage = 'Failed to fetch images for this project.';
          })
          .finally(() => {
            this.loadingProject = null;
          });
      } else {
        this.expandedProject = project;
      }
    },
    openPreview(project, index) {
      this.currentProject = project;
      this.currentIndex = index;
      this.currentImage = this.images[project][index];
      this.isPreview = true;
    },
    closePreview() {
      this.isPreview = false;
    }
  }
};
</script>

<style scoped>
.project-gallery {
  margin: 20px;
}

.project-list {
  width: 80%; /* 设置固定宽度，可以根据需要调整 */
  margin: 0 auto; /* 居中对齐 */
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.project-item {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.project-header {
  padding: 10px;
  padding-left: 20px;
  padding-right: 50px;
  font-weight: bold;
  cursor: pointer;
  background-color: #006666;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-header:hover {
  background-color: #008080; /* 你可以换成你喜欢的颜色 */
  transform: scale(1.02);
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
  padding: 10px;
  background-color: #eef4f4;
}

.image-item-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-item {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s;
}

.image-item:hover {
  transform: scale(1.05);
}

.image-name {
  margin-top: 5px;
  font-size: 12px;
  color: #666;
}

/* 全屏预览 */
.fullscreen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.fullscreen-image {
  max-width: 90vw;
  max-height: 80vh;
  border-radius: 8px;
}

.fullscreen-name {
  margin-top: 10px;
  color: white;
  font-size: 18px;
}

/* 全局加载动画 */
.global-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  font-size: 18px;
  color: #006666;
}

.spinner {
  margin-bottom: 10px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top-color: #006666;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 0.8s linear infinite;
}

.spinner-small {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 0.6s linear infinite;
  margin-left: 10px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
