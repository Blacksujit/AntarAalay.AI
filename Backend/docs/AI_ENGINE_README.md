# AI Interior Styling Engine

A production-grade, layout-preserving image-to-image transformation system for interior design using state-of-the-art AI models.

## 🎯 Features

### Core Capabilities
- **Layout Preservation**: Uses ControlNet with edge detection to preserve room geometry
- **Multi-Engine Support**: Local SDXL, Replicate API, and HuggingFace Inference
- **Rate Limiting**: Per-user quotas with cost control
- **High Quality**: SDXL-based generation with optimized prompts
- **Production Ready**: Comprehensive monitoring, error handling, and scaling

### Technical Features
- **Strategy Pattern**: Easy engine switching and extensibility
- **Async Architecture**: High-performance concurrent processing
- **Smart Caching**: Edge map and prompt caching for performance
- **Health Monitoring**: Built-in health checks and metrics
- **Comprehensive Testing**: Unit, integration, and end-to-end tests

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI        │    │   AI Engines    │
│   (React)       │◄──►│   Backend        │◄──►│   - Local SDXL  │
└─────────────────┘    └──────────────────┘    │   - Replicate   │
                                │                │   - HF Inference│
                                ▼                └─────────────────┘
                       ┌──────────────────┐
                       │   Storage & DB   │
                       │   - Local Files  │
                       │   - SQLite       │
                       │   - Rate Limits  │
                       └──────────────────┘
```

### Components

1. **BaseEngine**: Abstract interface for all AI engines
2. **LocalSDXLEngine**: Development with local GPU and ControlNet
3. **ReplicateEngine**: Production with hosted Replicate API
4. **HFEngine**: Production with HuggingFace Inference Endpoints
5. **PromptBuilder**: Optimized prompts for interior styling
6. **ControlNetAdapter**: Edge detection and layout preservation
7. **RateLimiter**: Usage quotas and cost management
8. **AIDesignService**: Complete workflow orchestration

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/antaraalay-ai.git
cd antaraalay-ai/backend

# Install dependencies
pip install -r requirements-ai.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration
```

### Development Setup

```bash
# Start with local SDXL engine
export AI_ENGINE=local_sdxl
export DEVICE=cuda  # or cpu

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Setup

```bash
# Use Replicate for production
export AI_ENGINE=replicate
export REPLICATE_API_KEY=your_key_here

# Start with production server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📖 Usage

### Generate Interior Design

```python
import asyncio
from app.services.ai_engine import EngineFactory, GenerationRequest

async def generate_design():
    # Get engine from environment
    engine = EngineFactory.get_engine_from_env()
    
    # Prepare generation request
    request = GenerationRequest(
        primary_image=open('room_north.jpg', 'rb').read(),
        room_images={
            'north': open('room_north.jpg', 'rb').read(),
            'south': open('room_south.jpg', 'rb').read(),
            'east': open('room_east.jpg', 'rb').read(),
            'west': open('room_west.jpg', 'rb').read()
        },
        room_type='living',
        furniture_style='modern',
        wall_color='white',
        flooring_material='hardwood',
        controlnet_weight=1.0,
        image_strength=0.4
    )
    
    # Generate designs
    result = await engine.generate_img2img(request)
    
    if result.success:
        print(f"Generated {len(result.generated_images)} designs")
        for url in result.generated_images:
            print(f"Design: {url}")
    else:
        print(f"Generation failed: {result.error_message}")

# Run generation
asyncio.run(generate_design())
```

### API Usage

```bash
# Upload room images (4 directions)
curl -X POST "http://localhost:8000/api/room/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "north=@north.jpg" \
  -F "south=@south.jpg" \
  -F "east=@east.jpg" \
  -F "west=@west.jpg"

# Generate design
curl -X POST "http://localhost:8000/api/design/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "room_id": "your-room-id",
    "room_type": "living",
    "style": "modern",
    "wall_color": "white",
    "flooring_material": "hardwood"
  }'
```

## ⚙️ Configuration

### Engine Selection

```bash
# Local development (requires GPU)
AI_ENGINE=local_sdxl

# Production with Replicate
AI_ENGINE=replicate
REPLICATE_API_TOKEN=your_token

# Enterprise with HF Endpoints
AI_ENGINE=hf_inference
HF_API_KEY=your_key
HF_ENDPOINT_URL=your_endpoint
```

### Generation Parameters

