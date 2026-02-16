from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db_manager, Base
from app.routes import room, design, vastu
from app.config import get_settings
from app.services import firebase_client

settings = get_settings()

# Get database engine from manager
db_manager = get_db_manager()
engine = db_manager.engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered interior design platform with Vastu integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(room.router, prefix="/api")
app.include_router(design.router, prefix="/api")
app.include_router(vastu.router, prefix="/api")


@app.get("/api/mock-storage/{bucket}/{path:path}")
async def get_mock_storage_object(bucket: str, path: str):
    """Serve mock Firebase Storage objects when running in MOCK mode."""
    store = getattr(firebase_client, "_mock_blob_store", None)
    if not isinstance(store, dict):
        raise HTTPException(status_code=404, detail="Mock storage not available")

    bucket_store = store.get(bucket)
    if not isinstance(bucket_store, dict):
        raise HTTPException(status_code=404, detail="Bucket not found")

    data = bucket_store.get(path)
    if data is None:
        raise HTTPException(status_code=404, detail="Object not found")

    return Response(content=data, media_type="image/jpeg")


@app.get("/")
async def root():
    return {
        "message": "Welcome to AntarAalay.ai API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
