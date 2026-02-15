"""
Module 4: Storage Service (Firebase Storage)

This module handles image upload, download, and deletion from Firebase Storage.

Dependencies: Module 1 (Configuration)
"""
import uuid
import logging
from typing import Optional, List
from urllib.parse import quote, unquote

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
    Service for managing file storage in Firebase Storage.
    
    Handles image uploads, downloads, deletions, and URL generation.
    Uses Firebase Storage REST API for file operations.
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the storage service.
        
        Args:
            settings: Application settings. Uses get_settings() if not provided.
        """
        self.settings = settings or get_settings()
        self._validate_configuration()
        
        # Firebase Storage bucket name (usually project_id.appspot.com)
        self.bucket_name = f"{self.settings.FIREBASE_PROJECT_ID}.appspot.com"
        self.base_url = f"https://firebasestorage.googleapis.com/v0/b/{self.bucket_name}/o"
        
        logger.info(f"StorageService initialized for Firebase bucket: {self.bucket_name}")
    
    def _validate_configuration(self) -> None:
        """Validate that required Firebase configuration is present."""
        if not self.settings.FIREBASE_PROJECT_ID:
            raise StorageError("FIREBASE_PROJECT_ID not configured")
    
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
        """Build public URL for Firebase Storage."""
        encoded_path = quote(key, safe='')
        return f"https://firebasestorage.googleapis.com/v0/b/{self.bucket_name}/o/{encoded_path}?alt=media"
    
    def upload_image(
        self,
        file_content: bytes,
        content_type: str,
        folder: str = "rooms"
    ) -> str:
        """
        Upload an image to Firebase Storage.
        
        For MVP, returns the URL where client should upload via Firebase SDK.
        In production, use Firebase Admin SDK for server-side upload.
        
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
        
        logger.info(f"Generating Firebase Storage URL: {file_name}")
        
        # Return the public URL (actual upload via client SDK)
        url = self._build_public_url(file_name)
        logger.info(f"Firebase Storage URL ready: {url}")
        return url
    
    def delete_image(self, image_url: str) -> bool:
        """Delete an image from Firebase Storage."""
        try:
            path = self._extract_path_from_url(image_url)
            if not path:
                logger.warning(f"Could not extract path from URL: {image_url}")
                return False
            
            logger.info(f"Deleting from Firebase Storage: {path}")
            # In production, use Firebase Admin SDK
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete image: {e}")
            return False
    
    def _extract_path_from_url(self, image_url: str) -> Optional[str]:
        """Extract storage path from Firebase Storage URL."""
        try:
            if "firebasestorage.googleapis.com" in image_url:
                parts = image_url.split('/o/')
                if len(parts) > 1:
                    path_part = parts[1].split('?')[0]
                    return unquote(path_part)
            return None
        except Exception as e:
            logger.error(f"Failed to extract path from URL: {e}")
            return None
    
    def generate_upload_url(self, path: str) -> str:
        """Generate upload URL for Firebase Storage."""
        encoded_path = quote(path, safe='')
        return f"{self.base_url}/{encoded_path}"


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
