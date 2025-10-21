from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.auth.firebase import get_current_user, get_optional_user, CurrentUser
from app.db.mongo import get_database

# IST timezone (UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))

router = APIRouter(prefix="/api/v1", tags=["user-activity"])


class UserProfileRequest(BaseModel):
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    auth_provider: str = "email"  # "email" or "google"


class SearchRequest(BaseModel):
    query: str
    results_count: Optional[int] = 0


class ActivityRequest(BaseModel):
    event: str
    payload: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    id: str
    query: str
    results_count: int
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ActivityResponse(BaseModel):
    id: str
    event: str
    payload: Dict[str, Any]
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


@router.post("/searches", response_model=Dict[str, bool])
async def save_search(
    search_data: SearchRequest,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Save user's search query to MongoDB.
    Requires authentication.
    """
    print(f"📥 Received search save request from user: {user.email}")
    print(f"   Query: {search_data.query}")
    print(f"   Results count: {search_data.results_count}")
    
    db = get_database()
    if db is None:
        print("❌ Database not available!")
        raise HTTPException(status_code=503, detail="Database not available")
    
    doc = {
        "uid": user.uid,
        "email": user.email,
        "query": search_data.query,
        "results_count": search_data.results_count,
        "created_at": datetime.now(IST),
    }
    
    print(f"💾 Attempting to save document: {doc}")
    
    try:
        result = await db.searches.insert_one(doc)
        print(f"✅ Search saved successfully! ID: {result.inserted_id}")
        return {"success": True}
    except Exception as e:
        print(f"❌ Failed to save search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save search: {str(e)}")


@router.get("/searches", response_model=List[SearchResponse])
async def get_user_searches(
    limit: int = 20,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Get user's search history.
    Requires authentication.
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        cursor = db.searches.find({"uid": user.uid}).sort("created_at", -1).limit(limit)
        
        searches = []
        async for doc in cursor:
            # Ensure datetime has IST timezone info
            created_at = doc["created_at"]
            if created_at.tzinfo is None:
                # If no timezone, assume it's UTC and convert to IST
                created_at = created_at.replace(tzinfo=timezone.utc).astimezone(IST)
            elif created_at.tzinfo != IST:
                # If different timezone, convert to IST
                created_at = created_at.astimezone(IST)
            
            searches.append(SearchResponse(
                id=str(doc["_id"]),
                query=doc["query"],
                results_count=doc.get("results_count", 0),
                created_at=created_at
            ))
        
        return searches
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch searches: {str(e)}")


@router.post("/activity", response_model=Dict[str, bool])
async def save_activity(
    activity_data: ActivityRequest,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Log user activity (clicks, views, etc.).
    Requires authentication.
    
    Example events:
    - "clicked_product"
    - "viewed_results"
    - "clicked_retailer"
    - "expanded_view_more"
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    doc = {
        "uid": user.uid,
        "email": user.email,
        "event": activity_data.event,
        "payload": activity_data.payload or {},
        "created_at": datetime.now(IST),
    }
    
    try:
        await db.activity.insert_one(doc)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save activity: {str(e)}")


@router.get("/activity", response_model=List[ActivityResponse])
async def get_user_activity(
    limit: int = 50,
    event_type: Optional[str] = None,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Get user's activity history.
    Optionally filter by event type.
    Requires authentication.
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        query = {"uid": user.uid}
        if event_type:
            query["event"] = event_type
        
        cursor = db.activity.find(query).sort("created_at", -1).limit(limit)
        
        activities = []
        async for doc in cursor:
            # Ensure datetime has IST timezone info
            created_at = doc["created_at"]
            if created_at.tzinfo is None:
                # If no timezone, assume it's UTC and convert to IST
                created_at = created_at.replace(tzinfo=timezone.utc).astimezone(IST)
            elif created_at.tzinfo != IST:
                # If different timezone, convert to IST
                created_at = created_at.astimezone(IST)
            
            activities.append(ActivityResponse(
                id=str(doc["_id"]),
                event=doc["event"],
                payload=doc.get("payload", {}),
                created_at=created_at
            ))
        
        return activities
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch activity: {str(e)}")


@router.get("/profile", response_model=Dict[str, Any])
async def get_user_profile(user: CurrentUser = Depends(get_current_user)):
    """
    Get current user's profile information.
    Requires authentication.
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Get search count
        search_count = await db.searches.count_documents({"uid": user.uid})
        
        # Get recent searches
        recent_searches = await db.searches.find(
            {"uid": user.uid}
        ).sort("created_at", -1).limit(5).to_list(length=5)
        
        return {
            "uid": user.uid,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
            "email_verified": user.email_verified,
            "stats": {
                "total_searches": search_count,
                "recent_searches": [s["query"] for s in recent_searches]
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")


@router.post("/users/create-or-update", response_model=Dict[str, bool])
async def create_or_update_user(
    user_data: UserProfileRequest,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Create or update user profile in MongoDB.
    This should be called after user signs up or logs in.
    Requires authentication.
    """
    print(f"📝 Creating/updating user profile for: {user.email}")
    
    db = get_database()
    if db is None:
        print("❌ Database not available!")
        raise HTTPException(status_code=503, detail="Database not available")
    
    # Check if user already exists
    existing_user = await db.users.find_one({"uid": user.uid})
    
    user_doc = {
        "uid": user.uid,
        "email": user.email,
        "email_verified": user.email_verified,
        "auth_provider": user_data.auth_provider,
        "updated_at": datetime.now(IST),
    }
    
    # Add optional fields if provided
    if user_data.display_name:
        user_doc["display_name"] = user_data.display_name
    elif user.name:
        user_doc["display_name"] = user.name
    
    if user_data.phone_number:
        user_doc["phone_number"] = user_data.phone_number
    
    if user.picture:
        user_doc["picture"] = user.picture
    
    try:
        if existing_user:
            # Update existing user
            print(f"✏️ Updating existing user: {user.email}")
            await db.users.update_one(
                {"uid": user.uid},
                {"$set": user_doc}
            )
        else:
            # Create new user
            print(f"➕ Creating new user: {user.email}")
            user_doc["created_at"] = datetime.now(IST)
            await db.users.insert_one(user_doc)
        
        print(f"✅ User profile saved successfully: {user.email}")
        return {"success": True}
    
    except Exception as e:
        print(f"❌ Failed to save user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save user profile: {str(e)}")


@router.get("/users/me", response_model=Dict[str, Any])
async def get_user_profile(user: CurrentUser = Depends(get_current_user)):
    """
    Get current user's profile from MongoDB.
    Requires authentication.
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        user_doc = await db.users.find_one({"uid": user.uid})
        
        if not user_doc:
            # Return basic info from Firebase if not in MongoDB yet
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.name,
                "email_verified": user.email_verified,
                "picture": user.picture,
                "auth_provider": "unknown",
                "created_at": None
            }
        
        # Convert ObjectId to string
        user_doc["_id"] = str(user_doc["_id"])
        
        return user_doc
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user profile: {str(e)}")


@router.get("/users/check-exists", response_model=Dict[str, bool])
async def check_user_exists(user: CurrentUser = Depends(get_current_user)):
    """
    Check if user exists in MongoDB database.
    Returns {"exists": true/false}
    Used to verify user hasn't been deleted.
    """
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        user_doc = await db.users.find_one({"uid": user.uid})
        return {"exists": user_doc is not None}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check user existence: {str(e)}")


@router.delete("/users/me", response_model=Dict[str, Any])
async def delete_user_account(user: CurrentUser = Depends(get_current_user)):
    """
    Delete user account and all associated data (cascade delete).
    This will remove:
    - User profile from users collection
    - All searches from searches collection
    - All activity logs from activity collection
    
    Requires authentication.
    """
    print(f"🗑️ Deleting user account: {user.email}")
    
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Count documents to be deleted
        searches_count = await db.searches.count_documents({"uid": user.uid})
        activity_count = await db.activity.count_documents({"uid": user.uid})
        
        # Delete user's searches
        searches_result = await db.searches.delete_many({"uid": user.uid})
        print(f"🗑️ Deleted {searches_result.deleted_count} searches")
        
        # Delete user's activity logs
        activity_result = await db.activity.delete_many({"uid": user.uid})
        print(f"🗑️ Deleted {activity_result.deleted_count} activity logs")
        
        # Delete user profile
        user_result = await db.users.delete_one({"uid": user.uid})
        print(f"🗑️ Deleted user profile: {user.email}")
        
        if user_result.deleted_count == 0:
            print(f"⚠️ User profile not found in database: {user.email}")
        
        print(f"✅ Successfully deleted user account: {user.email}")
        
        return {
            "success": True,
            "deleted": {
                "user": user_result.deleted_count,
                "searches": searches_result.deleted_count,
                "activity": activity_result.deleted_count,
                "total": user_result.deleted_count + searches_result.deleted_count + activity_result.deleted_count
            }
        }
    
    except Exception as e:
        print(f"❌ Failed to delete user account: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete user account: {str(e)}")
