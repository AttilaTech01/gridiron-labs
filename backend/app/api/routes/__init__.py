from fastapi import APIRouter
from app.api.routes import lineup, players, roster

api_router = APIRouter()
api_router.include_router(lineup.router)
api_router.include_router(players.router)
api_router.include_router(roster.router)