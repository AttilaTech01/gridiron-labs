from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.core.database import get_db
from app.models import Lineup, Roster

# Hardcoded user_id for now — will be replaced by Clerk auth later
DEV_USER_ID = 1

router = APIRouter(prefix="/lineup", tags=["lineup"])

class LineupEntry(BaseModel):
    player_id: int
    slot: str
    is_starter: bool


@router.get("/")
async def get_lineup(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lineup).where(Lineup.user_id == DEV_USER_ID)
    )
    lineup = result.scalars().all()
    print("result :", result)
    print("lineup :", lineup)
    return lineup


@router.post("/set")
async def set_lineup(entries: list[LineupEntry], db: AsyncSession = Depends(get_db)):
    # Verify all players are on the user's roster
    for entry in entries:
        roster_check = await db.execute(
            select(Roster).where(
                Roster.user_id == DEV_USER_ID,
                Roster.player_id == entry.player_id
            )
        )
        if not roster_check.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Player {entry.player_id} is not on your roster"
            )
        
    # Clear existing lineup
    existing = await db.execute(
        select(Lineup).where(Lineup.user_id == DEV_USER_ID)
    )
    for row in existing.scalars().all():
        await db.delete(row)

    # Insert new lineup
    for entry in entries:
        lineup_entry = Lineup(
            user_id=DEV_USER_ID,
            player_id=entry.player_id,
            slot=entry.slot,
            is_starter=entry.is_starter
        )
        db.add(lineup_entry)
    
    await db.commit()
    return {"message": "Lineup updated successfully"}