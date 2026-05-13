import { useQuery } from "@tanstack/react-query";
import apiFetch from "@/lib/api";
import type { Player } from "@/types/player";

export function usePlayers(position?: string, search?: string) {
  return useQuery<Player[]>({
    queryKey: ["players", position, search],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (position) params.append("position", position);
      if (search) params.append("search", search);

      const query = params.toString() ? `?${params.toString()}` : "";
      return apiFetch<Player[]>(`/players/${query}`);
    },
  });
}
