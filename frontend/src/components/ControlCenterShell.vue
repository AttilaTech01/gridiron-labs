<template>
  <v-app>
    <v-app-bar color="primary" dark elevated>
      <v-toolbar-title>Gridiron Labs</v-toolbar-title>
      <v-spacer />
      <v-btn icon variant="tonal" color="secondary" aria-label="Analytics mode">
        <v-icon>mdi-flask</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid class="pa-4">
        <section class="mb-6">
          <player-pool @show-detail="openDetail" />
        </section>
      </v-container>

      <PlayerDetailsCard v-model="detailOpen" :player="selectedPlayer" @update:modelValue="detailOpen = $event" />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { Player } from "@/types/player";
import PlayerPool from "./PlayerPool.vue";
import PlayerDetailsCard from "./PlayerDetailsDialog.vue";

const selectedPlayer = ref<Player | null>(null);
const detailOpen = ref(false);

function openDetail(player: Player) {
  selectedPlayer.value = player;
  detailOpen.value = true;
}
</script>
