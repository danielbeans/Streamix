<template>
  <el-container v-loading="!data?.items" class="mt-16">
    <MigrationList
      v-if="data?.items"
      :migration="migration"
      :playlist_items="data.items"
    />
  </el-container>
</template>

<script lang="ts">
import { defineComponent, watchEffect } from "vue";
import { FetchStatus } from "../enum/status.enum";
import { useRoute } from "vue-router";
import useAuth from "../composables/use-auth";
import useAxios from "../composables/use-axios";
import MigrationList from "../components/MigrationLists.vue";

export default defineComponent({
  name: "Migrate",
  components: { MigrationList },
  setup() {
    const { id } = useRoute().params;
    const { access_token } = useAuth();
    const { migration } = useRoute().query;
    // ! fetch playlist data here
    const { data, status } = useAxios(
      {
        method: "get",
        headers: { Authorization: `Bearer ${access_token.value}` },
        url: `/api/${migration[0].toLowerCase()}/tracks/${id}`,
      },
      true
    );
    return {
      data,
      migration,
      FetchStatus,
      status,
    };
  },
});
</script>
