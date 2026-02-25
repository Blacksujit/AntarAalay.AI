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
    room_type: Optional[str] = "living"
    budget: Optional[float] = None
    wall_color: Optional[str] = "white"
    flooring_material: Optional[str] = "hardwood"


class DesignResponse(BaseModel):
    id: str
    room_id: str
    user_id: str
    style: str
    budget: Optional[float] = None
    image_1_url: Optional[str] = None
    image_2_url: Optional[str] = None
    image_3_url: Optional[str] = None
    estimated_cost: Optional[float] = None
    budget_match_percentage: Optional[float] = None
    furniture_breakdown: Optional[Dict] = None
    vastu_score: Optional[float] = None
    vastu_suggestions: Optional[List[str]] = None
    vastu_warnings: Optional[List[str]] = None
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
