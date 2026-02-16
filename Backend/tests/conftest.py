"""
Pytest configuration and fixtures for AntarAalay.ai Backend tests
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import Mock, patch
import tempfile
import os

from main import app
from app.services.firebase_client import initialize_firebase
from app.services.stability_engine import StabilityEngine


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client():
    """Create an async test client for the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_firebase():
    """Mock Firebase services for testing."""
    with patch('app.services.firebase_client.initialize_firebase') as mock_init:
        mock_app = Mock()
        mock_init.return_value = mock_app
        
        with patch('app.services.firebase_client.get_firestore') as mock_firestore:
            mock_fs = Mock()
            mock_firestore.return_value = mock_fs
            
            with patch('app.services.firebase_client.get_firebase_storage') as mock_storage:
                mock_storage_service = Mock()
                mock_storage.return_value = mock_storage_service
                
                yield {
                    'app': mock_app,
                    'firestore': mock_fs,
                    'storage': mock_storage_service
                }


@pytest.fixture
def mock_stability_engine():
    """Mock Stability AI engine for testing."""
    with patch('app.services.stability_engine.get_stability_engine') as mock_get:
        mock_engine = Mock(spec=StabilityEngine)
        mock_get.return_value = mock_engine
        
        # Mock successful generation
        mock_engine.generate_designs.return_value = asyncio.Future()
        mock_engine.generate_designs.return_value.set_result(Mock(
            success=True,
            image_urls=[
                "https://example.com/design1.jpg",
                "https://example.com/design2.jpg", 
                "https://example.com/design3.jpg"
            ],
            prompt_used="Modern interior design with clean lines"
        ))
        
        yield mock_engine


@pytest.fixture
def sample_room_data():
    """Sample room data for testing."""
    return {
        "id": "test-room-123",
        "name": "Test Living Room",
        "user_id": "test-user-456",
        "images": {
            "north": "https://example.com/north.jpg",
            "south": "https://example.com/south.jpg",
            "east": "https://example.com/east.jpg",
            "west": "https://example.com/west.jpg"
        },
        "created_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_design_data():
    """Sample design data for testing."""
    return {
        "id": "test-design-789",
        "room_id": "test-room-123",
        "user_id": "test-user-456",
        "style": "modern",
        "customization": {
            "wall_color": "white",
            "flooring": "hardwood",
            "furniture_style": "minimal"
        },
        "prompt_used": "Modern interior design with clean lines",
        "generated_images": [
            "https://example.com/design1.jpg",
            "https://example.com/design2.jpg",
            "https://example.com/design3.jpg"
        ],
        "version": 1,
        "created_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def mock_user_token():
    """Mock Firebase user token for testing."""
    return {
        "uid": "test-user-456",
        "email": "test@example.com",
        "localId": "test-user-456"
    }


@pytest.fixture
def temp_image_files():
    """Create temporary image files for testing uploads."""
    temp_files = []
    
    for direction in ['north', 'south', 'east', 'west']:
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            # Write minimal JPEG header
            tmp.write(b'\xff\xd8\xff\xe0\x00\x10JFIF')
            tmp.write(b'\x00' * 100)  # Some dummy data
            tmp.flush()
            temp_files.append(tmp.name)
    
    yield temp_files
    
    # Cleanup
    for file_path in temp_files:
        if os.path.exists(file_path):
            os.unlink(file_path)


@pytest.fixture
def mock_upload_files(temp_image_files):
    """Mock UploadFile objects for testing."""
    from fastapi import UploadFile
    
    files = {}
    directions = ['north', 'south', 'east', 'west']
    
    for i, direction in enumerate(directions):
        with open(temp_image_files[i], 'rb') as f:
            files[direction] = UploadFile(
                filename=f"{direction}.jpg",
                file=f,
                content_type="image/jpeg"
            )
    
    return files
