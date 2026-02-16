from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_current_user_optional
from app.schemas.vastu import VastuAnalyzeRequest, VastuAnalyzeResponse, VastuDirectionInfo
from app.services.vastu_engine import get_vastu_engine

router = APIRouter(prefix="/vastu", tags=["vastu"])


@router.post("/analyze", response_model=VastuAnalyzeResponse)
async def analyze_vastu(
    request: VastuAnalyzeRequest,
    current_user: dict = Depends(get_current_user_optional)
):
    """
    Analyze Vastu compliance for a direction and room type combination
    """
    try:
        vastu_result = get_vastu_engine().analyze(request.direction, request.room_type)
        return VastuAnalyzeResponse(**vastu_result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vastu analysis failed: {str(e)}"
        )


@router.get("/direction/{direction}", response_model=VastuDirectionInfo)
async def get_direction_info(
    direction: str,
    current_user: dict = Depends(get_current_user_optional)
):
    """
    Get Vastu information for a specific direction
    """
    direction = direction.lower()
    rules = get_vastu_engine().rules.get(direction)
    if not rules:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid direction. Valid directions: {', '.join(get_vastu_engine().rules.keys())}"
        )
    
    return VastuDirectionInfo(
        direction=direction,
        ruling_element=rules["element"],
        suitable_rooms=rules["suitable_rooms"],
        colors=rules["colors"],
        tips=rules["dos"]
    )


@router.get("/score/{direction}/{room_type}")
async def get_vastu_score(
    direction: str,
    room_type: str,
    current_user: dict = Depends(get_current_user_optional)
):
    """
    Get Vastu score for a specific direction and room type
    """
    try:
        result = get_vastu_engine().analyze(direction, room_type)
        return {
            "direction": direction,
            "room_type": room_type,
            "vastu_score": result["vastu_score"],
            "rating": result["direction_rating"],
            "element": result["element_balance"]["dominant_element"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Vastu score: {str(e)}"
        )


@router.get("/remedies/{direction}/{room_type}")
async def get_vastu_remedies(
    direction: str,
    room_type: str,
    current_user: dict = Depends(get_current_user_optional)
):
    """
    Get Vastu remedies for a non-compliant placement
    """
    try:
        remedies = get_vastu_engine().get_remedies(direction, room_type)
        analysis = get_vastu_engine().analyze(direction, room_type)
        
        return {
            "direction": direction,
            "room_type": room_type,
            "current_score": analysis["vastu_score"],
            "remedies": remedies,
            "improvement_potential": min(100, analysis["vastu_score"] + 20)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get remedies: {str(e)}"
        )


@router.get("/directions")
async def get_all_directions(
    current_user: dict = Depends(get_current_user_optional)
):
    """
    Get all Vastu directions and their basic info
    """
    directions = []
    for direction, rules in get_vastu_engine().rules.items():
        directions.append({
            "direction": direction,
            "element": rules["element"],
            "ruling_planet": rules["ruling_planet"],
            "suitable_rooms": rules["suitable_rooms"][:3],  # Top 3
            "colors": rules["colors"][:3]  # Top 3
        })
    
    return {"directions": directions}
