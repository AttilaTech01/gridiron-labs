<template>
  <v-sheet color="surface" elevation="3" class="pa-4 rounded-lg">
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h2 class="text-h6">Bench & Roster</h2>
        <p class="text-body-2 text-white text-opacity-70">Players waiting for a starting opportunity.</p>
      </div>
    </div>

    <v-list two-line>
      <v-list-item
        v-for="player in benchPlayers"
        :key="player.id"
        class="rounded-lg"
        elevation="1"
      >
        <v-list-item-content>
          <v-list-item-title class="text-white">{{ player.full_name }}</v-list-item-title>
          <v-list-item-subtitle class="text-white text-opacity-70">
            {{ player.position }} · {{ player.team ?? 'N/A' }}
          </v-list-item-subtitle>
        </v-list-item-content>

        <v-btn size="small" variant="text" color="primary" @click="$emit('show-detail', player)">
          View
        </v-btn>
        <v-btn size="small" variant="tonal" color="primary" @click="$emit('promote-player', player)">
          Start
        </v-btn>
      </v-list-item>
    </v-list>

    <v-alert v-if="benchPlayers.length === 0" type="info" color="info" text-color="white" border="start">
      Bench is empty. Add more players to fill the roster.
    </v-alert>
  </v-sheet>
</template>

<script setup lang="ts">
import type { Player } from '@/types/player'

const props = defineProps<{ benchPlayers: Player[] }>()
const emit = defineEmits<{
  (e: 'show-detail', player: Player): void
  (e: 'promote-player', player: Player): void
}>()
</script>
