"""
Gridiron Grade Engine
---------------------
Computes a 0-100 confidence score for a player.

Score components:
  - Opportunity Score  (40%): Volume / role security
  - Matchup Score      (40%): Opponent defensive weakness vs this position
  - Chaos Score        (20%): Boom/bust potential

Opportunity share is split into rush and receiving to account for
multi-dimensional players (receiving RBs, rushing QBs, etc).

Position weights:
  QB  → pass 85% / rush 15%
  RB  → rush 70% / receiving 30%
  WR  → receiving 95% / rush 5%
  TE  → receiving 95% / rush 5%
  K   → excluded for MVP
"""

from dataclasses import dataclass
from typing import TypedDict
from app.schemas.enums import MatchupGrade, OpportunityTrend

# Weights for rush vs receiving opportunity by position
OPPORTUNITY_WEIGHTS: dict[str, tuple[float, float]] = {
    # rush, receiving
    "QB": (0.15, 0.85),
    "RB": (0.70, 0.30),
    "WR": (0.05, 0.95),
    "TE": (0.05, 0.95),
}

# Elite opportunity share threshold by position
ELITE_RUSH_SHARE: dict[str, float] = {
    "QB": 0.15,   # Mobile QB gets ~15% of team rush attempts
    "RB": 0.65,   # Featured back gets ~65% of carries
    "WR": 0.02,
    "TE": 0.01,
}

ELITE_RECEIVING_SHARE: dict[str, float] = {
    "QB": 1.00,
    "RB": 0.12,   # Pass-catching RB gets ~12% of targets
    "WR": 0.30,
    "TE": 0.20,
}

# Elite red zone opportunity share by position
ELITE_RZ_RUSH_SHARE: dict[str, float] = {
    "QB": 0.20,
    "RB": 0.50,
    "WR": 0.02,
    "TE": 0.02,
}

ELITE_RZ_RECEIVING_SHARE: dict[str, float] = {
    "QB": 1.00,
    "RB": 0.15,
    "WR": 0.30,
    "TE": 0.30,
}

# Elite explosive play share by position
ELITE_EXPLOSIVE_RUSH_SHARE: dict[str, float] = {
    "QB": 0.05,
    "RB": 0.15,   # 10+ yard carries
    "WR": 0.01,
    "TE": 0.01,
}

ELITE_EXPLOSIVE_RECEIVING_SHARE: dict[str, float] = {
    "QB": 0.10,
    "RB": 0.02,
    "WR": 0.15,   # Deep targets (20+ yards)
    "TE": 0.10,
}

class GridironGradeResult(TypedDict):
    gridiron_grade: int
    matchup_grade: MatchupGrade
    chaos_score: int
    opportunity_trend: OpportunityTrend

@dataclass
class GradeInput:
    position: str

    # Volume — split by rush and receiving
    rush_opportunity_share: float              # carries / team rush attempts
    receiving_opportunity_share: float         # targets / team targets
    season_rush_opportunity_share: float       # season average
    season_receiving_opportunity_share: float  # season average

    # Matchup
    opponent_rank_points_allowed: int               # 1-32, higher is better (20% matchup score)
    opponent_rank_yards_allowed: int                # 1-32, higher is better (10% matchup score)
    opponent_rank_vs_position: int                  # 1-32, higher is better (40% matchup score)
    opponent_rank_yards_allowed_vs_position: int    # 1-32, higher is better (30% matchup score)

    # Chaos — split by rush and receiving
    red_zone_rush_share: float         # RZ carries / team RZ rush attempts
    red_zone_receiving_share: float    # RZ targets / team RZ targets
    explosive_rush_share: float        # 10+ yard carries / team rush attempts
    explosive_receiving_share: float   # 20+ yard targets / team targets

    injury_modifier: float = 1.0        # 1.0 = healthy, 0.7 = questionable, ...


