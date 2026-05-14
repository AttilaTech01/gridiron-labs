---
name: api-change
description: Plan or implement a backend API contract change.
agent: Planner
argument-hint: endpoint/change=<describe API change>
---
Analyze this backend/API change for Gridiron Labs:

`${input:change:Describe the endpoint or API behavior to add/change}`

Read:

- `ARCHITECTURE.md`
- `CONTRIBUTING.md`
- `docs/API.md`
- `docs/DATA_MODEL.md`
- `TESTING.md`

Return:

1. Current route behavior
2. Proposed request/response contracts
3. Pydantic schema changes
4. SQLAlchemy/model/migration impact
5. Frontend hook/type impact
6. Tests to add
7. Backward compatibility risks

Do not edit files unless explicitly asked after the plan is reviewed.
