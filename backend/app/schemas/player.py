from pydantic import BaseModel
from pydantic import ConfigDict
from app.schemas.enums import MatchupGrade, OpportunityTrend

class PlayerResponse(BaseModel):
    id: int
    sleeper_id: str
    full_name: str
    position: str
    team: str | None
    status: str
    gridiron_grade: int
    matchup_grade: MatchupGrade
    chaos_score: int
    opportunity_trend: OpportunityTrend

    model_config = ConfigDict(from_attributes=True)