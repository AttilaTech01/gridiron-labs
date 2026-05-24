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
          <div class="d-flex flex-column gap-2">
            <h1 class="text-h4 text-white">Start / Sit Optimizer</h1>
            <p class="text-body-1 text-white text-opacity-70">A single-page control center for the player pool, active lineup, and roster bench.</p>
          </div>
        </section>

        <v-row density="comfortable" class="fill-height" align="stretch">
          <v-col cols="12" xl="3">
            <player-pool
              :players="availablePlayers"
              :position-filter="positionFilter"
              :search="search"
              @update:search="search = $event"
              @update:positionFilter="positionFilter = $event"
              @show-detail="openDetail"
              @add-player="openDrawer"
            />
          </v-col>

          <v-col cols="12" xl="5">
            <lineup-board :players="activeLineup" @show-detail="openDetail" @remove-player="moveToBench" />
          </v-col>

          <v-col cols="12" xl="4">
            <roster-panel :bench-players="benchPlayers" @show-detail="openDetail" @promote-player="openDrawer" />
          </v-col>
        </v-row>

        <v-skeleton-loader v-if="isLoading" type="list-item-two-line" class="mt-6" />
      </v-container>

      <v-dialog v-model="detailOpen" width="640">
        <v-card v-if="selectedPlayer">
          <v-card-title class="text-h6">{{ selectedPlayer.full_name }}</v-card-title>
          <v-card-subtitle class="text-body-2 text-white text-opacity-70">
            {{ selectedPlayer.position }} · {{ selectedPlayer.team ?? "N/A" }} • {{ selectedPlayer.matchup_grade }}
          </v-card-subtitle>
          <v-card-text>
            <div class="d-flex flex-column gap-3">
              <div class="d-flex justify-space-between align-center">
                <span>Grade</span>
                <v-chip :color="gradeColor(selectedPlayer.gridiron_grade)" text-color="white">
                  {{ selectedPlayer.gridiron_grade }}
                </v-chip>
              </div>
              <div class="d-flex justify-space-between align-center">
                <span>Chaos Score</span>
                <span class="text-body-2 text-white text-opacity-70">{{ selectedPlayer.chaos_score }}</span>
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
            <v-btn variant="tonal" color="primary" @click="detailOpen = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-navigation-drawer v-model="drawerOpen" right temporary width="360">
        <v-sheet class="pa-4" color="surface">
          <div class="d-flex flex-column gap-4">
            <div>
              <h2 class="text-h6">Assign Player</h2>
              <p class="text-body-2 text-white text-opacity-70">Confirm roster placement for the selected player.</p>
            </div>

            <div v-if="selectedPlayer">
              <div class="text-body-1 text-white mb-2">{{ selectedPlayer.full_name }}</div>
              <v-select v-model="selectedSlot" :items="slotOptions" label="Target slot" variant="outlined" />
            </div>

            <div class="d-flex gap-3">
              <v-btn color="primary" variant="tonal" @click="confirmAddToLineup"> Confirm </v-btn>
              <v-btn variant="text" color="white" @click="drawerOpen = false">Cancel</v-btn>
            </div>
          </div>
        </v-sheet>
      </v-navigation-drawer>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { Player } from "@/types/player";
import type { LineupEntry, LineupPayload } from "@/types/lineup";
import type { RosterEntry } from "@/types/roster";
import PlayerPool from "./PlayerPool.vue";
import LineupBoard from "./LineupBoard.vue";
import RosterPanel from "./RosterPanel.vue";
import { usePlayers } from "@/composables/usePlayers";
import { useRoster } from "@/composables/useRoster";
import { useLineup } from "@/composables/useLineup";

const search = ref("");
const positionFilter = ref("All");
const selectedPlayer = ref<Player | null>(null);
const detailOpen = ref(false);
const drawerOpen = ref(false);
const selectedSlot = ref("RB");
const slotOptions = ["QB", "RB", "WR", "TE", "FLEX"];

const playersQuery = usePlayers(positionFilter, search);
const allPlayersQuery = usePlayers(ref("All"), ref(""));
const { rosterQuery, addToRoster, removeFromRoster } = useRoster();
const { lineupQuery, setLineup } = useLineup();

const players = computed<Player[]>(() => playersQuery.data.value ?? []);
const allPlayers = computed<Player[]>(() => allPlayersQuery.data.value ?? []);
const rosterEntries = computed<RosterEntry[]>(() => rosterQuery.data.value ?? []);
const lineupEntries = computed<LineupEntry[]>(() => lineupQuery.data.value ?? []);

const rosterIds = computed(() => rosterEntries.value.map((entry) => entry.player_id));
const lineupIds = computed(() => lineupEntries.value.map((entry) => entry.player_id));
const playersById = computed(() => new Map<number, Player>(allPlayers.value.map((player) => [player.id, player])));

const availablePlayers = computed(() => players.value.filter((player) => !rosterIds.value.includes(player.id)));

const activeLineup = computed<(Player & { slot: string })[]>(() =>
  lineupEntries.value
    .map((lineup) => {
      const player = playersById.value.get(lineup.player_id);
      return player ? { ...player, slot: lineup.slot } : null;
    })
    .filter((player): player is Player & { slot: string } => Boolean(player)),
);

const benchPlayers = computed(() => allPlayers.value.filter((player) => rosterIds.value.includes(player.id) && !lineupIds.value.includes(player.id)));

const isLoading = computed(() => playersQuery.isLoading || rosterQuery.isLoading || lineupQuery.isLoading);

function openDetail(player: Player) {
  selectedPlayer.value = player;
  detailOpen.value = true;
}

function openDrawer(player: Player) {
  selectedPlayer.value = player;
  selectedSlot.value = player.position;
  drawerOpen.value = true;
}

async function confirmAddToLineup() {
  if (!selectedPlayer.value) return;

  const player = selectedPlayer.value;
  const nextLineup: LineupPayload[] = lineupEntries.value
    .filter((entry) => entry.player_id !== player.id)
    .map((entry) => ({
      player_id: entry.player_id,
      slot: entry.slot,
      is_starter: true,
    }));

  nextLineup.push({
    player_id: player.id,
    slot: selectedSlot.value,
    is_starter: true,
  });

  if (!rosterIds.value.includes(player.id)) {
    await addToRoster.mutateAsync(player.id);
  }

  await setLineup.mutateAsync(nextLineup);
  drawerOpen.value = false;
}

async function moveToBench(player: Player) {
  const nextLineup: LineupPayload[] = lineupEntries.value
    .filter((entry) => entry.player_id !== player.id)
    .map((entry) => ({
      player_id: entry.player_id,
      slot: entry.slot,
      is_starter: entry.is_starter,
    }));

  await setLineup.mutateAsync(nextLineup);
}

function gradeColor(value: number) {
  if (value >= 80) return "success";
  if (value >= 60) return "warning";
  return "error";
}
</script>
