<template>
  <section class="migration-lists pb-10 w-full">
    <h3 class="text-2xl text-center mb-5">
      Migrate from {{ capitalizeWord(migration[0]) }} to
      {{ capitalizeWord(migration[1]) }}
    </h3>
    <div class="w-1/2 mx-auto mb-8">
      <el-input
        v-model="playlistName"
        class="flex mx-auto w-1/2 mb-2"
        placeholder="Playlist Name: "
      />
      <p
        v-show="beganTyping && playlistName.length < MIN_PLAYLIST_NAME"
        class="text-red-500 text-center text-sm"
      >
        Please enter a valid playlist name.
      </p>
    </div>

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
import { ref, watchEffect, watch, reactive, computed } from "vue";
import { MigrationTypes } from "../enum/migration.enum";
import { PlaylistItem } from "../interfaces/playlist-item.interface";
import { capitalizeWord } from "../helpers/capitalize-word";
import { randomString } from "../helpers/random-string";
import useAxios from "../composables/use-axios";

const MIN_PLAYLIST_NAME = 4;
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
  if (migration[0] === MigrationTypes.SPOTIFY) {
    return playlistItems.map(({ track }) => ({
      value: track.id,
      title: track.name,
      disabled: false,
    }));
  } else {
    console.log(playlistItems);
    return playlistItems.map((item) => ({
      value: item.id,
      title: item.snippet.title,
      disabled: false,
    }));
  }
};

const playlistName = ref(``);
const beganTyping = ref(false);
watch(playlistName, () => (beganTyping.value = playlistName.value.length >= 1));
const { playlist_items, migration } = defineProps<Props>();
const data = ref<Option[]>(generateMigrationData(playlist_items));
const values = ref([]);

const migrate = async () => {
  if (!beganTyping.value || playlistName.value.length < MIN_PLAYLIST_NAME)
    return;

  const selectedTracks = data.value.filter(
    ({ value }) => values.value.indexOf(value) !== -1
  );
  console.log(
    selectedTracks.map(({ title }) => {
      name: title;
    })
  );
  console.log();
  const migrationRequest = useAxios(
    {
      method: "post",
      url: `/api/playlist/create/spotify/`,
      data: {
        playlist_name: playlistName.value || randomString("playlist-"),
        tracks: selectedTracks.map((value) => ({ name: { ...value }.title })),
      },
    },
    true
  );
  await migrationRequest.run();
  console.log(migrationRequest.data);

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
