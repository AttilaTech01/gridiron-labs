import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import { apiFetch } from "@/lib/api";
import type { LineupEntry, LineupPayload } from "@/types/lineup";

export function useLineup() {
  const queryClient = useQueryClient();

  const lineupQuery = useQuery<LineupEntry[]>({
    queryKey: ["lineup"],
    queryFn: async () => apiFetch<LineupEntry[]>("/lineup/"),
  });

  const setLineup = useMutation<{ message: string }, Error, LineupPayload[]>({
    mutationFn: async (entries: LineupPayload[]) => {
      return apiFetch<{ message: string }>("/lineup/set", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(entries),
      });
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: ["lineup"] });
    },
  });

  return { lineupQuery, setLineup };
}
