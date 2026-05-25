# Gridiron Labs: Design & Branding Decisions

## 1. Core Visual Identity

- **Theme:** "Sober Analytics." A dark, professional, and data-centric aesthetic that emphasizes a "Labs" environment.
- **Primary Background:** Deep, desaturated tones (Slate/Charcoal/Zinc-950) to minimize eye strain and establish a "terminal" feel.
- **Brand Accent:** **Teal-800** (`#115e59`). Used for interactive elements, side-drawer headers, and subtle UI highlights to distinguish app controls from player data.

## 2. Color-Coded Indicators (The "Pop")

To support the "Five-Second View" for the Busy Manager, bright colors are reserved strictly for data visualization:

- **Safe/Positive (Gridiron/Matchup Grades):** Neon Green.
- **Neutral/Caution:** Vivid Yellow.
- **Risky/Negative:** Bright Crimson/Red.
- **Chaos Score (Volatility):** Electric Purple. Chosen to stand outside the standard traffic-light spectrum to represent "boom/bust" potential.

## 3. Typography

- **UI Text:** Clean sans-serif (e.g., Inter or Geist) for readability in menus and labels.
- **Data & Analytics:** Monospaced font (e.g., JetBrains Mono) for Gridiron Grades, Chaos Scores, and numerical stats to reinforce the analytics vibe.

## 4. Layout & Navigation

- **Structure:** A merged "Control Center" dashboard (Single-Page App approach) replacing the separate Players and Lineup pages.
- **Three-Column Layout:**
  1.  **Left Sidebar:** Player Pool with search and position filters.
  2.  **Center Column:** Active Lineup slots (Started players).
  3.  **Right Column:** Roster/Bench view.
- **Player Cards:** Horizontal "Strip" cards designed for high density (seeing the whole lineup without scrolling) while maintaining breathing room via subtle borders.

## 5. Interaction Patterns

- **The "Five-Minute View" (Deep Dive):** Clicking a player card opens a **Modal**. This provides a focused, full-screen environment for the Power User to study detailed evidence and trends.
- **Roster Placement:** Adding a player from the sidebar triggers a **Side-Drawer**. This guides the user to select a specific roster slot, providing clear "Actionable Analytics".
- **Interactive Controls:** Buttons and active tabs will use **Teal-800** or neutral grays to avoid visual competition with performance grades.
