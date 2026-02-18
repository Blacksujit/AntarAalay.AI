# AI Interior Styling Engine - Production Deployment Guide

## Overview

This guide covers production deployment of the AntarAalay.ai AI Interior Styling Engine with state-of-the-art image-to-image transformation and layout preservation.

## Architecture

### Engine Strategy Pattern
- **Local SDXL**: Development and testing with local GPU
- **Replicate**: Production with hosted API
- **HF Inference**: Production with dedicated endpoints

### Core Components
1. **BaseEngine**: Abstract interface for all AI engines
2. **PromptBuilder**: Optimized prompts for interior styling
3. **ControlNetAdapter**: Edge detection for layout preservation
4. **RateLimiter**: Per-user quotas and cost control
5. **AIDesignService**: Complete workflow orchestration

## Environment Configuration

### Development Environment (.env.development)
```bash
# Engine Configuration
AI_ENGINE=local_sdxl
DEVICE=cuda
DETERMINISTIC_GENERATION=true

# Local SDXL Configuration
SDXL_MODEL_PATH=stabilityai/stable-diffusion-xl-base-1.0
CONTROLNET_MODEL=lllyasviel/sd-controlnet-canny
MAX_RESOLUTION=512,512
AI_TIMEOUT_SECONDS=120

# Rate Limiting (Development - More Lenient)
FREE_DAILY_LIMIT=10
AUTHENTICATED_DAILY_LIMIT=20
GLOBAL_REQUESTS_PER_MINUTE=30
```

### Production Environment (.env.production)
```bash
# Engine Configuration
AI_ENGINE=replicate
DETERMINISTIC_GENERATION=false

# Replicate Configuration
REPLICATE_API_TOKEN=your_replicate_token_here

# Rate Limiting (Production - Strict)
FREE_DAILY_LIMIT=3
AUTHENTICATED_DAILY_LIMIT=5
PREMIUM_DAILY_LIMIT=20
ADMIN_DAILY_LIMIT=100
GLOBAL_REQUESTS_PER_MINUTE=60
GLOBAL_REQUESTS_PER_HOUR=500
BLOCK_DURATION_MINUTES=60

# Performance
AI_TIMEOUT_SECONDS=60
MAX_RESOLUTION=1024,1024

# Monitoring
LOG_LEVEL=INFO
METRICS_ENABLED=true
```

### Enterprise Environment (.env.enterprise)
```bash
# Engine Configuration
AI_ENGINE=hf_inference

# HuggingFace Configuration
HF_API_KEY=your_hf_api_key_here
HF_ENDPOINT_URL=https://your-endpoint.runpod.cloud/v1
HF_MODEL_NAME=stabilityai/stable-diffusion-xl-base-1.0

# Rate Limiting (Enterprise - High Volume)
FREE_DAILY_LIMIT=5
AUTHENTICATED_DAILY_LIMIT=10
PREMIUM_DAILY_LIMIT=50
ADMIN_DAILY_LIMIT=500
GLOBAL_REQUESTS_PER_MINUTE=120
GLOBAL_REQUESTS_PER_HOUR=2000

# Performance
AI_TIMEOUT_SECONDS=45
MAX_RESOLUTION=1536,1536
```

## Model Deployment Options

### Option 1: Replicate (Recommended for Startups)
**Pros:**
- No infrastructure management
- Pay-per-use pricing
- Easy scaling
- High availability

**Cons:**
- Less control over models
- Potential queue times
- Cost at scale

**Setup:**
1. Create Replicate account
2. Add API token to environment
3. Set `AI_ENGINE=replicate`

**Expected Cost:** ~$0.05 per generation

### Option 2: HuggingFace Inference Endpoints (Recommended for Scale)
**Pros:**
- Dedicated endpoints
- Better performance
- More control
- Predictable costs

**Cons:**
- Infrastructure management
- Higher fixed costs
- Requires monitoring

**Setup:**
1. Deploy SDXL + ControlNet to HF Endpoints
2. Configure endpoint URL
3. Set `AI_ENGINE=hf_inference`

**Expected Cost:** ~$0.60/hour per endpoint

### Option 3: Self-Hosted (Enterprise Only)
**Pros:**
- Full control
- Maximum privacy
- Custom models
- Lowest marginal cost

**Cons:**
- High infrastructure cost
- Complex maintenance
- Requires ML expertise

**Setup:**
1. Deploy to Kubernetes/GPU cluster
2. Set up load balancing
3. Configure monitoring
4. Set `AI_ENGINE=local_sdxl`

## Infrastructure Requirements

### Minimum Requirements (Replicate)
- **CPU:** 2 cores
- **RAM:** 4GB
- **Storage:** 50GB SSD
- **Network:** 100Mbps

### Recommended Requirements (HF Endpoints)
- **CPU:** 4 cores
- **RAM:** 8GB
- **Storage:** 100GB SSD
- **Network:** 1Gbps

