# Contributing Guide

## Development mindset

Gridiron Labs is early MVP software. Keep changes small, explicit, and easy to validate.

The best contribution is not the most clever implementation. It is the one that preserves the product promise:

> A fast fantasy football lineup recommendation that can be explained clearly.

## Before changing code

Read these files first:

1. `PRODUCT.md`
2. `ARCHITECTURE.md`
3. `docs/API.md`
4. `docs/DATA_MODEL.md`
5. `docs/GRIDIRON_GRADE_ENGINE.md` when touching scores or football logic
6. `TESTING.md` when adding or changing behavior

## Branching and commits

Recommended branch names:

```txt
feature/<short-feature-name>
fix/<short-bug-name>
docs/<short-doc-name>
refactor/<short-refactor-name>
```

Recommended commit style:

```txt
Add lineup slot validation
Fix roster duplicate handling
Document grading engine assumptions
Refactor player response schema
```

Keep commits scoped. Avoid mixing UI polish, API changes, and database migrations in the same commit unless they are part of one planned feature.

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
- avoid debug `print()` statements;
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
5. Update `docs/DATA_MODEL.md`.
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
├── hooks/            # data-fetching hooks and reusable React hooks
├── lib/              # API client and utilities
├── pages/            # route-level screens
└── types/            # TypeScript contracts
```

### State management

Use this order of preference:

1. Local component state for UI-only state.
2. TanStack Query for server state.
3. URL/search params when state should be linkable.
4. Zustand only when state is truly global and not server-owned.

### API usage

- Use `apiFetch<T>()` or a typed API helper.
- Keep query keys stable and descriptive.
- Invalidate only the queries affected by a mutation.
- Do not duplicate backend contracts across multiple files; centralize types in `src/types/` until shared generated contracts exist.

### Component rules

- Keep pages focused on orchestration.
- Extract repeated UI into components.
- Prefer semantic names: `PlayerGradeCard`, `MatchupBadge`, `RosterTable`, `LineupSlotSelect`.
- Keep football calculations out of React components.
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

## Review checklist

Before merging a change, check:

- Does this support the current MVP or roadmap?
- Are affected docs updated?
- Are API contracts clear?
- Are database migrations reviewed?
- Are tests added or updated where practical?
- Does the frontend handle loading, error, and empty states?
- Does the code avoid leaking secrets or env values?
- Does this preserve the difference between mock grades and real grades?

## Documentation update rule

Any change that alters product behavior, API shape, data model, or scoring logic should update at least one of:

- `PRODUCT.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `docs/API.md`
- `docs/DATA_MODEL.md`
- `docs/GRIDIRON_GRADE_ENGINE.md`
- `docs/NEXT_STEPS.md`
- `docs/SETUP.md`
