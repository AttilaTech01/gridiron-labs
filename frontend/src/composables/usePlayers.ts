import { computed, type Ref } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { buildApiPath, apiFetch } from "@/lib/api";
import type { Player } from "@/types/player";

export function usePlayers(position: Ref<string>, search: Ref<string>) {
  const queryKey = computed(
    () =>
      [
        "players",
        {
          position: position.value === "All" ? undefined : position.value,
          search: search.value || undefined,
        },
      ] as const,
  );

  return useQuery<Player[]>({
    queryKey,
    queryFn: async () => {
      const params = {
        position: position.value === "All" ? undefined : position.value,
        search: search.value || undefined,
      };
      const path = buildApiPath("/players/", params);
      return apiFetch<Player[]>(path);
    },
  });
}
