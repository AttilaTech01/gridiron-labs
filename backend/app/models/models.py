from __future__ import annotations
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    clerk_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    roster: Mapped[list[Roster]] = relationship("Roster", back_populates="user")
    lineup: Mapped[list[Lineup]] = relationship("Lineup", back_populates="user")


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sleeper_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=False)
    team: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")

    target_share: Mapped[float | None] = mapped_column(Float, nullable=True)
    season_target_share: Mapped[float | None] = mapped_column(Float, nullable=True)
    gridiron_grade: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chaos_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    matchup_grade: Mapped[str | None] = mapped_column(String, nullable=True)


class Roster(Base):
    __tablename__ = "rosters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="roster")
    player: Mapped[Player] = relationship("Player")


class Lineup(Base):
    __tablename__ = "lineups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)
    slot: Mapped[str | None] = mapped_column(String, nullable=True)
    is_starter: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[User] = relationship("User", back_populates="lineup")
    player: Mapped[Player] = relationship("Player")