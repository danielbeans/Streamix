<template>
  <section class="migrate mt-8">
    <MigrationList :migration="migration" :playlist_items="playlist_items" />
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import MigrationList from "../components/MigrationLists.vue";

export default defineComponent({
  name: "Migrate",
  components: { MigrationList },
  setup() {
    const { id } = useRoute().params;
    const { migration } = useRoute().query;
    // ! fetch playlist data here
    const playlist_items = [
      {
        id: "1",
        title: "The Best of The Beatles",
        artist: "The Beatles",
        ableToMigrate: false,
      },
      {
        id: "2",
        title: "The Best of The Rolling Stones",
        artist: "The Rolling Stones",
        ableToMigrate: true,
      },
      {
        id: "3",
        title: "The Best of The Beach Boys",
        artist: " The Beach Boys",
        ableToMigrate: true,
      },
      {
        id: "4",
        title: "The Best of Aerosmith",
        artist: "Aerosmith",
        ableToMigrate: true,
      },
      {
        id: "5",
        title: "The Best of Roy Orbison",
        artist: "Roy Orbison",
        ableToMigrate: false,
      },
    ];
    return {
      playlist_items,
      migration,
    };
  },
});
</script>
