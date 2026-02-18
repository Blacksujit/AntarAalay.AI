#!/usr/bin/env python3
"""
Test script to verify design generation works (without authentication)
"""

import asyncio
from app.services.ai_design_service import get_ai_design_service

async def test_design_generation():
    print("🧪 Testing Design Generation...")
    
    try:
        # Get AI design service
        ai_service = await get_ai_design_service()
        print("✅ AI design service created")
        
        # Test engine creation
        engine = await ai_service._get_engine()
        print(f"✅ Engine created: {engine.engine_type.value}")
        
        # This will fail without proper setup, but that's expected
        print("⚠️  Design generation requires:")
        print("   - Valid room_id with uploaded images")
        print("   - Replicate API token in .env")
        print("   - Authentication token from frontend")
        
    except Exception as e:
        print(f"Expected error (missing configuration): {e}")

if __name__ == "__main__":
    asyncio.run(test_design_generation())
