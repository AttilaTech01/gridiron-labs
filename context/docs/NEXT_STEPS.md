# Recommended Next Steps

This list is based on the current uploaded codebase.

## Work In Progress

Making sure the fundamentals of the app work:

- User can scroll through the players pool;
- User can log in and setup his league parameters;
- User can add/remove players from his roster;
- User can manage his lineup (start/bench his players);
- UI/UX for those features is sharp and professional.

## Highest priority

### 1. Move API contracts into schemas

Current routes mix local `TypedDict`, local `BaseModel`, and raw ORM responses.

Create:

```txt
backend/app/schemas/players.py
backend/app/schemas/roster.py
backend/app/schemas/lineup.py
backend/app/schemas/common.py
```

Then add `response_model=` to FastAPI routes.

### 2. Implement auth

Clerk is in the roadmap and docs, but not wired.

Before implementing auth, make sure to:

- add Pydantic schemas;
- add route tests against `DEV_USER_ID` behavior;
- then replace user resolution and update tests.

### 3. Add slot validation and default league parameters

Current frontend defines slots, but backend accepts any string.

Suggested backend enum:

```txt
QB, RB, WR, TE, FLEX, BN
```

A specific user, once logged in, has default league params.
The functionalities of the app must adapt to this params.

Default params:

```txt
to be determined
```

### 4. Add basic UI components

Current UI works but is table-first, unstyled and only showing the players pool.

Components to implement:

```txt
to be determined
```

## Medium priority

### 5. Add tests for the Gridiron Grade engine

Why:

- the scoring engine is core product logic;
- it is already written as pure functions;
- tests will protect future real-data integration.

Start with:

```txt
backend/tests/services/test_gridiron_grade.py
```

### 6. Add Vue Router

A frontend router is not currently used; navigation is managed locally in `App.vue`.

Router becomes useful when adding:

- settings/auth pages;
- user account page;
- lineup optimizer page;
- trade architect page.

### 7. Improve API error handling on the frontend

Current `apiFetch()` assumes error bodies have a useful `detail` string. FastAPI can also return arrays or objects for validation errors.

Improve error normalization before building more UI.

### 8. Add frontend tests after extracting components

Testing will be easier after reusable components exist.

Start with:

- API client tests;
- player page add/remove behavior;
- lineup slot assignment behavior.

## Product/data priority

### 9. Create a real GradeInput translator layer

The scoring engine should remain provider-agnostic.

Create a module that converts source data into `GradeInput`:

```txt
backend/app/services/grade_inputs.py
```

Later, add provider-specific modules under:

```txt
backend/app/services/data_sources/
```

### 10. Decide what a lineup means by week

Current `lineups` table has no week or season. For fantasy football, this will eventually matter.

Questions to answer:

- Is a lineup a saved current lineup only?
- Should lineups be historical by NFL week?
- Should grades be stored by week/player?
- How does the app handle bye weeks?

## Known technical debt

- `backend/app/schemas/` exists but is empty.
- `DEV_USER_ID = 1` must be replaced when auth is implemented.
- `players.py` computes mock grades per request instead of using real data.
- frontend navigation is local state, not Vue Router.
