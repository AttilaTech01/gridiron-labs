# Project Specification: Gridiron Labs (MVP Phase)

## 1. Project Vision

**Gridiron Labs** is a fantasy football companion app designed for "Power Users" and "Busy Managers." It translates complex, high-frequency data into simple, actionable recommendations (Start/Sit, Trades, and Diagnostics).

## 2. Core Philosophy

- **Progressive Disclosure:** Simple, color-coded recommendations for the "Busy Manager," with expandable raw data (Target Share, Volatility) for the "Power User."
- **Actionable Analytics:** Moves beyond basic projections to focus on Volume (Target Share) and Environment (Matchup Strength).

## 3. Feature Roadmap (Priority Order)

### Phase 1: The "Start/Sit" Optimizer (Current Focus)

This is a weekly win engine for the user. It needs to give an answer in five seconds but provide five minutes of data if the user wants it. It answers the question: "Considering the current situation, my league setup and my lineup, how can I optimize my start/sit decision to make sure I have to most chances to win this week."

1. The "Five Second" Answer (The Hook)
   To achieve this, your UI needs a Single Score of Truth. \* The "Gridiron Grade": Instead of showing projected points (which they can get anywhere), show a "Confidence Score" (0–100).

The Visual: A simple Green/Yellow/Red card for every player on their roster.

Why it works: It satisfies the "Busy Manager" who needs to set a lineup while walking into a meeting or during a commercial break.

2. The "Five Minute" Data (The Depth)
   This is where you build loyalty with the "Power User." When they click that Green/Yellow/Red card, they should see exactly why the engine made that choice.

The "Volume" Tab: Show the Target Share trends we discussed—is the player's role growing?

The "Environment" Tab: Show the Matchup Strength—specific defensive weaknesses (e.g., "The opponent allows the most yards to slot receivers").

The "Chaos" Tab: Show the Volatility/Ceiling—"This player has a low floor but a massive ceiling due to deep-ball targets."

#### Phase 1: Features

- **Logic:** A decision matrix balancing **Target Share** (Volume) and **Matchup Strength** (Environment).
- **Volatility Metric:** A "Chaos" score identifying high-ceiling "Boom/Bust" players based on red-zone usage and deep-ball targets.
- **Predictive Layer:** Integration of injury risk profiles into the weekly win probability.

1. User searches and adds players to their roster
2. User sets their weekly lineup (marks starters vs bench)
3. Gridiron Labs grades each player and suggests optimizations

#### Phase 1: UI/UX Details

- **The Busy Manager View:** A simple "Chaos Recommendation"—a percentage-based win probability for each lineup combination. A "Volume Score" (e.g., 9/10). This tells them the player is a focal point of the offense and is a "safe" start. A color-coded "Matchup Grade" (Green/Yellow/Red).
- **The Power User View:** An expandable "Volatility Heatmap." Instead of just one projected score, you show a range (Foor: What happens if this player gets zero "Chaos" plays (long catches/TDs), Ceiling: What happens if the matchup follows a high-volatility script). The raw percentage of team targets over the last three weeks compared to the season average. This helps them identify if a player’s role is growing or shrinking. Specific defensive vulnerabilities. For example: "The opponent's slot cornerback allows a 120.0 passer rating; your WR plays 80% of snaps in the slot."
- **The Competitive Edge:** Integrating Predictive Injury Modeling. If a player is "Questionable," the tool shouldn't just say "check news"; it should show how your win probability drops if they are a late scratch. You can highlight "High-Value Targets"—targets in the red zone or deep passes (20+ yards). This feeds your "Chaos Scoring" logic by identifying players with high "explosive" potential. Account for defensive injuries. If a star cornerback is out, the "Strength of Matchup" should automatically shift in real-time.

### Phase 2: The Trade Architect - To refine

- **Mechanism:** Monte Carlo simulations to predict the impact of a trade on season-long playoff probability. It runs thousands of scenarios for the rest of the season to see how a trade changes the user's chance of making the playoffs.
- **Key Metric:** Playoff Strength of Schedule (Weeks 15–17).

### Phase 3: Post-Game Autopsy (Diagnostic) - To refine

- **Logic:** Expected Points (xP) vs. Actual Points to identify "Bad Luck" scenarios and "Buy Low" candidates.

## 4. Technical Requirements Suggestions

- **Data Strategy:** \*
  - **Primary Source:** Free/Scraped data (e.g., `nfl_data_py`, Sleeper API, ESPN or NFL APIs).
  - **Granularity:** Requires play-by-play data to calculate Target Share and efficiency metrics.
- **Suggested Tech Stack:** \*
  - **Frontend:** React, TanStack Query, Zustand, Shadcn/ui, React Router.
  - **Backend:** Python (FastAPI), SQLAlchemy and Alembic.
  - **Database:** PostgreSQL.
  - **Authentication:** Clerk or Auth0.
  - **Caching:** Redis for live score updates and simulation results.
- **Suggested Repository Architecture:** \* One monorepo with shared types between frontend and backend contracts (simpler PR mechanics, CI/CD and versioning).

## 5. Data Logic for AI Implementation

- **Target Share Calculation:** `(Player Targets / Total Team Pass Attempts)` per game/season.
- **Matchup Grade:** Weighted average of opponent's points allowed per position and efficiency metrics (e.g., Yards per Target allowed).
- **Win Probability:** A simplified simulation comparing the "Standard" projected score of the user's lineup against the opponent's projected score.

# Work in progress: MVP

## Done

[X] Monorepo structure
[X] Frontend — Vite + React + TypeScript + Tailwind + shadcn/ui
[X] Backend — FastAPI running on port 8000
[X] Database — PostgreSQL with all tables created
[X] Redis — running in Docker
[X] Database viewer — SQLTools connected

## Next steps

1. Data Pipeline
   Before building any UI, we need real data flowing in. This is the foundation of every feature.

Connect to the Sleeper API (free, no key needed)
Write ingestion scripts that pull player stats and store them in the DB
Build your Target Share calculation logic in Python
Cache aggressively with Redis from day one

Get comfortable with the shape of the data before trying to display it.

2. The Gridiron Grade
   Build the actual core logic — the thing that makes the app worth using.

Implement the Matchup Grade scoring
Implement the Chaos Score
Combine into the Gridiron Grade (0-100)
Expose it via a FastAPI endpoint

Test this heavily with real data before touching the UI.

3. The UI
   Only now do we build the frontend. We'll know exactly what data we have and what shape it comes in.

Set up TanStack Query to hit your backend
Build the player card component (Green/Yellow/Red)
Build the expandable detail view (Volume / Environment / Chaos tabs)
Wire up Zustand for lineup selection state