def compute_opportunity_score(inputs: GradeInput) -> int:
    position = inputs.position
    rush_weight, rec_weight = OPPORTUNITY_WEIGHTS.get(position, (0.50, 0.50)) # Default to 50/50 if position not found

    elite_rush = ELITE_RUSH_SHARE.get(position, 0.25)
    elite_rec = ELITE_RECEIVING_SHARE.get(position, 0.25)

    rush_score = min(inputs.rush_opportunity_share / elite_rush, 1.0) * 100
    rec_score = min(inputs.receiving_opportunity_share / elite_rec, 1.0) * 100

    base = (rush_score * rush_weight) + (rec_score * rec_weight)

    # Trend bonus — if either dimension is growing
    rush_growing = (
        inputs.rush_opportunity_share > inputs.season_rush_opportunity_share * 1.1
    )
    rec_growing = (
        inputs.receiving_opportunity_share > inputs.season_receiving_opportunity_share * 1.1
    )
    trend_bonus = 10 if (rush_growing or rec_growing) else 0

    return min(int(base + trend_bonus), 100)


def compute_opportunity_trend(inputs: GradeInput) -> OpportunityTrend:
    rush_growing = (
        inputs.rush_opportunity_share > inputs.season_rush_opportunity_share * 1.1
    )
    rec_growing = (
        inputs.receiving_opportunity_share > inputs.season_receiving_opportunity_share * 1.1
    )
    rush_shrinking = (
        inputs.rush_opportunity_share < inputs.season_rush_opportunity_share * 0.9
    )
    rec_shrinking = (
        inputs.receiving_opportunity_share < inputs.season_receiving_opportunity_share * 0.9
    )

    if rush_growing or rec_growing:
        return "GROWING"
    elif rush_shrinking and rec_shrinking:
        return "SHRINKING"
    return "STABLE"

    
def compute_matchup_score(
    rank_points_allowed: int,
    rank_yards_allowed: int,
    rank_vs_position: int,
    rank_yards_allowed_vs_position: int) -> int:
    # Normalize each rank to 0-100 (rank 32 = 100, rank 1 = ~3)
    def normalize(rank: int) -> float:
        return (rank / 32) * 100
    
    score = (
        normalize(rank_points_allowed) * 0.2 +
        normalize(rank_yards_allowed) * 0.1 +
        normalize(rank_vs_position) * 0.4 +
        normalize(rank_yards_allowed_vs_position) * 0.3
    )

    return min(int(score), 100)


def compute_matchup_grade(matchup_score: int) -> MatchupGrade:
    if matchup_score >= 65:
        return "GREEN"
    elif matchup_score >= 40:
        return "YELLOW"
    return "RED"
    
    
def compute_chaos_score(inputs: GradeInput) -> int:
    position = inputs.position
    rush_weight, rec_weight = OPPORTUNITY_WEIGHTS.get(position, (0.50, 0.50))

    elite_rz_rush = ELITE_RZ_RUSH_SHARE.get(position, 0.30)
    elite_rz_rec = ELITE_RZ_RECEIVING_SHARE.get(position, 0.25)
    elite_exp_rush = ELITE_EXPLOSIVE_RUSH_SHARE.get(position, 0.05)
    elite_exp_rec = ELITE_EXPLOSIVE_RECEIVING_SHARE.get(position, 0.10)

    rz_score = (
        min(inputs.red_zone_rush_share / elite_rz_rush, 1.0) * rush_weight +
        min(inputs.red_zone_receiving_share / elite_rz_rec, 1.0) * rec_weight
    ) * 50

    explosive_score = (
        min(inputs.explosive_rush_share / elite_exp_rush, 1.0) * rush_weight +
        min(inputs.explosive_receiving_share / elite_exp_rec, 1.0) * rec_weight
    ) * 50

    return min(int(rz_score + explosive_score), 100)
    
    
def compute_gridiron_grade(inputs: GradeInput) -> GridironGradeResult:
    opportunity_score = compute_opportunity_score(inputs)
    matchup_score = compute_matchup_score(inputs.opponent_rank_points_allowed, inputs.opponent_rank_yards_allowed, inputs.opponent_rank_vs_position, inputs.opponent_rank_yards_allowed_vs_position)
    chaos_score = compute_chaos_score(inputs)

    raw_grade = (
        (opportunity_score * 0.40) + 
        (matchup_score * 0.40) + 
        (chaos_score * 0.20) 
    )
    final_grade = int(raw_grade * inputs.injury_modifier)

    result: GridironGradeResult = {
        "gridiron_grade": min(final_grade, 100),
        "matchup_grade": compute_matchup_grade(matchup_score),
        "chaos_score": chaos_score,
        "opportunity_trend": compute_opportunity_trend(inputs),
    }
    return result