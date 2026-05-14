# Gridiron Labs

Gridiron Labs is a fantasy football decision-support application focused on helping users make better weekly lineup decisions.

## Project Purpose

The goal of Gridiron Labs is to provide clear, explainable fantasy football recommendations instead of black-box suggestions.

The application should help users answer questions like:

- Which player should I start this week?
- How does one player compare to another?
- Why did a player receive a better grade?
- What roster or lineup decisions need attention?

## Current MVP Scope

The current MVP centers on a **Start/Sit Optimizer** that lets a user manage players, view a roster, and compare lineup options using a deterministic grading system. The project is structured as a modern full-stack application with a React/Vite/TypeScript frontend and a FastAPI backend backed by PostgreSQL and Redis.

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Component-based UI structure
- Tailwind CSS + shadcn/ui

### Backend

- FastAPI
- Python
- PostgreSQL
- Redis
- Alembic migrations

### Development Context

The application currently uses development-friendly assumptions, including mock grading logic and a development user context. These choices are appropriate for the MVP but should be revisited before production use.

## Repository Documentation

This repository includes a documentation and Copilot context pack designed to help both developers and AI coding assistants understand the project.

### Root-Level Documentation

| File              | Description                                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| `PRODUCT.md`      | Explains the product vision, user goals, MVP scope, and future direction of Gridiron Labs.                   |
| `ARCHITECTURE.md` | Describes the high-level system architecture, including frontend, backend, database, and service boundaries. |
| `CONTRIBUTING.md` | Defines development conventions, coding expectations, branch workflow, and contribution guidelines.          |
| `TESTING.md`      | Describes the recommended testing strategy for frontend, backend, API, and grading logic.                    |

### `docs/` Directory

| File                                 | Description                                                                                                        |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `docs/API.md`                        | Documents the current API structure, route responsibilities, and expected backend behavior.                        |
| `docs/DATA_MODEL.md`                 | Describes the main data entities, relationships, and persistence model used by the application.                    |
| `docs/GRIDIRON_GRADE_ENGINE.md`      | Explains the grading engine concept, current mock logic, expected evolution, and rules for future scoring changes. |
| `docs/SETUP.md`                      | Provides local setup guidance for installing dependencies, configuring services, and running the project.          |
| `docs/NEXT_STEPS.md`                 | Lists recommended next improvements and technical priorities for moving the MVP forward.                           |
| `docs/HOW_TO_USE_PROJECT_CONTEXT.md` | Explains how to use the documentation pack with GitHub Copilot and VS Code.                                        |

### `.github/` Copilot Context Files

| File                              | Description                                                                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `.github/copilot-instructions.md` | Provides persistent project instructions for GitHub Copilot so AI-generated code follows the project’s architecture and conventions. |

### `.github/agents/` Directory

| File                                     | Description                                                                                                                    |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `.github/agents/implementation.agent.md` | Defines a implementation-focus agent that should apply small changes to the codebase.                                          |
| `.github/agents/plan.agent.md`           | Defines a planning-focused Copilot agent that should analyze features and produce implementation plans before code is written. |
| `.github/agents/tdd.agent.md`            | Defines a test-driven development agent that should write or update tests before implementing feature logic.                   |
| `.github/agents/reviewer.agent.md`       | Defines a review-focused agent that checks changes against the architecture, conventions, and project goals.                   |
