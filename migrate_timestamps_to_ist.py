"""
Migration script to convert all UTC timestamps to IST in MongoDB.
This will update created_at and updated_at fields in users, searches, and activity collections.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# IST timezone (UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))

# MongoDB connection string
MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://smartcart2025:smartcart2025@smartcart.gh9rs42.mongodb.net/SmartCart")

async def migrate_timestamps():
    """Migrate all UTC timestamps to IST"""
    print("🚀 Starting timestamp migration to IST...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database("SmartCart")
    
    try:
        # Migrate users collection
        print("\n📊 Migrating users collection...")
        users_cursor = db.users.find({})
        users_updated = 0
        async for user in users_cursor:
            update_fields = {}
            
            if 'created_at' in user and user['created_at'].tzinfo is None:
                # If no timezone info, assume it's UTC and convert to IST
                utc_time = user['created_at'].replace(tzinfo=timezone.utc)
                ist_time = utc_time.astimezone(IST)
                update_fields['created_at'] = ist_time
            elif 'created_at' in user and user['created_at'].tzinfo == timezone.utc:
                # If it's explicitly UTC, convert to IST
                ist_time = user['created_at'].astimezone(IST)
                update_fields['created_at'] = ist_time
            
            if 'updated_at' in user and user['updated_at'].tzinfo is None:
                utc_time = user['updated_at'].replace(tzinfo=timezone.utc)
                ist_time = utc_time.astimezone(IST)
                update_fields['updated_at'] = ist_time
            elif 'updated_at' in user and user['updated_at'].tzinfo == timezone.utc:
                ist_time = user['updated_at'].astimezone(IST)
                update_fields['updated_at'] = ist_time
            
            if update_fields:
                await db.users.update_one({'_id': user['_id']}, {'$set': update_fields})
                users_updated += 1
        
        print(f"✅ Updated {users_updated} user records")
        
        # Migrate searches collection
        print("\n📊 Migrating searches collection...")
        searches_cursor = db.searches.find({})
        searches_updated = 0
        async for search in searches_cursor:
            update_fields = {}
            
            if 'created_at' in search and search['created_at'].tzinfo is None:
                utc_time = search['created_at'].replace(tzinfo=timezone.utc)
                ist_time = utc_time.astimezone(IST)
                update_fields['created_at'] = ist_time
            elif 'created_at' in search and search['created_at'].tzinfo == timezone.utc:
                ist_time = search['created_at'].astimezone(IST)
                update_fields['created_at'] = ist_time
            
            if update_fields:
                await db.searches.update_one({'_id': search['_id']}, {'$set': update_fields})
                searches_updated += 1
        
        print(f"✅ Updated {searches_updated} search records")
        
        # Migrate activity collection
        print("\n📊 Migrating activity collection...")
        activity_cursor = db.activity.find({})
        activity_updated = 0
        async for activity in activity_cursor:
            update_fields = {}
            
            if 'created_at' in activity and activity['created_at'].tzinfo is None:
                utc_time = activity['created_at'].replace(tzinfo=timezone.utc)
                ist_time = utc_time.astimezone(IST)
                update_fields['created_at'] = ist_time
            elif 'created_at' in activity and activity['created_at'].tzinfo == timezone.utc:
                ist_time = activity['created_at'].astimezone(IST)
                update_fields['created_at'] = ist_time
            
            if update_fields:
                await db.activity.update_one({'_id': activity['_id']}, {'$set': update_fields})
                activity_updated += 1
        
        print(f"✅ Updated {activity_updated} activity records")
        
        print("\n✨ Migration completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Users: {users_updated} records")
        print(f"   - Searches: {searches_updated} records")
        print(f"   - Activity: {activity_updated} records")
        print(f"   - Total: {users_updated + searches_updated + activity_updated} records")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise
    finally:
        client.close()
        print("\n🔌 Database connection closed")

if __name__ == "__main__":
    asyncio.run(migrate_timestamps())
