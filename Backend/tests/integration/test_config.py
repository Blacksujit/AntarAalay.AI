"""
Module 1: Configuration Tests

Test coverage for app/config.py
Following test-driven development principles.
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
import os
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

# Import the module under test
from app.config import (
    Settings,
    ConfigurationError,
    get_settings,
    validate_production_config,
    clear_settings_cache,
)


class TestSettings:
    """Test cases for Settings class."""
    
    def test_default_settings(self):
        """Test that settings have sensible defaults."""
        # Ignore any local .env / env var overrides when checking code defaults
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings(_env_file=None)
        
        assert settings.APP_NAME == "AntarAalay.ai"
        assert settings.APP_VERSION == "1.0.0"
        assert settings.DEBUG is False
        assert settings.ENVIRONMENT == "development"
        assert settings.PORT == 8000
        assert settings.HOST == "0.0.0.0"
        
    def test_allowed_image_types_default(self):
        """Test default allowed image types."""
        settings = Settings()
        
        assert "image/jpeg" in settings.allowed_image_types_list
        assert "image/png" in settings.allowed_image_types_list
        assert "image/webp" in settings.allowed_image_types_list
        assert len(settings.allowed_image_types_list) == 3
        
    def test_allowed_image_types_from_string(self):
        """Test parsing comma-separated image types from env string."""
        # Simulate env var as string
        with patch.dict(os.environ, {"ALLOWED_IMAGE_TYPES": "image/jpeg, image/png, image/gif"}):
            settings = Settings()
            assert "image/jpeg" in settings.allowed_image_types_list
            assert "image/png" in settings.allowed_image_types_list
            assert "image/gif" in settings.allowed_image_types_list
            
    def test_max_upload_size_validation_too_small(self):
        """Test that upload size < 1KB raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            Settings(MAX_UPLOAD_SIZE=500)  # 500 bytes
        
        assert "at least 1KB" in str(exc_info.value)
        
    def test_max_upload_size_validation_too_large(self):
        """Test that upload size > 50MB raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            Settings(MAX_UPLOAD_SIZE=100 * 1024 * 1024)  # 100MB
        
        assert "cannot exceed 50MB" in str(exc_info.value)
        
    def test_max_upload_size_valid(self):
        """Test valid upload sizes."""
        settings = Settings(MAX_UPLOAD_SIZE=5 * 1024 * 1024)  # 5MB
        assert settings.MAX_UPLOAD_SIZE == 5 * 1024 * 1024
        
    def test_database_url_validation_invalid(self):
        """Test that non-postgresql URL raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            Settings(DATABASE_URL="mysql://user:pass@localhost/db")
        
        assert "PostgreSQL" in str(exc_info.value)
        
    def test_database_url_validation_valid_postgresql(self):
        """Test valid postgresql URL."""
        settings = Settings(DATABASE_URL="postgresql://user:pass@localhost/db")
        assert settings.DATABASE_URL == "postgresql://user:pass@localhost/db"
        
    def test_database_url_validation_valid_postgres(self):
        """Test valid postgres:// URL (alternate prefix)."""
        settings = Settings(DATABASE_URL="postgres://user:pass@localhost/db")
        assert settings.DATABASE_URL == "postgres://user:pass@localhost/db"
        
    def test_environment_values(self):
        """Test environment can be development, staging, or production."""
        dev = Settings(ENVIRONMENT="development")
        assert dev.ENVIRONMENT == "development"
        
        staging = Settings(ENVIRONMENT="staging")
        assert staging.ENVIRONMENT == "staging"
        
        prod = Settings(ENVIRONMENT="production")
        assert prod.ENVIRONMENT == "production"
        
    def test_aws_configuration(self):
        """Test AWS configuration fields."""
        settings = Settings(
            AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE",
            AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            AWS_REGION="ap-south-1",
            S3_BUCKET_NAME="my-bucket",
            S3_ENDPOINT_URL="http://localhost:9000"
        )
        
        assert settings.AWS_ACCESS_KEY_ID == "AKIAIOSFODNN7EXAMPLE"
        assert settings.AWS_SECRET_ACCESS_KEY == "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        assert settings.AWS_REGION == "ap-south-1"
        assert settings.S3_BUCKET_NAME == "my-bucket"
        assert settings.S3_ENDPOINT_URL == "http://localhost:9000"
        
    def test_firebase_configuration(self):
        """Test Firebase configuration fields."""
        settings = Settings(
            FIREBASE_PROJECT_ID="my-project",
            FIREBASE_API_KEY="api-key-123",
            FIREBASE_AUTH_EMULATOR_HOST="localhost:9099"
        )
        
        assert settings.FIREBASE_PROJECT_ID == "my-project"
        assert settings.FIREBASE_API_KEY == "api-key-123"
        assert settings.FIREBASE_AUTH_EMULATOR_HOST == "localhost:9099"
        
    def test_stability_ai_configuration(self):
        """Test Stability AI configuration."""
        settings = Settings(
            STABLE_DIFFUSION_API_KEY="sk-my-key",
            STABLE_DIFFUSION_API_URL="https://api.custom.com/v1",
            STABLE_DIFFUSION_TIMEOUT=120,
            STABLE_DIFFUSION_MAX_RETRIES=5
        )
        
        assert settings.STABLE_DIFFUSION_API_KEY == "sk-my-key"
        assert settings.STABLE_DIFFUSION_API_URL == "https://api.custom.com/v1"
        assert settings.STABLE_DIFFUSION_TIMEOUT == 120
        assert settings.STABLE_DIFFUSION_MAX_RETRIES == 5
        
    def test_extra_env_vars_ignored(self):
        """Test that undefined env vars are ignored (Config.extra = "ignore")."""
        # This should not raise an error
        with patch.dict(os.environ, {"UNDEFINED_VAR": "value"}):
            settings = Settings()
            # Should not have UNDEFINED_VAR attribute
            assert not hasattr(settings, "UNDEFINED_VAR")


