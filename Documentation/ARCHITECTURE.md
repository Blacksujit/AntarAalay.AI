# AntarAalay.ai - Paper Architecture Definition
## Phase 0: System Design Document

**Version**: 1.0  
**Date**: Feb 15, 2026  
**Status**: Draft

---

## 1. System Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  React + TypeScript + Vite                                                  │
│  ├── Auth Module (Firebase Auth)                                             │
│  ├── Upload Module (Drag/Drop + Validation)                                  │
│  ├── Design Module (Display + Compare)                                       │
│  └── Vastu Module (Analysis + Score Display)                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTPS + JWT Bearer
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER (FastAPI)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ├── Routes (Room, Design, Vastu, Auth)                                      │
│  ├── Schemas (Pydantic validation)                                           │
│  └── Dependencies (JWT validation, DB session injection)                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SERVICE LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ├── StorageService    → AWS S3 (Images)                                     │
│  ├── AIEngine          → Stability AI (Stable Diffusion)                     │
│  ├── VastuEngine       → Internal Rules + External API                       │
│  └── BudgetEngine      → Price calculations                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PERSISTENCE LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  Supabase PostgreSQL                                                          │
│  ├── Users (Firebase UID, email, profile)                                    │
│  ├── Rooms (image_url, type, direction, user_id)                             │
│  └── Designs (generated images, budget, vastu_score, status)                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Flow

### Flow 1: Upload → Generate → Return

```
1. User uploads room image
   └─→ Frontend: Drag/drop validation
       └─→ POST /api/room/upload
           └─→ Route: validate file (type, size)
               └─→ Service: StorageService.upload_image()
                   └─→ AWS S3: Store image
               └─→ Model: Room.create() → DB
           └─→ Response: { room_id, image_url }

2. User requests design generation
   └─→ POST /api/design/generate
       └─→ Route: validate room_id, style, budget
           └─→ Background Task:
               ├─→ Service: AIEngine.generate(room_image, style)
               │   └─→ External: Stability AI API
               │       └─→ Returns: 3 image URLs
               ├─→ Service: BudgetEngine.calculate(room_type, style, budget)
               │   └─→ Returns: estimated_cost, breakdown
               └─→ Service: VastuEngine.analyze(direction, room_type)
                   └─→ Returns: vastu_score, suggestions, warnings
           └─→ Model: Design.create() → DB
           └─→ Response: { design_id, status: "pending" }

3. User polls/fetches designs
   └─→ GET /api/design/room/{room_id}
       └─→ Route: validate room ownership
           └─→ Model: Design.query() → DB
           └─→ Response: [{ design_id, images, budget, vastu_score }]
```

### Flow 2: Vastu Analysis

```
1. User requests Vastu analysis
   └─→ POST /api/vastu/analyze
       └─→ Route: validate direction, room_type
           └─→ Service: VastuEngine.analyze()
               ├─→ Internal: VastuRules.get_score(direction, room_type)
               └─→ External: AstrologyAPI.com (optional)
           └─→ Response: { vastu_score, suggestions, warnings, rating }
```

---

## 3. Domain Models

### 3.1 User

```python
class User:
    id: str (Firebase UID, PK)
    email: str (unique, indexed)
    name: str (nullable)
    photo_url: str (nullable)
    created_at: datetime
    updated_at: datetime
    
    Relationships:
    - rooms: List[Room] (one-to-many)
    - designs: List[Design] (one-to-many)
```

### 3.2 Room

```python
class Room:
    id: str (UUID, PK)
    user_id: str (FK → User.id, indexed)
    image_url: str (S3 URL, required)
    room_type: str (enum: bedroom, living, kitchen, dining, study, bathroom)
    direction: str (enum: north, south, east, west, northeast, northwest, southeast, southwest)
    created_at: datetime
    updated_at: datetime
    
    Relationships:
    - user: User (many-to-one)
    - designs: List[Design] (one-to-many)
    
    Constraints:
    - image_url NOT NULL
    - user_id NOT NULL
```

### 3.3 Design

