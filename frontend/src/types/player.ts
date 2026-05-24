export interface Player {
  id: number
  sleeper_id: string
  full_name: string
  position: string
  team: string | null
  status: string
  gridiron_grade: number
  matchup_grade: string
  chaos_score: number
  opportunity_trend: string
}
