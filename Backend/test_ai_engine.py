#!/usr/bin/env python3
"""
Quick test script to verify AI engine installation
"""

import asyncio
from app.services.ai_engine import (
    EngineFactory, 
    EngineType,
    PromptBuilder, 
    StyleParameters, 
    ControlNetAdapter,
    RateLimiter, 
    RateLimitConfig
)

async def test_components():
    print("🧪 Testing AI Engine Components...")
    
    # Test 1: Engine Factory
    print("\n1. Testing Engine Factory...")
    try:
        config = {'replicate_api_token': 'test'}
        engine = EngineFactory.create_engine(EngineType.REPLICATE, config)
        print(f"✅ Replicate engine created: {engine.engine_type.value}")
    except Exception as e:
        print(f"❌ Engine Factory failed: {e}")
        return
    
    # Test 2: Prompt Builder
    print("\n2. Testing Prompt Builder...")
    try:
        builder = PromptBuilder()
        params = StyleParameters(
            room_type='living',
            furniture_style='modern', 
            wall_color='white',
            flooring_material='hardwood'
        )
        prompt = builder.build_positive_prompt(params)
        print(f"✅ Prompt builder working - Length: {len(prompt)} chars")
    except Exception as e:
        print(f"❌ Prompt Builder failed: {e}")
        return
    
    # Test 3: ControlNet Adapter
    print("\n3. Testing ControlNet Adapter...")
    try:
        adapter = ControlNetAdapter({'default_resolution': (512, 512)})
        print("✅ ControlNet adapter working")
    except Exception as e:
        print(f"❌ ControlNet Adapter failed: {e}")
        return
    
    # Test 4: Rate Limiter
    print("\n4. Testing Rate Limiter...")
    try:
        config = RateLimitConfig(free_daily_limit=3)
        limiter = RateLimiter(config)
        
        user_data = {'uid': 'test_user'}
        allowed, error = await limiter.check_rate_limit('user1', user_data)
        print(f"✅ Rate limiter working - First request allowed: {allowed}")
        
        usage = await limiter.get_user_usage('user1')
        print(f"✅ Usage tracking working - Count: {usage['count']}")
    except Exception as e:
        print(f"❌ Rate Limiter failed: {e}")
        return
    
    print("\n🎉 All components working correctly!")
    print("\n📋 Next Steps:")
    print("1. Set AI_ENGINE=replicate in your .env file")
    print("2. Add your REPLICATE_API_TOKEN")
    print("3. Start the server: uvicorn main:app --reload")
    print("4. Test the API endpoints")

if __name__ == "__main__":
    asyncio.run(test_components())
