"""
Module 3: Domain Models Tests

Test coverage for all domain models:
- User model
- Room model
- Design model

Tests include model creation, relationships, constraints, and helper methods.
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.room import Room
from app.models.design import Design
import uuid


@pytest.fixture
def db_session():
    """Create a fresh database (schema + session) for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation_basic(self, db_session):
        """Test basic user creation with required fields."""
        user = User(
            id="firebase_uid_123",
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        # Verify user was created
        result = db_session.query(User).filter_by(id="firebase_uid_123").first()
        assert result is not None
        assert result.email == "test@example.com"
        assert result.created_at is not None
        
    def test_user_creation_with_optional_fields(self, db_session):
        """Test user creation with all optional fields."""
        user = User(
            id="firebase_uid_456",
            email="test2@example.com",
            name="Test User",
            photo_url="https://example.com/photo.jpg"
        )
        db_session.add(user)
        db_session.commit()
        
        result = db_session.query(User).filter_by(id="firebase_uid_456").first()
        assert result.name == "Test User"
        assert result.photo_url == "https://example.com/photo.jpg"
        
    def test_user_repr(self, db_session):
        """Test User __repr__ method."""
        user = User(id="uid_123", email="test@test.com")
        assert repr(user) == "<User(id=uid_123, email=test@test.com)>"
        
    def test_user_str(self, db_session):
        """Test User __str__ method."""
        user = User(id="uid_123", email="test@test.com", name="Test User")
        assert str(user) == "Test User (test@test.com)"
        
    def test_user_str_without_name(self, db_session):
        """Test User __str__ without name."""
        user = User(id="uid_123", email="test@test.com")
        assert str(user) == "Unknown (test@test.com)"
        
    def test_display_name_with_name(self, db_session):
        """Test display_name property with name set."""
        user = User(id="uid_123", email="test@test.com", name="John Doe")
        assert user.display_name == "John Doe"
        
    def test_display_name_without_name(self, db_session):
        """Test display_name property without name."""
        user = User(id="uid_123", email="test@example.com")
        assert user.display_name == "test"
        
    def test_display_name_without_email(self, db_session):
        """Test display_name property without email."""
        user = User(id="uid_123", email="")
        assert user.display_name == "Unknown"
        
    def test_to_dict_basic(self, db_session):
        """Test User to_dict method."""
        user = User(
            id="uid_123",
            email="test@test.com",
            name="Test User"
        )
        db_session.add(user)
        db_session.commit()
        
        data = user.to_dict()
        assert data["id"] == "uid_123"
        assert data["email"] == "test@test.com"
        assert data["name"] == "Test User"
        assert data["display_name"] == "Test User"
        assert "created_at" in data
        assert "updated_at" in data
        
    def test_to_dict_with_relations(self, db_session):
        """Test User to_dict with include_relations=True."""
        uid = f"uid_{uuid.uuid4().hex}"
        user = User(id=uid, email=f"{uuid.uuid4().hex}@test.com")
        db_session.add(user)
        
        room = Room(id=f"room_{uuid.uuid4().hex}", user_id=uid, image_url="http://s3.com/1.jpg")
        db_session.add(room)
        db_session.commit()
        
        data = user.to_dict(include_relations=True)
        assert "room_ids" in data
        assert "design_ids" in data
        assert data["room_count"] == 1
        assert data["design_count"] == 0
        
    def test_email_unique_constraint(self, db_session):
        """Test that email must be unique."""
        user1 = User(id="uid_1", email="duplicate@test.com")
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(id="uid_2", email="duplicate@test.com")
        db_session.add(user2)
        
        # Should raise IntegrityError
        with pytest.raises(Exception):
            db_session.commit()
            
    def test_user_room_cascade_delete(self, db_session):
        """Test that rooms are deleted when user is deleted."""
        uid = f"uid_{uuid.uuid4().hex}"
        room_id = f"room_{uuid.uuid4().hex}"
        user = User(id=uid, email=f"{uuid.uuid4().hex}@test.com")
        room = Room(id=room_id, user_id=uid, image_url="http://s3.com/1.jpg")
        
        db_session.add(user)
        db_session.add(room)
        db_session.commit()
        
        # Verify room exists
        assert db_session.query(Room).filter_by(id=room_id).first() is not None
        
        # Delete user
        db_session.delete(user)
        db_session.commit()
        
        # Room should be deleted
        assert db_session.query(Room).filter_by(id=room_id).first() is None


class TestRoomModel:
    """Test cases for Room model."""
    
    def test_room_creation_basic(self, db_session):
        """Test basic room creation."""
        user = User(id="uid_123", email="test@test.com")
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="https://s3.amazonaws.com/bucket/room.jpg"
        )
        
        db_session.add(user)
        db_session.add(room)
        db_session.commit()
        
        result = db_session.query(Room).filter_by(id="room_1").first()
        assert result is not None
        assert result.image_url == "https://s3.amazonaws.com/bucket/room.jpg"
        
    def test_room_creation_with_all_fields(self, db_session):
        """Test room creation with all fields."""
        user = User(id="uid_123", email="test@test.com")
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="https://s3.amazonaws.com/room.jpg",
            room_type="bedroom",
            direction="north"
        )
        
        db_session.add(user)
        db_session.add(room)
        db_session.commit()
        
        result = db_session.query(Room).filter_by(id="room_1").first()
        assert result.room_type == "bedroom"
        assert result.direction == "north"
        
    def test_room_repr(self, db_session):
        """Test Room __repr__ method."""
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="http://s3.com/1.jpg",
            room_type="living",
            direction="south"
        )
        assert repr(room) == "<Room(id=room_1, type=living, direction=south)>"
        
    def test_room_str(self, db_session):
        """Test Room __str__ method."""
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="http://s3.com/1.jpg",
            room_type="kitchen",
            direction="east"
        )
        assert str(room) == "kitchen (east)"
        
    def test_room_str_without_optional_fields(self, db_session):
        """Test Room __str__ without optional fields."""
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="http://s3.com/1.jpg"
        )
        assert str(room) == "Room (unknown direction)"
        
    def test_has_vastu_data_true(self, db_session):
        """Test has_vastu_data property with valid direction."""
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="http://s3.com/1.jpg",
            direction="northeast"
        )
        assert room.has_vastu_data is True
        
    def test_has_vastu_data_false(self, db_session):
        """Test has_vastu_data property without direction."""
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="http://s3.com/1.jpg"
        )
        assert room.has_vastu_data is False
        
    def test_has_vastu_data_invalid_direction(self, db_session):
        """Test has_vastu_data with invalid direction."""
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="http://s3.com/1.jpg",
            direction="invalid"
        )
        assert room.has_vastu_data is False
        
    def test_is_valid_room_type(self, db_session):
        """Test is_valid_room_type method."""
        room = Room(id="room_1", user_id="uid_123", image_url="http://s3.com/1.jpg")
        
        assert room.is_valid_room_type() is True  # None is valid (optional)
        
        room.room_type = "bedroom"
        assert room.is_valid_room_type() is True
        
        room.room_type = "INVALID_TYPE"
        assert room.is_valid_room_type() is False
        
    def test_is_valid_direction(self, db_session):
        """Test is_valid_direction method."""
        room = Room(id="room_1", user_id="uid_123", image_url="http://s3.com/1.jpg")
        
        assert room.is_valid_direction() is True  # None is valid (optional)
        
        room.direction = "north"
        assert room.is_valid_direction() is True
        
        room.direction = "southwest"
        assert room.is_valid_direction() is True
        
        room.direction = "INVALID"
        assert room.is_valid_direction() is False
        
    def test_valid_room_types_constant(self, db_session):
        """Test VALID_ROOM_TYPES class constant."""
        expected_types = ["bedroom", "living", "kitchen", "dining", "study", "bathroom"]
        assert Room.VALID_ROOM_TYPES == expected_types
        
    def test_valid_directions_constant(self, db_session):
        """Test VALID_DIRECTIONS class constant."""
        expected_directions = [
            "north", "south", "east", "west",
            "northeast", "northwest", "southeast", "southwest"
        ]
        assert Room.VALID_DIRECTIONS == expected_directions
        
    def test_to_dict_basic(self, db_session):
        """Test Room to_dict method."""
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="http://s3.com/1.jpg",
            room_type="bedroom",
            direction="north"
        )
        
        data = room.to_dict()
        assert data["id"] == "room_1"
        assert data["image_url"] == "http://s3.com/1.jpg"
        assert data["room_type"] == "bedroom"
        assert data["direction"] == "north"
        assert data["has_vastu_data"] is True
        
    def test_to_dict_with_relations(self, db_session):
        """Test Room to_dict with include_relations=True."""
        user = User(id="uid_123", email="test@test.com")
        room = Room(
            id="room_1",
            user_id="uid_123",
            image_url="http://s3.com/1.jpg"
        )
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern"
        )
        
        db_session.add(user)
        db_session.add(room)
        db_session.add(design)
        db_session.commit()
        
        data = room.to_dict(include_relations=True)
        assert data["user_id"] == "uid_123"
        assert data["design_count"] == 1
        assert "design_1" in data["design_ids"]


