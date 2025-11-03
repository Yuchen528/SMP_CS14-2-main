<template>
    <div class="page">

      <!-- Form for 'About Me' page -->
      <div class="form-wrapper">
        <h1 class="form-title">Tell Us About You</h1>
        <form @submit.prevent="handleNext">
          <div class="form-row">
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input v-model="lastName" id="lastName" required />
            </div>

            <div class="form-group">
              <label for="firstName">First Name</label>
              <input v-model="firstName" id="firstName" required />
            </div>
          </div>

          <div class="form-group">
            <label for="email">Email Address</label>
            <input type="email" v-model="email" id="email" required />
          </div>
        </form>
      </div>

      <slot name="navigation" />

    </div>
</template>
  
<script>
  import { v4 as uuidv4 } from 'uuid';
  export default {
    name: 'PageOne',
    props: {
      isDark: Boolean
    },
    data() {
      return {
        firstName: '',
        lastName: '',
        email: ''
      };
    },
    methods: {
      validateAndNext() {
        const form = this.$el.querySelector("form");
        if (form && !form.checkValidity()) {
          form.reportValidity();
          return false;
        }

        // Generate 'uuid' for current tester
        const id = uuidv4();
        this.$emit('user-info', {
          uuid: id,
          firstName: this.firstName,
          lastName: this.lastName,
          email: this.email
        });

        return true;
      }
    }
  };
</script>
  
<style>
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color);
}
  
.form-wrapper {
  background-color: var(--wrap-color);
  max-width: 700px;
  width: 90%;      
  margin: 30px auto 0;
  padding: 24px;
  border-radius: 12px;         
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-title {
  font-size: 28px;
  margin-bottom: 30px;
  text-align: left;
}

form {
  width: 100%;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 6px;
}

input {
  padding: 8px 12px;
  font-size: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

input:focus {
  outline: none;
  border-color: #42b983;
}

@media (max-width: 600px) {
  .form-row {
    flex-direction: column;
  }
}
</style>
  