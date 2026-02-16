"""
Configuration Module for AntarAalay.ai

This module handles environment variable loading, validation,
and provides typed settings to the application.

Following the paper architecture: Configuration is Module 1.
It has no dependencies on other modules.
"""
from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationError


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses pydantic-settings for type validation and .env file support.
    All settings have defaults for development, but must be overridden
    in production via environment variables.
    """
    
    # Application Metadata
    APP_NAME: str = "AntarAalay.ai"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database - SQLite for local dev
    DATABASE_URL: str = "sqlite:///./antaralay.db"
    
    # Firebase Configuration
    FIREBASE_API_KEY: str = "AIzaSyANQciKqx_Cyi92ahSVaLy_MewUDkZY3fg"
    FIREBASE_AUTH_DOMAIN: str = "antaraalayai.firebaseapp.com"
    FIREBASE_PROJECT_ID: str = "antaraalayai"
    FIREBASE_STORAGE_BUCKET: str = "antaraalayai.firebasestorage.app"
    FIREBASE_MESSAGING_SENDER_ID: str = "656663048044"
    FIREBASE_APP_ID: str = "1:656663048044:web:802e1ef31aaf30eb2a0d49"
    FIREBASE_MEASUREMENT_ID: str = "G-07QNHQGWJ0"
    FIREBASE_AUTH_EMULATOR_HOST: Optional[str] = None  # For local testing
    FIREBASE_CREDENTIALS_PATH: str = ""  # Path to service account JSON (for backend)
    
    # External APIs
    STABLE_DIFFUSION_API_KEY: str = ""
    STABLE_DIFFUSION_API_URL: str = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    STABLE_DIFFUSION_TIMEOUT: int = 60  # seconds
    STABLE_DIFFUSION_MAX_RETRIES: int = 3
    
    VASTU_API_KEY: str = ""
    VASTU_API_URL: str = ""
    VASTU_API_TIMEOUT: int = 10
    
    # Security & Validation
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/webp"

    # AWS / S3 Configuration (legacy + optional)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = ""
    S3_BUCKET_NAME: str = ""
    S3_ENDPOINT_URL: str = ""
    
    @property
    def allowed_image_types_list(self) -> List[str]:
        """Get ALLOWED_IMAGE_TYPES as a list."""
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",") if t.strip()]
    
    @field_validator("MAX_UPLOAD_SIZE")
    @classmethod
    def validate_max_upload_size(cls, v):
        """Ensure max upload size is reasonable (1KB to 50MB)."""
        if v < 1024:
            raise ValueError("MAX_UPLOAD_SIZE must be at least 1KB")
        if v > 50 * 1024 * 1024:
            raise ValueError("MAX_UPLOAD_SIZE cannot exceed 50MB")
        return v
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v):
        """Ensure database URL is valid (PostgreSQL or SQLite)."""
        if v and not v.startswith(("postgresql://", "postgres://", "sqlite:///", "sqlite://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL or SQLite connection string")
        return v
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars not defined here


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""
    
    def __init__(self, message: str, missing_vars: List[str] = None):
        self.message = message
        self.missing_vars = missing_vars or []
        if self.missing_vars:
            super().__init__(f"{self.message}: {', '.join(self.missing_vars)}")
        else:
            super().__init__(self.message)


def validate_production_config(settings: Settings) -> None:
    """
    Validate that all required production configuration is present.
    
    Raises:
        ConfigurationError: If any required production config is missing.
    """
    required_vars = {
        "DATABASE_URL": settings.DATABASE_URL,
        "AWS_ACCESS_KEY_ID": settings.AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": settings.AWS_SECRET_ACCESS_KEY,
        "AWS_REGION": settings.AWS_REGION,
        "S3_BUCKET_NAME": settings.S3_BUCKET_NAME,
        "FIREBASE_API_KEY": settings.FIREBASE_API_KEY,
        "FIREBASE_AUTH_DOMAIN": settings.FIREBASE_AUTH_DOMAIN,
        "FIREBASE_PROJECT_ID": settings.FIREBASE_PROJECT_ID,
        "FIREBASE_STORAGE_BUCKET": settings.FIREBASE_STORAGE_BUCKET,
        "FIREBASE_MESSAGING_SENDER_ID": settings.FIREBASE_MESSAGING_SENDER_ID,
        "FIREBASE_APP_ID": settings.FIREBASE_APP_ID,
        "FIREBASE_MEASUREMENT_ID": settings.FIREBASE_MEASUREMENT_ID,
    }
    
    missing = [name for name, value in required_vars.items() if not value]
    
    if missing:
        raise ConfigurationError(
            f"Missing required production configuration: {', '.join(missing)}",
            missing_vars=missing
        )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to avoid re-loading configuration on every call.
    Settings are loaded once at startup and cached.
    
    Returns:
        Settings: Application configuration object.
    
    Raises:
        ConfigurationError: If configuration validation fails.
    """
    try:
        settings = Settings()
        
        # In production, validate all required vars are present
        if settings.ENVIRONMENT == "production":
            validate_production_config(settings)
        
        return settings
    except ValidationError as e:
        # Convert pydantic errors to our custom exception
        missing = []
        for error in e.errors():
            missing.append(f"{error['loc'][0]}: {error['msg']}")
        raise ConfigurationError(
            f"Configuration validation failed: {'; '.join(missing)}"
        )


def clear_settings_cache() -> None:
    """Clear the settings cache. Useful for testing."""
    get_settings.cache_clear()


# Convenience exports
__all__ = [
    "Settings",
    "ConfigurationError",
    "get_settings",
    "validate_production_config",
    "clear_settings_cache",
]
