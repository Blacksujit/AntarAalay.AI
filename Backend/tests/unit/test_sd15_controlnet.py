#!/usr/bin/env python3
"""
Test SD15 ControlNet Engine for GTX 1650
"""

import asyncio
from app.services.ai_engine import EngineFactory, EngineType

async def test_sd15_controlnet_engine():
    try:
        config = {
            'device': 'cpu',  # Use CPU for testing (change to 'cuda' for GPU)
            'resolution': 512,
            'num_inference_steps': 25,
            'guidance_scale': 7.0,
            'strength': 0.45,
            'controlnet_conditioning_scale': 0.8,
            'enable_xformers': False,  # Disable for CPU testing
            'enable_attention_slicing': True,
            'enable_cpu_offload': True
        }
        
        # Use LOCAL_SDXL which defaults to SD15 ControlNet
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, config)
        print('✅ SD15 ControlNet Engine created successfully')
        
        # Test health check
        health = await engine.health_check()
        print(f'Health check: {health}')
        
        # Get model info
        info = engine.get_model_info()
        print(f'Engine Type: {info["engine_type"]}')
        print(f'Base Model: {info["base_model"]}')
        print(f'ControlNet Model: {info["controlnet_model"]}')
        print(f'Resolution: {info["resolution"]}')
        print(f'Device: {info["device"]}')
        print(f'GPU Requirements: {info["gpu_requirements"]}')
        
        print('\nMemory Optimizations:')
        for opt, enabled in info["memory_optimizations"].items():
            print(f'  {opt}: {enabled}')
        
        print('\nGeneration Parameters:')
        for param, value in info["generation_params"].items():
            print(f'  {param}: {value}')
        
        print('\nFeatures:')
        for feature in info["features"]:
            print(f'  ✅ {feature}')
        
    except ImportError as e:
        print(f'⚠️  Missing dependencies: {e}')
        print('Install with: pip install torch torchvision diffusers transformers accelerate')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(test_sd15_controlnet_engine())
