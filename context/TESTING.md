# Testing Strategy

## Current testing state

The uploaded project includes backend testing dependencies:

- `pytest`
- `pytest-asyncio`

Frontend test tooling such as Vitest, Vue Testing Library, or Playwright is not currently configured in `package.json`.

## Testing priorities

Because the app is early MVP, tests should focus first on business logic and API behavior.

Recommended order:

1. Backend API tests for players, roster, and lineup.
2. Frontend hook/component tests for the core user workflows.
3. End-to-end tests once UI routing and styling are more stable.

## Backend unit tests

## Backend API tests

Recommended route tests:

### Players

- `GET /api/v1/players/` returns players excluding kickers.
- `GET /api/v1/players/?position=QB` returns only QBs.
- `GET /api/v1/players/?search=<name>` filters by name.
- each player response includes grading fields.

### Roster

- `GET /api/v1/roster/` returns the dev user's roster.
- `POST /api/v1/roster/add/{player_id}` adds a valid player.
- adding a missing player returns 404.
- adding a duplicate player returns 400.
- `DELETE /api/v1/roster/remove/{player_id}` removes a roster player.
- removing a missing roster player returns 404.

### Lineup

- `GET /api/v1/lineup/` returns the dev user's lineup.
- `POST /api/v1/lineup/set` rejects players not on the roster.
- `POST /api/v1/lineup/set` replaces the previous lineup.
- starter flags are stored correctly.

## Database test strategy

For a reliable backend test suite we have a dedicated database `gridiron_test`.

Recommended approach:

- create a separate PostgreSQL test database;
- override `get_db()` in FastAPI tests;
- wrap each test in setup/cleanup;
- seed only the data required for the test;
- avoid depending on the real Sleeper seed data.

## Frontend tests

Frontend tests are not configured yet. When ready, consider:

- Vitest
- Vue Testing Library or Vue Test Utils
- MSW for API mocking
- Playwright for end-to-end workflows

Recommended first frontend tests:

### API client

- `apiFetch()` prefixes `/api/v1`.
- `apiFetch()` throws a useful error on non-OK responses.

### Hooks

- `usePlayers()` builds query params correctly.
- roster mutations invalidate the `roster` query.
- lineup mutation invalidates the `lineup` query.

### Components / pages

- `Players` displays loading state.
- `Players` displays error state.
- `Players` shows Add or Remove based on roster membership.
- `Lineup` initializes slots from existing lineup.
- `Lineup` submits one entry per roster player.

## End-to-end tests

Add e2e tests after the UI is more stable.

First useful happy path:

1. Start backend and frontend against a known seed state.
2. Open Players page.
3. Search for a player.
4. Add player to roster.
5. Go to Lineup page.
6. Assign slot.
7. Save lineup.
8. Refresh and verify saved lineup persists.

## Manual QA checklist

Before shipping MVP changes, manually verify:

- backend `/health` returns OK;
- frontend loads without console errors;
- players page loads data;
- position filters work;
- search works;
- add/remove roster works;
- lineup page reflects current roster;
- save lineup works;
- API errors are visible enough to debug;
- no UI claims that mock grades are real live data.

## Commands currently available

### Frontend

```bash
cd frontend
npm install
npm run dev
npm run build
```

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
python -m alembic upgrade head
python -m pytest
```

## Testing rule for AI agents

When an AI agent changes code, it should propose or add tests for the behavior it changed. For scoring logic, tests are mandatory because the formulas are central to product trust.