```bash
# ControlNet settings
CONTROLNET_WEIGHT=1.0          # Layout preservation strength
IMAGE_STRENGTH=0.4             # Transformation intensity
NUM_INFERENCE_STEPS=30         # Quality vs speed
GUIDANCE_SCALE=7.0             # Prompt adherence

# Rate limiting
FREE_DAILY_LIMIT=3
AUTHENTICATED_DAILY_LIMIT=5
GLOBAL_REQUESTS_PER_MINUTE=60
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_ai_engine.py::TestPromptBuilder -v
pytest tests/test_ai_engine.py::TestRateLimiter -v
pytest tests/test_ai_engine.py::TestIntegration -v

# Run with coverage
pytest tests/ --cov=app/services/ai_engine --cov-report=html
```

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Metrics (Prometheus)

```bash
curl http://localhost:8000/metrics
```

### Key Metrics to Monitor

- **Generation Success Rate**: Target >95%
- **Average Generation Time**: Target <60s
- **API Response Time**: Target <2s
- **Error Rate**: Target <5%
- **Rate Limit Hit Rate**: Monitor abuse

## 🔧 Engine Details

### Local SDXL Engine

**Best for:**
- Development and testing
- Maximum control
- No external dependencies
- Custom model training

**Requirements:**
- NVIDIA GPU (8GB+ VRAM recommended)
- PyTorch, Diffusers, Transformers
- ~10GB disk space for models

**Performance:**
- ~30 seconds per generation
- 3 variations per request
- 512x512 to 1024x1024 resolution

### Replicate Engine

**Best for:**
- Startups and SMBs
- Quick deployment
- Predictable costs
- High availability

**Requirements:**
- Replicate API token
- Internet connection
- ~$0.05 per generation

**Performance:**
- ~45 seconds per generation
- Queue-based processing
- Up to 1024x1024 resolution

### HF Inference Engine

**Best for:**
- Enterprise scale
- High throughput
- Custom endpoints
- Data privacy

**Requirements:**
- HuggingFace account
- Dedicated endpoints
- ~$0.60/hour per endpoint

**Performance:**
- ~20 seconds per generation
- Concurrent processing
- Up to 1536x1536 resolution

## 🎨 Prompt Engineering

The system uses optimized prompts for interior design:

### Positive Prompt Template
```
Photorealistic architectural interior transformation of an empty {room_type}.
Preserve original room geometry, wall positions, and perspective exactly.
Add realistic {furniture_style} furnishing that fits the space naturally.
Walls painted {wall_color}. Flooring: {flooring_material}.
Maintain realistic scale, proper furniture placement, natural lighting interaction.
Ultra realistic, high detail, professional architectural photography.
```

### Negative Prompt
```
distorted perspective, warped walls, broken geometry, floating furniture,
unrealistic proportions, deformed objects, low resolution, blurry,
text, watermark, duplicate objects, extra windows, doors in wrong places,
furniture clipping through walls, cartoon, illustration, painting.
```

## 🔒 Security & Cost Control

### Rate Limiting
- **Free Users**: 3 generations/day
- **Authenticated Users**: 5 generations/day
- **Premium Users**: 20 generations/day
- **Admin Users**: 100 generations/day

### Cost Management
- Per-user generation quotas
- Global throttling
- Usage tracking and analytics
- Cost alerts and budgets

### Security Measures
- Input validation and sanitization
- File upload restrictions
- API authentication
- Rate limiting by IP and user

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements-ai.txt .
RUN pip install -r requirements-ai.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-engine
  template:
    metadata:
      labels:
        app: ai-engine
    spec:
      containers:
      - name: ai-engine
        image: antaraalay/ai-engine:latest
        ports:
        - containerPort: 8000
        env:
        - name: AI_ENGINE
          value: "replicate"
        - name: REPLICATE_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: replicate-token
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: [Full Production Guide](docs/PRODUCTION_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/your-org/antaraalay-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/antaraalay-ai/discussions)

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Additional ControlNet models (Depth, Normal)
- [ ] Style transfer capabilities
- [ ] Batch processing
- [ ] Advanced caching

### Version 1.2 (Planned)
- [ ] Custom model fine-tuning
- [ ] Real-time generation
- [ ] Mobile optimization
- [ ] Multi-language support

### Version 2.0 (Future)
- [ ] 3D room reconstruction
- [ ] AR/VR integration
- [ ] Furniture placement AI
- [ ] Material simulation

---

Built with ❤️ by the AntarAalay.ai team
