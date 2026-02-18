"""
Module 8: API Routes Tests

Test cases for all API routes using FastAPI TestClient.
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# Set up test environment BEFORE importing app
import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ENVIRONMENT"] = "testing"
os.environ["FIREBASE_PROJECT_ID"] = "test-project"

# Now import the FastAPI app
from main import app
from app.database import get_db, Base
from app.dependencies import get_current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Test database setup
@pytest.fixture
def test_db():
    """Create test database session."""
    from app.database import Base
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create test client with overridden dependencies."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    def override_get_current_user():
        return {
            "uid": "test_user_123",
            "localId": "test_user_123",
            "email": "test@example.com",
            "name": "Test User"
        }
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def unauth_client(test_db):
    """Create test client without auth override for testing auth failures."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "message" in response.json()
        assert "AntarAalay.ai" in response.json()["message"]
        
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestRoomRoutes:
    """Test room upload routes."""
    
    @patch('app.routes.room.room_upload_service')
    def test_upload_room_success(self, mock_room_service, client, test_db):
        """Test successful room image upload."""
        # Mock room upload service
        mock_room_service.upload_room_images = AsyncMock(return_value={
            "room_id": "room_123",
            "images": {
                "north": "https://storage.googleapis.com/test/north.jpg",
                "south": "https://storage.googleapis.com/test/south.jpg",
                "east": "https://storage.googleapis.com/test/east.jpg",
                "west": "https://storage.googleapis.com/test/west.jpg"
            }
        })
        
        # Create test files
        test_files = [
            ("north", ("north.jpg", b"fake-north-data", "image/jpeg")),
            ("south", ("south.jpg", b"fake-south-data", "image/jpeg")),
            ("east", ("east.jpg", b"fake-east-data", "image/jpeg")),
            ("west", ("west.jpg", b"fake-west-data", "image/jpeg"))
        ]
        
        response = client.post(
            "/api/room/upload",
            files=test_files
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "room_id" in data
        assert "images" in data
        
    def test_upload_room_without_auth(self, unauth_client):
        """Test upload without authentication fails."""
        test_files = [
            ("north", ("north.jpg", b"fake-north-data", "image/jpeg")),
            ("south", ("south.jpg", b"fake-south-data", "image/jpeg")),
            ("east", ("east.jpg", b"fake-east-data", "image/jpeg")),
            ("west", ("west.jpg", b"fake-west-data", "image/jpeg"))
        ]
        
        response = unauth_client.post(
            "/api/room/upload",
            files=test_files
        )
        
        # Should require authentication - FastAPI returns 401 for missing auth
        assert response.status_code == 401


class TestVastuRoutes:
    """Test Vastu analysis routes."""
    
    def test_analyze_vastu_success(self, client):
        """Test Vastu analysis endpoint."""
        response = client.post(
            "/api/vastu/analyze",
            json={"direction": "north", "room_type": "living"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "vastu_score" in data
        assert "suggestions" in data
        
    def test_analyze_vastu_invalid_direction(self, client):
        """Test Vastu analysis with invalid direction."""
        response = client.post(
            "/api/vastu/analyze",
            json={"direction": "invalid", "room_type": "living"}
        )
        
        assert response.status_code == 200
        
    def test_get_direction_info(self, client):
        """Test get direction info endpoint."""
        response = client.get("/api/vastu/direction/north")
        
        assert response.status_code == 200
        data = response.json()
        assert data["direction"] == "north"
        assert "ruling_element" in data
        
    def test_get_all_directions(self, client):
        """Test get all directions endpoint."""
        response = client.get("/api/vastu/directions")
        
        assert response.status_code == 200
        data = response.json()
        assert "directions" in data
        assert len(data["directions"]) == 8


class TestDesignRoutes:
    """Test design generation routes."""
    
    def test_generate_design_unauthorized(self, unauth_client):
        """Test design generation without auth fails."""
        response = unauth_client.post(
            "/api/design/generate",
            json={"room_id": "room-123", "style": "modern"}
        )
        
        assert response.status_code == 401


class TestErrorHandling:
    """Test API error handling."""
    
    def test_404_error(self, client):
        """Test 404 error for non-existent endpoint."""
        response = client.get("/api/nonexistent")
        
        assert response.status_code == 404
        
    def test_validation_error(self, client):
        """Test validation error for invalid request."""
        response = client.post(
            "/api/vastu/analyze",
            json={}  # Missing required fields
        )
        
        assert response.status_code == 422


# Run with: pytest tests/test_routes.py -v
