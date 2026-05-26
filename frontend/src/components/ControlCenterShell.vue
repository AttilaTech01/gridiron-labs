<template>
  <v-app>
    <v-app-bar color="primary" dark elevated>
      <v-toolbar-title>Gridiron Labs Control Center</v-toolbar-title>
      <v-spacer />
      <v-btn icon variant="tonal" color="secondary" aria-label="Analytics mode">
        <v-icon>mdi-flask</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid class="pa-4">
        <section class="mb-6">
          <player-pool
            :players="players"
            :position-filter="positionFilter"
            :search="search"
            @update:search="search = $event"
            @update:positionFilter="positionFilter = $event"
            @show-detail="openDetail"
          />
        </section>

        <v-skeleton-loader v-if="isLoading" type="list-item-two-line" class="mt-6" />
      </v-container>

      <PlayerDetailsCard :model-value="detailOpen" :player="selectedPlayer" @update:modelValue="detailOpen = $event" />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { Player } from "@/types/player";
import PlayerPool from "./PlayerPool.vue";
import PlayerDetailsCard from "./PlayerDetailsDialog.vue";
import { usePlayers } from "@/composables/usePlayers";

const search = ref("");
const positionFilter = ref("All");
const selectedPlayer = ref<Player | null>(null);
const detailOpen = ref(false);

const playersQuery = usePlayers(positionFilter, search);

const players = computed<Player[]>(() => playersQuery.data.value ?? []);

const isLoading = computed(() => playersQuery.isLoading);

function openDetail(player: Player) {
  selectedPlayer.value = player;
  detailOpen.value = true;
}
</script>
