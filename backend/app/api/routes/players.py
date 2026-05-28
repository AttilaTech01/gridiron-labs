from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models import Player
from app.services.mock_grades import get_mock_grade
from app.schemas.player import PlayerResponse

router = APIRouter(prefix="/players", tags=["players"])

POSITION_LIMIT = 200  # Max players returned when filtering by position only
SEARCH_LIMIT = 20     # Max players returned when searching by name

@router.get("/", response_model=list[PlayerResponse])
async def get_players(
    position: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    response: list[PlayerResponse] = []

    # No filter and no search — return nothing
    if not position and not search:
        return response

    # Search requires at least 3 characters
    if search and len(search) < 3:
        return response
    
    query = select(Player)

    if position:
        query = query.where(Player.position == position.upper())

    if search:
        query = query.where(Player.full_name.ilike(f"%{search}%"))

    # Apply the right limit
    limit = SEARCH_LIMIT if search else POSITION_LIMIT
    query = query.order_by(Player.full_name).limit(limit)

    result = await db.execute(query)
    players = result.scalars().all()

    for p in players:
        grade = get_mock_grade(p.id, p.position)
        response.append(PlayerResponse(
            id=p.id,
            sleeper_id=p.sleeper_id,
            full_name=p.full_name,
            position=p.position,
            team=p.team,
            status=p.status,
            gridiron_grade=grade["gridiron_grade"],
            matchup_grade=grade["matchup_grade"],
            chaos_score=grade["chaos_score"],
            opportunity_trend=grade["opportunity_trend"],
        ))
    return response