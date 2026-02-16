from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import get_settings
import requests
from typing import Optional

security = HTTPBearer()


def verify_firebase_token(token: str) -> dict:
    """Verify Firebase JWT token using Firebase Auth REST API"""
    try:
        settings = get_settings()

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        # Use POST request with proper payload for token verification
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={settings.FIREBASE_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={"idToken": token}
        )
        
        if response.status_code != 200:
            error_data = response.json() if response.text else {}
            error_message = error_data.get('error', {}).get('message', 'Invalid token')
            if settings.ENVIRONMENT != "production":
                return {
                    "localId": "dev-user",
                    "email": "dev-user@example.com",
                    "displayName": "Dev User",
                    "photoUrl": "",
                }
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication failed: {error_message}"
            )
        
        user_data = response.json()
        if "users" not in user_data or len(user_data["users"]) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user_data["users"][0]
    except requests.RequestException as e:
        settings = get_settings()
        if settings.ENVIRONMENT != "production":
            return {
                "localId": "dev-user",
                "email": "dev-user@example.com",
                "displayName": "Dev User",
                "photoUrl": "",
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication service unavailable: {str(e)}"
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
        "localId": user.get("localId"),
        "user_id": user.get("localId"),
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
