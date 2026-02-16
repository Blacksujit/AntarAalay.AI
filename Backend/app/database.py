"""
Module 2: Database Module

This module provides database connectivity, session management,
and dependency injection for the AntarAalay.ai application.

Dependencies: Module 1 (Configuration)
"""
from typing import Generator, Optional, Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import logging
import ssl

from app.config import get_settings, Settings

# Module-level logger
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages database connections and session lifecycle.
    
    This class encapsulates engine creation, session factory setup,
    and provides methods for session management.
    """
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the database manager.
        
        Args:
            settings: Application settings. Uses get_settings() if not provided.
        """
        self.settings = settings or get_settings()
        self.engine: Optional[Engine] = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self) -> None:
        """Create the database engine and session factory."""
        try:
            # Force SQLite for local development
            database_url = self.settings.DATABASE_URL
            if "postgresql" in database_url and self.settings.ENVIRONMENT != "production":
                database_url = "sqlite:///./antaralay.db"
                logger.info("Forcing SQLite for local development")
            
            # Build connection arguments for SSL if needed
            connect_args: Dict[str, Any] = {}
            
            # For cloud Postgres (Render, Supabase, etc.), use SSL
            if self.settings.ENVIRONMENT == "production" or ("render.com" in database_url and "postgresql" in database_url):
                # Create SSL context for cloud providers
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                connect_args["sslmode"] = "require"
                connect_args["sslrootcert"] = None
            
            # SQLite specific: check_same_thread=False
            if "sqlite" in database_url:
                connect_args["check_same_thread"] = False
            
            self.engine = create_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=3600,   # Recycle connections after 1 hour
                echo=self.settings.DEBUG,  # Log SQL in debug mode
                connect_args=connect_args,
            )
            
            # Add event listeners for connection monitoring
            event.listen(self.engine, 'connect', self._on_connect)
            event.listen(self.engine, 'checkout', self._on_checkout)
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("Database engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseConnectionError(f"Database initialization failed: {e}")
    
    @staticmethod
    def _on_connect(dbapi_conn, connection_record):
        """Called when a new connection is created."""
        logger.debug("New database connection established")
    
    @staticmethod
    def _on_checkout(dbapi_conn, connection_record, connection_proxy):
        """Called when a connection is retrieved from the pool."""
        logger.debug("Database connection checked out from pool")
    
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get a database session generator.
        
        Yields:
            Session: SQLAlchemy session object
            
        Example:
            for db in db_manager.get_session():
                user = db.query(User).first()
        """
        if not self.SessionLocal:
            raise DatabaseConnectionError("Database not initialized")
        
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope around a series of operations.
        
        Automatically commits on success or rolls back on exception.
        
        Example:
            with db_manager.session_scope() as session:
                session.add(user)
                # Automatically committed if no exception
        """
        if not self.SessionLocal:
            raise DatabaseConnectionError("Database not initialized")
        
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def close(self) -> None:
        """Close all database connections and dispose of the engine."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.SessionLocal = None
            logger.info("Database connections closed")
    
    def ping(self) -> bool:
        """
        Check if database connection is alive.
        
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        if not self.engine:
            return False
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database ping failed: {e}")
            return False


class DatabaseConnectionError(Exception):
    """Raised when database connection fails."""
    pass


# Create the declarative base for all models
Base = declarative_base()

# Global database manager instance (initialized lazily)
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """
    Get or create the global database manager instance.
    
    Returns:
        DatabaseManager: The singleton database manager.
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def reset_db_manager() -> None:
    """Reset the global database manager. Useful for testing."""
    global _db_manager
    if _db_manager:
        _db_manager.close()
    _db_manager = None


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.
    
    Usage in routes:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Session: Database session that auto-closes after request.
    """
    manager = get_db_manager()
    yield from manager.get_session()


def init_db(settings: Optional[Settings] = None) -> None:
    """
    Initialize database by creating all tables.
    
    Args:
        settings: Optional settings override for testing.
    """
    manager = DatabaseManager(settings) if settings else get_db_manager()
    
    try:
        Base.metadata.create_all(bind=manager.engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise DatabaseConnectionError(f"Table creation failed: {e}")


def drop_db(settings: Optional[Settings] = None) -> None:
    """
    Drop all database tables. USE WITH CAUTION.
    
    Primarily used for testing or complete database reset.
    
    Args:
        settings: Optional settings override for testing.
    """
    manager = DatabaseManager(settings) if settings else get_db_manager()
    
    try:
        Base.metadata.drop_all(bind=manager.engine)
        logger.warning("All database tables dropped")
    except Exception as e:
        logger.error(f"Failed to drop database tables: {e}")
        raise DatabaseConnectionError(f"Table drop failed: {e}")


# Convenience exports
__all__ = [
    "Base",
    "Session",
    "DatabaseManager",
    "DatabaseConnectionError",
    "get_db",
    "get_db_manager",
    "reset_db_manager",
    "init_db",
    "drop_db",
]
