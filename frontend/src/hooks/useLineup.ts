import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiFetch from "@/lib/api";
import type { LineupEntry, LineupRequest } from "@/types/lineup";
import type { MutationResponse } from "@/types/shared";

export function useLineup() {
  return useQuery<LineupEntry[]>({
    queryKey: ["lineup"],
    queryFn: () => apiFetch<LineupEntry[]>("/lineup"),
  });
}

export function useSetLineup() {
  const queryClient = useQueryClient();

  return useMutation<MutationResponse, Error, LineupRequest[]>({
    mutationFn: (entries: LineupRequest[]) =>
      apiFetch<MutationResponse>("/lineup/set", {
        method: "POST",
        body: JSON.stringify(entries),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["lineup"] });
    },
  });
}
