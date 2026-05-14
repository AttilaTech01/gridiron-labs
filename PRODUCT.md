# Gridiron Labs Product Context

## One-line product definition

Gridiron Labs is a fantasy football companion app that turns complex NFL data into simple, actionable start/sit decisions for weekly fantasy football lineup management.

## Product promise

Give the user a useful answer in five seconds, then provide deeper evidence in five minutes when they want to understand the reasoning.

The core user-facing promise is:

> Build your roster, set your lineup, and let Gridiron Labs highlight who is safe, risky, or explosive this week.

## Target users

### Busy Manager

The Busy Manager wants to set a lineup quickly without studying projections, advanced stats, injury reports, matchup data, and defensive tendencies manually.

They need:

- one clear recommendation;
- color-coded confidence;
- minimal friction;
- fast roster and lineup management;
- warnings for risky decisions.

### Power User

The Power User wants the reason behind the recommendation and wants to see whether the model is relying on volume, matchup, volatility, or injury context.

They need:

- detailed breakdowns;
- target/opportunity trends;
- matchup explanation;
- volatility and ceiling indicators;
- transparent formulas and assumptions.

## Core philosophy

### Progressive disclosure

Show the simple answer first. Make deeper analytics available only when the user asks for it.

A player card should eventually support two levels:

1. **Five-second view:** Gridiron Grade, matchup color, chaos score, start/sit recommendation.
2. **Five-minute view:** volume trend, matchup reasoning, red-zone involvement, explosive-play profile, injury sensitivity, and data source context.

### Actionable analytics

The app should not only mirror generic projected fantasy points. It should convert player context into decisions.

The most important current concepts are:

- **Gridiron Grade:** 0-100 confidence score.
- **Opportunity / Volume:** how central the player is to the offense.
- **Matchup Grade:** green/yellow/red view of defensive matchup quality.
- **Chaos Score:** boom/bust or explosive-play potential.
- **Opportunity Trend:** growing, shrinking, or stable role.

## MVP scope

The current MVP is the **Start/Sit Optimizer**.

### Current user workflow

1. User searches NFL players.
2. User filters players by position and/or name.
3. User adds/removes players from their roster.
4. User assigns rostered players to lineup slots.
5. User saves the lineup.
6. Backend returns Gridiron Grade, Matchup Grade, Chaos Score, and Opportunity Trend for each player.

### Current MVP screens

- **Players page:** search/filter players and manage roster membership.
- **Lineup page:** assign each roster player to a slot and save the lineup.

### Current MVP backend capabilities

- Player listing with search and position filter.
- Roster add/remove.
- Lineup get/set.
- Deterministic mock grading per player.
- PostgreSQL models and initial Alembic migration.
- Sleeper API seed script for player data.

## Out of scope for current MVP

These are planned or implied by the project vision, but are not implemented in the codebase:

- Clerk authentication and per-user auth resolution.
- Real fantasy league integration.
- Real weekly matchup data.
- Real play-by-play and target-share calculations.
- Injury data integration.
- Win probability simulation.
- Trade Architect.
- Post-Game Autopsy.
- Production-grade UI polish.
- End-to-end and unit tests.

## Product roadmap

### Phase 1 — Start/Sit Optimizer

Primary question:

> Considering my roster, league setup, and weekly lineup, who gives me the best chance to win this week?

Core deliverables:

- roster management;
- lineup management;
- Gridiron Grade;
- Matchup Grade;
- Chaos Score;
- opportunity trend;
- expandable reasoning view;
- real data pipeline replacing mock grades;
- authentication.

### Phase 2 — Trade Architect

Primary question:

> How does this trade affect my playoff odds and roster strength over the rest of the season?

Likely deliverables:

- trade input flow;
- rest-of-season simulation;
- playoff schedule weighting;
- Monte Carlo-style scenarios;
- roster strength delta before/after trade.

### Phase 3 — Post-Game Autopsy

Primary question:

> What happened this week, what was bad luck, and what should I do next?

Likely deliverables:

- expected points vs actual points;
- buy-low candidates;
- role change detection;
- usage trend diagnostics;
- weekly learning loop.

## Product decision principles

When adding features, prioritize in this order:

1. Help the user make a weekly lineup decision faster.
2. Explain the recommendation in plain language.
3. Preserve trust by exposing assumptions and data limitations.
4. Avoid adding generic fantasy football data unless it changes the recommendation.
5. Design first for the Busy Manager, then reveal depth for the Power User.

## MVP success criteria

The MVP is successful when a user can:

- build a roster;
- save a lineup;
- understand which players are safer or riskier;
- see why a recommendation was made;
- trust that the app is not randomly assigning grades.

## Important product caution

The current grading values are mock-generated. Any UI copy must avoid implying that current grades are powered by live NFL data until the real data pipeline is implemented.
