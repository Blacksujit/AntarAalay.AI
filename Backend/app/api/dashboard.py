"""
Dashboard API Routes
GET /api/dashboard/stats
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.database import get_db_manager, get_db
from app.dependencies import get_current_user
from app.models import Room, Design
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics for the current user.
    """
    try:
        user_id = current_user.get('localId') or current_user.get('user_id')
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found"
            )
        
        logger.info(f"Fetching dashboard stats for user {user_id}")
        
        # Get total designs
        total_designs = db.query(Design).filter(
            Design.user_id == user_id
        ).count()
        
        # Get this month's designs
        this_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        this_month_designs = db.query(Design).filter(
            Design.user_id == user_id,
            Design.created_at >= this_month_start
        ).count()
        
        # Get average generation time (mock data for now)
        avg_generation_time = 45  # seconds
        
        # Get favorite style (most used)
        favorite_style_query = db.query(
            Design.style
        ).filter(
            Design.user_id == user_id
        ).group_by(Design.style).order_by(
            func.count(Design.style).desc()
        ).first()
        
        favorite_style = favorite_style_query[0] if favorite_style_query else 'modern'
        
        # Get recent designs
        recent_designs = db.query(Design).options(
            joinedload(Design.room)
        ).filter(
            Design.user_id == user_id
        ).order_by(
            Design.created_at.desc()
        ).limit(6).all()
        
        # Format recent designs for frontend
        recent_designs_data = []
        for design in recent_designs:
            # Get room_type from the related Room
            room_type = None
            if design.room:
                room_type = design.room.room_type
            
            recent_designs_data.append({
                'id': design.id,
                'style': design.style,
                'room_type': room_type,
                'wall_color': design.wall_color,
                'flooring_material': design.flooring_material,
                'image_1_url': design.image_1_url,
                'image_2_url': design.image_2_url,
                'image_3_url': design.image_3_url,
                'estimated_cost': design.estimated_cost,
                'status': 'completed',
                'created_at': design.created_at.isoformat() if design.created_at else datetime.now().isoformat()
            })
        
        stats = {
            'totalDesigns': total_designs,
            'thisMonth': this_month_designs,
            'avgGenerationTime': avg_generation_time,
            'favoriteStyle': favorite_style
        }
        
        logger.info(f"Dashboard stats for user {user_id}: {stats}")
        
        return {
            'status': 'success',
            'stats': stats,
            'recentDesigns': recent_designs_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch dashboard statistics"
        )
