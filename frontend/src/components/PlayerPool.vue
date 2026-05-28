<template>
  <v-sheet color="surface" elevation="3" class="pa-4 rounded-lg">
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h2 class="text-h6">Player Pool</h2>
        <p class="text-body-2 text-white text-opacity-70">Search and filter the available players.</p>
      </div>
    </div>

    <v-text-field v-model="search" label="Search players" variant="outlined" class="mb-4" hide-details />

    <v-chip-group v-model="positionFilter" column active-class="v-chip--active" class="mb-4">
      <v-chip value="All" color="primary" variant="tonal">All</v-chip>
      <v-chip value="QB" color="primary" variant="tonal">QB</v-chip>
      <v-chip value="RB" color="primary" variant="tonal">RB</v-chip>
      <v-chip value="WR" color="primary" variant="tonal">WR</v-chip>
      <v-chip value="TE" color="primary" variant="tonal">TE</v-chip>
      <v-chip value="K" color="primary" variant="tonal">K</v-chip>
    </v-chip-group>

    <!-- No filter active -->
    <v-alert v-if="!hasFilter" type="info" variant="tonal" class="mb-4"> Select a position or search for a player to get started. </v-alert>

    <!-- Loading -->
    <v-skeleton-loader v-else-if="isLoading" type="list-item-two-line@5" />

    <!-- Error -->
    <v-alert v-else-if="isError" type="error" variant="tonal" class="mb-4"> Something went wrong loading players. Please try again. </v-alert>

    <!-- Search too short -->
    <v-alert v-else-if="search.length > 0 && !isSearchValid && positionFilter === 'All'" type="info" variant="tonal" class="mb-4">
      Keep typing — search requires at least 3 characters.
    </v-alert>

    <!-- No results -->
    <v-alert v-else-if="players.length === 0" type="warning" variant="tonal" class="mb-4"> No players found. Try a different search or position. </v-alert>

    <!-- Player list -->
    <v-list v-else two-line>
      <v-list-item v-for="player in players" :key="player.id" class="rounded-lg" elevation="1">
        <v-list-item-content>
          <v-list-item-title class="text-white">{{ player.full_name }}</v-list-item-title>
          <v-list-item-subtitle class="text-white text-opacity-70"> {{ player.position }} · {{ player.team ?? "N/A" }} </v-list-item-subtitle>
        </v-list-item-content>

        <v-chip class="me-2" :color="gradeColor(player.gridiron_grade)" text-color="white">
          {{ player.gridiron_grade }}
        </v-chip>

        <v-btn size="small" variant="text" color="primary" @click="$emit('show-detail', player)"> Details </v-btn>
      </v-list-item>
    </v-list>
  </v-sheet>
</template>

<script setup lang="ts">
import { usePlayers } from "@/composables/usePlayers";
import { gradeColor } from "@/lib/utilities";
import type { Player } from "@/types/player";

const emit = defineEmits<{
  (e: "show-detail", player: Player): void;
}>();

const { search, positionFilter, players, isLoading, isError, hasFilter, isSearchValid } = usePlayers();
</script>
