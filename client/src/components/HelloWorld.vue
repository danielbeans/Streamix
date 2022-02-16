<template>
  <div class="hello">
    {{ num }}
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ref
export default defineComponent({
  name: "HelloWorld",
  setup() {
    const num = ref(42);
    return { num };
  },
  props: {
    msg: String,
  },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
