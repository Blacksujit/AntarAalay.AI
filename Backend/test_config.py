#!/usr/bin/env python3
"""Test configuration loading"""

from app.config import get_settings

def test_config():
    settings = get_settings()
    print('✅ Configuration loaded:')
    print(f'HF_TOKEN: {"✅" if settings.HF_TOKEN else "❌"}')
    print(f'AI_ENGINE: {settings.AI_ENGINE}')
    print(f'DEVICE: {settings.DEVICE}')
    print(f'FLUX_MAX_GENERATIONS_PER_HOUR: {settings.FLUX_MAX_GENERATIONS_PER_HOUR}')
    print('Backend ready to start!')

if __name__ == "__main__":
    test_config()
