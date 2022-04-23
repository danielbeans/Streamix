<template>
  <section class="dashboard container mx-auto pb-10">
    <section class="mt-8 yt-carousel">
      <h3 class="text-2xl text-center">Youtube Playlists</h3>
      <el-divider />
      <Carousel
        :data="youtubePlaylists"
        :migration="[MigrationTypes.YOUTUBE, MigrationTypes.SPOTIFY]"
      />
    </section>
    <section class="mt-8 yt-carousel">
      <h3 class="text-2xl text-center">Spotify Playlists</h3>
      <el-divider />
      <Carousel
        :data="spotifyPlaylists"
        :migration="[MigrationTypes.SPOTIFY, MigrationTypes.YOUTUBE]"
      />
    </section>
  </section>
</template>

<script lang="ts">
import { defineComponent, onUnmounted, ref } from "vue";
import useAuth from "../composables/use-auth";
import useAxios from "../composables/use-axios";
import Carousel from "../components/Carousel.vue";
import { MigrationTypes } from "../enum/migration.enum";
import { useRoute } from "vue-router";
import { FetchStatus } from "../enum/status.enum";

export default defineComponent({
  name: "Dashboard",
  components: { Carousel },
  setup(props, ctx) {
    const { spotify_authenticated } = useRoute().query ?? false;
    const { youtube_authenticated } = useRoute().query ?? false;
    const noAuth = !spotify_authenticated && !youtube_authenticated;
    let auth = useAuth();
    // if (spotify_authenticated || youtube_authenticated) auth.authenticate();
    let youtubeRequest: any = useAxios(
      {
        method: "get",
        headers: { Authorization: `Bearer ${auth.access_token.value}` },
        url: `/api/youtube/playlists`,
      },
      true
    );
    let spotifyRequest: any = useAxios(
      {
        method: "get",
        headers: {
          Authorization: `Bearer ${auth.access_token.value}`,
        },
        url: `/api/spotify/playlists`,
      },
      true
    );

    return {
      ...auth,
      spotifyRequest,
      youtubePlaylists: {
        items: youtubeRequest?.data,
        status: youtubeRequest?.status,
      } ?? { items: [], status: null },
      spotifyPlaylists: {
        status: spotifyRequest?.status,
        items: spotifyRequest?.data,
      } ?? { items: [], status: null },
      MigrationTypes,
      FetchStatus,
    };
  },
});
</script>