### Enterprise Requirements (Self-Hosted)
- **GPU:** NVIDIA A100/V100
- **CPU:** 16 cores
- **RAM:** 64GB
- **Storage:** 500GB NVMe
- **Network:** 10Gbps

## Deployment Steps

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/your-org/antaraalay-ai.git
cd antaraalay-ai/backend

# Install dependencies
pip install -r requirements.txt

# Install ML dependencies (for local development)
pip install diffusers transformers accelerate torch torchvision

# Copy environment template
cp .env.production .env
# Edit .env with your configuration
```

### 2. Database Setup
```bash
# Initialize SQLite database
python -c "from app.database import init_db; init_db()"

# Or use PostgreSQL for production
DATABASE_URL=postgresql://user:pass@localhost:antaraalay
```

### 3. Storage Setup
```bash
# Create uploads directory
mkdir -p uploads/generated/designs
mkdir -p uploads/users

# Set proper permissions
chmod 755 uploads
```

### 4. Start Application
```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Monitoring and Observability

### Key Metrics
- **Generation Success Rate:** Target >95%
- **Average Generation Time:** Target <60s
- **API Response Time:** Target <2s
- **Error Rate:** Target <5%
- **Rate Limit Hit Rate:** Monitor abuse

### Monitoring Setup
```python
# Add to main.py
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
generation_counter = Counter('ai_generations_total', ['engine', 'status'])
generation_duration = Histogram('ai_generation_duration_seconds')
rate_limit_counter = Counter('rate_limit_exceeded_total', ['user_type'])

# Add endpoints
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Logging Configuration
```python
# production logging config
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["default", "file"],
    },
}
```

## Security Considerations

### API Security
- Use HTTPS in production
- Implement API key authentication
- Rate limit by IP and user
- Validate all inputs
- Sanitize file uploads

### Cost Control
- Set strict rate limits
- Monitor API usage
- Implement cost alerts
- Use quotas per user
- Track generation costs

### Data Privacy
- Store images securely
- Implement data retention policies
- Use encrypted storage
- Consider GDPR compliance
- Allow user data deletion

## Performance Optimization

### Caching Strategy
```python
# Cache ControlNet edge maps
@lru_cache(maxsize=1000)
def get_cached_edge_map(image_hash: str) -> bytes:
    # Generate or retrieve cached edge map
    pass

# Cache prompt hashes
@lru_cache(maxsize=500)
def get_cached_prompt(style_params_hash: str) -> str:
    # Generate or retrieve cached prompt
    pass
```

### Load Balancing
```nginx
# nginx configuration
upstream ai_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://ai_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Database Optimization
```sql
-- Add indexes for performance
CREATE INDEX idx_designs_user_room ON designs(user_id, room_id);
CREATE INDEX idx_designs_created_at ON designs(created_at DESC);
CREATE INDEX idx_usage_user_date ON usage(user_id, date);
```

## Scaling Strategy

### Horizontal Scaling
- Deploy multiple app instances
- Use load balancer
- Share storage via network file system
- Use external database

### Vertical Scaling
- Increase GPU memory for local engines
- Add more CPU cores
- Increase RAM for caching
- Use faster storage

### Geographic Scaling
- Deploy to multiple regions
- Use CDN for static assets
- Region-specific API endpoints
- Data replication considerations

## Testing in Production

### Canary Deployment
1. Deploy new version to subset of servers
2. Monitor error rates and performance
3. Gradually increase traffic
4. Full rollout after validation

### A/B Testing
- Test different prompts
- Compare engine performance
- Measure user satisfaction
- Optimize generation parameters

## Troubleshooting

### Common Issues
1. **GPU Memory Errors**: Reduce batch size or resolution
2. **API Timeouts**: Increase timeout or optimize models
3. **Rate Limiting**: Adjust quotas or implement caching
4. **Storage Issues**: Check disk space and permissions

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Test engine health
curl http://localhost:8000/health

# Check rate limits
curl http://localhost:8000/api/rate-limit/status
```

## Backup and Recovery

### Data Backup
```bash
# Database backup
pg_dump antaraalay > backup_$(date +%Y%m%d).sql

# File storage backup
rsync -av uploads/ backup/uploads_$(date +%Y%m%d)/
```

### Disaster Recovery
1. Maintain off-site backups
2. Document recovery procedures
3. Test recovery regularly
4. Have rollback plan

## Cost Management

### Cost Optimization
- Use appropriate engine for workload
- Implement smart caching
- Optimize generation parameters
- Monitor and eliminate waste

### Budget Planning
- Track per-generation costs
- Set monthly budgets
- Implement cost alerts
- Plan for scaling costs

## Support and Maintenance

### Regular Tasks
- Monitor system performance
- Update models and dependencies
- Review rate limit settings
- Analyze usage patterns

### Emergency Procedures
- Service outage response
- Data breach procedures
- Performance degradation handling
- Customer escalation process
