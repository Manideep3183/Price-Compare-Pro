import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
# Support both MONGODB_URI (standard/Vercel) and MONGO_URL (legacy)
MONGO_URL = os.getenv("MONGODB_URI") or os.getenv("MONGO_URL", "mongodb://localhost:27017/SmartCart")
DATABASE_NAME = "SmartCart"

# Global client and database
_client: Optional[AsyncIOMotorClient] = None
_db = None


def get_database():
    """Get MongoDB database instance"""
    global _db
    if _db is None:
        print("⚠️  Database not available. MongoDB connection failed.")
        return None
    return _db


async def init_db():
    """Initialize MongoDB connection"""
    global _client, _db
    
    if not MONGO_URL:
        print("⚠️  MongoDB URL not configured. Running without database.")
        return
    
    try:
        _client = AsyncIOMotorClient(
            MONGO_URL,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000
        )
        
        # Parse database name from connection string or use default
        if "mongodb+srv" in MONGO_URL or "mongodb://" in MONGO_URL:
            # Extract database name from URL if present
            if "/" in MONGO_URL.split("@")[-1]:
                db_part = MONGO_URL.split("@")[-1].split("/")[1].split("?")[0]
                if db_part:
                    _db = _client[db_part]
                else:
                    _db = _client[DATABASE_NAME]
            else:
                _db = _client[DATABASE_NAME]
        else:
            _db = _client.get_default_database()
        
        # Test connection
        await _client.admin.command('ping')
        print(f"✅ MongoDB connected successfully! Database: {_db.name}")
        
        # Create indexes
        await create_indexes()
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"⚠️  Failed to connect to MongoDB: DNS/Network issue")
        print(f"⚠️  Error: {str(e)[:100]}...")
        print("⚠️  Running without database. Authentication and search history features will not work.")
        _client = None
        _db = None
    except Exception as e:
        print(f"⚠️  MongoDB initialization error: {str(e)}")
        print("⚠️  Running without database. Some features may not work.")
        _client = None
        _db = None


async def create_indexes():
    """Create database indexes for better performance"""
    db = get_database()
    
    if db is None:
        return
    
    try:
        # Users collection indexes
        await db.users.create_index([("uid", 1)], unique=True)
        await db.users.create_index([("email", 1)])
        await db.users.create_index([("auth_provider", 1)])
        await db.users.create_index([("created_at", -1)])
        
        # Searches collection indexes
        await db.searches.create_index([("uid", 1), ("created_at", -1)])
        await db.searches.create_index([("created_at", -1)])
        await db.searches.create_index([("query", 1)])
        
        # Activity collection indexes
        await db.activity.create_index([("uid", 1), ("created_at", -1)])
        await db.activity.create_index([("event", 1)])
        await db.activity.create_index([("created_at", -1)])
        await db.activity.create_index([("uid", 1), ("event", 1)])
        
        print("✅ Database indexes created successfully")
        print("   - Users: uid (unique), email, auth_provider, created_at")
        print("   - Searches: uid+created_at, created_at, query")
        print("   - Activity: uid+created_at, event, created_at, uid+event")
    
    except Exception as e:
        print(f"⚠️ Warning: Failed to create indexes: {e}")


async def close_db():
    """Close MongoDB connection"""
    global _client
    if _client:
        _client.close()
        print("✅ MongoDB connection closed")
