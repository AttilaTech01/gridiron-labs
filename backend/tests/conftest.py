import pytest_asyncio
from typing import Any, cast, AsyncGenerator
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.database import engine


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=cast(Any, app)),
        base_url="http://test"
    ) as ac:
        yield ac
    await engine.dispose()