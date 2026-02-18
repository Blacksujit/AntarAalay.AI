# Test Suite for AntarAalay.ai Backend

## 🧪 Test Structure

### Unit Tests (`unit/`)
Test individual components in isolation:

- **`test_gtx1650_config.py`** - GTX 1650 configuration validation
- **`test_sd15_controlnet.py`** - SD15 ControlNet engine tests
- **`test_ai_engine.py`** - Core AI engine functionality
- **`test_engine_no_token.py`** - Engine behavior without API tokens
- **`test_hf_engine.py`** - HuggingFace engine tests
- **`test_free_engine.py`** - Free model engine tests
- **`test_interior_specific.py`** - Interior design specific engine tests
- **`test_local_open_source.py`** - Local open-source engine tests
- **`test_real_token.py`** - Real API token tests
- **`test_state_of_the_art.py`** - State-of-the-art engine tests

### Integration Tests (`integration/`)
Test full workflows and component interactions:

- **`test_design_generation.py`** - End-to-end design generation
- **`test_budget.py`** - Budget management integration
- **`test_config.py`** - Configuration integration
- **`test_database.py`** - Database operations
- **`test_engines.py`** - Multi-engine integration
- **`test_models.py`** - Database model integration
- **`test_room_routes.py`** - Room upload endpoints
- **`test_routes.py`** - General API routes
- **`test_storage.py`** - Storage system integration

## 🏃 Running Tests

### From Backend Root
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

### Individual Test Files
```bash
# Run a specific unit test
python tests/unit/test_gtx1650_config.py

# Run a specific integration test
python tests/integration/test_design_generation.py
```

## 📊 Test Categories

### Engine Tests
- Validate AI engine configurations
- Test model loading and health checks
- Verify memory optimizations
- Test prompt building and controlnet functionality

### API Tests
- Test endpoint functionality
- Validate request/response handling
- Test error scenarios
- Verify rate limiting

### Database Tests
- Test model operations
- Validate data integrity
- Test transaction handling
- Verify query performance

### Integration Tests
- Test complete workflows
- Validate component interactions
- Test error propagation
- Verify end-to-end functionality

## 🔧 Test Configuration

Tests use the following configuration:
- **Device**: CPU (for compatibility)
- **Models**: Mocked when not available
- **Database**: In-memory SQLite for isolation
- **Storage**: Temporary directories

## 📝 Writing New Tests

### Unit Test Template
```python
#!/usr/bin/env python3
"""
Test [Component Name]
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

def test_[function_name]():
    """Test [specific functionality]"""
    try:
        # Test implementation
        assert True, "Test passed"
        print("✅ test_[function_name] - PASSED")
    except Exception as e:
        print(f"❌ test_[function_name] - FAILED: {e}")

if __name__ == "__main__":
    test_[function_name]()
```

### Integration Test Template
```python
#!/usr/bin/env python3
"""
Test [Workflow Name]
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

async def test_[workflow_name]():
    """Test [specific workflow]"""
    try:
        # Test implementation
        assert True, "Test passed"
        print("✅ test_[workflow_name] - PASSED")
    except Exception as e:
        print(f"❌ test_[workflow_name] - FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_[workflow_name]())
```

## 🐛 Debugging Tests

### Common Issues
1. **Import Errors**: Ensure backend directory is in Python path
2. **Model Loading**: Tests use CPU by default, models may not be loaded
3. **Database**: Tests use isolated database instances
4. **File Paths**: Use absolute paths from backend directory

### Debug Mode
```bash
# Run with verbose output
python -v tests/unit/test_gtx1650_config.py

# Run with debugger
python -m pdb tests/unit/test_gtx1650_config.py
```

## 📈 Test Coverage

Current test coverage focuses on:
- ✅ AI Engine configurations
- ✅ Model loading and health checks
- ✅ API endpoint functionality
- ✅ Database operations
- ✅ Error handling
- ✅ Rate limiting

### Areas for Expansion
- Performance testing
- Load testing
- Security testing
- Cross-platform compatibility
