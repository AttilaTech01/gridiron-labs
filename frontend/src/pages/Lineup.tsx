import { useEffect, useState } from "react";
import { useRoster } from "@/hooks/useRoster";
import { useLineup, useSetLineup } from "@/hooks/useLineup";
import type { LineupRequest } from "@/types/lineup";

const SLOTS = ["QB", "RB1", "RB2", "WR1", "WR2", "FLEX", "TE", "BN"];

export default function Lineup() {
  const { data: roster } = useRoster();
  const { data: lineup } = useLineup();
  const { mutate: setLineup } = useSetLineup();

  const [assignments, setAssignments] = useState<Record<number, string>>({});

  useEffect(() => {
    if (!roster || !lineup) return;

    const initial: Record<number, string> = {};
    roster.forEach((r) => {
      const existingSlot = lineup.find((l) => l.player_id === r.player_id)?.slot;
      initial[r.player_id] = existingSlot ?? "BN";
    });
    setAssignments(initial);
  }, [roster, lineup]);

  const assign = (playerId: number, slot: string) => {
    setAssignments((prev) => ({ ...prev, [playerId]: slot }));
  };

  const handleSave = () => {
    if (!roster) return;

    const entries: LineupRequest[] = roster.map((r) => ({
      player_id: r.player_id,
      slot: assignments[r.player_id] ?? "BN",
      is_starter: assignments[r.player_id] !== "BN",
    }));

    setLineup(entries);
  };

  return (
    <div>
      <h1>Lineup</h1>

      {roster && roster.length === 0 && <p>No players on your roster yet. Add some from the Players page.</p>}

      {roster && roster.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Player ID</th>
              <th>Slot</th>
            </tr>
          </thead>
          <tbody>
            {roster.map((r) => {
              const currentLineup = lineup?.find((l) => l.player_id === r.player_id);
              return (
                <tr key={r.player_id}>
                  <td>{r.player_id}</td>
                  <td>
                    <select value={assignments[r.player_id] ?? currentLineup?.slot ?? "BN"} onChange={(e) => assign(r.player_id, e.target.value)}>
                      {SLOTS.map((slot) => (
                        <option key={slot} value={slot}>
                          {slot}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

      <button onClick={handleSave}>Save Lineup</button>
    </div>
  );
}
