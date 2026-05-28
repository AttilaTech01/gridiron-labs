import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.models import Player, User
from app.core.database import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gridiron_test"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def seed():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        users = [
            User(clerk_id="dev_user", email="dev@gridironlabs.com", username="DevUser"),
        ]
        players = [
            Player(sleeper_id="1", full_name="Patrick Mahomes", position="QB", team="KC", status="active"),
            Player(sleeper_id="2", full_name="Derrick Henry", position="RB", team="TEN", status="active"),
            Player(sleeper_id="3", full_name="Tyreek Hill", position="WR", team="MIA", status="active"),
            Player(sleeper_id="4", full_name="Travis Kelce", position="TE", team="KC", status="active"),
            Player(sleeper_id="5", full_name="Justin Tucker", position="K", team="BAL", status="active"),
            Player(sleeper_id="6", full_name="Stefon Diggs", position="WR", team="BUF", status="active"),
            Player(sleeper_id="7", full_name="Josh Allen", position="QB", team="BUF", status="active"),
            Player(sleeper_id="8", full_name="Christian McCaffrey", position="RB", team="SF", status="active"),
        ]
        session.add_all(users + players)
        await session.commit()

    print("Test database seeded successfully!")
    await test_engine.dispose()


asyncio.run(seed())