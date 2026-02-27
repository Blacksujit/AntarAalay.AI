from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import get_db_manager, Base
from app.routes import room, design, vastu  # ar temporarily disabled
from app.api import dashboard
from app.config import get_settings
from app.services import firebase_client

settings = get_settings()

# Get database engine from manager
db_manager = get_db_manager()
engine = db_manager.engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AntarAalay AI API",
    description="AI-powered interior design and Vastu consultation API",
    version="1.0.0"
)

# Simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Backend is running"}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
    return response

# Add request logging middleware
import time
@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    print(f"➡️  {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        duration = time.time() - start
        print(f"⬅️  {request.method} {request.url.path} - {response.status_code} ({duration:.2f}s)")
        return response
    except Exception as e:
        print(f"❌ {request.method} {request.url.path} - ERROR: {e}")
        raise

# Include routers
app.include_router(room.router, prefix="/api")
app.include_router(design.router, prefix="/api")
app.include_router(vastu.router, prefix="/api")
# app.include_router(ar.router)  # Temporarily disabled due to missing models
app.include_router(dashboard.router, prefix="/api")

# Create uploads directory if it doesn't exist
import os
os.makedirs("uploads", exist_ok=True)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


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
