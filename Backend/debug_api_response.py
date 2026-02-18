#!/usr/bin/env python3
"""
Debug the with-details API response
"""

import httpx
import asyncio
import json

async def test_with_details():
    """Test the with-details endpoint and see exact response"""
    
    # This assumes the server is running and a design exists
    # Get the latest design from database
    import sys
    from pathlib import Path
    
    backend_dir = Path(__file__).parent
    sys.path.insert(0, str(backend_dir))
    
    from app.database import get_db_manager
    from app.models.design import Design
    
    db_manager = get_db_manager()
    with db_manager.session_scope() as session:
        design = session.query(Design).order_by(Design.created_at.desc()).first()
        
        if not design:
            print("No designs found in database")
            return
        
        print(f"Latest design from database:")
        print(f"  ID: {design.id}")
        print(f"  Room ID: {design.room_id}")
        print(f"  Style: {design.style}")
        print(f"  Estimated Cost: {design.estimated_cost}")
        print(f"  Budget Match: {design.budget_match_percentage}")
        print(f"  Vastu Score: {design.vastu_score}")
        print(f"  Status: {design.status}")
        
        # Now check the API response structure
        print(f"\nBuilding API response structure...")
        
        # Simulate what the endpoint does
        designs_list = []
        
        # Parse furniture_breakdown from JSON string if needed
        furniture_data = design.furniture_breakdown
        if isinstance(furniture_data, str):
            try:
                import json
                furniture_data = json.loads(furniture_data)
            except:
                furniture_data = {}
        
        design_dict = {
            'id': design.id,
            'room_id': design.room_id,
            'user_id': design.user_id,
            'style': design.style,
            'budget': design.budget or 0,
            'image_1_url': design.image_1_url,
            'image_2_url': design.image_2_url,
            'image_3_url': design.image_3_url,
            'estimated_cost': design.estimated_cost or 50000,
            'budget_match_percentage': design.budget_match_percentage or 85,
            'furniture_breakdown': furniture_data or {},
            'vastu_score': design.vastu_score or 85,
            'vastu_suggestions': [],
            'vastu_warnings': [],
            'status': design.status,
            'created_at': design.created_at.isoformat() if design.created_at else None,
        }
        
        print(f"\nDesign dict for API response:")
        print(json.dumps(design_dict, indent=2))
        
        # Now wrap it like the endpoint does
        from app.schemas.design import DesignResponse
        
        try:
            design_obj = DesignResponse(**design_dict)
            print(f"\nDesignResponse object created successfully")
            print(f"  estimated_cost: {design_obj.estimated_cost}")
            print(f"  model_dump: {design_obj.model_dump()}")
            
            # Full response structure
            response = {
                "design": design_obj.model_dump(),
                "room_image_url": design.image_1_url,
                "budget_summary": None,
            }
            
            print(f"\nFull API response item:")
            print(json.dumps(response, indent=2))
            
        except Exception as e:
            print(f"Error creating DesignResponse: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_details())
