#!/usr/bin/env python3
"""
Setup script for Local Open-Source Interior Design Engine
"""

import os
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install required packages."""
    print("🔧 Installing required packages...")
    
    packages = [
        "torch",
        "torchvision", 
        "diffusers",
        "transformers",
        "accelerate",
        "safetensors",
        "Pillow",
        "numpy"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def create_models_directory():
    """Create models directory."""
    models_dir = Path("./models")
    models_dir.mkdir(exist_ok=True)
    print(f"✅ Created models directory: {models_dir}")
    return models_dir

def download_instructions():
    """Print download instructions for models."""
    print("\n📥 MODEL DOWNLOAD INSTRUCTIONS:")
    print("=" * 50)
    
    models = {
        "interior-scene-xl.safetensors": {
            "url": "https://civitai.com/api/download/models/715747",
            "size": "6.46 GB",
            "description": "SDXL-based interior design with luxury style"
        },
        "interior-design-v1.safetensors": {
            "url": "https://civitai.com/api/download/models/54699", 
            "size": "1.99 GB",
            "description": "Dreambooth trained on 500 living room images"
        },
        "interiordesign-lulu-v1.0.safetensors": {
            "url": "https://civitai.com/api/download/models/622597",
            "size": "3.59 GB", 
            "description": "Universal model for multi-style home design"
        }
    }
    
    for filename, info in models.items():
        print(f"\n📁 {filename}")
        print(f"   Size: {info['size']}")
        print(f"   Description: {info['description']}")
        print(f"   Download URL: {info['url']}")
        print(f"   Save to: ./models/{filename}")
    
    print("\n" + "=" * 50)
    print("⚠️  You need to manually download these models from Civitai")
    print("⚠️  Create a free Civitai account to download")
    print("⚠️  Start with 'interior-scene-xl.safetensors' for best results")

def test_setup():
    """Test the setup."""
    print("\n🧪 Testing setup...")
    
    try:
        from app.services.ai_engine import EngineFactory, EngineType
        
        config = {
            'device': 'cpu',
            'primary_model': 'interior_scene_xl',
            'model_path': './models/interior-scene-xl.safetensors'
        }
        
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, config)
        print("✅ Engine created successfully")
        
        info = engine.get_model_info()
        print(f"✅ Engine Type: {info['engine_type']}")
        print(f"✅ Primary Model: {info['primary_model']}")
        print(f"✅ Cost: {info['cost']}")
        print(f"✅ Features: {len(info['features'])} features available")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🏠 LOCAL OPEN-SOURCE INTERIOR DESIGN ENGINE SETUP")
    print("=" * 60)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        return
    
    # Step 2: Create models directory
    models_dir = create_models_directory()
    
    # Step 3: Show download instructions
    download_instructions()
    
    # Step 4: Test setup
    if test_setup():
        print("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("\n📋 NEXT STEPS:")
        print("1. Download the models from Civitai (see URLs above)")
        print("2. Save them to ./models/ directory")
        print("3. Update your .env file with the configuration")
        print("4. Restart the server")
        print("5. Test with a real room image")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
