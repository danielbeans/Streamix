<template>
  <nav v-if="!!activeIndex">
    <el-menu
      align="right"
      mode="horizontal"
      :default-active="activeIndex"
      :unique-opened="true"
      :router="true"
      menu-trigger="click"
      :collapse-transition="false"
      menu
    >
      <template v-if="isLoggedIn">
        <el-menu-item class="ml-auto" index="/dashboard"
          >Dashboard</el-menu-item
        >
        <!-- logout button here -->
      </template>
      <template v-else>
        <el-menu-item class="ml-auto" index="/login">Log in</el-menu-item>
        <el-menu-item index="/signup">Sign up</el-menu-item>
      </template>
      <!-- ! Add an else condition for a logout button here. Redirect to login page. -->
    </el-menu>
  </nav>
</template>

<script lang="ts" setup>
import { computed } from "@vue/reactivity";
import { useRoute } from "vue-router";
import useAuth from "../composables/use-auth";
const route = useRoute();
const { isLoggedIn, unauthenticate } = useAuth(); // ! Need to add logout functionality to `useAuth` composable.
/*
  1. Make a function to logout the user (using unauthenticate)
  2. Display a modal/popup to confirm logout. (Are you sure you want to logout?)
  3. When they click yes, logout the user and redirect to the login page.
  Note: In order to redirect the user, utilize a <router-linK> component.
*/
// here
const activeIndex = computed(() => (route.name as string)?.toLowerCase());
</script>
