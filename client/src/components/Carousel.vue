<template>
  <section class="carousel" v-if="items?.items && viewportSize != null">
    <div v-if="type === MigrationTypes.SPOTIFY">
      <div v-if="!hasSpotifyAuth" class="flex">
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
        <el-carousel-item v-for="item in items.items" :key="item.id">
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
      <div v-if="!hasYoutubeAuth" class="flex">
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
        <el-carousel-item v-for="item in items.items" :key="item.id">
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
    <el-carousel v-else :autoplay="false" height="480px">
      <el-carousel-item v-for="item in items.items" :key="item.id">
        <div class="mx-auto w-full">
          <h3 class="text-xl mb-4 text-center">{{ item.title }}</h3>
          <router-link :to="`/migrate/${item.id}`">
            <el-button class="mx-auto mb-5 flex justify-center"
              >Migrate from {{ capitalizeWord(migration[0]) }} to
              {{ capitalizeWord(migration[1]) }}
            </el-button>
          </router-link>
          <div class="flex justify-center items-center">
            <img
              :src="item.snippet.thumbnails.high.url"
              :key="item.snippet.thumbnails.high.url"
            />
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </section>
</template>

<script setup lang="ts">
import useViewport from "../composables/use-viewport";
import { MigrationTypes } from "../enum/migration.enum";
import { ref } from "vue";
import useAuth from "../composables/use-auth";
import { capitalizeWord } from "../helpers/capitalize-word";

interface CarouselItem {
  readonly id: string;
  readonly title: string;
  readonly src: string;
}

interface Props {
  items: CarouselItem[];
  migration: [MigrationTypes, MigrationTypes];
}

const { hasSpotifyAuth, hasYoutubeAuth, access_token } = useAuth();
const { items, migration } = defineProps<Props>();

const type = migration[0];
const { viewportSize } = useViewport();
</script>
