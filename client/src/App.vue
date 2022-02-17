<template>
  <Navigation />
  <section class="container mx-auto">
    <router-view />
  </section>
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
