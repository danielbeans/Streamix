<template>
  <section class="dashboard">
    <h3 class="mt-5 text-xl">This is Dashboard</h3>
    <el-button type="primary" class="mt-3" @click="authenticate"
      >Authenticate</el-button
    >
    <el-button type="danger" class="mt-3" @click="unauthenticate"
      >Unauthenticate</el-button
    >
    <h3 class="text-xl my-3">Access: {{ access_token }}</h3>
    <h3 class="text-xl my-3">Refresh: {{ refresh_token }}</h3>
    <h3 class="text-xl my-3">Expires: {{ expires_at }}</h3>
    <div>Is Logged In: {{ isLoggedIn }}</div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import useAuth from "../composables/use-auth";

export default defineComponent({
  name: "Dashboard",
  components: {},
  setup(props, ctx) {
    const auth = useAuth();
    return {
      ...auth,
    };
  },
});
</script>
