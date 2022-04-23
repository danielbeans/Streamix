<template>
  <section>
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="30%">
      <span>{{ dialogMessage }}</span>
      <el-scrollbar v-if="dialogTitle === `Success`">
        <p
          v-for="track in foundTracks"
          :key="track"
          class="scrollbar-demo-item"
        >
          <span v-html="track"></span>
        </p>
      </el-scrollbar>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false"
            >Confirm</el-button
          >
        </span>
      </template>
    </el-dialog>
    <section class="migration-lists pb-10 w-full mx-auto">
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
        :disabled="values.length >= 20"
        type="primary"
        size="large"
        class="flex mx-auto mt-8"
        >Migrate</el-button
      >
      <p
        v-show="values.length >= 20"
        class="text-red-500 text-center text-sm mt-5"
      >
        Please select less than 20 songs due to quota limitations.
      </p>
    </section>
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
  playlist_items: any;
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

const dialogVisible = ref(false);
const dialogTitle = ref(``);
const foundTracks = ref([]);
const dialogMessage = ref(``);
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
    ({ value }) => (values.value as any).indexOf(value) !== -1
  );
  const migrationRequest = useAxios(
    {
      method: "post",
      url: `/api/playlist/create/${migration[1].toLowerCase()}/`,
      data: {
        playlist_name: playlistName.value || randomString("playlist-"),
        tracks: selectedTracks.map((value) => ({ name: { ...value }.title })),
      },
    },
    true
  );
  await migrationRequest.run();
  console.log(migrationRequest.data);
  if ((migrationRequest.data.value as any).found_tracks.length > 0) {
    dialogTitle.value = "Success";
    dialogMessage.value =
      "Successfully migrated playlist. Here are the tracks that were added to your playlist.";
    foundTracks.value = (migrationRequest.data.value as any).found_tracks;
  } else {
    dialogTitle.value = "Error";
    dialogMessage.value =
      "Playlist was created, however, no tracks were added to it. Please try again.";
  }
  dialogVisible.value = true;
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

.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
</style>
