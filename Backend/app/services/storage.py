"""
Module 4: Storage Service (Local File Storage)

This module handles image upload, download, and deletion from local file system.
Free alternative to Firebase Storage.

Dependencies: Module 1 (Configuration)
"""
import uuid
import logging
import os
import shutil
from typing import Optional, List
from urllib.parse import quote, unquote
from pathlib import Path

from app.config import get_settings, Settings

logger = logging.getLogger(__name__)


class StorageError(Exception):
    """Raised when storage operation fails."""
    pass


class InvalidContentTypeError(StorageError):
    """Raised when content type is not allowed."""
    pass


class FileTooLargeError(StorageError):
    """Raised when file exceeds maximum size."""
    pass


class StorageService:
    """
    Service for managing file storage in local file system.
    
    Handles image uploads, downloads, deletions, and URL generation.
    Uses local file system as FREE alternative to Firebase Storage.
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the storage service.
        
        Args:
            settings: Application settings. Uses get_settings() if not provided.
        """
        self.settings = settings or get_settings()
        self._validate_configuration()
        
        # Create local storage directory
        self.storage_dir = Path("uploads")
        self.storage_dir.mkdir(exist_ok=True)
        
        # Base URL for serving files
        self.base_url = "http://127.0.0.1:8000"
        
        logger.info(f"StorageService initialized with local storage: {self.storage_dir.absolute()}")
    
    def _validate_configuration(self) -> None:
        """Validate that required configuration is present."""
        # Local storage doesn't require any special configuration
        pass
    
    def _validate_content_type(self, content_type: str) -> bool:
        """
        Validate that content type is allowed.
        
        Args:
            content_type: MIME type to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        allowed_types = self.settings.allowed_image_types_list
        return content_type in allowed_types
    
    def _validate_file_size(self, file_content: bytes) -> bool:
        """
        Validate that file size is within limits.
        
        Args:
            file_content: File bytes to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        max_size = self.settings.MAX_UPLOAD_SIZE
        return len(file_content) <= max_size
    
    def _generate_filename(self, content_type: str, folder: str) -> str:
        """
        Generate a unique filename for S3 storage.
        
        Args:
            content_type: MIME type of the file
            folder: Folder path in S3 bucket
            
        Returns:
            str: Unique filename with extension
        """
        file_extension = content_type.split('/')[-1]
        if file_extension == 'jpeg':
            file_extension = 'jpg'
        
        unique_id = str(uuid.uuid4())
        return f"{folder}/{unique_id}.{file_extension}"
    
    def _build_public_url(self, key: str) -> str:
        """Build public URL for local file storage."""
        return f"{self.base_url}/uploads/{key}"
    
    def upload_image(
        self,
        file_content: bytes,
        content_type: str,
        folder: str = "rooms"
    ) -> str:
        """
        Upload an image to local file storage.
        
        Args:
            file_content: Raw file content as bytes
            content_type: MIME type of the file
            folder: Folder path for organization
            
        Returns:
            str: Public download URL of uploaded image
        """
        # Validate content type
        if not self._validate_content_type(content_type):
            raise InvalidContentTypeError(
                f"Content type '{content_type}' not allowed. "
                f"Allowed types: {', '.join(self.settings.allowed_image_types_list)}"
            )
        
        # Validate file size
        if not self._validate_file_size(file_content):
            max_mb = self.settings.MAX_UPLOAD_SIZE / (1024 * 1024)
            raise FileTooLargeError(
                f"File too large: {len(file_content)} bytes. "
                f"Maximum size: {max_mb:.1f}MB"
            )
        
        # Generate unique filename
        file_name = self._generate_filename(content_type, folder)
        
        # Create full directory path if it doesn't exist
        file_path = self.storage_dir / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save file locally
        try:
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            logger.info(f"Successfully saved file: {file_path}")
            return self._build_public_url(file_name)
            
        except Exception as e:
            logger.error(f"Failed to save file {file_path}: {e}")
            raise StorageError(f"Failed to upload file: {e}")
    
    def delete_image(self, image_url: str) -> bool:
        """Delete an image from local storage."""
        try:
            # Extract filename from URL
            if "/uploads/" in image_url:
                filename = image_url.split("/uploads/")[-1]
                file_path = self.storage_dir / filename
                
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"Successfully deleted file: {file_path}")
                    return True
                else:
                    logger.warning(f"File not found for deletion: {file_path}")
                    return False
            else:
                logger.warning(f"Invalid URL format for deletion: {image_url}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete image: {e}")
            return False
    
    def generate_upload_url(self, path: str) -> str:
        """Generate upload URL for local storage."""
        return f"{self.base_url}/uploads/{path}"


# Global storage service instance (initialized lazily)
_storage_service: Optional[StorageService] = None


def get_storage_service() -> StorageService:
    """Get or create the global storage service instance."""
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service


def reset_storage_service() -> None:
    """Reset the global storage service. Useful for testing."""
    global _storage_service
    _storage_service = None


__all__ = [
    "StorageService",
    "StorageError",
    "InvalidContentTypeError",
    "FileTooLargeError",
    "get_storage_service",
    "reset_storage_service",
]
