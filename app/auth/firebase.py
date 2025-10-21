import os
from typing import Optional
from fastapi import Depends, HTTPException, Header
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth as fb_auth, credentials

# Initialize Firebase Admin SDK (only once)
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase-service-account.json")
    
    if not os.path.exists(cred_path):
        raise RuntimeError(f"Firebase service account file not found at: {cred_path}")
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("✅ Firebase Admin SDK initialized successfully")


class CurrentUser(BaseModel):
    """Authenticated user model"""
    uid: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    email_verified: bool = False


async def get_current_user(authorization: Optional[str] = Header(None)) -> CurrentUser:
    """
    Dependency to get the currently authenticated user from Firebase token.
    
    Usage in routes:
        @router.get("/protected")
        async def protected_route(user: CurrentUser = Depends(get_current_user)):
            return {"message": f"Hello {user.email}"}
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Use: Bearer <token>"
        )
    
    # Extract token
    id_token = authorization.split(" ", 1)[1]
    
    try:
        # Verify the Firebase ID token
        decoded_token = fb_auth.verify_id_token(id_token)
        
        # Extract user information
        return CurrentUser(
            uid=decoded_token.get("uid"),
            email=decoded_token.get("email"),
            name=decoded_token.get("name"),
            picture=decoded_token.get("picture"),
            email_verified=decoded_token.get("email_verified", False)
        )
    
    except fb_auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )
    except fb_auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Authentication token has expired"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed: {str(e)}"
        )


async def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[CurrentUser]:
    """
    Optional authentication - returns user if authenticated, None otherwise.
    Useful for routes that work with or without authentication.
    """
    if not authorization:
        return None
    
    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None
