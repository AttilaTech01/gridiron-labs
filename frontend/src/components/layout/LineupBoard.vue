<template>
  <v-sheet color="surface" elevation="3" class="pa-4 rounded-lg">
    <div class="d-flex justify-space-between align-center mb-4">
      <div>
        <h2 class="text-h6">Active Lineup</h2>
        <p class="text-body-2 text-white text-opacity-70">Players currently in your starting lineup.</p>
      </div>
    </div>

    <v-row density="comfortable">
      <v-col cols="12" v-for="player in players" :key="player.id">
        <v-card color="surface" elevation="2" class="rounded-lg">
          <v-card-text>
            <div class="d-flex justify-space-between align-center mb-3">
              <div>
                <div class="text-subtitle-1 text-white">{{ player.full_name }}</div>
                <div class="text-body-2 text-white text-opacity-70">
                  {{ player.position }} · {{ player.team ?? 'N/A' }} · {{ player.slot }}
                </div>
              </div>
              <v-chip :color="gradeColor(player.gridiron_grade)" text-color="white">
                {{ player.gridiron_grade }}
              </v-chip>
            </div>
            <div class="d-flex justify-space-between align-center">
              <div class="text-body-2 text-white text-opacity-70">Matchup: {{ player.matchup_grade }}</div>
              <div class="d-flex gap-2">
                <v-btn size="small" variant="text" color="primary" @click="$emit('show-detail', player)">
                  Inspect
                </v-btn>
                <v-btn size="small" variant="outlined" color="error" @click="$emit('remove-player', player)">
                  Bench
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" v-if="players.length === 0">
        <v-alert type="info" border="start" color="info" text-color="white">
          No players in the lineup yet. Add talent from the player pool.
        </v-alert>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script setup lang="ts">
import type { Player } from '@/types/player'

const props = defineProps<{ players: (Player & { slot: string })[] }>()
const emit = defineEmits<{
  (e: 'show-detail', player: Player): void
  (e: 'remove-player', player: Player): void
}>()

function gradeColor(value: number) {
  if (value >= 80) return 'success'
  if (value >= 60) return 'warning'
  return 'error'
}
</script>
