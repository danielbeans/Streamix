<template>
  <div id="nav">
    <router-link class="mx-2" to="/login">Login</router-link> |
    <router-link class="mx-2" to="/signup">SIgnup</router-link>
  </div>
  <el-divider />
  <router-view />
</template>

<style lang="scss">
#app {
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: rgba(59, 130, 246, 1);
    }
  }
}
</style>