```python
class Design:
    id: str (UUID, PK)
    room_id: str (FK → Room.id, indexed)
    user_id: str (FK → User.id, indexed)
    style: str (required)
    budget: float (nullable)
    
    # Generated Images
    image_1_url: str (nullable)
    image_2_url: str (nullable)
    image_3_url: str (nullable)
    
    # Budget Breakdown
    estimated_cost: float (nullable)
    budget_match_percentage: float (nullable)
    furniture_breakdown: JSON (nullable)
    
    # Vastu Analysis
    vastu_score: float (nullable, 0-100)
    vastu_suggestions: List[str] (JSON, nullable)
    vastu_warnings: List[str] (JSON, nullable)
    
    # Status
    status: str (enum: pending, completed, failed, default: pending)
    
    created_at: datetime
    updated_at: datetime
    
    Relationships:
    - room: Room (many-to-one)
    - user: User (many-to-one)
```

### 3.4 BudgetBreakdown (Schema)

```python
class BudgetBreakdown:
    estimated_cost: float
    budget: float (nullable)
    budget_match_percentage: float (nullable)
    furniture_breakdown: Dict[str, FurnitureItem]
    style_multiplier: float
    
class FurnitureItem:
    base_price: float
    adjusted_price: float
    quantity: int
```

### 3.5 VastuReport (Schema)

```python
class VastuReport:
    vastu_score: float (0-100)
    suggestions: List[str]
    warnings: List[str]
    direction_rating: str (enum: excellent, good, neutral, poor)
    element_balance: Dict:
        - dominant_element: str (Water, Fire, Air, Earth, Space)
        - ruling_planet: str
        - balance_status: str
```

---

## 4. API Contracts (OpenAPI Spec Summary)

### 4.1 Standard Response Format

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2026-02-15T12:00:00Z",
    "request_id": "uuid"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error_code": "ERROR_CODE",
  "message": "Human readable message",
  "details": {},
  "meta": {
    "timestamp": "2026-02-15T12:00:00Z",
    "request_id": "uuid"
  }
}
```

### 4.2 Endpoints

#### POST /api/room/upload
**Request:**
```
Content-Type: multipart/form-data

file: File (image/jpeg, image/png, image/webp)
room_type: string (optional)
direction: string (optional)
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "room_id": "uuid",
    "image_url": "https://s3.amazonaws.com/...",
    "message": "Room image uploaded successfully"
  }
}
```

**Error Responses:**
- 400: INVALID_FILE_TYPE, FILE_TOO_LARGE
- 401: UNAUTHORIZED
- 500: UPLOAD_FAILED

#### POST /api/design/generate
**Request:**
```json
{
  "room_id": "uuid",
  "style": "modern",
  "budget": 50000
}
```

**Success Response (202):**
```json
{
  "success": true,
  "data": {
    "design_id": "uuid",
    "status": "pending",
    "message": "Design generation started"
  }
}
```

**Error Responses:**
- 400: INVALID_ROOM_ID, INVALID_STYLE
- 401: UNAUTHORIZED
- 404: ROOM_NOT_FOUND

#### GET /api/design/room/{room_id}
**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "designs": [
      {
        "id": "uuid",
        "style": "modern",
        "image_1_url": "url",
        "image_2_url": "url",
        "image_3_url": "url",
        "estimated_cost": 45000,
        "budget_match_percentage": 90,
        "vastu_score": 85,
        "status": "completed"
      }
    ],
    "total": 1
  }
}
```

#### POST /api/vastu/analyze
**Request:**
```json
{
  "direction": "north",
  "room_type": "bedroom"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "vastu_score": 40,
    "suggestions": ["..."],
    "warnings": ["..."],
    "direction_rating": "poor",
    "element_balance": {
      "dominant_element": "Water",
      "ruling_planet": "Mercury",
      "balance_status": "needs_attention"
    }
  }
}
```

---

## 5. Error Contract Standard

### Error Codes by Category

**Authentication (4xx):**
```
UNAUTHORIZED          - 401 - Missing or invalid token
TOKEN_EXPIRED         - 401 - JWT token expired
FORBIDDEN             - 403 - Valid token, insufficient permissions
```

**Client Errors (4xx):**
```
INVALID_FILE_TYPE     - 400 - File type not in [jpeg, png, webp]
FILE_TOO_LARGE        - 400 - File > 10MB
INVALID_ROOM_ID       - 400 - Room ID format invalid
ROOM_NOT_FOUND        - 404 - Room doesn't exist or not owned
INVALID_STYLE         - 400 - Style not in allowed list
INVALID_DIRECTION     - 400 - Direction not in Vastu rules
VALIDATION_ERROR      - 400 - Pydantic validation failed
```

