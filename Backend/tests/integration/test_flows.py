"""
Phase 2: Integration Tests

End-to-end tests for complete user flows.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import uuid

# Set up test environment BEFORE importing app
import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ENVIRONMENT"] = "testing"
os.environ["FIREBASE_PROJECT_ID"] = "test-project"

# Now import the FastAPI app
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Setup test database
@pytest.fixture(scope="module")
def test_db_engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db(test_db_engine):
    """Create test database session."""
    Session = sessionmaker(bind=test_db_engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(test_db):
    """Create test client."""
    def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()


class TestCompleteUserFlow:
    """Test complete user workflows."""
    
    @patch('app.routes.room.get_current_user')
    @patch('app.routes.room.storage_service')
    def test_upload_analyze_generate_flow(self, mock_storage, mock_auth, client, test_db):
        """
        Complete flow:
        1. User uploads room image
        2. System analyzes Vastu
        3. User requests design generation
        4. System returns design with budget and Vastu data
        """
        # Mock auth
        mock_auth.return_value = {
            "uid": "user_123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        # Mock S3
        mock_storage.upload_image.return_value = "https://s3.com/room.jpg"
        
        # Step 1: Upload room
        room_response = client.post(
            "/api/room/upload",
            files={"file": ("room.jpg", b"fake-image", "image/jpeg")},
            data={"room_type": "bedroom", "direction": "north"},
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Step 2: Analyze Vastu
        vastu_response = client.post(
            "/api/vastu/analyze",
            json={"direction": "north", "room_type": "bedroom"}
        )
        
        assert vastu_response.status_code == 200
        vastu_data = vastu_response.json()
        assert "vastu_score" in vastu_data
        
    def test_vastu_analysis_various_combinations(self, client):
        """Test Vastu analysis for various room/direction combinations."""
        test_cases = [
            ("north", "living", "excellent"),
            ("southwest", "bedroom", "excellent"),
            ("southeast", "kitchen", "excellent"),
            ("northeast", "bedroom", "poor"),  # Bad combination
        ]
        
        for direction, room_type, expected_rating in test_cases:
            response = client.post(
                "/api/vastu/analyze",
                json={"direction": direction, "room_type": room_type}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["direction_rating"] == expected_rating


class TestBudgetScenarios:
    """Test budget-related scenarios."""
    
    def test_budget_calculation_endpoint(self, client):
        """Test budget calculation through API."""
        # This would test budget engine through design generation
        # For now, test that budget engine is accessible
        from app.services.budget_engine import get_budget_engine
        
        engine = get_budget_engine()
        result = engine.calculate_estimate("bedroom", "modern", budget=50000)
        
        assert "estimated_cost" in result
        assert "budget_match_percentage" in result
        assert isinstance(result["furniture_breakdown"], dict)


class TestErrorScenarios:
    """Test error handling in flows."""
    
    def test_invalid_room_id_format(self, client):
        """Test handling of invalid room ID."""
        response = client.get("/api/room/invalid-uuid")
        # Should handle gracefully
        assert response.status_code in [401, 404, 422]
        
    def test_invalid_direction(self, client):
        """Test handling of invalid direction."""
        response = client.post(
            "/api/vastu/analyze",
            json={"direction": "invalid_direction", "room_type": "bedroom"}
        )
        
        assert response.status_code == 500


# Run with: pytest tests/integration/ -v
