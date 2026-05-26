<template>
  <v-dialog :model-value="modelValue" width="640" @update:model-value="$emit('update:modelValue', $event)">
    <v-card v-if="player">
      <v-card-title class="text-h6">{{ player.full_name }}</v-card-title>
      <v-card-subtitle class="text-body-2 text-white text-opacity-70">
        {{ player.position }} · {{ player.team ?? "N/A" }} • {{ player.matchup_grade }}
      </v-card-subtitle>
      <v-card-text>
        <div class="d-flex flex-column gap-3">
          <div class="d-flex justify-space-between align-center">
            <span>Grade</span>
            <v-chip :color="gradeColor(player.gridiron_grade)" text-color="white">
              {{ player.gridiron_grade }}
            </v-chip>
          </div>
          <div class="d-flex justify-space-between align-center">
            <span>Chaos Score</span>
            <span class="text-body-2 text-white text-opacity-70">{{ player.chaos_score }}</span>
          </div>
          <div>
            <p class="text-body-2 text-white text-opacity-70">
              The deep dive modal is the Power User workspace for matchup insight, trends, and placement guidance.
            </p>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="tonal" color="primary" @click="$emit('update:modelValue', false)">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { gradeColor } from "@/lib/utilities";
import type { Player } from "@/types/player";

const props = defineProps<{
  modelValue: boolean;
  player: Player | null;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();
</script>
