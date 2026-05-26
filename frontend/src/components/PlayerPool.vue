<template>
  <v-sheet color="surface" elevation="3" class="pa-4 rounded-lg">
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h2 class="text-h6">Player Pool</h2>
        <p class="text-body-2 text-white text-opacity-70">Search and filter the available players.</p>
      </div>
    </div>

    <v-text-field v-model="searchTerm" label="Search players" variant="outlined" class="mb-4" hide-details />

    <v-chip-group v-model="position" column active-class="v-chip--active" class="mb-4">
      <v-chip value="All" color="primary" variant="tonal">All</v-chip>
      <v-chip value="QB" color="primary" variant="tonal">QB</v-chip>
      <v-chip value="RB" color="primary" variant="tonal">RB</v-chip>
      <v-chip value="WR" color="primary" variant="tonal">WR</v-chip>
      <v-chip value="TE" color="primary" variant="tonal">TE</v-chip>
    </v-chip-group>

    <v-list two-line>
      <v-list-item v-for="player in filteredPlayers" :key="player.id" class="rounded-lg" elevation="1">
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
import { gradeColor } from "@/lib/utilities";
import type { Player } from "@/types/player";
import { computed } from "vue";

const props = defineProps<{
  players: Player[];
  positionFilter: string;
  search: string;
}>();
const emit = defineEmits<{
  (e: "update:search", value: string): void;
  (e: "update:positionFilter", value: string): void;
  (e: "show-detail", player: Player): void;
}>();

const position = computed({
  get: () => props.positionFilter,
  set: (value: string) => emit("update:positionFilter", value),
});

const searchTerm = computed({
  get: () => props.search,
  set: (value: string) => emit("update:search", value),
});

const filteredPlayers = computed(() => {
  const text = props.search.trim().toLowerCase();
  return props.players.filter((player) => {
    const matchesName = player.full_name.toLowerCase().includes(text);
    const matchesPosition = props.positionFilter === "All" || player.position === props.positionFilter;
    return matchesName && matchesPosition;
  });
});
</script>
