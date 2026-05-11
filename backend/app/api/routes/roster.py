from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models import Player, Roster

# Hardcoded user_id for now — will be replaced by Clerk auth later
DEV_USER_ID = 1

router = APIRouter(prefix="/roster", tags=["roster"])

@router.get("/")
async def get_roster(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Roster).where(Roster.user_id == DEV_USER_ID)
    )
    roster = result.scalars().all()
    return roster


@router.post("/add/{player_id}")
async def add_player(player_id: int, db: AsyncSession = Depends(get_db)):
    # Check if player exists
    result = await db.execute(select(Player).where(Player.id == player_id))
    player = result.scalar_one_or_none()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Check not already on roster
    existing = await db.execute(
        select(Roster).where(
            Roster.user_id == DEV_USER_ID,
            Roster.player_id == player_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Player already on roster")

    roster_entry = Roster(user_id=DEV_USER_ID, player_id=player_id)
    db.add(roster_entry)
    await db.commit()
    return {"message": "Player added to roster"}


@router.delete("/remove/{player_id}")
async def remove_player(player_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Roster).where(
            Roster.user_id == DEV_USER_ID,
            Roster.player_id == player_id
        )
    )
    roster_entry = result.scalar_one_or_none()
    if not roster_entry:
        raise HTTPException(status_code=404, detail="Player not on roster")

    await db.delete(roster_entry)
    await db.commit()
    return {"message": "Player removed from roster"}