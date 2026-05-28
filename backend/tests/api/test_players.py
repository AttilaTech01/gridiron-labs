import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_players_no_filter_returns_empty(client: AsyncClient):
    response = await client.get("/api/v1/players/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_players_search_too_short_returns_empty(client: AsyncClient):
    response = await client.get("/api/v1/players/?search=ab")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_players_by_position(client: AsyncClient):
    response = await client.get("/api/v1/players/?position=WR")
    assert response.status_code == 200
    players = response.json()
    assert len(players) > 0
    assert all(p["position"] == "WR" for p in players)


@pytest.mark.asyncio
async def test_get_players_search_by_name(client: AsyncClient):
    response = await client.get("/api/v1/players/?search=Mahomes")
    assert response.status_code == 200
    players = response.json()
    assert len(players) == 1
    assert players[0]["full_name"] == "Patrick Mahomes"


@pytest.mark.asyncio
async def test_get_players_response_has_grade_fields(client: AsyncClient):
    response = await client.get("/api/v1/players/?position=QB")
    assert response.status_code == 200
    players = response.json()
    assert len(players) > 0
    player = players[0]
    assert "gridiron_grade" in player
    assert "matchup_grade" in player
    assert "chaos_score" in player
    assert "opportunity_trend" in player


@pytest.mark.asyncio
async def test_get_players_matchup_grade_is_valid(client: AsyncClient):
    response = await client.get("/api/v1/players/?position=WR")
    assert response.status_code == 200
    players = response.json()
    for player in players:
        assert player["matchup_grade"] in ("GREEN", "YELLOW", "RED")


@pytest.mark.asyncio
async def test_get_players_opportunity_trend_is_valid(client: AsyncClient):
    response = await client.get("/api/v1/players/?position=WR")
    assert response.status_code == 200
    players = response.json()
    for player in players:
        assert player["opportunity_trend"] in ("GROWING", "SHRINKING", "STABLE")


@pytest.mark.asyncio
async def test_get_players_search_case_insensitive(client: AsyncClient):
    response = await client.get("/api/v1/players/?search=mahomes")
    assert response.status_code == 200
    players = response.json()
    assert len(players) == 1
    assert players[0]["full_name"] == "Patrick Mahomes"