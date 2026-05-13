import { useState } from "react";
import { usePlayers } from "@/hooks/usePlayers";
import { useRoster, useAddPlayer, useRemovePlayer } from "@/hooks/useRoster";
import type { Position } from "@/types/player";

const POSITIONS: Position[] = ["QB", "RB", "WR", "TE"];

export default function Players() {
  const [position, setPosition] = useState<Position | undefined>(undefined);
  const [search, setSearch] = useState("");

  const { data: players, isLoading, error } = usePlayers(position, search);
  const { data: roster } = useRoster();
  const { mutate: addPlayer } = useAddPlayer();
  const { mutate: removePlayer } = useRemovePlayer();

  const rosterPlayerIds = new Set(roster?.map((p) => p.player_id) ?? []);

  return (
    <div>
      <h1>Players</h1>

      <div>
        <button onClick={() => setPosition(undefined)}>All</button>
        {POSITIONS.map((pos) => (
          <button key={pos} onClick={() => setPosition(pos)}>
            {pos}
          </button>
        ))}
      </div>

      <input type="text" placeholder="Search players..." value={search} onChange={(e) => setSearch(e.target.value)} />

      {isLoading && <p>Loading...</p>}
      {error && <p>Error: {error.message}</p>}

      {players && (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Position</th>
              <th>Team</th>
              <th>Grade</th>
              <th>Matchup</th>
              <th>Chaos</th>
              <th>Trend</th>
              <th>Roster</th>
            </tr>
          </thead>
          <tbody>
            {players.map((player) => (
              <tr key={player.id}>
                <td>{player.full_name}</td>
                <td>{player.position}</td>
                <td>{player.team ?? "FA"}</td>
                <td>{player.gridiron_grade}</td>
                <td>{player.matchup_grade}</td>
                <td>{player.chaos_score}</td>
                <td>{player.opportunity_trend}</td>
                <td>
                  {rosterPlayerIds.has(player.id) ? (
                    <button onClick={() => removePlayer(player.id)}>Remove</button>
                  ) : (
                    <button onClick={() => addPlayer(player.id)}>Add</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