class TestConfigurationError:
    """Test cases for ConfigurationError exception."""
    
    def test_error_message(self):
        """Test error message is stored correctly."""
        error = ConfigurationError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert error.message == "Something went wrong"
        
    def test_error_with_missing_vars(self):
        """Test error can include list of missing variables."""
        missing = ["DATABASE_URL", "AWS_KEY"]
        error = ConfigurationError("Missing config", missing_vars=missing)
        
        assert error.missing_vars == missing
        assert "DATABASE_URL" in str(error)
        
    def test_error_with_empty_missing_vars(self):
        """Test error with no missing vars defaults to empty list."""
        error = ConfigurationError("Error")
        assert error.missing_vars == []


class TestValidateProductionConfig:
    """Test cases for validate_production_config function."""
    
    def test_all_required_vars_present(self):
        """Test no error when all required production vars are set."""
        settings = Settings(
            ENVIRONMENT="production",
            DATABASE_URL="postgresql://user:pass@localhost/db",
            AWS_ACCESS_KEY_ID="key",
            AWS_SECRET_ACCESS_KEY="secret",
            AWS_REGION="ap-south-1",
            S3_BUCKET_NAME="bucket",
            FIREBASE_PROJECT_ID="project"
        )
        
        # Should not raise
        validate_production_config(settings)
        
    def test_missing_database_url(self):
        """Test error when DATABASE_URL is missing in production."""
        settings = Settings(
            ENVIRONMENT="production",
            DATABASE_URL="",
            AWS_ACCESS_KEY_ID="key",
            AWS_SECRET_ACCESS_KEY="secret",
            AWS_REGION="ap-south-1",
            S3_BUCKET_NAME="bucket",
            FIREBASE_PROJECT_ID="project"
        )
        
        with pytest.raises(ConfigurationError) as exc_info:
            validate_production_config(settings)
        
        assert "DATABASE_URL" in str(exc_info.value)
        assert "DATABASE_URL" in exc_info.value.missing_vars
        
    def test_missing_aws_credentials(self):
        """Test error when AWS credentials are missing."""
        settings = Settings(
            ENVIRONMENT="production",
            DATABASE_URL="postgresql://user:pass@localhost/db",
            AWS_ACCESS_KEY_ID="",
            AWS_SECRET_ACCESS_KEY="",
            AWS_REGION="",
            S3_BUCKET_NAME="bucket",
            FIREBASE_PROJECT_ID="project"
        )
        
        with pytest.raises(ConfigurationError) as exc_info:
            validate_production_config(settings)
        
        assert "AWS_ACCESS_KEY_ID" in str(exc_info.value)
        assert "AWS_SECRET_ACCESS_KEY" in str(exc_info.value)
        assert "AWS_REGION" in str(exc_info.value)
        
    def test_missing_multiple_vars(self):
        """Test error lists all missing variables."""
        settings = Settings(
            ENVIRONMENT="production",
            DATABASE_URL="",
            AWS_ACCESS_KEY_ID="",
            AWS_SECRET_ACCESS_KEY="",
            AWS_REGION="",
            S3_BUCKET_NAME="",
            FIREBASE_PROJECT_ID=""
        )
        
        with pytest.raises(ConfigurationError) as exc_info:
            validate_production_config(settings)
        
        missing = exc_info.value.missing_vars
        assert len(missing) == 6
        assert "DATABASE_URL" in missing
        assert "S3_BUCKET_NAME" in missing
        assert "FIREBASE_PROJECT_ID" in missing


