<template>
  <section class="dashboard container mx-auto pb-10">
    <section class="mt-8 yt-carousel">
      <h3 class="text-2xl text-center">Youtube Playlists</h3>
      <el-divider />
      <Carousel
        :items="youtubePlaylists"
        :migration="[MigrationTypes.YOUTUBE, MigrationTypes.SPOTIFY]"
      />
    </section>
    <section class="mt-8 yt-carousel">
      <h3 class="text-2xl text-center">Spotify Playlists</h3>
      <el-divider />
      <Carousel
        :items="spotifyPlaylists"
        :migration="[MigrationTypes.SPOTIFY, MigrationTypes.YOUTUBE]"
      />
    </section>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import useAuth from "../composables/use-auth";
import useAxios from "../composables/use-axios";
import Carousel from "../components/Carousel.vue";
import { MigrationTypes } from "../enum/migration.enum";
import { useRoute } from "vue-router";

export default defineComponent({
  name: "Dashboard",
  components: { Carousel },
  setup(props, ctx) {
    const { spotify_authenticated } = useRoute().query ?? false;
    const { youtube_authenticated } = useRoute().query ?? false;
    const noAuth = !spotify_authenticated && !youtube_authenticated;
    const auth = useAuth(spotify_authenticated || youtube_authenticated);
    if (spotify_authenticated || youtube_authenticated) auth.authenticate();
    const youtubeRequest =
      youtube_authenticated ||
      (noAuth &&
        useAxios(
          {
            method: "get",
            headers: { Authorization: `Bearer ${auth.access_token.value}` },
            url: `/api/youtube/playlists`,
          },
          true
        ));
    const spotifyRequest =
      spotify_authenticated ||
      (noAuth &&
        useAxios(
          {
            method: "get",
            headers: {
              Authorization: `Bearer ${auth.access_token.value}`,
            },
            url: `/api/spotify/playlists`,
          },
          true
        ));
    return {
      ...auth,
      youtubePlaylists: youtubeRequest?.data ?? { items: [] },
      spotifyPlaylists: spotifyRequest?.data ?? { items: [] },
      MigrationTypes,
    };
  },
});
</script>
