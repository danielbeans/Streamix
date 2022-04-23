<template>
  <el-container v-loading="!data?.items" class="mt-16 justify-center">
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
import { MigrationTypes } from "../enum/migration.enum";

export default defineComponent({
  name: "Migrate",
  components: { MigrationList },
  setup() {
    const { id } = useRoute().params;
    const { access_token } = useAuth();
    const { migration }: any = useRoute().query;
    const config = {
      method: migration[0] === MigrationTypes.SPOTIFY ? "get" : "post",
      headers: { Authorization: `Bearer ${access_token.value}` },
      url:
        migration[0] === MigrationTypes.SPOTIFY
          ? `/api/${migration[0].toLowerCase()}/tracks/${id}`
          : `/api/${migration[0].toLowerCase()}/tracks/`,
    };
    const { data, status } = useAxios<any>(
      migration[0] === MigrationTypes.SPOTIFY
        ? config
        : ({ ...config, data: { playlist_id: id } } as any),
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
