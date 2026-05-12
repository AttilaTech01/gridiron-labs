"""
Mock grade generator
--------------------
Generates realistic-looking grade inputs per position for testing.
Replace with real data source translators when ready.
"""

import random
from app.services.gridiron_grade import GradeInput, compute_gridiron_grade, GridironGradeResult

# Realistic rush opportunity share ranges by position
RUSH_OPPORTUNITY_RANGES: dict[str, tuple[float, float]] = {
    "QB": (0.02, 0.25),
    "RB": (0.10, 0.85),
    "WR": (0.00, 0.05),
    "TE": (0.00, 0.03),
}

# Realistic receiving opportunity share ranges by position
RECEIVING_OPPORTUNITY_RANGES: dict[str, tuple[float, float]] = {
    "QB": (0.90, 1.00),
    "RB": (0.01, 0.25),
    "WR": (0.05, 0.35),
    "TE": (0.05, 0.30),
}

def generate_mock_input(player_id: int, position: str) -> GradeInput:
    """
    Deterministic mock inputs based on player_id —
    grades are consistent across requests for the same player.
    """
    rng = random.Random(player_id)

    rush_min, rush_max = RUSH_OPPORTUNITY_RANGES.get(position, (0.0, 0.15))
    rec_min, rec_max = RECEIVING_OPPORTUNITY_RANGES.get(position, (0.05, 0.20))

    recent_rush = rng.uniform(rush_min, rush_max)
    recent_rec = rng.uniform(rec_min, rec_max)
    season_rush = recent_rush * rng.uniform(0.85, 1.15)
    season_rec = recent_rec * rng.uniform(0.85, 1.15)

    return GradeInput(
        position=position,
        rush_opportunity_share=recent_rush,
        receiving_opportunity_share=recent_rec,
        season_rush_opportunity_share=season_rush,
        season_receiving_opportunity_share=season_rec,
        opponent_rank_points_allowed=rng.randint(1, 32),
        opponent_rank_yards_allowed=rng.randint(1, 32),
        opponent_rank_vs_position=rng.randint(1, 32),
        opponent_rank_yards_allowed_vs_position=rng.randint(1, 32),
        red_zone_rush_share=rng.uniform(0.0, 0.35),
        red_zone_receiving_share=rng.uniform(0.0, 0.25),
        explosive_rush_share=rng.uniform(0.0, 0.15),
        explosive_receiving_share=rng.uniform(0.0, 0.20),
        injury_modifier=rng.choice([1.0, 1.0, 1.0, 0.7]),
    )

def get_mock_grade(player_id: int, position: str) -> GridironGradeResult:
    inputs = generate_mock_input(player_id, position)
    return compute_gridiron_grade(inputs)