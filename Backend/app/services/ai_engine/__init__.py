"""
AI Engine Package

This package contains various AI engines for image generation:
- BaseEngine: Abstract interface
- ModelsLabEngine: Production with Models Lab API
- HuggingFaceEngine: Production with HuggingFace Inference
- SimpleSD15Engine: Local Stable Diffusion 1.5 for GTX 1650
"""

from .base_engine import BaseEngine, EngineType, EngineFactory, GenerationRequest, GenerationResult
from .models_lab_engine import ModelsLabEngine
from .huggingface_engine import HuggingFaceEngine
from .simple_sd15_engine import SimpleSD15Engine
from .flux_working_engine import FluxWorkingEngine

__all__ = [
    "BaseEngine",
    "EngineType", 
    "EngineFactory",
    "GenerationRequest",
    "GenerationResult",
    "ModelsLabEngine",
    "HuggingFaceEngine",
    "SimpleSD15Engine",
    "FluxWorkingEngine"
]
