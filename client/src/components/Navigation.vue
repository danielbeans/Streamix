<template>
  <nav>
    <el-menu
      align="right"
      mode="horizontal"
      :default-active="activeIndex"
      @select="handleSelect"
      :unique-opened="true"
      :router="true"
      menu-trigger="click"
      :collapse-transition="false"
      menu
    >
      <el-menu-item index="dashboard">Dashboard</el-menu-item>
      <el-sub-menu index="2"
        ><template #title>Playlists</template>
        <el-menu-item index="playlists">My Playlists</el-menu-item>
        <el-menu-item index="migrate">Migrate</el-menu-item>
        <el-menu-item index="party">Create/Join Playlist Party</el-menu-item>
      </el-sub-menu>
      <template v-if="!isLoggedIn">
        <el-menu-item class="ml-auto" index="login">Log in</el-menu-item>
        <el-menu-item index="signup">Sign up</el-menu-item>
      </template>
    </el-menu>
  </nav>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import useAuth from "../composables/use-auth";

const activeIndex = ref("login");

const { setAuth, isLoggedIn, auth } = useAuth();
</script>
