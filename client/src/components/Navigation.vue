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
        <el-menu-item class="ml-auto" index="dashboard">Dashboard</el-menu-item>
        <el-sub-menu index="sub-menu"
          ><template #title>Playlists</template>
          <el-menu-item index="playlists">My Playlists</el-menu-item>
          <el-menu-item index="migrate">Migrate</el-menu-item>
          <el-menu-item index="party">Create/Join Playlist Party</el-menu-item>
        </el-sub-menu></template
      >
      <template v-if="!isLoggedIn">
        <el-menu-item class="ml-auto" index="login">Log in</el-menu-item>
        <el-menu-item index="signup">Sign up</el-menu-item>
      </template>
    </el-menu>
  </nav>
</template>

<script lang="ts" setup>
import { computed } from "@vue/reactivity";
import { useRoute } from "vue-router";
import useAuth from "../composables/use-auth";
const route = useRoute();

const activeIndex = computed(() => (route.name as string)?.toLowerCase());

const { setAuth, isLoggedIn, auth } = useAuth({ token: "" });
</script>
