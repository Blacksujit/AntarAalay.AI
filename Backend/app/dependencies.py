from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import get_settings
import requests
from typing import Optional

security = HTTPBearer()


def verify_firebase_token(token: str) -> dict:
    """Verify Firebase JWT token"""
    try:
        # Firebase token verification using Firebase Auth REST API
        # In production, use firebase-admin SDK for better performance
        settings = get_settings()
        
        # For simplicity, we'll verify by calling Firebase Auth
        # In production, use firebase-admin SDK with service account
        response = requests.get(
            f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={settings.FIREBASE_API_KEY}",
            json={"idToken": token}
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        user_data = response.json()
        if "users" not in user_data or len(user_data["users"]) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user_data["users"][0]
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication service unavailable"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> dict:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    user = verify_firebase_token(token)
    return {
        "uid": user.get("localId"),
        "email": user.get("email"),
        "name": user.get("displayName", ""),
        "photo_url": user.get("photoUrl", "")
    }


async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[dict]:
    """Dependency to get optional authenticated user"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            return None
        user = verify_firebase_token(token)
        return {
            "uid": user.get("localId"),
            "email": user.get("email"),
            "name": user.get("displayName", ""),
            "photo_url": user.get("photoUrl", "")
        }
    except Exception:
        return None
