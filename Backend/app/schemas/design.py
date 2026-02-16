from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class DesignCustomizationRequest(BaseModel):
    wall_color: Optional[str] = None
    flooring: Optional[str] = None
    furniture_style: Optional[str] = None
    style: Optional[str] = None


class DesignGenerateRequest(BaseModel):
    room_id: str
    style: str
    budget: Optional[float] = None


class DesignResponse(BaseModel):
    id: str
    room_id: str
    user_id: str
    style: str
    budget: Optional[float]
    image_1_url: Optional[str]
    image_2_url: Optional[str]
    image_3_url: Optional[str]
    estimated_cost: Optional[float]
    budget_match_percentage: Optional[float]
    furniture_breakdown: Optional[Dict]
    vastu_score: Optional[float]
    vastu_suggestions: Optional[List[str]]
    vastu_warnings: Optional[List[str]]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DesignGenerateResponse(BaseModel):
    design_id: str
    status: str
    message: str


class DesignListResponse(BaseModel):
    designs: List[DesignResponse]
    total: int


class DesignWithDetails(BaseModel):
    design: DesignResponse
    room_image_url: str
    budget_summary: Dict
