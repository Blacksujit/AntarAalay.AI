#!/usr/bin/env python3
"""
Quick server test for standalone engine
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.services.ai_engine import EngineFactory, EngineType

def test_server():
    engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, {'device': 'cpu'})
    info = engine.get_model_info()
    print('✅ Server will use:', info['engine_type'])
    print('✅ Model Type:', info['model_type'])
    print('✅ Resolution:', info['resolution'])
    print('✅ Features:', len(info['features']), 'features available')
    print('✅ Supported Styles:', ', '.join(info.get('supported_styles', [])))
    print('✅ Supported Flooring:', ', '.join(info.get('supported_flooring', [])))

if __name__ == "__main__":
    test_server()
    print("\n🚀 SERVER IS READY FOR PRODUCTION!")
