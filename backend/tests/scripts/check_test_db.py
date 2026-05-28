import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        "postgresql://postgres:postgres@localhost:5432/gridiron_test"
    )
    print("Connected to test database successfully!")
    await conn.close()

asyncio.run(test())