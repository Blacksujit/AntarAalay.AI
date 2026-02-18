#!/usr/bin/env python3
"""
Test script with real Replicate token
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
from app.services.ai_engine import EngineFactory, EngineType

async def test_real_token():
    try:
        token = os.getenv('REPLICATE_API_TOKEN', '')
        if not token:
            print("WARNING: REPLICATE_API_TOKEN not set in environment")
            print("Set it in your .env file: REPLICATE_API_TOKEN=your_token")
            return
            
        config = {'replicate_api_token': token}
        engine = EngineFactory.create_engine(EngineType.REPLICATE, config)
        print('✅ Replicate engine created successfully')
        
        # Test health check
        health = await engine.health_check()
        print(f'Health check: {health}')
        
        # Get model info
        info = engine.get_model_info()
        print(f'Model: {info["model_name"]}')
        print(f'Specialization: {info["specialization"]}')
        print(f'Cost per generation: ${info["cost_per_generation"]}')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(test_real_token())
