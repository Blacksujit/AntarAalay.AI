"""
Firebase Client Module for AntarAalay.ai

Provides Firebase Admin SDK initialization for:
- Authentication (JWT verification)
- Firestore (NoSQL database)
- Storage (file uploads)
"""
import os
import json
from typing import Optional, Dict, Any
from functools import lru_cache
from threading import Lock

import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
from firebase_admin.exceptions import FirebaseError

from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


_mock_lock = Lock()
_mock_blob_store: Dict[str, Dict[str, bytes]] = {}


class _MockDocumentSnapshot:
    def __init__(self, data: Optional[Dict[str, Any]]):
        self._data = data

    @property
    def exists(self) -> bool:
        return self._data is not None

    def to_dict(self) -> Optional[Dict[str, Any]]:
        return self._data


class _MockDocumentRef:
    def __init__(self, store: Dict[str, Dict[str, Any]], doc_id: str):
        self._store = store
        self._doc_id = doc_id

    def set(self, data: Dict[str, Any]) -> None:
        with _mock_lock:
            self._store[self._doc_id] = dict(data)

    def get(self) -> _MockDocumentSnapshot:
        with _mock_lock:
            return _MockDocumentSnapshot(self._store.get(self._doc_id))


class _MockQuery:
    def __init__(self, store: Dict[str, Dict[str, Any]], filters: list[tuple[str, str, Any]]):
        self._store = store
        self._filters = filters

    def where(self, field: str, op: str, value: Any) -> "_MockQuery":
        return _MockQuery(self._store, [*self._filters, (field, op, value)])

    def stream(self):
        with _mock_lock:
            items = list(self._store.values())

        def matches(item: Dict[str, Any]) -> bool:
            for field, op, value in self._filters:
                if op != "==":
                    return False
                if item.get(field) != value:
                    return False
            return True

        for item in items:
            if matches(item):
                yield _MockDocumentSnapshot(item)

    def order_by(self, *args, **kwargs):
        return self

    def get(self):
        return list(self.stream())


class _MockCollection:
    def __init__(self, store: Dict[str, Dict[str, Any]]):
        self._store = store

    def document(self, doc_id: str) -> _MockDocumentRef:
        return _MockDocumentRef(self._store, doc_id)

    def where(self, field: str, op: str, value: Any) -> _MockQuery:
        return _MockQuery(self._store, [(field, op, value)])


class _MockBlob:
    def __init__(self, bucket_name: str, path: str):
        self._bucket_name = bucket_name
        self._path = path
        self._content: Optional[bytes] = None
        self._content_type: Optional[str] = None

    def upload_from_string(self, content: bytes, content_type: str = "application/octet-stream") -> None:
        self._content = content
        self._content_type = content_type
        with _mock_lock:
            bucket = _mock_blob_store.setdefault(self._bucket_name, {})
            bucket[self._path] = content

    def make_public(self) -> None:
        return None

    @property
    def public_url(self) -> str:
        # Served by backend route /api/mock-storage/{bucket}/{path}
        return f"http://127.0.0.1:8000/api/mock-storage/{self._bucket_name}/{self._path}"

    def delete(self) -> None:
        self._content = None
        with _mock_lock:
            bucket = _mock_blob_store.get(self._bucket_name)
            if bucket and self._path in bucket:
                del bucket[self._path]


class _MockBucket:
    def __init__(self, name: str = "mock-bucket"):
        self.name = name

    def blob(self, path: str) -> _MockBlob:
        return _MockBlob(self.name, path)

# Global Firebase app instance
_firebase_app: Optional[firebase_admin.App] = None


def initialize_firebase() -> Optional[firebase_admin.App]:
    """
    Initialize Firebase Admin SDK.
    
    Uses service account credentials from environment or file.
    Returns None if credentials not available (mock mode for dev).
    """
    global _firebase_app
    
    if _firebase_app is not None:
        return _firebase_app
    
    try:
        settings = get_settings()
        
        # Check if Firebase is already initialized
        if len(firebase_admin._apps) > 0:
            _firebase_app = firebase_admin.get_app()
            logger.info("Using existing Firebase app")
            return _firebase_app
        
        # Try to get credentials from environment variable
        cred_path = settings.FIREBASE_CREDENTIALS_PATH
        
        if cred_path and os.path.exists(cred_path):
            # Load from file
            cred = credentials.Certificate(cred_path)
            logger.info(f"Initialized Firebase from credentials file: {cred_path}")
        else:
            # Try to load from environment variable containing JSON
            cred_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
            if cred_json:
                cred_dict = json.loads(cred_json)
                cred = credentials.Certificate(cred_dict)
                logger.info("Initialized Firebase from environment JSON")
            else:
                # No credentials available - use mock mode
                logger.warning("No Firebase credentials found. Running in MOCK mode.")
                return None
        
        # Initialize with storage bucket if configured
        config = {}
        if settings.FIREBASE_STORAGE_BUCKET:
            config["storageBucket"] = settings.FIREBASE_STORAGE_BUCKET
        
        _firebase_app = firebase_admin.initialize_app(cred, config)
        logger.info("Firebase Admin SDK initialized successfully")
        
        return _firebase_app
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        # Return None to indicate mock mode
        return None


