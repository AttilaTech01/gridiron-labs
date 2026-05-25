# Contributing Guide

## Development mindset

Gridiron Labs is early MVP software. Keep changes small, explicit, and easy to validate.

The best contribution is not the most clever implementation. It is the one that preserves the product promise:

> A fast fantasy football lineup recommendation that can be explained clearly.

## Before changing code

Read these files first:

- `README.md` for project overview and setup instructions.
- `context/PRODUCT.md` for product goals, personas, MVP scope, and roadmap.
- `context/ARCHITECTURE.md` for repo structure, data flow, current constraints, and layer rules.
- `context/TESTING.md` for test strategy.
- `context/docs/API.md` before changing routes or frontend API calls.
- `context/docs/DATA_MODEL.md` before changing models or migrations.
- `context/docs/GRIDIRON_GRADE_ENGINE.md` before changing scoring logic.

## Product rules

- The current MVP is the Start/Sit Optimizer.
- The product should give a clear five-second answer and allow deeper five-minute analysis.
- Do not imply current grades are live real-data recommendations. They are currently deterministic mock grades.
- Preserve the distinction between the Busy Manager view and Power User depth.

## Current technical state

- Frontend: Vite, Vue 3, TypeScript, Vuetify, TanStack Query.
- Backend: FastAPI, async SQLAlchemy, Alembic, PostgreSQL, Redis dependency.
- Current API prefix: `/api/v1`.
- Auth is not implemented. Roster and lineup routes use `DEV_USER_ID = 1`.
- The scoring engine lives in `backend/app/services/gridiron_grade.py`.
- Mock scoring lives in `backend/app/services/mock_grades.py`.
- There are currently no test files in the project.

## Coding rules

- Keep changes small and focused.
- Do not mix unrelated UI, backend, migration, and auth work in one change.
- Do not move business logic into Vue components.
- Keep server state in TanStack Query hooks.
- Keep backend route handlers thin.
- Prefer explicit Pydantic schemas for API request/response contracts.
- Avoid returning raw ORM models from new endpoints.
- Do not introduce a real data source by rewriting the grading engine; create a translator into `GradeInput`.
- Never commit or expose real environment variable values.

## Backend conventions

### File organization

Use the existing structure:

```txt
backend/app/
├── api/routes/       # HTTP route handlers
├── core/             # config, database, shared infrastructure
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic request/response schemas
├── services/         # domain logic and integrations
└── main.py
```

### Route rules

Route handlers should:

- be thin;
- validate request input;
- call services when business logic grows beyond simple CRUD;
- return explicit Pydantic response schemas;
- raise `HTTPException` for known API errors;
- avoid returning raw ORM objects once response schemas exist.

### Service rules

Services should:

- contain domain logic;
- be testable without FastAPI;
- avoid direct HTTP request/response concerns;
- expose small, typed functions;
- keep formulas documented near the implementation.

### Database rules

When changing SQLAlchemy models:

1. Update the model.
2. Generate an Alembic migration.
3. Review the generated migration manually.
4. Apply the migration locally.
5. Update `context/docs/DATA_MODEL.md`.
6. Add/update tests.

Run from `backend/`:

```bash
python -m alembic revision --autogenerate -m "describe change"
python -m alembic upgrade head
```

### Python style

- Use type hints.
- Prefer small pure functions for scoring and calculations.
- Avoid hidden global state except explicit constants.
- Keep async database code async end-to-end.
- Prefer explicit names over abbreviations.
- Keep route-level request/response models in `schemas/` as the API matures.

## Frontend conventions

### File organization

Use the existing structure:

```txt
frontend/src/
├── components/       # reusable UI components
├── composables/      # data-fetching composables and reusable Vue composition helpers
├── lib/              # API client and utilities
├── plugins/          # Vue plugin registration
└── types/            # TypeScript contracts
```

### API usage

- Use `apiFetch<T>()` or a typed API helper.
- Keep query keys stable and descriptive.
- Invalidate only the queries affected by a mutation.
- Do not duplicate backend contracts across multiple files; centralize types in `src/types/` until shared generated contracts exist.

### Component rules

- Keep pages focused on orchestration.
- Extract repeated UI into components.
- Prefer semantic names: `PlayerGradeCard`, `MatchupBadge`, `RosterTable`, `LineupSlotSelect`.
- Keep football calculations out of Vue components.
- Display loading, error, empty, and success states deliberately.

## TypeScript style

- Prefer explicit exported types for API data.
- Use union types for known enums, such as position or matchup grade.
- Avoid `any`.
- Keep strictness from the existing `tsconfig` rules.
- Use `@/` imports for project-local imports.

## UI/UX guidelines

The UI should serve two product modes:

1. Busy Manager: fast, simple, decisive.
2. Power User: explainable, expandable, transparent.

When building UI:

- show Gridiron Grade prominently;
- use Matchup Grade as a color/status signal;
- show Chaos Score as a risk/ceiling signal;
- avoid overwhelming the default view;
- allow deeper context through expandable cards, drawers, tabs, or detail views.

## Authentication rules

Current code uses `DEV_USER_ID = 1`. Until auth is implemented:

- do not assume multiple real users exist;
- do not create product flows that claim user isolation;
- keep auth-related changes behind a focused plan.

When Clerk is implemented:

- create a dependency that resolves the authenticated user;
- avoid repeating auth logic in each route;
- handle first-time user creation or lookup consistently;
- update all roster and lineup queries to use the authenticated user id;
- update tests and documentation.

## Data integration rules

The current scoring engine expects normalized inputs through `GradeInput`.

When integrating real data:

- do not rewrite the scoring engine first;
- create a translator layer that converts raw provider data into `GradeInput`;
- keep provider-specific logic outside the scoring formulas;
- document source assumptions;
- build tests using fixed fixtures before connecting live data.

## Documentation update rule

Any change that alters product behavior, API shape, data model, or scoring logic should update at least one of:

- `context/PRODUCT.md`
- `context/ARCHITECTURE.md`
- `context/TESTING.md`
- `context/docs/API.md`
- `context/docs/DATA_MODEL.md`
- `context/docs/GRIDIRON_GRADE_ENGINE.md`
- `context/docs/NEXT_STEPS.md`
- `context/docs/SETUP.md`
