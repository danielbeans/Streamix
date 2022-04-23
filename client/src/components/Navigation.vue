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
      <template v-if="!!isLoggedIn">
        <el-menu-item class="ml-auto" index="/dashboard"
          >Dashboard</el-menu-item
        >
        <el-menu-item @click="logout" index="/login">Logout</el-menu-item>
      </template>
      <template v-else>
        <el-menu-item class="ml-auto" index="/login">Log in</el-menu-item>
        <el-menu-item index="/signup">Sign up</el-menu-item>
      </template>
    </el-menu>
  </nav>
</template>

<script lang="ts" setup>
import { computed } from "@vue/reactivity";
import { useRoute, useRouter } from "vue-router";
import useAuth from "../composables/use-auth";
const route = useRoute();
const router = useRouter();
const { isLoggedIn, unauthenticate } = useAuth();

const activeIndex = computed(() => (route.name as string)?.toLowerCase());

const logout = () => {
  unauthenticate();
  console.log("logged out");
};
</script>
