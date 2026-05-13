import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import apiFetch from "@/lib/api";
import type { RosterEntry } from "@/types/roster";
import type { MutationResponse } from "@/types/shared";

export function useRoster() {
  return useQuery<RosterEntry[]>({
    queryKey: ["roster"],
    queryFn: () => apiFetch("/roster"),
  });
}

export function useAddPlayer() {
  const queryClient = useQueryClient();

  return useMutation<MutationResponse, Error, number>({
    mutationFn: (playerId: number) =>
      apiFetch(`/roster/add/${playerId}`, {
        method: "POST",
        body: JSON.stringify({ playerId }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["roster"] });
    },
  });
}

export function useRemovePlayer() {
  const queryClient = useQueryClient();

  return useMutation<MutationResponse, Error, number>({
    mutationFn: (playerId: number) =>
      apiFetch(`/roster/remove/${playerId}`, {
        method: "DELETE",
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["roster"] });
    },
  });
}
