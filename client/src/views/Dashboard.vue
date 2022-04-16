<template>
  <section class="dashboard container mx-auto">
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
    <!-- <h3 class="mt-5 text-xl">This is Dashboard</h3>
    <el-button type="primary" class="mt-3" @click="authenticate"
      >Authenticate</el-button
    >
    <el-button type="danger" class="mt-3" @click="unauthenticate"
      >Unauthenticate</el-button
    >
    <h3 class="text-xl my-3">Access: {{ access_token }}</h3>
    <h3 class="text-xl my-3">Id: {{ id }}</h3>
    <h3 class="text-xl my-3">Name: {{ name }}</h3>
    <h3 class="text-xl my-3">Username: {{ username }}</h3>
    <h3 class="text-xl my-3">Email: {{ email }}</h3>
    <h3 class="text-xl my-3">Expires: {{ exp }}</h3>
    <div>Is Logged In: {{ isLoggedIn }}</div> -->
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import useAuth from "../composables/use-auth";
import Carousel from "../components/Carousel.vue";
import { MigrationTypes } from "../enum/migration.enum";

export default defineComponent({
  name: "Dashboard",
  components: { Carousel },
  setup(props, ctx) {
    const auth = useAuth();
    const youtubePlaylists = [
      {
        id: "12545",
        title: "Happy",
        src: "https://upload.wikimedia.org/wikipedia/en/2/23/Pharrell_Williams_-_Happy.jpg",
      },
      {
        id: "12541245",
        title: "Love The Way You Lie",
        src: "https://upload.wikimedia.org/wikipedia/en/e/ed/Love_the_Way_You_Lie_cover.png",
      },
      {
        id: "125412365121245",
        title: "Glamorous",
        src: "https://upload.wikimedia.org/wikipedia/en/e/eb/Fergie_-_Glamorous.png",
      },
      {
        id: "125412413255",
        title: "Kaonashi",
        src: "https://i1.sndcdn.com/artworks-ADn4ION52x6C-0-t240x240.jpg",
      },
      {
        id: "1925absf",
        title: "Wonderwall",
        src: "https://upload.wikimedia.org/wikipedia/en/1/17/Wonderwall_cover.jpg",
      },
    ];
    const spotifyPlaylists = [
      {
        id: "12545",
        title: "Happy",
        src: "https://upload.wikimedia.org/wikipedia/en/2/23/Pharrell_Williams_-_Happy.jpg",
      },
      {
        id: "12541245",
        title: "Love The Way You Lie",
        src: "https://upload.wikimedia.org/wikipedia/en/e/ed/Love_the_Way_You_Lie_cover.png",
      },
      {
        id: "125412365121245",
        title: "Glamorous",
        src: "https://upload.wikimedia.org/wikipedia/en/e/eb/Fergie_-_Glamorous.png",
      },
      {
        id: "125412413255",
        title: "Kaonashi",
        src: "https://i1.sndcdn.com/artworks-ADn4ION52x6C-0-t240x240.jpg",
      },
      {
        id: "1925absf",
        title: "Wonderwall",
        src: "https://upload.wikimedia.org/wikipedia/en/1/17/Wonderwall_cover.jpg",
      },
    ];
    return {
      ...auth,
      youtubePlaylists,
      spotifyPlaylists,
      MigrationTypes,
    };
  },
});
</script>
