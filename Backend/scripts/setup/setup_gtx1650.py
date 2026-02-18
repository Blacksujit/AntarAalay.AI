#!/usr/bin/env python3
"""
Setup script for GTX 1650 Interior Design Engine
"""

import os
import subprocess
import sys
from pathlib import Path

def install_pytorch_cuda():
    """Install PyTorch with CUDA 11.8 support for GTX 1650."""
    print("🔧 Installing PyTorch with CUDA 11.8 support...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "torch", "torchvision", 
            "--index-url", "https://download.pytorch.org/whl/cu118"
        ])
        print("✅ PyTorch with CUDA installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PyTorch: {e}")
        return False

def install_diffusers():
    """Install diffusers and related packages."""
    print("🔧 Installing diffusers and transformers...")
    
    packages = [
        "diffusers",
        "transformers", 
        "accelerate",
        "xformers",
        "opencv-python",
        "pillow",
        "numpy",
        "fastapi",
        "uvicorn",
        "sqlalchemy"
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

def check_cuda():
    """Check if CUDA is available."""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA is available")
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("⚠️  CUDA is not available. Will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet")
        return False

def create_storage_directories():
    """Create storage directories."""
    directories = [
        "./storage",
        "./storage/rooms", 
        "./storage/generated"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def test_setup():
    """Test the setup."""
    print("\n🧪 Testing GTX 1650 setup...")
    
    try:
        from app.services.ai_engine import EngineFactory, EngineType
        
        config = {
            'device': 'cuda' if check_cuda() else 'cpu',
            'resolution': 512,
            'num_inference_steps': 25,
            'enable_xformers': True,
            'enable_attention_slicing': True,
            'enable_cpu_offload': True
        }
        
        engine = EngineFactory.create_engine(EngineType.LOCAL_SDXL, config)
        print("✅ Engine created successfully")
        
        info = engine.get_model_info()
        print(f"✅ Engine: {info['engine_type']}")
        print(f"✅ Resolution: {info['resolution']}")
        print(f"✅ Device: {info['device']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🏠 GTX 1650 INTERIOR DESIGN ENGINE SETUP")
    print("=" * 60)
    
    # Step 1: Install PyTorch with CUDA
    if not install_pytorch_cuda():
        print("❌ Failed to install PyTorch")
        return
    
    # Step 2: Install other packages
    if not install_diffusers():
        print("❌ Failed to install dependencies")
        return
    
    # Step 3: Check CUDA
    cuda_available = check_cuda()
    
    # Step 4: Create storage directories
    create_storage_directories()
    
    # Step 5: Test setup
    if test_setup():
        print("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("\n📋 NEXT STEPS:")
        print("1. Update your .env file with the GTX 1650 configuration")
        print("2. Restart the server: python -m uvicorn main:app --reload")
        print("3. Test with a room image upload")
        print("4. Generate interior designs")
        
        if cuda_available:
            print("\n🚀 GPU ACCELERATION READY!")
            print("   Your GTX 1650 will handle generation efficiently")
        else:
            print("\n⚠️  RUNNING ON CPU")
            print("   Consider checking CUDA installation for GPU acceleration")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
