#!/usr/bin/env python3
"""
Test Local Open-Source Interior Design Engine
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
from app.services.ai_engine import EngineFactory, EngineType

async def test_local_open_source_engine():
    try:
        config = {
            'models_dir': './models',
            'device': 'cpu',  # Use CPU for testing
            'primary_model': 'interior_scene_xl',
            'use_controlnet': False  # Disable for testing
        }
        
        # Use LOCAL_SDXL with our open-source engine
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, config)
        print('✅ Local Open-Source Interior Design Engine created successfully')
        
        # Test health check
        health = await engine.health_check()
        print(f'Health check: {health}')
        
        # Get model info
        info = engine.get_model_info()
        print(f'Engine Type: {info["engine_type"]}')
        print(f'Primary Model: {info["primary_model"]}')
        print(f'Specialization: {info["specialization"]}')
        print(f'Base Model: {info["base_model"]}')
        print(f'Model Size: {info["model_size"]}')
        print(f'License: {info["license"]}')
        print(f'Device: {info["device"]}')
        print(f'Model Type: {info["model_type"]}')
        print(f'Cost: {info["cost"]}')
        print(f'Available Models: {info["available_models"]}')
        print(f'Features: {info["features"]}')
        
        print('\n📥 Download Instructions:')
        for model, instruction in info["download_instructions"].items():
            print(f'{model}: {instruction}')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(test_local_open_source_engine())
