<template>
  <section class="migration-lists w-full flex">
    <el-transfer
      class="mx-auto"
      v-model="values"
      :titles="migration.map(capitalizeWord)"
      :props="{ key: 'value', label: 'title' }"
      :button-texts="['Remove', 'Migrate']"
      :data="data"
    ></el-transfer>
  </section>
</template>

<script setup lang="ts">
// ! button text, add search feature, and add submit button
import { ref } from "vue";
import { MigrationTypes } from "../enum/migration.enum";
import { PlaylistItem } from "../interfaces/playlist-item.interface";
import { capitalizeWord } from "../helpers/capitalize-word";

interface Props {
  playlist_items: PlaylistItem[];
  migration: [MigrationTypes, MigrationTypes];
}

interface Option {
  value: string;
  title: string;
  disabled: boolean;
}

const generateMigrationData = (playlistItems: Props["playlist_items"]) => {
  return playlistItems.map((item) => {
    return {
      value: item.id,
      title: item.title,
      disabled: false,
    };
  });
};

const { playlist_items, migration } = defineProps<Props>();
const data = ref<Option[]>(generateMigrationData(playlist_items));
const values = ref([]);
</script>

<style lang="scss">
.transfer-footer {
  margin-left: 20px;
  padding: 6px 5px;
}
.el-transfer__button {
  margin: 0 1rem !important;
}

.el-transfer-panel {
  width: 400px !important;
}

.el-transfer-panel__body {
  height: 500px !important;
}

.el-transfer-panel__list.is-filterable {
  height: 468px !important;
}
</style>
