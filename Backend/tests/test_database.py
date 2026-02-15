"""
Module 2: Database Tests

Test coverage for app/database.py
Testing DatabaseManager, session management, and connection handling.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import (
    Base,
    DatabaseManager,
    DatabaseConnectionError,
    get_db_manager,
    reset_db_manager,
    init_db,
    drop_db,
    get_db,
)
from app.config import Settings, clear_settings_cache


# Test model for database operations
class TestModel(Base):
    """Simple test model for testing database operations."""
    __tablename__ = "test_items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class TestDatabaseManager:
    """Test cases for DatabaseManager class."""
    
    @pytest.fixture
    def test_settings(self):
        """Create test settings with SQLite in-memory database."""
        return Settings(
            DATABASE_URL="sqlite:///:memory:",
            DEBUG=False,
            ENVIRONMENT="testing"
        )
    
    @pytest.fixture
    def db_manager(self, test_settings):
        """Create a DatabaseManager instance for testing."""
        return DatabaseManager(test_settings)
    
    def test_initialization_creates_engine(self, db_manager):
        """Test that initialization creates the SQLAlchemy engine."""
        assert db_manager.engine is not None
        assert db_manager.SessionLocal is not None
        
    def test_initialization_with_default_settings(self):
        """Test initialization uses get_settings() when no settings provided."""
        with patch('app.database.get_settings') as mock_get_settings:
            mock_settings = Mock()
            mock_settings.DATABASE_URL = "sqlite:///:memory:"
            mock_settings.DEBUG = False
            mock_get_settings.return_value = mock_settings
            
            manager = DatabaseManager()
            assert manager.settings == mock_settings
            
    def test_initialization_failure_raises_error(self):
        """Test that initialization failure raises DatabaseConnectionError."""
        with patch('sqlalchemy.create_engine') as mock_create_engine:
            mock_create_engine.side_effect = Exception("Connection failed")
            
            with pytest.raises(DatabaseConnectionError) as exc_info:
                DatabaseManager(Settings(DATABASE_URL="invalid://url"))
                
            assert "Database initialization failed" in str(exc_info.value)
            
    def test_get_session_yields_session(self, db_manager):
        """Test that get_session yields a SQLAlchemy Session."""
        # Create tables first
        Base.metadata.create_all(bind=db_manager.engine)
        
        session_generator = db_manager.get_session()
        session = next(session_generator)
        
        assert isinstance(session, Session)
        assert session.is_active
        
        # Close generator
        try:
            next(session_generator)
        except StopIteration:
            pass
            
    def test_get_session_not_initialized_raises_error(self, db_manager):
        """Test that get_session raises error if not initialized."""
        db_manager.SessionLocal = None
        
        with pytest.raises(DatabaseConnectionError) as exc_info:
            next(db_manager.get_session())
            
        assert "Database not initialized" in str(exc_info.value)
        
    def test_session_scope_commits_on_success(self, db_manager):
        """Test that session_scope commits when no exception occurs."""
        # Create tables
        Base.metadata.create_all(bind=db_manager.engine)
        
        with db_manager.session_scope() as session:
            item = TestModel(name="test_item")
            session.add(item)
            
        # Verify item was committed by querying in new session
        with db_manager.session_scope() as session:
            result = session.query(TestModel).filter_by(name="test_item").first()
            assert result is not None
            assert result.name == "test_item"
            
    def test_session_scope_rolls_back_on_exception(self, db_manager):
        """Test that session_scope rolls back when exception occurs."""
        # Create tables
        Base.metadata.create_all(bind=db_manager.engine)
        
        try:
            with db_manager.session_scope() as session:
                item = TestModel(name="rollback_test")
                session.add(item)
                raise ValueError("Intentional error")
        except ValueError:
            pass
            
        # Verify item was NOT committed
        with db_manager.session_scope() as session:
            result = session.query(TestModel).filter_by(name="rollback_test").first()
            assert result is None
            
    def test_session_scope_not_initialized_raises_error(self, db_manager):
        """Test that session_scope raises error if not initialized."""
        db_manager.SessionLocal = None
        
        with pytest.raises(DatabaseConnectionError) as exc_info:
            with db_manager.session_scope() as session:
                pass
                
        assert "Database not initialized" in str(exc_info.value)
        
    def test_close_disposes_engine(self, db_manager):
        """Test that close properly disposes of the engine."""
        db_manager.close()
        
        # After close, ping should fail
        result = db_manager.ping()
        assert result is False
        
    def test_ping_success_with_valid_connection(self, db_manager):
        """Test ping returns True with valid connection."""
        result = db_manager.ping()
        assert result is True
        
    def test_ping_failure_with_invalid_connection(self):
        """Test ping returns False with invalid connection."""
        manager = DatabaseManager(Settings(DATABASE_URL="sqlite:///:memory:"))
        manager.close()
        
        result = manager.ping()
        assert result is False
        
    def test_ping_no_engine_returns_false(self, db_manager):
        """Test ping returns False when engine is None."""
        db_manager.engine = None
        
        result = db_manager.ping()
        assert result is False


class TestDatabaseManagerSingleton:
    """Test cases for database manager singleton pattern."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        reset_db_manager()
        
    def teardown_method(self):
        """Clean up after each test."""
        reset_db_manager()
        
    def test_get_db_manager_creates_singleton(self):
        """Test that get_db_manager creates a singleton instance."""
        manager1 = get_db_manager()
        manager2 = get_db_manager()
        
        assert manager1 is manager2
        
    def test_reset_db_manager_clears_singleton(self):
        """Test that reset_db_manager clears the singleton."""
        manager1 = get_db_manager()
        reset_db_manager()
        manager2 = get_db_manager()
        
        assert manager1 is not manager2
        
    def test_reset_db_manager_closes_existing(self):
        """Test that reset closes existing manager connections."""
        manager = get_db_manager()
        
        with patch.object(manager, 'close') as mock_close:
            reset_db_manager()
            mock_close.assert_called_once()


