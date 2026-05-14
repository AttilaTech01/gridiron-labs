---
name: test-plan
description: Create a focused test plan for a Gridiron Labs change.
agent: Planner
argument-hint: change=<describe behavior to test>
---
Create a test plan for this Gridiron Labs change:

`${input:change:Describe the behavior, bug, or feature to test}`

Use:

- `TESTING.md`
- `ARCHITECTURE.md`
- `docs/API.md`
- `docs/GRIDIRON_GRADE_ENGINE.md` if scoring is involved

Return:

1. Unit tests
2. API/integration tests
3. Frontend tests
4. Manual QA checklist
5. Test data/fixtures needed
6. Edge cases
7. What not to test yet

Do not edit files.
