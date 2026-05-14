---
name: feature-plan
description: Plan a Gridiron Labs feature before implementation.
agent: Planner
argument-hint: feature=<feature description>
---
Create an implementation plan for this Gridiron Labs feature:

`${input:feature:Describe the feature or change}`

Use the project context files:

- `PRODUCT.md`
- `ARCHITECTURE.md`
- `CONTRIBUTING.md`
- `TESTING.md`
- `docs/API.md`
- `docs/DATA_MODEL.md`
- `docs/GRIDIRON_GRADE_ENGINE.md` if scoring is involved

Return a plan with:

1. Goal
2. Current state
3. Affected files
4. Data/API impact
5. Implementation steps
6. Testing plan
7. Risks and open questions
8. Definition of done

Do not edit files.
