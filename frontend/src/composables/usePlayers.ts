import { useQuery } from "@tanstack/vue-query";
import { ref, computed, type Ref } from "vue";
import { refDebounced } from "@vueuse/core";

import { buildApiPath, apiFetch } from "@/lib/api";
import type { Player } from "@/types/player";

export function usePlayers() {
  const search = ref("");
  const positionFilter = ref("All");

  const debouncedSearch = refDebounced(search, 1000);

  const isSearchValid = computed(() => debouncedSearch.value.trim().length >= 3);

  const hasFilter = computed(() => positionFilter.value !== "All" || debouncedSearch.value.trim().length >= 1);

  const queryKey = computed(
    () =>
      [
        "players",
        {
          position: positionFilter.value === "All" ? undefined : positionFilter.value,
          search: isSearchValid.value ? debouncedSearch.value : undefined,
        },
      ] as const,
  );

  const query = useQuery<Player[]>({
    queryKey,
    queryFn: async () => {
      const params = {
        position: positionFilter.value === "All" ? undefined : positionFilter.value,
        search: isSearchValid.value ? debouncedSearch.value : undefined,
      };
      const path = buildApiPath("/players/", params);
      return apiFetch<Player[]>(path);
    },
    enabled: hasFilter,
  });

  return {
    search,
    positionFilter,
    hasFilter,
    isSearchValid,
    players: computed(() => query.data.value ?? []),
    isLoading: query.isLoading,
    isError: query.isError,
    error: query.error,
  };
}
