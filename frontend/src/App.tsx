import { useState } from "react";
import Lineup from "@/pages/Lineup";
import Players from "@/pages/Players";

type Page = "players" | "lineup";

export default function App() {
  const [page, setPage] = useState<Page>("players");

  return (
    <div>
      <nav>
        <button onClick={() => setPage("players")}>Players</button>
        <button onClick={() => setPage("lineup")}>Lineup</button>
      </nav>
      {page === "players" && <Players />}
      {page === "lineup" && <Lineup />}
    </div>
  );
}
