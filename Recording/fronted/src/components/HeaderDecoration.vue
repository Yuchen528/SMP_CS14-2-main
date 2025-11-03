<template>
  <header class="header-container">
    <div class="header-left">
      <div class="header-logo">
        <img
          src="@/assets/logo.png"
          alt="Site Logo"
          class="logo-image"
        />
      </div>
      <nav class="header-nav">
        <ul>
          <li><router-link to="/home">Home</router-link></li>
          <li><router-link to="/about">About</router-link></li>
          <li><router-link to="/output">Contact Us</router-link></li>
        </ul>
      </nav>
    </div>

    <div class="mode-toggle">
      <label class="switch">
        <input
          type="checkbox"
          :checked="isDark"
          @change="$emit('toggle-mode', !isDark)"
        />
        <span class="slider"></span>
      </label>
    </div>

  </header>
</template>

<script>
export default {
  name: "TheHeader",
  props: {
    isDark: Boolean
  }
};
</script>

<style scoped>
  .header-container {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    background-color: #006666;
    color: #ffffff;
  }

  .header-left {
    display: flex;
    align-items: center;
  }

  .logo-image {
    height: 60px; 
    margin-left: 2rem;
    margin-right: 6rem; 
  }

  .header-nav ul {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .header-nav li {
    margin-right: 1.5rem;
  }

  .header-nav a {
    color: #ffffff;
    text-decoration: none;
    font-weight: bold; 
    transition: color 0.3s;
  }

  .header-nav a:hover {
    color: #fffbcc;
  }

  .switch {
    position: relative;
    display: inline-block;
    width: 40px;
    height: 20px;
  }

  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
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

  .mode-toggle {
    margin-right: 10px;
  }
</style>
