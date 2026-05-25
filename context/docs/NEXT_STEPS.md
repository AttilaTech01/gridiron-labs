# Recommended Next Steps

This list is based on the current uploaded codebase.

## Work In Progress

Making sure the fundamentals of the app work:

- User can scroll through the players pool;
- User can add/remove players from his roster;
- User can manage his lineup (start/bench his players);
- UI/UX for those features is sharp and professional.

## Highest priority

### 1. Add tests for the Gridiron Grade engine

Why:

- the scoring engine is core product logic;
- it is already written as pure functions;
- tests will protect future real-data integration.

Start with:

```txt
backend/tests/services/test_gridiron_grade.py
```

### 2. Move API contracts into schemas

Current routes mix local `TypedDict`, local `BaseModel`, and raw ORM responses.

Create:

```txt
backend/app/schemas/players.py
backend/app/schemas/roster.py
backend/app/schemas/lineup.py
backend/app/schemas/common.py
```

Then add `response_model=` to FastAPI routes.

### 3. Remove debug prints

Remove from `backend/app/api/routes/lineup.py`:

```py
print("result :", result)
print("lineup :", lineup)
```

### 4. Add database constraints

Recommended constraints:

- unique `(user_id, player_id)` on `rosters`;
- unique `(user_id, player_id)` on `lineups`;
- possibly non-null `status` and `is_starter` consistency with models.

### 5. Add basic UI components for player grades

Current UI works but is table-first and unstyled.

Useful components:

```txt
frontend/src/components/players/PlayerGradeCard.tsx
frontend/src/components/players/MatchupBadge.tsx
frontend/src/components/players/ChaosScoreBadge.tsx
frontend/src/components/lineup/LineupSlotSelect.tsx
```

## Medium priority

### 6. Add slot validation

Current frontend defines slots, but backend accepts any string.

Suggested backend enum:

```txt
QB, RB, WR, TE, FLEX, BN
```

### 7. Add Vue Router

A frontend router is not currently used; navigation is managed locally in `App.vue`.

Router becomes useful when adding:

- player detail page;
- lineup optimizer page;
- settings/auth pages;
- trade architect page.

### 8. Improve API error handling on the frontend

Current `apiFetch()` assumes error bodies have a useful `detail` string. FastAPI can also return arrays or objects for validation errors.

Improve error normalization before building more UI.

### 9. Add frontend tests after extracting components

Testing will be easier after reusable components exist.

Start with:

- API client tests;
- player page add/remove behavior;
- lineup slot assignment behavior.

## Product/data priority

### 10. Create a real GradeInput translator layer

The scoring engine should remain provider-agnostic.

Create a module that converts source data into `GradeInput`:

```txt
backend/app/services/grade_inputs.py
```

Later, add provider-specific modules under:

```txt
backend/app/services/data_sources/
```

### 11. Decide what a lineup means by week

Current `lineups` table has no week or season. For fantasy football, this will eventually matter.

Questions to answer:

- Is a lineup a saved current lineup only?
- Should lineups be historical by NFL week?
- Should grades be stored by week/player?
- How does the app handle bye weeks?

### 12. Implement auth only after API contracts are cleaned up

Clerk is in the roadmap and docs, but not wired.

Before implementing auth:

- add Pydantic schemas;
- add route tests against `DEV_USER_ID` behavior;
- then replace user resolution and update tests.

## Known technical debt

- `backend/app/schemas/` exists but is empty.
- `lineup.py` contains debug `print()` statements.
- `DEV_USER_ID = 1` must be replaced when auth is implemented.
- `players.py` computes mock grades per request instead of using real data.
- database uniqueness constraints are missing for roster and lineup membership.
- frontend navigation is local state, not Vue Router.

## Suggested implementation sequence

1. Tests for scoring engine.
2. Backend schemas and API cleanup.
3. Database constraints and migration.
4. Frontend component extraction and basic styling.
5. Real data translator boundary.
6. Auth integration.
7. Player detail / expandable explanation UI.
8. Lineup optimization logic.
