from pydantic import BaseModel
from typing import Optional, List


class VastuAnalyzeRequest(BaseModel):
    direction: str
    room_type: str


class VastuAnalyzeResponse(BaseModel):
    vastu_score: float
    suggestions: List[str]
    warnings: List[str]
    direction_rating: str  # excellent, good, neutral, poor
    element_balance: Optional[dict] = None


class VastuDirectionInfo(BaseModel):
    direction: str
    ruling_element: str
    suitable_rooms: List[str]
    colors: List[str]
    tips: List[str]
