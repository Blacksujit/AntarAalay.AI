# Setup Scripts for AntarAalay.ai

## 🛠️ Available Scripts

### Setup Scripts (`setup/`)

#### `setup_gtx1650.py`
**Purpose**: Automated setup for GTX 1650 interior design engine

**Features**:
- Installs PyTorch with CUDA 11.8 support
- Installs diffusers and dependencies
- Checks CUDA availability
- Creates storage directories
- Tests configuration

**Usage**:
```bash
python scripts/setup/setup_gtx1650.py
```

**Requirements**:
- GTX 1650 4GB VRAM (or compatible NVIDIA GPU)
- CUDA 11.8 compatible drivers
- Python 3.8+

#### `setup_local_interior_engine.py`
**Purpose**: Setup for local open-source interior design models

**Features**:
- Installs required packages
- Creates models directory
- Provides download instructions for Civitai models
- Tests local engine configuration

**Usage**:
```bash
python scripts/setup/setup_local_interior_engine.py
```

**Requirements**:
- CPU or GPU with 4GB+ VRAM
- 10GB+ disk space for models
- Internet connection for model downloads

## 🚀 Quick Setup

### For GTX 1650 Users
```bash
# Run automated setup
python scripts/setup/setup_gtx1650.py

# Configure environment
cp config/env-gtx1650.txt .env

# Start server
python -m uvicorn main:app --reload
```

### For Local Model Users
```bash
# Run setup script
python scripts/setup/setup_local_interior_engine.py

# Download models (follow script instructions)
# Save to ./models/ directory

# Configure environment
cp config/env-local-open-source.txt .env

# Start server
python -m uvicorn main:app --reload
```

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10/11, Linux, or macOS
- **Python**: 3.8 or higher
- **Memory**: 8GB+ RAM recommended
- **Storage**: 10GB+ free space

### GPU Requirements (Optional)
- **NVIDIA GPU**: GTX 1650 or better
- **VRAM**: 4GB+ recommended
- **CUDA**: 11.8 compatible drivers

### Software Dependencies
- Git
- Python 3.8+
- pip (Python package manager)

## 🔧 Manual Installation

If setup scripts fail, you can install manually:

### PyTorch (CUDA)
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### PyTorch (CPU)
```bash
pip install torch torchvision
```

### Diffusers and Dependencies
```bash
pip install diffusers transformers accelerate
pip install xformers  # Optional, for memory efficiency
pip install opencv-python pillow numpy
pip install fastapi uvicorn sqlalchemy
```

## 🐛 Troubleshooting

### Common Issues

#### CUDA Not Available
```bash
# Check CUDA installation
python -c "import torch; print(torch.cuda.is_available())"

# If False, install CPU version or check GPU drivers
```

#### Out of Memory Errors
- Reduce resolution in configuration
- Enable CPU offload
- Use smaller models

#### Import Errors
- Ensure Python path includes backend directory
- Check all dependencies are installed
- Verify Python version compatibility

#### Permission Errors
- Run as administrator if needed
- Check file permissions
- Use virtual environment

### Debug Mode
```bash
# Run setup with verbose output
python -v scripts/setup/setup_gtx1650.py

# Check installed packages
pip list | grep torch
pip list | grep diffusers
```

## 📚 Additional Resources

- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [Diffusers Documentation](https://huggingface.co/docs/diffusers/)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
- [GTX 1650 Specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/gtx-1650/)

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review the test output for specific error messages
3. Ensure all prerequisites are met
4. Try manual installation as a fallback

For additional support:
- Check the [GTX 1650 Production Guide](../docs/guides/GTX1650_PRODUCTION_GUIDE.md)
- Review the [test documentation](../tests/README.md)
- Run diagnostic tests with `python run_tests.py --engine`
