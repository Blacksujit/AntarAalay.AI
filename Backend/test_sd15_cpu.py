#!/usr/bin/env python3
"""
Test SD15 ControlNet Engine with CPU Configuration
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import asyncio
from app.services.ai_engine import EngineFactory, EngineType

async def test_sd15_cpu():
    try:
        print("🏠 Testing SD15 ControlNet Engine (CPU Configuration)")
        print("=" * 60)
        
        # CPU configuration (no CUDA issues)
        config = {
            'device': 'cpu',
            'resolution': 512,
            'num_inference_steps': 25,
            'guidance_scale': 7.0,
            'strength': 0.45,
            'controlnet_conditioning_scale': 0.8,
            'enable_xformers': False,  # Disable for CPU
            'enable_attention_slicing': True,
            'enable_cpu_offload': True
        }
        
        print("✅ Configuration loaded")
        print(f"   Device: {config['device']}")
        print(f"   Xformers: {config['enable_xformers']}")
        print(f"   Attention Slicing: {config['enable_attention_slicing']}")
        print(f"   CPU Offload: {config['enable_cpu_offload']}")
        
        # Create engine (this will test model loading)
        print("\n🔧 Creating engine...")
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, config)
        print("✅ Engine created successfully")
        
        # Test health check
        print("\n🏥 Testing health check...")
        health = await engine.health_check()
        print(f"Health check: {'✅ PASSED' if health else '❌ FAILED'}")
        
        # Get model info
        print("\n📋 Getting model info...")
        info = engine.get_model_info()
        print(f"Engine Type: {info['engine_type']}")
        print(f"Base Model: {info['base_model']}")
        print(f"ControlNet: {info['controlnet_model']}")
        print(f"Resolution: {info['resolution']}")
        print(f"Device: {info['device']}")
        
        print("\n🎉 SD15 ControlNet Engine test completed successfully!")
        print("📝 Note: Models may not be fully loaded without proper installation")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  Import error: {e}")
        print("💡 Install dependencies: pip install torch torchvision diffusers transformers accelerate")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_sd15_cpu())
    sys.exit(0 if success else 1)
