from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db_manager, Base
from app.routes import room, design, vastu
from app.config import get_settings

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
app.include_router(room.router)
app.include_router(design.router)
app.include_router(vastu.router)


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
