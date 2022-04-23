<template>
  <section class="carousel" v-if="viewportSize != null">
    <div v-if="type === MigrationTypes.SPOTIFY">
      <div
        v-if="
          !hasSpotifyAuth ||
          data?.status?.value === FetchStatus.ERROR ||
          !data?.items?.value
        "
        class="flex"
      >
        <a
          class="mx-auto"
          :href="`http://localhost:8000/api/auth/${migration[0].toLowerCase()}?access_token=${access_token}`"
        >
          <el-button class="mx-auto">
            Grant {{ capitalizeWord(migration[0]) }} Access to
            Playlists</el-button
          >
        </a>
      </div>
      <el-carousel v-else :autoplay="false" height="650px">
        <el-carousel-item v-for="item in data.items.value.items" :key="item.id">
          <div class="mx-auto w-full">
            <h3 class="text-xl mb-4 text-center">{{ item.name }}</h3>
            <router-link
              :to="{
                path: `/migrate/${item.id}`,
                query: { migration },
              }"
            >
              <el-button class="mx-auto mb-5 flex justify-center"
                >Migrate from {{ capitalizeWord(migration[0]) }} to
                {{ capitalizeWord(migration[1]) }}
              </el-button>
            </router-link>
            <div class="flex justify-center items-center">
              <img :src="item.images[0]?.url" :key="item.src" />
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>
    <div v-else-if="type === MigrationTypes.YOUTUBE">
      <div
        v-if="
          !hasYoutubeAuth ||
          data?.status?.value === FetchStatus.ERROR ||
          !data?.items?.value
        "
        class="flex"
      >
        <a
          class="mx-auto"
          :href="`http://localhost:8000/api/auth/${migration[0].toLowerCase()}?access_token=${access_token}`"
        >
          <el-button>
            Grant {{ capitalizeWord(migration[0]) }} Access to
            Playlists</el-button
          >
        </a>
      </div>
      <el-carousel v-else :autoplay="false" height="480px">
        <el-carousel-item v-for="item in data.items.value.items" :key="item.id">
          <div class="mx-auto w-full">
            <h3 class="text-xl mb-4 text-center">{{ item.snippet.title }}</h3>
            <router-link
              :to="{
                path: `/migrate/${item.id}`,
                query: { migration },
              }"
            >
              <el-button class="mx-auto mb-5 flex justify-center"
                >Migrate from {{ capitalizeWord(migration[0]) }} to
                {{ capitalizeWord(migration[1]) }}
              </el-button>
            </router-link>
            <div class="flex justify-center items-center">
              <img
                :src="item.snippet.thumbnails.high?.url"
                :key="item.snippet.thumbnails.high.url"
              />
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>
  </section>
</template>

<script setup lang="ts">
import useViewport from "../composables/use-viewport";
import { MigrationTypes } from "../enum/migration.enum";
import { onUnmounted, Ref, ref, watchEffect } from "vue";
import useAuth from "../composables/use-auth";
import { capitalizeWord } from "../helpers/capitalize-word";
import { FetchStatus } from "../enum/status.enum";
import { access } from "fs";
interface CarouselItem {
  readonly id: string;
  readonly title: string;
  readonly src: string;
}

interface Props {
  data: { items: any; status: any };
  migration: [MigrationTypes, MigrationTypes];
}

const { hasSpotifyAuth, hasYoutubeAuth, access_token } = useAuth();
const { data, migration } = defineProps<Props>();
const type = migration[0];
const { viewportSize } = useViewport();
</script>
