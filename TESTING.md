# AntarAalay.ai - Local Testing Guide

## Quick Start Commands

### 1. Backend Testing
```bash
cd Backend

# Run all backend tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_engines.py -v
python -m pytest tests/test_storage.py -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

### 2. Frontend Testing
```bash
cd Frontend

# Run all frontend tests
npm test

# Run tests once (CI mode)
npm run test:run

# Run specific test file
npx vitest run src/test/services/upload.test.ts
```

### 3. Start Development Servers

**Backend (Terminal 1):**
```bash
cd Backend
python -m uvicorn app.main:app --reload --port 8000
```
Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

**Frontend (Terminal 2):**
```bash
cd Frontend
npm run dev
```
Frontend runs at: http://localhost:5173

### 4. Environment Setup

**Backend `.env`:**
```
DATABASE_URL=sqlite:///./test.db
FIREBASE_PROJECT_ID=antaraalayai
FIREBASE_API_KEY=AIzaSyANQciKqx_Cyi92ahSVaLy_MewUDkZY3fg
ENVIRONMENT=development
DEBUG=true
```

**Frontend `.env`:**
```
VITE_FIREBASE_API_KEY=AIzaSyANQciKqx_Cyi92ahSVaLy_MewUDkZY3fg
VITE_FIREBASE_PROJECT_ID=antaraalayai
VITE_API_URL=http://localhost:8000
```

### 5. Test Specific Scenarios

**Test Vastu Analysis:**
```bash
curl http://localhost:8000/api/vastu/analyze \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"direction": "north", "room_type": "bedroom"}'
```

**Test Design Generation (mock):**
```bash
curl http://localhost:8000/api/design/generate \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"room_id": "test-room", "style": "modern", "budget": 50000}'
```

### 6. Docker Testing (Full Stack)
```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f backend
```

### 7. Debug Mode

**Enable verbose logging:**
```python
# In Backend/app/config.py
LOG_LEVEL = "DEBUG"
```

**Frontend debug:**
```bash
cd Frontend
npm run dev -- --debug
```

## Current Test Status

| Test Suite | Status | Count |
|------------|--------|-------|
| Backend Engines | ✅ PASS | 15/15 |
| Backend Storage | ✅ PASS | 8/8 |
| Frontend Upload | ✅ PASS | 4/4 |

**Run tests now:**
```bash
# Backend
cd Backend && python -m pytest tests/test_engines.py tests/test_storage.py -v

# Frontend  
cd Frontend && npm run test:run
```
