# AntarAalay.ai Documentation

## 📚 Documentation Structure

### 📋 Guides (`docs/guides/`)
- **[GTX 1650 Production Guide](guides/GTX1650_PRODUCTION_GUIDE.md)** - Complete setup and deployment guide for GTX 1650

### 🔌 API Documentation (`docs/api/`)
- API endpoints documentation (coming soon)

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python run_tests.py

# Run only unit tests
python run_tests.py --unit

# Run only integration tests  
python run_tests.py --integration

# Run only engine tests
python run_tests.py --engine
```

### Test Structure
- **Unit Tests** (`tests/unit/`) - Test individual components
- **Integration Tests** (`tests/integration/`) - Test full workflows

## 🛠️ Setup Scripts

### Setup Scripts (`scripts/setup/`)
- **[setup_gtx1650.py](../scripts/setup/setup_gtx1650.py)** - Automated setup for GTX 1650
- **[setup_local_interior_engine.py](../scripts/setup/setup_local_interior_engine.py)** - Setup for local interior design models

## ⚙️ Configuration

### Environment Configs (`config/`)
- `env-gtx1650.txt` - GTX 1650 optimized configuration
- `env-local-open-source.txt` - Local open-source model configuration
- `env-interior-design-specific.txt` - Interior design specific configuration
- `env-free-state-of-the-art.txt` - Free state-of-the-art configuration
- `env-state-of-the-art.txt` - State-of-the-art configuration

## 🏗️ Project Structure

```
backend/
├── app/                    # Main application code
│   ├── services/ai_engine/ # AI engine implementations
│   ├── routes/            # API endpoints
│   └── models/            # Database models
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docs/                 # Documentation
│   ├── guides/           # User guides
│   └── api/              # API documentation
├── scripts/              # Utility scripts
│   └── setup/            # Setup scripts
├── config/               # Configuration files
└── storage/              # Local storage
```

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   python scripts/setup/setup_gtx1650.py
   ```

2. **Configure**
   ```bash
   cp config/env-gtx1650.txt .env
   ```

3. **Run Tests**
   ```bash
   python run_tests.py --engine
   ```

4. **Start Server**
   ```bash
   python -m uvicorn main:app --reload
   ```

## 📖 More Information

- [GTX 1650 Production Guide](guides/GTX1650_PRODUCTION_GUIDE.md) - Complete deployment guide
- [Test Documentation](../tests/README.md) - Testing framework details
- [API Documentation](api/) - API endpoints and usage