class TestGetDbDependency:
    """Test cases for get_db FastAPI dependency."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        reset_db_manager()
        
    def teardown_method(self):
        """Clean up after each test."""
        reset_db_manager()
        
    @patch('app.database.get_db_manager')
    def test_get_db_yields_session(self, mock_get_manager):
        """Test that get_db yields a database session."""
        # Mock the manager and session
        mock_session = Mock(spec=Session)
        mock_manager = Mock()
        mock_manager.get_session.return_value = iter([mock_session])
        mock_get_manager.return_value = mock_manager
        
        # Get the generator
        gen = get_db()
        session = next(gen)
        
        assert session == mock_session
        
        # Clean up
        try:
            next(gen)
        except StopIteration:
            pass


class TestInitDb:
    """Test cases for init_db function."""
    
    def setup_method(self):
        """Reset singleton and clear cache before each test."""
        reset_db_manager()
        clear_settings_cache()
        
    def teardown_method(self):
        """Clean up after each test."""
        reset_db_manager()
        
    def test_init_db_creates_tables(self):
        """Test that init_db creates all tables."""
        settings = Settings(
            DATABASE_URL="sqlite:///:memory:",
            DEBUG=False,
            ENVIRONMENT="testing"
        )
        
        init_db(settings)
        
        # Verify we can query (tables exist)
        manager = DatabaseManager(settings)
        with manager.session_scope() as session:
            # Should not raise - tables exist
            result = session.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in result]
            assert "test_items" in tables
            
    def test_init_db_with_existing_manager(self):
        """Test init_db uses existing manager when no settings provided."""
        # Pre-initialize the singleton
        settings = Settings(
            DATABASE_URL="sqlite:///:memory:",
            DEBUG=False,
            ENVIRONMENT="testing"
        )
        manager = DatabaseManager(settings)
        
        with patch('app.database.get_db_manager') as mock_get_manager:
            mock_get_manager.return_value = manager
            
            # Should use the existing manager
            init_db()
            mock_get_manager.assert_called_once()
            
    def test_init_db_failure_raises_error(self):
        """Test that init_db failure raises DatabaseConnectionError."""
        with patch.object(Base.metadata, 'create_all') as mock_create:
            mock_create.side_effect = SQLAlchemyError("Creation failed")
            
            settings = Settings(
                DATABASE_URL="sqlite:///:memory:",
                DEBUG=False,
                ENVIRONMENT="testing"
            )
            
            with pytest.raises(DatabaseConnectionError) as exc_info:
                init_db(settings)
                
            assert "Table creation failed" in str(exc_info.value)


class TestDropDb:
    """Test cases for drop_db function."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        reset_db_manager()
        
    def teardown_method(self):
        """Clean up after each test."""
        reset_db_manager()
        
    def test_drop_db_removes_tables(self):
        """Test that drop_db removes all tables."""
        settings = Settings(
            DATABASE_URL="sqlite:///:memory:",
            DEBUG=False,
            ENVIRONMENT="testing"
        )
        
        # First create tables
        init_db(settings)
        
        # Then drop them
        drop_db(settings)
        
        # Verify tables are gone
        manager = DatabaseManager(settings)
        with manager.session_scope() as session:
            result = session.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in result]
            # Only sqlite_sequence should remain (system table)
            assert "test_items" not in tables
            
    def test_drop_db_failure_raises_error(self):
        """Test that drop_db failure raises DatabaseConnectionError."""
        with patch.object(Base.metadata, 'drop_all') as mock_drop:
            mock_drop.side_effect = SQLAlchemyError("Drop failed")
            
            settings = Settings(
                DATABASE_URL="sqlite:///:memory:",
                DEBUG=False,
                ENVIRONMENT="testing"
            )
            
            with pytest.raises(DatabaseConnectionError) as exc_info:
                drop_db(settings)
                
            assert "Table drop failed" in str(exc_info.value)