**Server Errors (5xx):**
```
UPLOAD_FAILED         - 500 - S3 upload error
AI_GENERATION_FAILED  - 500 - Stability AI API error
DATABASE_ERROR        - 500 - SQLAlchemy error
VASTU_ANALYSIS_FAILED - 500 - Vastu engine error
INTERNAL_ERROR        - 500 - Unhandled exception
```

### Error Response Format
```json
{
  "success": false,
  "error_code": "ROOM_NOT_FOUND",
  "message": "Room not found or access denied",
  "details": {
    "room_id": "invalid-uuid",
    "user_id": "user-123"
  },
  "meta": {
    "timestamp": "2026-02-15T12:00:00Z",
    "request_id": "req-uuid",
    "path": "/api/design/generate"
  }
}
```

---

## 6. Module Interface Contracts

### 6.1 Configuration Module
```python
class Settings:
    # Properties
    DATABASE_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET_NAME: str
    FIREBASE_PROJECT_ID: str
    STABLE_DIFFUSION_API_KEY: str
    
    # Methods
    def validate_required() -> bool: ...
```

### 6.2 Storage Service
```python
class StorageService:
    # Methods
    def upload_image(file_content: bytes, content_type: str, folder: str) -> str: ...
    def delete_image(image_url: str) -> bool: ...
    def generate_signed_url(key: str, expiration: int) -> str: ...
    
    # Exceptions
    raises StorageUploadError, InvalidContentTypeError
```

### 6.3 AI Engine
```python
class AIEngine:
    # Methods
    def generate_design_variations(
        room_image_url: str,
        style: str,
        room_type: str
    ) -> List[str]: ...
    
    def analyze_room_image(image_url: str) -> RoomAnalysis: ...
    
    # Exceptions
    raises AIAPIError, TimeoutError, InvalidResponseError
```

### 6.4 Vastu Engine
```python
class VastuEngine:
    # Methods
    def analyze(direction: str, room_type: str) -> VastuReport: ...
    def get_remedies(direction: str, room_type: str) -> List[str]: ...
    def get_direction_info(direction: str) -> DirectionInfo: ...
    
    # Exceptions
    raises InvalidDirectionError, VastuAPIError
```

### 6.5 Budget Engine
```python
class BudgetEngine:
    # Methods
    def calculate_estimate(
        room_type: str,
        style: str,
        budget: Optional[float]
    ) -> BudgetBreakdown: ...
    
    def get_style_suggestions(budget: float, room_type: str) -> List[str]: ...
```

---

## 7. Testing Strategy

### Unit Tests (Every Module)
- Configuration loading and validation
- Database connection and transactions
- Model constraints and relationships
- Service logic with mocked dependencies
- Route validation and response format

### Integration Tests (Flow Level)
- Upload → Generate → Fetch
- Vastu analysis end-to-end
- Error handling and rollback
- Authentication flow

### Test Data
- Use test database (SQLite or isolated Postgres schema)
- Mock all external APIs (S3, Stability AI, Vastu API)
- Use pytest fixtures for common setup

---

## 8. Acceptance Criteria

### Module Completion Checklist
- [ ] Code follows PEP8
- [ ] Type hints on all public methods
- [ ] Unit tests with >80% coverage
- [ ] Docstrings for all classes/functions
- [ ] No external dependencies in unit tests (mocked)
- [ ] Error handling follows Error Contract

### Integration Completion Checklist
- [ ] All API endpoints return correct format
- [ ] Authentication flow works end-to-end
- [ ] Image upload → S3 → URL flow works
- [ ] AI generation (mocked) creates design records
- [ ] Vastu analysis returns valid scores
- [ ] Database transactions roll back on errors

---

## Next Steps

1. **Phase 1**: Build Module 1 (Configuration) with tests
2. Run tests, fix issues
3. **Phase 1**: Build Module 2 (Database) with tests
4. Continue through all 8 modules
5. **Phase 2**: Integration testing
6. **Phase 3**: Frontend modules
7. **Phase 4**: System validation
8. **Phase 5**: Deployment

DO NOT proceed to code without understanding this architecture.
DO NOT skip tests for any module.
BUILD CLEANLY. TEST THOROUGHLY.