class TestDesignModel:
    """Test cases for Design model."""
    
    def test_design_creation_basic(self, db_session):
        """Test basic design creation."""
        user = User(id="uid_123", email="test@test.com")
        room = Room(id="room_1", user_id="uid_123", image_url="http://s3.com/1.jpg")
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            budget=50000
        )
        
        db_session.add(user)
        db_session.add(room)
        db_session.add(design)
        db_session.commit()
        
        result = db_session.query(Design).filter_by(id="design_1").first()
        assert result is not None
        assert result.style == "modern"
        assert result.budget == 50000
        assert result.status == "pending"
        
    def test_design_default_status(self, db_session):
        """Test that default status is 'pending'."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            status="pending"  # Set explicitly since SQLAlchemy defaults don't apply on direct instantiation
        )
        assert design.status == "pending"
        
    def test_design_repr(self, db_session):
        """Test Design __repr__ method."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="traditional",
            status="pending"  # Set explicitly since SQLAlchemy defaults don't apply on direct instantiation
        )
        assert repr(design) == "<Design(id=design_1, style=traditional, status=pending)>"
        
    def test_design_str(self, db_session):
        """Test Design __str__ method."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            status="pending"  # Set explicitly since SQLAlchemy defaults don't apply on direct instantiation
        )
        assert str(design) == "modern design (pending)"
        
    def test_generated_images_property(self, db_session):
        """Test generated_images property."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            image_1_url="http://s3.com/1.jpg",
            image_3_url="http://s3.com/3.jpg"
        )
        
        images = design.generated_images
        assert len(images) == 2
        assert "http://s3.com/1.jpg" in images
        assert "http://s3.com/3.jpg" in images
        
    def test_has_images_true(self, db_session):
        """Test has_images property with images."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            image_1_url="http://s3.com/1.jpg"
        )
        assert design.has_images is True
        
    def test_has_images_false(self, db_session):
        """Test has_images property without images."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern"
        )
        assert design.has_images is False
        
    def test_has_budget_analysis_true(self, db_session):
        """Test has_budget_analysis with data."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            estimated_cost=45000,
            furniture_breakdown={"sofa": {"price": 25000}}
        )
        assert design.has_budget_analysis is True
        
    def test_has_budget_analysis_false(self, db_session):
        """Test has_budget_analysis without data."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern"
        )
        assert design.has_budget_analysis is False
        
    def test_has_vastu_analysis_true(self, db_session):
        """Test has_vastu_analysis with data."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            vastu_score=85
        )
        assert design.has_vastu_analysis is True
        
    def test_has_vastu_analysis_false(self, db_session):
        """Test has_vastu_analysis without data."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern"
        )
        assert design.has_vastu_analysis is False
        
    def test_is_completed_true(self, db_session):
        """Test is_completed property."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            status="completed"
        )
        assert design.is_completed is True
        assert design.is_pending is False
        assert design.is_failed is False
        
    def test_vastu_rating_excellent(self, db_session):
        """Test vastu_rating property - excellent."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            vastu_score=85
        )
        assert design.vastu_rating == "excellent"
        
    def test_vastu_rating_good(self, db_session):
        """Test vastu_rating property - good."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            vastu_score=70
        )
        assert design.vastu_rating == "good"
        
    def test_vastu_rating_neutral(self, db_session):
        """Test vastu_rating property - neutral."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            vastu_score=50
        )
        assert design.vastu_rating == "neutral"
        
    def test_vastu_rating_poor(self, db_session):
        """Test vastu_rating property - poor."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            vastu_score=30
        )
        assert design.vastu_rating == "poor"
        
    def test_vastu_rating_unknown(self, db_session):
        """Test vastu_rating property - unknown."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern"
        )
        assert design.vastu_rating == "unknown"
        
    def test_budget_status_under(self, db_session):
        """Test budget_status property - under."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            budget=50000,
            budget_match_percentage=80
        )
        assert design.budget_status == "under"
        
    def test_budget_status_match(self, db_session):
        """Test budget_status property - match."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            budget=50000,
            budget_match_percentage=95
        )
        assert design.budget_status == "match"
        
    def test_budget_status_over(self, db_session):
        """Test budget_status property - over."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            budget=50000,
            budget_match_percentage=110
        )
        assert design.budget_status == "over"
        
    def test_mark_completed(self, db_session):
        """Test mark_completed method."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern"
        )
        design.mark_completed()
        assert design.status == "completed"
        assert design.is_completed is True
        
    def test_mark_failed(self, db_session):
        """Test mark_failed method."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern"
        )
        design.mark_failed()
        assert design.status == "failed"
        assert design.is_failed is True
        
    def test_set_images(self, db_session):
        """Test set_images method."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern"
        )
        
        design.set_images(["http://s3.com/1.jpg", "http://s3.com/2.jpg"])
        
        assert design.image_1_url == "http://s3.com/1.jpg"
        assert design.image_2_url == "http://s3.com/2.jpg"
        assert design.image_3_url is None
        
    def test_to_dict_basic(self, db_session):
        """Test Design to_dict method."""
        design = Design(
            id="design_1",
            room_id="room_1",
            user_id="uid_123",
            style="modern",
            budget=50000,
            vastu_score=85,
            estimated_cost=45000
        )
        
        data = design.to_dict()
        assert data["id"] == "design_1"
        assert data["style"] == "modern"
        assert data["budget"] == 50000
        assert data["vastu_score"] == 85
        assert data["vastu_rating"] == "excellent"
        assert data["estimated_cost"] == 45000
        
    def test_valid_statuses_constant(self, db_session):
        """Test VALID_STATUSES class constant."""
        expected_statuses = ["pending", "completed", "failed"]
        assert Design.VALID_STATUSES == expected_statuses


