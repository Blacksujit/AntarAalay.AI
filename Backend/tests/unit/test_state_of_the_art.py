#!/usr/bin/env python3
"""
Test State-of-the-Art Interior Design Engine
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
from app.services.ai_engine import EngineFactory, EngineType

async def test_state_of_the_art_engine():
    try:
        token = os.getenv('HUGGINGFACE_TOKEN', '')
        if not token:
            print("WARNING: HUGGINGFACE_TOKEN not set in environment")
            print("Set it in your .env file: HUGGINGFACE_TOKEN=your_token")
            return
            
        config = {
            'hf_api_key': token,
            'use_refiner': True,
            'max_retries': 3
        }
        
        engine = EngineFactory.create_engine(EngineType.STATE_OF_THE_ART, config)
        print('✅ State-of-the-Art Interior Design Engine created successfully')
        
        # Test health check
        health = await engine.health_check()
        print(f'Health check: {health}')
        
        # Get model info
        info = engine.get_model_info()
        print(f'Engine Type: {info["engine_type"]}')
        print(f'Primary Model: {info["primary_model"]}')
        print(f'Specialization: {info["specialization"]}')
        print(f'Quality: {info["quality"]}')
        print(f'ControlNet: {info["controlnet"]}')
        print(f'Available Models: {info["available_models"]}')
        print(f'Features: {info["features"]}')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(test_state_of_the_art_engine())
