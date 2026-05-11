from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models import Player

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/")
async def get_players(
    position: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Player)

    if position:
        query = query.where(Player.position == position.upper())

    if search:
        query = query.where(Player.full_name.ilike(f"%{search}%"))

    result = await db.execute(query)
    players = result.scalars().all()
    return players