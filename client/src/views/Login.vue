<template>
  <section class="login">
    <LoginForm />
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import LoginForm from "../components/LoginForm.vue";

export default defineComponent({
  name: "Login",
  components: { LoginForm },
});
</script>
