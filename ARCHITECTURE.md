# Gridiron Labs Architecture

## Current architecture summary

Gridiron Labs is a monorepo with:

- a **frontend** built with Vite, React, TypeScript, Tailwind CSS, shadcn/ui-style components, and TanStack Query;
- a **backend** built with FastAPI, SQLAlchemy async sessions, Alembic migrations, PostgreSQL, and Redis;
- a **database** with users, players, rosters, and lineups;
- a **mock scoring service** that produces deterministic Gridiron Grade values until real football data is integrated.

## Repository layout

```txt
gridiron-labs/
├── frontend/
│   ├── src/
│   │   ├── components/ui/      # Reusable UI primitives
│   │   ├── hooks/              # React Query hooks
│   │   ├── lib/                # API client and utilities
│   │   ├── pages/              # Current screens
│   │   └── types/              # Frontend TypeScript contracts
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig*.json
├── backend/
│   ├── app/
│   │   ├── api/routes/         # FastAPI route modules
│   │   ├── core/               # Config and database session setup
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Currently empty; future Pydantic schemas
│   │   ├── services/           # Gridiron scoring and mock data logic
│   │   └── main.py             # FastAPI app entry point
│   ├── db/                     # Alembic migrations
│   ├── scripts/                # Seed scripts
│   └── requirements.txt
├── docker-compose.yml
├── README.md
└── gridiron-labs-context.md
```

## Runtime architecture

```mermaid
flowchart LR
  Browser[React app on localhost:5173]
  API[FastAPI app on localhost:8000]
  DB[(PostgreSQL gridiron DB)]
  Redis[(Redis cache)]
  Sleeper[Sleeper API]

  Browser -->|fetch /api/v1| API
  API -->|SQLAlchemy async sessions| DB
  API -. future cache .-> Redis
  SeedScript[backend/scripts/seed_players.py] --> Sleeper
  SeedScript --> DB
```

## Frontend architecture

### Current stack

- Vite
- React
- TypeScript
- Tailwind CSS v4-style setup
- shadcn/ui-style primitives
- TanStack Query
- React Router dependency is installed, but current navigation is local state in `App.tsx`
- Zustand dependency is installed, but no store is currently used

### Current screens

#### `frontend/src/pages/Players.tsx`

Responsibilities:

- maintain local search and position filter state;
- load players from `/players/`;
- load roster from `/roster/`;
- add/remove players from the roster;
- render a basic table with grading fields.

Key hooks:

- `usePlayers(position, search)`
- `useRoster()`
- `useAddPlayer()`
- `useRemovePlayer()`

#### `frontend/src/pages/Lineup.tsx`

Responsibilities:

- load current roster;
- load saved lineup;
- initialize assignments by player id;
- allow the user to choose slots;
- save lineup entries to `/lineup/set`.

Key hooks:

- `useRoster()`
- `useLineup()`
- `useSetLineup()`

### API client

`frontend/src/lib/api.ts` defines a generic `apiFetch<T>()` wrapper.

Current behavior:

- base URL comes from `VITE_API_URL`, defaulting to `http://localhost:8000`;
- all paths are prefixed with `/api/v1`;
- JSON content type is sent on every request;
- non-OK responses throw `Error(error.detail ?? "Unknown error")`.

### Frontend conventions

When adding frontend code:

- keep server state in TanStack Query hooks;
- keep UI-only state local unless it is genuinely shared;
- define frontend contracts in `src/types/`;
- keep API calls in `src/lib/api.ts` or feature-specific API helpers;
- prefer reusable components for player cards, grade badges, matchup indicators, lineup slots, and empty/loading/error states;
- avoid putting domain formulas directly in React components.

## Backend architecture

### Current stack

- FastAPI
- SQLAlchemy async engine and async sessions
- Pydantic settings
- Alembic
- PostgreSQL
- Redis dependency is present and Dockerized, but not yet used in application code
- `httpx` is used by the seed script
- `pytest` and `pytest-asyncio` are installed, but no tests are currently present

