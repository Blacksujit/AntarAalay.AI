#!/usr/bin/env python3
"""
Test HuggingFace engine (Python 3.14 compatible)
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
from app.services.ai_engine import EngineFactory, EngineType

async def test_hf_engine():
    try:
        token = os.getenv('HUGGINGFACE_TOKEN', '')
        if not token:
            print("WARNING: HUGGINGFACE_TOKEN not set in environment")
            print("Set it in your .env file: HUGGINGFACE_TOKEN=your_token")
            return
            
        config = {
            'hf_api_key': token,
            'hf_endpoint_url': 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0'
        }
        engine = EngineFactory.create_engine(EngineType.HF_INFERENCE, config)
        print('✅ HuggingFace engine created successfully')
        
        # Test health check
        health = await engine.health_check()
        print(f'Health check: {health}')
        
        # Get model info
        info = engine.get_model_info()
        print(f'Model: {info["model_name"]}')
        print(f'Specialization: {info["specialization"]}')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(test_hf_engine())
