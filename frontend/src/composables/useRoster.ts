import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import { apiFetch } from "@/lib/api";
import type { RosterEntry } from "@/types/roster";

export function useRoster() {
  const queryClient = useQueryClient();

  const rosterQuery = useQuery<RosterEntry[]>({
    queryKey: ["roster"],
    queryFn: async () => apiFetch<RosterEntry[]>("/roster/"),
  });

  const addToRoster = useMutation<{ message: string }, Error, number>({
    mutationFn: async (playerId: number) => {
      return apiFetch<{ message: string }>(`/roster/add/${playerId}`, {
        method: "POST",
      });
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: ["roster"] });
      queryClient.invalidateQueries({ queryKey: ["players"] });
    },
  });

  const removeFromRoster = useMutation<{ message: string }, Error, number>({
    mutationFn: async (playerId: number) => {
      return apiFetch<{ message: string }>(`/roster/remove/${playerId}`, {
        method: "DELETE",
      });
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: ["roster"] });
      queryClient.invalidateQueries({ queryKey: ["players"] });
    },
  });

  return { rosterQuery, addToRoster, removeFromRoster };
}
