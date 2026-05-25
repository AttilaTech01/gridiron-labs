# Gridiron Grade Engine

## Purpose

The Gridiron Grade Engine converts football context into a 0-100 confidence score for start/sit decisions.

It is designed to support the product promise:

> Give the user a simple answer quickly, with enough underlying data to explain why.

## Current implementation files

```txt
backend/app/services/gridiron_grade.py
backend/app/services/mock_grades.py
```

## Current output

The engine returns:

```ts
type GridironGradeResult = {
  gridiron_grade: number;
  matchup_grade: "GREEN" | "YELLOW" | "RED";
  chaos_score: number;
  opportunity_trend: "GROWING" | "SHRINKING" | "STABLE";
};
```

The Python code uses a `TypedDict` for this structure.

## Input model

The engine expects a `GradeInput` with four broad categories:

1. Position
2. Volume / opportunity
3. Matchup rankings
4. Chaos / volatility indicators
5. Injury modifier

Important fields:

```py
@dataclass
class GradeInput:
    position: str
    rush_opportunity_share: float
    receiving_opportunity_share: float
    season_rush_opportunity_share: float
    season_receiving_opportunity_share: float
    opponent_rank_points_allowed: int
    opponent_rank_yards_allowed: int
    opponent_rank_vs_position: int
    opponent_rank_yards_allowed_vs_position: int
    red_zone_rush_share: float
    red_zone_receiving_share: float
    explosive_rush_share: float
    explosive_receiving_share: float
    injury_modifier: float = 1.0
```

## Score composition

The final grade is calculated from:

| Component | Weight | Meaning |
|---|---:|---|
| Opportunity Score | 40% | Role security and offensive volume. |
| Matchup Score | 40% | Quality of the defensive matchup. |
| Chaos Score | 20% | Boom/bust upside through red-zone and explosive-play usage. |

Formula:

```txt
raw_grade = opportunity_score * 0.40 + matchup_score * 0.40 + chaos_score * 0.20
final_grade = raw_grade * injury_modifier
```

The final grade is capped at 100.

## Opportunity Score

Opportunity is position-aware.

Current rush/receiving weights:

| Position | Rush weight | Receiving/pass weight |
|---|---:|---:|
| QB | 15% | 85% |
| RB | 70% | 30% |
| WR | 5% | 95% |
| TE | 5% | 95% |

The engine compares recent opportunity share against elite thresholds for the player's position.

It also applies a trend bonus when recent rush or receiving opportunity is more than 10% above the season average.

## Opportunity Trend

Current trend rules:

- `GROWING` if rush or receiving opportunity is more than 10% above season average.
- `SHRINKING` if both rush and receiving opportunity are more than 10% below season average.
- `STABLE` otherwise.

## Matchup Score

The matchup score normalizes defensive ranking inputs where higher ranks are better for the offensive player.

Current weighting:

| Matchup input | Weight |
|---|---:|
| Opponent rank by points allowed | 20% |
| Opponent rank by yards allowed | 10% |
| Opponent rank vs position | 40% |
| Opponent rank yards allowed vs position | 30% |

Rank normalization:

```txt
normalized = rank / 32 * 100
```

## Matchup Grade

Current thresholds:

| Score | Grade |
|---:|---|
| 65+ | GREEN |
| 40-64 | YELLOW |
| 0-39 | RED |

## Chaos Score

Chaos Score is a volatility/upside metric.

It combines:

- red-zone rush share;
- red-zone receiving share;
- explosive rush share;
- explosive receiving share.

The engine compares those shares against position-specific elite thresholds and applies the same rush/receiving position weights used for opportunity.

Interpretation:

- High chaos means the player may have more touchdown or explosive-play upside.
- High chaos does not necessarily mean safe.
- UI copy should distinguish upside from floor.

## Injury modifier

`injury_modifier` defaults to `1.0`.

Current mock generator sometimes uses `0.7`, which reduces the final grade.

Future real-data implementation should map injury statuses explicitly, for example:

| Status | Possible modifier |
|---|---:|
| Healthy | 1.0 |
| Questionable | 0.7-0.9 |
| Doubtful | 0.2-0.5 |
| Out | 0.0 |

These values should be validated before production use.

## Mock grade generator

`mock_grades.py` creates deterministic pseudo-random `GradeInput` values by seeding `random.Random(player_id)`.

This means:

- the same player gets the same grade across requests;
- the frontend can be developed against stable values;
- the values are not real football projections.

Do not describe mock grades as live data or as final recommendations.

## Replacement strategy for real data

When adding real football data, preserve the engine boundary:

```txt
raw provider data -> translator/normalizer -> GradeInput -> compute_gridiron_grade()
```

Do not let provider-specific raw fields leak into the scoring formulas.

Recommended new modules:

```txt
backend/app/services/data_sources/sleeper.py
backend/app/services/data_sources/nfl_data.py
backend/app/services/grade_inputs.py
```

## First tests to add

Add unit tests for:

- matchup thresholds;
- opportunity trend boundaries;
- grade cap at 100;
- injury modifier;
- deterministic mock grades;
- RB vs WR weighting behavior;
- chaos score cap at 100.

## Product caution

The Gridiron Grade is a confidence score, not a guarantee. UI should avoid overclaiming precision.
