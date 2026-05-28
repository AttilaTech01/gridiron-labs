from typing import Any
from app.services.gridiron_grade import (
    GradeInput,
    compute_gridiron_grade,
    compute_matchup_grade,
    compute_opportunity_trend,
)


def make_input(**overrides: Any) -> GradeInput:
    """Base GradeInput with sensible defaults. Override any field as needed."""
    defaults: dict[str, Any] = {
        "position": "WR",
        "rush_opportunity_share": 0.02,
        "receiving_opportunity_share": 0.25,
        "season_rush_opportunity_share": 0.02,
        "season_receiving_opportunity_share": 0.25,
        "opponent_rank_points_allowed": 16,
        "opponent_rank_yards_allowed": 16,
        "opponent_rank_vs_position": 16,
        "opponent_rank_yards_allowed_vs_position": 16,
        "red_zone_rush_share": 0.05,
        "red_zone_receiving_share": 0.15,
        "explosive_rush_share": 0.05,
        "explosive_receiving_share": 0.10,
        "injury_modifier": 1.0,
    }
    defaults.update(overrides)
    return GradeInput(**defaults)


# --- compute_matchup_grade ---

def test_matchup_grade_green():
    assert compute_matchup_grade(65) == "GREEN"
    assert compute_matchup_grade(100) == "GREEN"


def test_matchup_grade_yellow():
    assert compute_matchup_grade(40) == "YELLOW"
    assert compute_matchup_grade(64) == "YELLOW"


def test_matchup_grade_red():
    assert compute_matchup_grade(0) == "RED"
    assert compute_matchup_grade(39) == "RED"


# --- compute_opportunity_trend ---

def test_opportunity_trend_growing():
    inputs = make_input(
        receiving_opportunity_share=0.30,
        season_receiving_opportunity_share=0.20,
    )
    assert compute_opportunity_trend(inputs) == "GROWING"


def test_opportunity_trend_shrinking():
    inputs = make_input(
        rush_opportunity_share=0.01,
        receiving_opportunity_share=0.15,
        season_rush_opportunity_share=0.02,
        season_receiving_opportunity_share=0.25,
    )
    assert compute_opportunity_trend(inputs) == "SHRINKING"


def test_opportunity_trend_stable():
    inputs = make_input(
        receiving_opportunity_share=0.25,
        season_receiving_opportunity_share=0.25,
    )
    assert compute_opportunity_trend(inputs) == "STABLE"


# --- compute_gridiron_grade ---

def test_gridiron_grade_never_exceeds_100():
    inputs = make_input(
        receiving_opportunity_share=1.0,
        opponent_rank_vs_position=32,
        opponent_rank_yards_allowed_vs_position=32,
        opponent_rank_points_allowed=32,
        opponent_rank_yards_allowed=32,
        red_zone_receiving_share=1.0,
        explosive_receiving_share=1.0,
    )
    result = compute_gridiron_grade(inputs)
    assert result["gridiron_grade"] <= 100


def test_gridiron_grade_never_below_zero():
    inputs = make_input(
        receiving_opportunity_share=0.0,
        opponent_rank_vs_position=1,
        opponent_rank_yards_allowed_vs_position=1,
        opponent_rank_points_allowed=1,
        opponent_rank_yards_allowed=1,
        red_zone_receiving_share=0.0,
        explosive_receiving_share=0.0,
    )
    result = compute_gridiron_grade(inputs)
    assert result["gridiron_grade"] >= 0


def test_gridiron_grade_injury_modifier_reduces_grade():
    healthy = compute_gridiron_grade(make_input(injury_modifier=1.0))
    questionable = compute_gridiron_grade(make_input(injury_modifier=0.7))
    assert questionable["gridiron_grade"] < healthy["gridiron_grade"]


def test_gridiron_grade_qb_scores_higher_with_high_snap_share():
    qb = make_input(
        position="QB",
        rush_opportunity_share=0.08,
        receiving_opportunity_share=0.95,
        season_rush_opportunity_share=0.08,
        season_receiving_opportunity_share=0.95,
    )
    rb = make_input(
        position="RB",
        rush_opportunity_share=0.08,
        receiving_opportunity_share=0.95,
        season_rush_opportunity_share=0.08,
        season_receiving_opportunity_share=0.95,
    )
    qb_result = compute_gridiron_grade(qb)
    rb_result = compute_gridiron_grade(rb)
    assert qb_result["gridiron_grade"] > rb_result["gridiron_grade"]


def test_gridiron_grade_result_has_all_fields():
    result = compute_gridiron_grade(make_input())
    assert "gridiron_grade" in result
    assert "matchup_grade" in result
    assert "chaos_score" in result
    assert "opportunity_trend" in result