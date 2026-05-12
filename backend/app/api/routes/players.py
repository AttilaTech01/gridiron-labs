from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import TypedDict

from app.core.database import get_db
from app.models import Player
from app.services.mock_grades import get_mock_grade

router = APIRouter(prefix="/players", tags=["players"])

class PlayerResponse(TypedDict):
    id: int
    sleeper_id: str
    full_name: str
    position: str
    team: str | None
    status: str
    gridiron_grade: int
    matchup_grade: str
    chaos_score: int
    opportunity_trend: str

@router.get("/")
async def get_players(
    position: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Player).where(Player.position != "K")

    if position:
        query = query.where(Player.position == position.upper())

    if search:
        query = query.where(Player.full_name.ilike(f"%{search}%"))

    result = await db.execute(query)
    players = result.scalars().all()

    response: list[PlayerResponse] = []

    for p in players:
        grade = get_mock_grade(p.id, p.position)
        response.append({
            "id": p.id,
            "sleeper_id": p.sleeper_id,
            "full_name": p.full_name,
            "position": p.position,
            "team": p.team,
            "status": p.status,
            "gridiron_grade": grade["gridiron_grade"],
            "matchup_grade": grade["matchup_grade"],
            "chaos_score": grade["chaos_score"],
            "opportunity_trend": grade["opportunity_trend"],
        })
    return response