<template>
  <section class="migration-lists pb-10 w-full">
    <div class="flex w-full">
      <el-transfer
        class="mx-auto flex flex-wrap"
        v-model="values"
        :titles="migration.map(capitalizeWord)"
        :props="{ key: 'value', label: 'title' }"
        :button-texts="['Remove', 'Migrate']"
        :data="data"
      ></el-transfer>
    </div>
    <el-button
      @click="migrate"
      type="primary"
      size="large"
      class="flex mx-auto mt-8"
      >Migrate</el-button
    >
  </section>
</template>

<script setup lang="ts">
// ! button text, add search feature, and add submit button
import { ref, watch } from "vue";
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
  return playlistItems.map(({ track }) => {
    return {
      track: { ...track },
      value: track.id,
      title: track.name,
      disabled: false,
    };
  });
};
const { playlist_items, migration } = defineProps<Props>();
console.log(migration);
const data = ref<Option[]>(generateMigrationData(playlist_items));
watch(
  () => playlist_items,
  () => {
    console.log(playlist_items);
    data.value = generateMigrationData(playlist_items);
  }
);
const values = ref([]);
const migrate = () => {
  const selectedTracks = data.value.filter(
    ({ value }) => values.value.indexOf(value) !== -1
  );
  console.log(selectedTracks);
  // send request with tracks to migrate
};
</script>

<style lang="scss">
.transfer-footer {
  margin-left: 20px;
  padding: 6px 5px;
}

.el-transfer__button {
  margin: 0 1rem !important;
}

.el-transfer__buttons {
  display: flex !important;
  align-items: center !important;
  @media only screen and (max-width: 1200px) {
    width: 100% !important;
    justify-content: center !important;
    margin: 2rem 0 !important;
  }
}

.el-transfer-panel {
  width: 400px !important;

  @media only screen and (max-width: 1200px) {
    margin: 0 auto !important;
    width: 90% !important;
    justify-content: center !important;
  }
}

.el-transfer-panel__body {
  height: 500px !important;
}

.el-transfer-panel__list.is-filterable {
  height: 468px !important;
}

.el-transfer-panel__list {
  height: 100% !important;
}
</style>
