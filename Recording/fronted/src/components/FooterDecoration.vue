<template>
  <footer class="footer-container">
    <div class="footer-subscribe">
      <h3>Subscribe for Research Updates</h3>
      <form @submit.prevent="handleSubscribe" class="subscribe-form">
        <input
          v-model="email"
          type="email"
          placeholder="Email Address"
          required
        />
        <button type="submit">Subscribe</button>
      </form>
    </div>

    <div class="footer-main">
      <div class="footer-brand">
        <img
          src="@/assets/footer-logo.png"
          alt="Site Footer Logo"
          class="footer-logo"
        />
        <p>Diverse Insights as a Service</p>
      </div>

      <div class="footer-info-group">
        <div class="footer-contact">
          <h4>Say hello!</h4>
          <p>hello@seemeplease.com</p>
          <p>+61 42 4490 9933</p>
        </div>
        <div class="footer-location">
          <h4>Our Location</h4>
          <p>Level 2, York St, Sydney NSW 2000</p>
          <p>27 Old Gloucester St, Holborn, London, WC1N 3AX</p>
        </div>
        <div class="footer-other">
          <h4>Other</h4>
          <p><a href="#">Team</a></p>
          <p><a href="#">Terms of Service</a></p>
          <p><a href="#">Privacy Policy</a></p>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>Digital Discovery Pty Ltd (Trading as See Me Please) | ABN: 22 668 639 156</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: "TheFooter",
  data() {
    return {
      email: "",
    };
  },
  methods: {
    handleSubscribe() {
      alert(`You have subscribed with email: ${this.email}`);
      this.email = "";
    },
  },
};
</script>

<style scoped>
  .footer-container {
    background-color: rgba(234, 241, 241, 0.8);
    color: #333;
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .footer-subscribe {
    align-self: flex-end;
    text-align: left;
    display: flex;
    flex-direction: column;
  }

  .footer-subscribe h3 {
    margin-bottom: 0.5rem;
    color: #006666;
  }

  .subscribe-form {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
    width: 30%;
  }

  .subscribe-form input[type="email"] {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 35px;
    min-width: 200px;
    height: 40px;
  }

  .subscribe-form button {
    padding: 0.5rem 1rem;
    background-color: #ffffff;
    color: #006666;
    border: 2px solid #006666;
    border-radius: 35px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: bold;
    min-width: 120px;
    height: 55px;
  }

  .footer-main {
    display: flex;
    gap: 25rem; 
    align-items: flex-start;
  }

  .footer-brand {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .footer-logo {
    height: 100px; 
    margin-bottom: 0.5rem;
  }

  .footer-info-group {
    display: flex;
    gap: 3rem;
    flex: 1;
  }

  .footer-contact,
  .footer-location,
  .footer-other {
    flex: 1 1 200px;
  }

  .footer-contact h4,
  .footer-location h4,
  .footer-other h4 {
    color: #006666;
  }

  .footer-other p a {
    color: #000000;
    text-decoration: underline;
    font-weight: 500;
  }

  .footer-bottom {
    display: flex;
    justify-content: flex-start; 
    text-align: left;           
  }
</style>
