# How to Use the Project Context Files

These files are designed to become the project memory for **Gridiron Labs**. They are not only documentation for humans; they also help GitHub Copilot and VS Code understand the product, architecture, conventions, and development workflow.

The most important file for Copilot is:

```txt
.github/copilot-instructions.md
```

This file gives Copilot persistent project instructions so it does not have to rediscover your architecture, conventions, and product logic every time you open a new chat.

## 1. Use the docs before asking Copilot to code

Instead of asking Copilot a broad request like:

```txt
Build the lineup optimizer feature.
```

Use a context-aware prompt:

```txt
Read PRODUCT.md, ARCHITECTURE.md, docs/API.md, and docs/GRIDIRON_GRADE_ENGINE.md.

Then create an implementation plan for improving the Start/Sit Optimizer.
Do not write code yet.
```

This gives you a plan before Copilot starts modifying files.

## 2. Use the prompt files for repeatable tasks

Prompt files are located here:

```txt
.github/prompts/
```

Use them to standardize repeated tasks such as planning, reviewing, and testing.

Examples:

```txt
Use the feature-plan prompt to plan adding real NFL player projections.
```

```txt
Use the code-review prompt to review the changes in this branch.
```

```txt
Use the test-strategy prompt to propose tests for the grading engine.
```

## 3. Use the agent files for different development modes

Agent files are located here:

```txt
.github/agents/
```

They help Copilot behave differently depending on the task.

### Planning agent

Use this when you want Copilot to analyze first and avoid editing code too early.

```txt
Use the planning agent to analyze this feature:
"Add player projection data to the grading engine."

Return a plan only. Do not modify files.
```

### TDD agent

Use this when you want tests before implementation.

```txt
Use the TDD agent to implement the grade calculation rules from docs/GRIDIRON_GRADE_ENGINE.md.

Write tests first, then implementation.
```

### Review agent

Use this after a feature is implemented.

```txt
Use the review agent to inspect this branch against ARCHITECTURE.md and CONTRIBUTING.md.
```

## 4. Keep the documentation updated

These files should change as the project changes.

| When this changes                | Update this file                  |
| -------------------------------- | --------------------------------- |
| Product direction                | `PRODUCT.md`                      |
| Frontend or backend architecture | `ARCHITECTURE.md`                 |
| API routes                       | `docs/API.md`                     |
| Database tables or relationships | `docs/DATA_MODEL.md`              |
| Grade calculation logic          | `docs/GRIDIRON_GRADE_ENGINE.md`   |
| Local setup process              | `docs/SETUP.md`                   |
| Coding style or workflow         | `CONTRIBUTING.md`                 |
| Testing strategy                 | `TESTING.md`                      |
| Copilot behavior                 | `.github/copilot-instructions.md` |

At the end of a feature, ask Copilot:

```txt
Based on the changes in this branch, tell me which documentation files should be updated.
Do not edit files yet.
```

## Recommended workflow

```txt
1. Ask Copilot to read the relevant docs.
2. Ask for a plan.
3. Review the plan.
4. Ask Copilot to implement.
5. Ask Copilot to write or update tests.
6. Ask Copilot to review against the docs.
7. Update the docs if the code changed the architecture.
```

## Main goal

The purpose of these files is simple:

> Copilot should stop guessing how Gridiron Labs works and start following the project rules you defined.