class FirebaseAuthService:
    """Service for Firebase Authentication operations."""
    
    def __init__(self):
        self.app = initialize_firebase()
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify Firebase JWT token.
        
        Args:
            token: Firebase ID token
            
        Returns:
            Decoded token claims
            
        Raises:
            ValueError: If token is invalid
        """
        try:
            decoded_token = auth.verify_id_token(token, app=self.app)
            logger.info(f"Token verified for user: {decoded_token.get('uid')}")
            return decoded_token
        except auth.InvalidIdTokenError:
            logger.error("Invalid Firebase ID token")
            raise ValueError("Invalid authentication token")
        except auth.ExpiredIdTokenError:
            logger.error("Expired Firebase ID token")
            raise ValueError("Authentication token has expired")
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            raise ValueError(f"Authentication failed: {str(e)}")
    
    async def get_user(self, uid: str) -> Dict[str, Any]:
        """Get user by UID."""
        try:
            user = auth.get_user(uid, app=self.app)
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "photo_url": user.photo_url,
            }
        except Exception as e:
            logger.error(f"Failed to get user {uid}: {e}")
            raise


class FirestoreService:
    """Service for Firestore database operations."""
    
    def __init__(self):
        self.app = initialize_firebase()
        self.db = None
        self._mock_rooms: Dict[str, Dict[str, Any]] = {}
        self._mock_designs: Dict[str, Dict[str, Any]] = {}
        if self.app:
            self.db = firestore.client(app=self.app)
        else:
            logger.warning("FirestoreService running in MOCK mode - no Firebase app")
    
    def _check_mock(self):
        """Check if in mock mode and raise error."""
        if self.db is None:
            raise RuntimeError("Firebase not initialized. Configure FIREBASE_CREDENTIALS_PATH or FIREBASE_SERVICE_ACCOUNT_JSON.")

    def collection(self, name: str):
        """Firestore-like collection accessor.

        In MOCK mode this returns an in-memory collection that supports the subset
        of methods used by the app (document().set/get and where().stream()).
        """
        if self.db is not None:
            return self.db.collection(name)
        if name == "rooms":
            return _MockCollection(self._mock_rooms)
        if name == "designs":
            return _MockCollection(self._mock_designs)
        return _MockCollection({})
    
    # Room operations
    async def create_room(
        self,
        room_id: str,
        user_id: str,
        images: Dict[str, str],
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Create a room document in Firestore."""
        from datetime import datetime
        
        room_data = {
            "room_id": room_id,
            "user_id": user_id,
            "images": images,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "status": "uploaded",
            "metadata": metadata or {}
        }
        
        await asyncio.to_thread(
            self.collection("rooms").document(room_id).set,
            room_data
        )
        
        logger.info(f"Room created: {room_id}")
        return room_data
    
    async def get_room(self, room_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get room by ID, verifying user ownership."""
        doc_ref = self.collection("rooms").document(room_id)
        doc = await asyncio.to_thread(doc_ref.get)
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        if data.get("user_id") != user_id:
            logger.warning(f"User {user_id} attempted to access room {room_id}")
            return None
        
        return data
    
    async def get_user_rooms(self, user_id: str) -> list:
        """Get all rooms for a user."""
        query = self.collection("rooms").where("user_id", "==", user_id)
        docs = await asyncio.to_thread(query.get)
        
        rooms = []
        for doc in docs:
            rooms.append(doc.to_dict())
        
        return rooms
    
    # Design operations
    async def create_design(
        self,
        design_id: str,
        room_id: str,
        user_id: str,
        style: str,
        customization: Dict[str, Any],
        prompt_used: str,
        generated_images: list,
        version: int = 1
    ) -> Dict[str, Any]:
        """Create a design document in Firestore."""
        from datetime import datetime
        
        image_1_url = generated_images[0] if len(generated_images) > 0 else None
        image_2_url = generated_images[1] if len(generated_images) > 1 else None
        image_3_url = generated_images[2] if len(generated_images) > 2 else None

        design_data = {
            "id": design_id,
            "room_id": room_id,
            "user_id": user_id,
            "style": style,
            "budget": None,
            "image_1_url": image_1_url,
            "image_2_url": image_2_url,
            "image_3_url": image_3_url,
            "estimated_cost": None,
            "budget_match_percentage": None,
            "furniture_breakdown": None,
            "vastu_score": None,
            "vastu_suggestions": None,
            "vastu_warnings": None,
            "status": "completed",
            "created_at": datetime.utcnow().isoformat(),
            "customization": customization,
            "prompt_used": prompt_used,
            "version": version,
        }
        
        await asyncio.to_thread(
            self.collection("designs").document(design_id).set,
            design_data
        )
        
        logger.info(f"Design created: {design_id}")
        return design_data
    
    async def get_design(self, design_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get design by ID, verifying user ownership."""
        doc_ref = self.collection("designs").document(design_id)
        doc = await asyncio.to_thread(doc_ref.get)
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        if data.get("user_id") != user_id:
            logger.warning(f"User {user_id} attempted to access design {design_id}")
            return None
        
        return data
    
    async def get_room_designs(self, room_id: str, user_id: str) -> list:
        """Get all designs for a room."""
        query = (
            self.collection("designs")
            .where("room_id", "==", room_id)
            .where("user_id", "==", user_id)
            .order_by("created_at", direction=firestore.Query.DESCENDING)
        )
        docs = await asyncio.to_thread(query.get)
        
        designs = []
        for doc in docs:
            designs.append(doc.to_dict())
        
        return designs


class FirebaseStorageService:
    """Service for Firebase Storage operations."""
    
    def __init__(self):
        self.app = initialize_firebase()
        self.bucket = None
        if self.app:
            self.bucket = storage.bucket(app=self.app)
        else:
            logger.warning("FirebaseStorageService running in MOCK mode - no Firebase app")
            self.bucket = _MockBucket()
    
    def _check_mock(self):
        """Check if in mock mode and raise error."""
        if self.bucket is None:
            raise RuntimeError("Firebase Storage not initialized. Configure FIREBASE_CREDENTIALS_PATH or FIREBASE_SERVICE_ACCOUNT_JSON.")
    
    async def upload_image(
        self,
        file_content: bytes,
        content_type: str,
        folder: str,
        filename: str
    ) -> str:
        """
        Upload image to Firebase Storage.
        
        Args:
            file_content: Binary image data
            content_type: MIME type (image/jpeg, image/png)
            folder: Storage folder path (e.g., "users/{user_id}/rooms/{room_id}")
            filename: Name for the file
            
        Returns:
            Public download URL
        """
        import uuid
        from datetime import datetime, timedelta
        
        # Generate unique filename
        ext = content_type.split("/")[-1]
        if ext == "jpeg":
            ext = "jpg"
        
        unique_name = f"{filename}_{uuid.uuid4().hex[:8]}.{ext}"
        blob_path = f"{folder}/{unique_name}"
        
        blob = self.bucket.blob(blob_path)
        
        # Upload with content type
        await asyncio.to_thread(
            blob.upload_from_string,
            file_content,
            content_type=content_type
        )
        
        # Make publicly accessible
        await asyncio.to_thread(blob.make_public)
        
        # Get public URL
        public_url = blob.public_url
        
        logger.info(f"Image uploaded: {blob_path}")
        return public_url
    
    async def delete_image(self, url: str) -> bool:
        """Delete image from Firebase Storage by URL."""
        try:
            # Extract blob path from URL
            # URL format: https://storage.googleapis.com/{bucket}/{path}
            path_start = url.find(".com/") + 5
            blob_path = url[path_start:]
            
            blob = self.bucket.blob(blob_path)
            await asyncio.to_thread(blob.delete)
            
            logger.info(f"Image deleted: {blob_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete image: {e}")
            return False


# Import asyncio for Firestore operations
import asyncio


# Singleton instances
@lru_cache()
def get_firebase_auth() -> FirebaseAuthService:
    return FirebaseAuthService()


@lru_cache()
def get_firestore() -> FirestoreService:
    return FirestoreService()


@lru_cache()
def get_firebase_storage() -> FirebaseStorageService:
    return FirebaseStorageService()


def get_storage_bucket():
    return get_firebase_storage().bucket