class TestGetSettings:
    """Test cases for get_settings function."""
    
    def setup_method(self):
        """Clear cache before each test."""
        clear_settings_cache()
        
    def test_returns_settings_instance(self):
        """Test function returns Settings instance."""
        settings = get_settings()
        assert isinstance(settings, Settings)
        
    def test_caching_behavior(self):
        """Test that settings are cached (same instance returned)."""
        settings1 = get_settings()
        settings2 = get_settings()
        
        # Should be same object due to lru_cache
        assert settings1 is settings2
        
    def test_clear_cache(self):
        """Test that clear_settings_cache actually clears the cache."""
        settings1 = get_settings()
        clear_settings_cache()
        settings2 = get_settings()
        
        # Should be different objects after cache clear
        assert settings1 is not settings2
        
    @patch.dict(os.environ, {
        "ENVIRONMENT": "production",
        "DATABASE_URL": "",
        "AWS_ACCESS_KEY_ID": "",
    }, clear=True)
    def test_raises_error_in_production_with_missing_config(self):
        """Test that get_settings raises ConfigurationError in production with missing config."""
        # Need to clear cache to pick up new env vars
        clear_settings_cache()
        
        with pytest.raises(ConfigurationError) as exc_info:
            get_settings()
        
        assert "Missing required production configuration" in str(exc_info.value)
        
    @patch.dict(os.environ, {
        "ENVIRONMENT": "development",
        "DATABASE_URL": "",
    }, clear=True)
    def test_allows_missing_config_in_development(self):
        """Test that missing config is allowed in development mode."""
        clear_settings_cache()
        
        # Should not raise in development
        settings = get_settings()
        assert settings.ENVIRONMENT == "development"


class TestConfigurationIntegration:
    """Integration-style tests for the configuration module."""
    
    def setup_method(self):
        """Clear cache and clean env before each test."""
        clear_settings_cache()
        
    def test_full_configuration_workflow(self):
        """Test complete configuration loading workflow."""
        # Set up environment
        with patch.dict(os.environ, {
            "ENVIRONMENT": "staging",
            "APP_NAME": "TestApp",
            "DATABASE_URL": "postgresql://test:test@localhost/testdb",
            "AWS_REGION": "eu-west-1",
            "MAX_UPLOAD_SIZE": "5242880",  # 5MB
        }, clear=True):
            clear_settings_cache()
            
            settings = get_settings()
            
            assert settings.ENVIRONMENT == "staging"
            assert settings.APP_NAME == "TestApp"
            assert settings.DATABASE_URL == "postgresql://test:test@localhost/testdb"
            assert settings.AWS_REGION == "eu-west-1"
            assert settings.MAX_UPLOAD_SIZE == 5242880
            
    def test_validation_error_conversion(self):
        """Test that pydantic ValidationError is converted to ConfigurationError."""
        with patch.dict(os.environ, {
            "MAX_UPLOAD_SIZE": "100",  # Invalid: too small
        }, clear=True):
            clear_settings_cache()
            
            with pytest.raises(ConfigurationError) as exc_info:
                get_settings()
            
            assert "Configuration validation failed" in str(exc_info.value)
            assert "at least 1KB" in str(exc_info.value)


# Run tests with: pytest tests/test_config.py -v