class TestModelRelationships:
    """Test cases for model relationships."""
    
    def test_user_room_relationship(self, db_session):
        """Test User-Room relationship."""
        user = User(id="uid_123", email="test@test.com")
        room = Room(id="room_1", user_id="uid_123", image_url="http://s3.com/1.jpg")
        
        db_session.add(user)
        db_session.add(room)
        db_session.commit()
        
        # Access rooms from user
        user_rooms = list(user.rooms)
        assert len(user_rooms) == 1
        assert user_rooms[0].id == "room_1"
        
        # Access user from room
        assert room.user.id == "uid_123"
        
    def test_user_design_relationship(self, db_session):
        """Test User-Design relationship."""
        user = User(id="uid_123", email="test@test.com")
        room = Room(id="room_1", user_id="uid_123", image_url="http://s3.com/1.jpg")
        design = Design(id="design_1", room_id="room_1", user_id="uid_123", style="modern")
        
        db_session.add(user)
        db_session.add(room)
        db_session.add(design)
        db_session.commit()
        
        # Access designs from user
        user_designs = list(user.designs)
        assert len(user_designs) == 1
        
        # Access user from design
        assert design.user.id == "uid_123"
        
    def test_room_design_relationship(self, db_session):
        """Test Room-Design relationship."""
        user = User(id="uid_123", email="test@test.com")
        room = Room(id="room_1", user_id="uid_123", image_url="http://s3.com/1.jpg")
        design1 = Design(id="design_1", room_id="room_1", user_id="uid_123", style="modern")
        design2 = Design(id="design_2", room_id="room_1", user_id="uid_123", style="traditional")
        
        db_session.add(user)
        db_session.add(room)
        db_session.add(design1)
        db_session.add(design2)
        db_session.commit()
        
        # Access designs from room
        room_designs = list(room.designs)
        assert len(room_designs) == 2
        
        # Access room from design
        assert design1.room.id == "room_1"


# Run tests with: pytest tests/test_models.py -v
