"""
Module 4: Storage Service Tests (Firebase Storage)

Test coverage for app/services/storage.py with Firebase Storage.
"""
import pytest
from unittest.mock import Mock, patch

from app.config import Settings, clear_settings_cache
from app.services.storage import (
    StorageService,
    StorageError,
    InvalidContentTypeError,
    FileTooLargeError,
    get_storage_service,
    reset_storage_service,
)


@pytest.fixture
def mock_settings():
    """Create test settings for Firebase Storage."""
    return Settings(
        FIREBASE_PROJECT_ID="test-project",
        MAX_UPLOAD_SIZE=10 * 1024 * 1024,  # 10MB
        ALLOWED_IMAGE_TYPES=["image/jpeg", "image/png", "image/webp"]
    )


class TestStorageServiceInitialization:
    """Test cases for StorageService initialization with Firebase."""
    
    def test_initialization_with_valid_config(self, mock_settings):
        """Test successful initialization with valid Firebase configuration."""
        service = StorageService(mock_settings)
        
        assert service.bucket_name == "test-project.appspot.com"
        assert service.settings == mock_settings
        
    def test_initialization_missing_project_id(self, mock_settings):
        """Test initialization fails without Firebase Project ID."""
        mock_settings.FIREBASE_PROJECT_ID = ""
        
        with pytest.raises(StorageError) as exc_info:
            StorageService(mock_settings)
            
        assert "FIREBASE_PROJECT_ID not configured" in str(exc_info.value)
        
    def test_bucket_name_format(self, mock_settings):
        """Test bucket name follows Firebase format."""
        service = StorageService(mock_settings)
        assert service.bucket_name.endswith(".appspot.com")


class TestURLBuilding:
    """Test cases for Firebase Storage URL building."""
    
    def test_build_public_url(self, mock_settings):
        """Test URL building for Firebase Storage."""
        service = StorageService(mock_settings)
        
        url = service._build_public_url("rooms/test-file.jpg")
        
        assert "firebasestorage.googleapis.com" in url
        assert "test-project.appspot.com" in url
        assert "rooms%2Ftest-file.jpg" in url or "rooms/test-file.jpg" in url
        assert "alt=media" in url
        
    def test_generate_upload_url(self, mock_settings):
        """Test upload URL generation."""
        service = StorageService(mock_settings)
        
        url = service.generate_upload_url("rooms/test.jpg")
        
        assert "firebasestorage.googleapis.com" in url
        assert service.bucket_name in url


class TestExtractPathFromURL:
    """Test cases for extracting path from Firebase URL."""
    
    def test_extract_path_from_firebase_url(self, mock_settings):
        """Test path extraction from Firebase Storage URL."""
        service = StorageService(mock_settings)
        
        url = "https://firebasestorage.googleapis.com/v0/b/test-project.appspot.com/o/rooms%2Fabc123.jpg?alt=media"
        path = service._extract_path_from_url(url)
        
        assert path == "rooms/abc123.jpg"
        
    def test_extract_path_invalid_url(self, mock_settings):
        """Test path extraction from invalid URL."""
        service = StorageService(mock_settings)
        
        url = "https://example.com/image.jpg"
        path = service._extract_path_from_url(url)
        
        assert path is None


class TestUploadImage:
    """Test cases for upload_image method with Firebase."""
    
    def test_upload_image_success(self, mock_settings):
        """Test successful image upload returns Firebase URL."""
        service = StorageService(mock_settings)
        file_content = b"fake-image-data"
        
        url = service.upload_image(file_content, "image/jpeg", "rooms")
        
        assert "firebasestorage.googleapis.com" in url
        assert "alt=media" in url
        
    def test_upload_image_invalid_content_type(self, mock_settings):
        """Test upload fails with invalid content type."""
        service = StorageService(mock_settings)
        
        with pytest.raises(InvalidContentTypeError) as exc_info:
            service.upload_image(b"data", "image/gif", "rooms")
            
        assert "not allowed" in str(exc_info.value)
        
    def test_upload_image_file_too_large(self, mock_settings):
        """Test upload fails when file exceeds size limit."""
        service = StorageService(mock_settings)
        
        # 15MB file (over 10MB limit)
        large_content = b"x" * (15 * 1024 * 1024)
        
        with pytest.raises(FileTooLargeError) as exc_info:
            service.upload_image(large_content, "image/jpeg", "rooms")
            
        assert "File too large" in str(exc_info.value)


class TestDeleteImage:
    """Test cases for delete_image method with Firebase."""
    
    def test_delete_image_success(self, mock_settings):
        """Test successful image deletion."""
        service = StorageService(mock_settings)
        image_url = "https://firebasestorage.googleapis.com/v0/b/test-project.appspot.com/o/rooms%2Ffile.jpg?alt=media"
        
        result = service.delete_image(image_url)
        
        assert result is True
        
    def test_delete_image_invalid_url(self, mock_settings):
        """Test deletion with invalid URL returns False."""
        service = StorageService(mock_settings)
        
        result = service.delete_image("")
        
        assert result is False


class TestStorageServiceSingleton:
    """Test cases for storage service singleton pattern."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        reset_storage_service()
        
    @patch('app.services.storage.get_settings')
    def test_get_storage_service_creates_singleton(self, mock_get_settings):
        """Test that get_storage_service creates singleton."""
        mock_get_settings.return_value = Settings(
            FIREBASE_PROJECT_ID="test-project",
            MAX_UPLOAD_SIZE=10 * 1024 * 1024,
            ALLOWED_IMAGE_TYPES=["image/jpeg", "image/png", "image/webp"]
        )
        
        service1 = get_storage_service()
        service2 = get_storage_service()
        
        assert service1 is service2
        
    @patch('app.services.storage.get_settings')
    def test_reset_storage_service_clears_singleton(self, mock_get_settings):
        """Test that reset clears the singleton."""
        mock_get_settings.return_value = Settings(
            FIREBASE_PROJECT_ID="test-project",
            MAX_UPLOAD_SIZE=10 * 1024 * 1024,
            ALLOWED_IMAGE_TYPES=["image/jpeg", "image/png", "image/webp"]
        )
        
        service1 = get_storage_service()
        reset_storage_service()
        service2 = get_storage_service()
        
        assert service1 is not service2


# Run tests with: pytest tests/test_storage.py -v
