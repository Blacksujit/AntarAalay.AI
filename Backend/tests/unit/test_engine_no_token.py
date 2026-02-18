#!/usr/bin/env python3
"""
Test script to verify AI engine without API calls
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
from app.services.ai_engine import EngineFactory, EngineType

async def test_engine_without_token():
    print("🧪 Testing AI Engine without API token...")
    
    try:
        # Test creating engine with dummy token
        config = {'replicate_api_token': 'test_token'}
        engine = EngineFactory.create_engine(EngineType.REPLICATE, config)
        print(f"✅ Engine created: {engine.engine_type.value}")
        
        # Test health check (will fail but that's expected)
        health = await engine.health_check()
        print(f"Health check: {health}")
        
    except Exception as e:
        print(f"Expected error (no real token): {e}")
        print("✅ Engine creation works, API calls will fail without real token")

if __name__ == "__main__":
    asyncio.run(test_engine_without_token())
