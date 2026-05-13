export type Position = "QB" | "RB" | "WR" | "TE";
export type MatchupGrade = "GREEN" | "YELLOW" | "RED";
export type OpportunityTrend = "GROWING" | "SHRINKING" | "STABLE";

export interface Player {
  id: number;
  sleeper_id: string;
  full_name: string;
  position: Position;
  team: string | null;
  status: string;
  gridiron_grade: number;
  matchup_grade: MatchupGrade;
  chaos_score: number;
  opportunity_trend: OpportunityTrend;
}