### App entry point

`backend/app/main.py`:

- creates the FastAPI app;
- enables CORS for `http://localhost:5173`;
- includes all API routes under `/api/v1`;
- exposes `/health`.

### API routing

Routes are mounted through `backend/app/api/routes/__init__.py`.

Current route groups:

- `/api/v1/players`
- `/api/v1/roster`
- `/api/v1/lineup`

### Database session management

`backend/app/core/database.py`:

- reads `settings.database_url`;
- converts `postgresql://` to `postgresql+asyncpg://` for async SQLAlchemy;
- creates `AsyncSessionLocal`;
- exposes `get_db()` dependency.

### Configuration

`backend/app/core/config.py` uses Pydantic Settings.

Known backend env keys:

- `DATABASE_URL`
- `REDIS_URL`
- `ENVIRONMENT`
- `CLERK_SECRET_KEY`

Known frontend env keys:

- `VITE_API_URL`
- `VITE_CLERK_PUBLISHABLE_KEY` is documented in `README.md`, but the uploaded `.env.local` only shows `VITE_API_URL` as set.

Never commit real secret values.

## Data model summary

Current SQLAlchemy entities:

- `User`
- `Player`
- `Roster`
- `Lineup`

Relationships:

- one user has many roster entries;
- one user has many lineup entries;
- each roster entry points to one player;
- each lineup entry points to one player.

See `docs/DATA_MODEL.md` for details.

## Scoring architecture

Current scoring is split into two services:

- `app/services/gridiron_grade.py`: actual scoring formulas and typed result structure.
- `app/services/mock_grades.py`: deterministic mock input generator seeded by `player_id`.

The current API calls `get_mock_grade(p.id, p.position)` for each player returned by the player search endpoint.

Important: the database has columns for `target_share`, `season_target_share`, `gridiron_grade`, `chaos_score`, and `matchup_grade`, but the current `/players/` endpoint does not use those stored values. It computes mock grades per request.

## Current important constraints

### Auth is not implemented yet

`roster.py` and `lineup.py` use:

```py
DEV_USER_ID = 1
```

This means every roster and lineup operation is tied to user id 1. Do not build multi-user features until Clerk auth or another user resolution mechanism is implemented.

### Grades are mock data

Player grades are deterministic but not real. They are useful for UI and data-flow testing, not final product claims.

### Tests are missing

No backend or frontend test files are present in the uploaded project.

### API schemas are mixed

Current route files return ORM objects directly in some endpoints and use local `TypedDict`/`BaseModel` types in others. The `backend/app/schemas/` folder exists but is empty. Future work should move request/response models into this folder.

### No global frontend routing yet

`react-router-dom` is installed, but `App.tsx` currently uses local state for page switching.

## Recommended next architectural improvements

1. Add backend Pydantic schemas for player, roster, lineup, and mutation responses.
2. Add backend tests for the grading engine.
3. Add API integration tests for players, roster, and lineup.
4. Replace direct ORM responses with explicit response schemas.
5. Remove debug `print()` statements from `lineup.py`.
6. Add basic frontend components for grade cards, matchup badges, and roster/player rows.
7. Add React Router if the app grows beyond the current two-screen MVP.
8. Implement Clerk auth and replace `DEV_USER_ID` with authenticated user resolution.
9. Create a real data ingestion boundary that converts football data into `GradeInput`.
10. Use Redis only when a real caching need exists, such as expensive simulations, live updates, or external API response caching.

## Architecture rule for AI agents

Before making large changes, an AI agent should identify which layer is affected:

- product logic;
- frontend presentation;
- frontend server-state hooks;
- API route contract;
- backend domain/service logic;
- database model/migration;
- data ingestion;
- authentication.

Changes that cross more than two layers should start with an implementation plan.
