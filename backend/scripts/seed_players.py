import asyncio
import httpx

from app.core.database import AsyncSessionLocal
from app.models import Player

SLEEPER_URL = "https://api.sleeper.app/v1/players/nfl"

# Only skill positions we care about
RELEVANT_POSITIONS = {"QB", "RB", "WR", "TE", "K"}

async def fetch_players() -> dict[str, dict[str, str | None]]:
    print("Fetching players from Sleeper API...")
    async with httpx.AsyncClient() as client:
        response = await client.get(SLEEPER_URL, timeout=30)
        response.raise_for_status()
        return response.json()

    
async def seed():
    data = await fetch_players()
    print(f"Fetched {len(data)} total players from Sleeper")

    players_to_insert: list[Player] = []

    for sleeper_id, player in data.items():
        position = player.get("position")
        full_name = player.get("full_name")
        status = player.get("status", "inactive")
        team = player.get("team")

        # Skip players without a name, position, or not in a skill position
        if not full_name or position not in RELEVANT_POSITIONS:
            continue

        # Only keep active players or free agents with a team
        if status not in ("active", "inactive") and not team:
            continue

        players_to_insert.append(Player(
            sleeper_id=sleeper_id,
            full_name=full_name,
            position=position,
            team=team,
            status=status,
        ))

    print(f"Inserting {len(players_to_insert)} relevant players...")

    async with AsyncSessionLocal() as session:
        session.add_all(players_to_insert)
        await session.commit()

    print("Done! Players table seeded successfully.")
    

if __name__ == "__main__":
    asyncio.run(seed())