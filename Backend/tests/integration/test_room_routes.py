"""
Test suite for Room API routes
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
import json

from main import app
from app.dependencies import get_current_user


class TestRoomRoutes:
    """Test cases for room upload and retrieval endpoints"""

    def test_upload_room_success(self, client, mock_firebase, mock_user_token, temp_image_files):
        """Test successful room upload with all 4 images"""
        app.dependency_overrides[get_current_user] = lambda: mock_user_token
        try:
            with patch('app.routes.room.room_upload_service.upload_room_images', new=AsyncMock()) as mock_upload:
                mock_upload.return_value = {
                    "room_id": "test-room-123",
                    "status": "success",
                    "message": "Room uploaded successfully"
                }
                
                with open(temp_image_files[0], 'rb') as north, \
                     open(temp_image_files[1], 'rb') as south, \
                     open(temp_image_files[2], 'rb') as east, \
                     open(temp_image_files[3], 'rb') as west:
                    
                    response = client.post(
                        "/api/room/upload",
                        files={
                            "north": ("north.jpg", north, "image/jpeg"),
                            "south": ("south.jpg", south, "image/jpeg"),
                            "east": ("east.jpg", east, "image/jpeg"),
                            "west": ("west.jpg", west, "image/jpeg")
                        }
                    )
                
                assert response.status_code == 200
                data = response.json()
                assert data["room_id"] == "test-room-123"
                assert data["status"] == "success"
                mock_upload.assert_called_once()
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_upload_room_missing_images(self, client, mock_user_token):
        """Test room upload with missing images returns validation error"""
        app.dependency_overrides[get_current_user] = lambda: mock_user_token
        try:
            response = client.post("/api/room/upload")
            # FastAPI validation should catch missing files
            assert response.status_code == 422
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_upload_room_invalid_file_type(self, client, mock_user_token):
        """Test room upload with invalid file type"""
        app.dependency_overrides[get_current_user] = lambda: mock_user_token
        try:
            with patch('app.routes.room.room_upload_service.upload_room_images', new=AsyncMock()) as mock_upload:
                mock_upload.return_value = {
                    "room_id": "test-room-123",
                    "status": "success",
                    "message": "Room uploaded successfully"
                }
                response = client.post(
                    "/api/room/upload",
                    files={
                        "north": ("test.txt", b"not an image", "text/plain"),
                        "south": ("test.txt", b"not an image", "text/plain"),
                        "east": ("test.txt", b"not an image", "text/plain"),
                        "west": ("test.txt", b"not an image", "text/plain")
                    }
                )
                # Should succeed at API level, validation happens in service
                assert response.status_code == 200
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_get_room_success(self, client, mock_firebase, mock_user_token, sample_room_data):
        """Test successful room retrieval"""
        app.dependency_overrides[get_current_user] = lambda: mock_user_token
        try:
            with patch('app.routes.room.room_upload_service.get_room', new=AsyncMock()) as mock_get:
                mock_get.return_value = sample_room_data
                
                response = client.get("/api/room/test-room-123")
                
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == "test-room-123"
                assert data["name"] == "Test Living Room"
                assert "images" in data
                mock_get.assert_called_once_with("test-room-123", "test-user-456")
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_get_room_not_found(self, client, mock_firebase, mock_user_token):
        """Test room retrieval for non-existent room"""
        app.dependency_overrides[get_current_user] = lambda: mock_user_token
        try:
            with patch('app.routes.room.room_upload_service.get_room', new=AsyncMock()) as mock_get:
                mock_get.return_value = None
                
                response = client.get("/api/room/nonexistent-room")
                
                assert response.status_code == 404
                assert "Room not found" in response.json()["detail"]
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_get_room_unauthorized(self, client, sample_room_data):
        """Test room retrieval without authentication"""
        with patch('app.routes.room.room_upload_service.get_room', new=AsyncMock()) as mock_get:
            mock_get.return_value = sample_room_data
            
            response = client.get("/api/room/test-room-123")
            
            # Should be unauthorized due to missing auth token
            assert response.status_code == 401

    def test_get_user_rooms_success(self, client, mock_firebase, mock_user_token, sample_room_data):
        """Test successful retrieval of user's rooms"""
        app.dependency_overrides[get_current_user] = lambda: mock_user_token
        try:
            with patch('app.routes.room.room_upload_service.get_user_rooms', new=AsyncMock()) as mock_get:
                mock_get.return_value = [sample_room_data]
                
                response = client.get("/api/room/user/rooms")
                
                assert response.status_code == 200
                data = response.json()
                assert len(data["rooms"]) == 1
                assert data["rooms"][0]["id"] == "test-room-123"
                assert data["total"] == 1
                mock_get.assert_called_once_with("test-user-456")
        finally:
            app.dependency_overrides.pop(get_current_user, None)

    def test_get_user_rooms_empty(self, client, mock_firebase, mock_user_token):
        """Test retrieval when user has no rooms"""
        app.dependency_overrides[get_current_user] = lambda: mock_user_token
        try:
            with patch('app.routes.room.room_upload_service.get_user_rooms', new=AsyncMock()) as mock_get:
                mock_get.return_value = []
                
                response = client.get("/api/room/user/rooms")
                
                assert response.status_code == 200
                data = response.json()
                assert len(data["rooms"]) == 0
                assert data["total"] == 0
        finally:
            app.dependency_overrides.pop(get_current_user, None)
