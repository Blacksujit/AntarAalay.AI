# Configuration Files for AntarAalay.ai

## ⚙️ Available Configurations

### Environment Configurations

#### `env-gtx1650.txt` ⭐ **Recommended for GTX 1650**
**Purpose**: Optimized for GTX 1650 4GB VRAM

**Features**:
- SD15 ControlNet engine
- 512x512 resolution
- Memory optimizations enabled
- CUDA acceleration

**Use Case**: Production deployment on GTX 1650

#### `env-local-open-source.txt`
**Purpose**: Local open-source models

**Features**:
- Local model loading
- No API dependencies
- Interior design specific models
- Offline capability

**Use Case**: Offline deployment or when APIs are unavailable

#### `env-interior-design-specific.txt`
**Purpose**: Interior design specific models

**Features**:
- Fine-tuned interior design models
- Room segmentation ControlNet
- Image-to-image specialization
- High-quality interior output

**Use Case**: When interior design quality is priority

#### `env-free-state-of-the-art.txt`
**Purpose**: Free state-of-the-art models

**Features**:
- Stable Diffusion 3.5 Large
- No API costs
- Latest model technology
- Commercial use allowed

**Use Case**: When cost is concern but quality is needed

#### `env-state-of-the-art.txt`
**Purpose**: Premium state-of-the-art models

**Features**:
- Juggernaut XL
- Realistic Vision V6.0
- SDXL Refiner
- Highest quality output

**Use Case**: When quality is absolute priority

## 🚀 Quick Start

### 1. Choose Configuration
```bash
# For GTX 1650 (recommended)
cp config/env-gtx1650.txt .env

# For local models
cp config/env-local-open-source.txt .env

# For interior design specific
cp config/env-interior-design-specific.txt .env
```

### 2. Customize (Optional)
Edit `.env` file to modify:
- API keys
- Model paths
- Generation parameters
- Rate limits

### 3. Start Server
```bash
python -m uvicorn main:app --reload
```

## 📋 Configuration Options

### AI Engine Settings
```bash
# Engine type
AI_ENGINE=local_sdxl          # Use local SDXL engine
AI_ENGINE=hf_inference        # Use HuggingFace API
AI_ENGINE=replicate          # Use Replicate API

# Device configuration
DEVICE=cuda                  # Use GPU (recommended)
DEVICE=cpu                   # Use CPU (slower)

# Generation parameters
RESOLUTION=512               # Image resolution (512 for 4GB VRAM)
NUM_INFERENCE_STEPS=25       # Generation steps (20-30)
GUIDANCE_SCALE=7.0          # Prompt guidance (7-10)
STRENGTH=0.45               # Image-to-image strength (0.3-0.7)
```

### Memory Optimization
```bash
# For 4GB VRAM (GTX 1650)
ENABLE_XFORMERS=true         # Memory efficient attention
ENABLE_ATTENTION_SLICING=true # Reduce memory usage
ENABLE_CPU_OFFLOAD=true      # Move layers to CPU

# For more VRAM
ENABLE_XFORMERS=true
ENABLE_ATTENTION_SLICING=false
ENABLE_CPU_OFFLOAD=false
```

### API Configuration
```bash
# HuggingFace
HF_API_KEY=your_key_here
HF_ENDPOINT_URL=optional_model_url

# Replicate
REPLICATE_API_TOKEN=your_token_here

# Stability AI
STABLE_DIFFUSION_API_KEY=your_key_here
```

### Rate Limiting
```bash
FREE_DAILY_LIMIT=3           # Generations per day for free users
GLOBAL_REQUESTS_PER_MINUTE=60 # Global rate limit
```

### Storage Configuration
```bash
STORAGE_PATH=./storage       # Base storage directory
UPLOAD_PATH=./storage/rooms  # Room upload directory
GENERATED_PATH=./storage/generated # Generated images directory
```

## 🔧 Configuration Validation

### Test Configuration
```bash
# Test GTX 1650 configuration
python run_tests.py --engine

# Test specific configuration
python tests/unit/test_gtx1650_config.py
```

### Validate Setup
```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Check GPU memory
python -c "import torch; print(f'GPU Memory: {torch.cuda.get_device_properties(0).total_memory/1024**3:.1f}GB')" 2>/dev/null || echo "No GPU available"
```

## 📊 Performance Comparison

| Configuration | VRAM Usage | Speed | Quality | Cost |
|---------------|------------|-------|---------|------|
| GTX 1650 | ~3.2GB | Fast | Good | Free |
| Local Open Source | ~4GB | Medium | Excellent | Free |
| Interior Design Specific | ~3.5GB | Medium | Excellent | Free |
| Free State-of-the-Art | ~2GB | Slow | Very Good | Free |
| State-of-the-Art | ~4GB | Fast | Best | Paid |

## 🐛 Troubleshooting

### Common Issues

#### Out of Memory
```bash
# Reduce resolution
RESOLUTION=512

# Enable more optimizations
ENABLE_CPU_OFFLOAD=true
ENABLE_ATTENTION_SLICING=true
```

#### CUDA Not Available
```bash
# Switch to CPU
DEVICE=cpu

# Or install CUDA drivers
```

#### Model Loading Errors
```bash
# Check model paths
MODEL_PATH=./models/model_name.safetensors

# Verify file exists
ls -la ./models/
```

#### API Key Errors
```bash
# Verify API keys
HF_API_KEY=your_actual_key
REPLICATE_API_TOKEN=your_actual_token
```

## 🎯 Recommendations

### For GTX 1650 Users
1. Use `env-gtx1650.txt`
2. Enable all memory optimizations
3. Keep resolution at 512x512
4. Use sequential generation

### For Production
1. Use `env-gtx1650.txt` or `env-interior-design-specific.txt`
2. Set appropriate rate limits
3. Monitor GPU memory usage
4. Enable logging

### For Development
1. Use `env-local-open-source.txt`
2. Enable debug mode
3. Use CPU for testing
4. Lower inference steps for speed

## 📝 Custom Configuration

### Creating Custom Config
1. Copy an existing configuration
2. Modify parameters as needed
3. Test with `python run_tests.py --engine`
4. Deploy when validated

### Example Custom Config
```bash
# Custom high-quality config
AI_ENGINE=local_sdxl
DEVICE=cuda
RESOLUTION=512
NUM_INFERENCE_STEPS=30
GUIDANCE_SCALE=8.0
STRENGTH=0.5
ENABLE_XFORMERS=true
ENABLE_ATTENTION_SLICING=true
ENABLE_CPU_OFFLOAD=false
FREE_DAILY_LIMIT=5
```

## 📚 Additional Information

- [GTX 1650 Production Guide](../docs/guides/GTX1650_PRODUCTION_GUIDE.md)
- [Test Documentation](../tests/README.md)
- [Setup Scripts](../scripts/README.md)