class TestDatabaseIntegration:
    """Integration tests for database module."""
    
    def setup_method(self):
        """Reset singleton before each test."""
        reset_db_manager()
        clear_settings_cache()
        
    def teardown_method(self):
        """Clean up after each test."""
        reset_db_manager()
        
    def test_full_database_lifecycle(self):
        """Test complete database lifecycle: init → operations → drop."""
        settings = Settings(
            DATABASE_URL="sqlite:///:memory:",
            DEBUG=False,
            ENVIRONMENT="testing"
        )
        
        # Initialize database
        init_db(settings)
        
        manager = DatabaseManager(settings)
        
        # Create item
        with manager.session_scope() as session:
            item = TestModel(name="lifecycle_test")
            session.add(item)
            
        # Read item
        with manager.session_scope() as session:
            result = session.query(TestModel).filter_by(name="lifecycle_test").first()
            assert result is not None
            
        # Drop database
        drop_db(settings)
        
        # Verify tables gone
        manager2 = DatabaseManager(settings)
        with manager2.session_scope() as session:
            result = session.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in result]
            assert "test_items" not in tables
            
    def test_multiple_sessions_independent(self):
        """Test that multiple sessions are independent."""
        settings = Settings(
            DATABASE_URL="sqlite:///:memory:",
            DEBUG=False,
            ENVIRONMENT="testing"
        )
        
        init_db(settings)
        manager = DatabaseManager(settings)
        
        # Create two independent sessions
        with manager.session_scope() as session1:
            item1 = TestModel(name="item1")
            session1.add(item1)
            
        with manager.session_scope() as session2:
            # session2 should see item1 (committed by session1)
            result = session2.query(TestModel).filter_by(name="item1").first()
            assert result is not None
            
            # Add item2 in session2
            item2 = TestModel(name="item2")
            session2.add(item2)
            
        # Verify both items exist
        with manager.session_scope() as session3:
            items = session3.query(TestModel).all()
            assert len(items) == 2


# Run tests with: pytest tests/test_database.py -v
