# Gridiron Labs Copilot Instructions

You are helping develop Gridiron Labs, a fantasy football companion app focused on actionable start/sit recommendations.

## Always read project context first

Before making meaningful code changes, use these files as project context:

- `PRODUCT.md` for product goals, personas, MVP scope, and roadmap.
- `ARCHITECTURE.md` for repo structure, data flow, current constraints, and layer rules.
- `CONTRIBUTING.md` for coding conventions and review expectations.
- `TESTING.md` for test strategy.
- `docs/API.md` before changing routes or frontend API calls.
- `docs/DATA_MODEL.md` before changing models or migrations.
- `docs/GRIDIRON_GRADE_ENGINE.md` before changing scoring logic.

## Product rules

- The current MVP is the Start/Sit Optimizer.
- The product should give a clear five-second answer and allow deeper five-minute analysis.
- Do not imply current grades are live real-data recommendations. They are currently deterministic mock grades.
- Preserve the distinction between the Busy Manager view and Power User depth.

## Current technical state

- Frontend: Vite, React, TypeScript, Tailwind CSS, shadcn/ui-style components, TanStack Query.
- Backend: FastAPI, async SQLAlchemy, Alembic, PostgreSQL, Redis dependency.
- Current API prefix: `/api/v1`.
- Auth is not implemented. Roster and lineup routes use `DEV_USER_ID = 1`.
- The scoring engine lives in `backend/app/services/gridiron_grade.py`.
- Mock scoring lives in `backend/app/services/mock_grades.py`.
- There are currently no test files in the project.

## Coding rules

- Keep changes small and focused.
- Do not mix unrelated UI, backend, migration, and auth work in one change.
- Do not move business logic into React components.
- Keep server state in TanStack Query hooks.
- Keep backend route handlers thin.
- Prefer explicit Pydantic schemas for API request/response contracts.
- Avoid returning raw ORM models from new endpoints.
- Do not introduce a real data source by rewriting the grading engine; create a translator into `GradeInput`.
- Never commit or expose real environment variable values.

## Testing expectations

- For scoring logic changes, add or update backend unit tests.
- For API behavior changes, add route tests when practical.
- If tests cannot be added yet, state exactly what should be tested manually.

## Planning rule

For changes touching more than two layers, produce a plan before editing. A good plan should include:

- affected files;
- API/data contract changes;
- database migration needs;
- testing approach;
- risks and open questions.

## Known technical debt

- `backend/app/schemas/` exists but is empty.
- `lineup.py` contains debug `print()` statements.
- `DEV_USER_ID = 1` must be replaced when auth is implemented.
- `players.py` computes mock grades per request instead of using real data.
- database uniqueness constraints are missing for roster and lineup membership.
- frontend navigation is local state, not React Router.
