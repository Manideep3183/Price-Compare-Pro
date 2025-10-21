"""
MongoDB Connection Test Script
Run this to diagnose MongoDB connection issues
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

print("=" * 70)
print("MongoDB Connection Diagnostic Test")
print("=" * 70)
print()

# Test 1: Check if MONGO_URL is set
print("Test 1: Environment Variable Check")
print("-" * 70)
if MONGO_URL:
    # Mask password for security
    masked_url = MONGO_URL.replace(MONGO_URL.split('@')[0].split('://')[1], '***:***')
    print(f"✅ MONGO_URL is set: {masked_url}")
else:
    print("❌ MONGO_URL is not set in .env file")
    print("   Please add MONGO_URL to your .env file")
    exit(1)
print()

# Test 2: DNS Resolution
print("Test 2: DNS Resolution")
print("-" * 70)
import socket
try:
    # Extract hostname from URL
    if "mongodb+srv://" in MONGO_URL:
        hostname = MONGO_URL.split("@")[1].split("/")[0].split("?")[0]
        print(f"Testing DNS for: {hostname}")
        
        # Try to resolve DNS
        ip_addresses = socket.gethostbyname_ex(hostname)
        print(f"✅ DNS Resolution Successful!")
        print(f"   Hostname: {ip_addresses[0]}")
        print(f"   IP Addresses: {', '.join(ip_addresses[2])}")
    else:
        print("⚠️  Not using SRV connection (mongodb+srv://)")
        hostname = MONGO_URL.split("@")[1].split(":")[0] if "@" in MONGO_URL else "localhost"
        print(f"Testing DNS for: {hostname}")
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution Successful: {ip}")
        
except socket.gaierror as e:
    print(f"❌ DNS Resolution Failed: {e}")
    print()
    print("Possible Solutions:")
    print("  1. Check if MongoDB Atlas cluster is ACTIVE (not paused)")
    print("  2. Verify internet connection")
    print("  3. Try changing DNS to Google DNS (8.8.8.8)")
    print("  4. Disconnect VPN if using one")
    print("  5. Check firewall/antivirus settings")
    print()
    print("To change DNS on Windows:")
    print("  Control Panel → Network → Change Adapter Settings")
    print("  Right-click network → Properties → IPv4 → Properties")
    print("  Use: 8.8.8.8 (Preferred) and 8.8.4.4 (Alternate)")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
print()

# Test 3: MongoDB Connection
print("Test 3: MongoDB Connection")
print("-" * 70)

async def test_mongo_connection():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
        
        print("Attempting to connect to MongoDB Atlas...")
        print("(This may take up to 10 seconds)")
        print()
        
        client = AsyncIOMotorClient(
            MONGO_URL,
            serverSelectionTimeoutMS=10000,  # 10 second timeout
            connectTimeoutMS=10000
        )
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB Connection Successful!")
        print()
        
        # Get database name
        if "mongodb+srv" in MONGO_URL or "mongodb://" in MONGO_URL:
            if "/" in MONGO_URL.split("@")[-1]:
                db_name = MONGO_URL.split("@")[-1].split("/")[1].split("?")[0]
                if not db_name:
                    db_name = "smartcart"
            else:
                db_name = "smartcart"
        else:
            db_name = "smartcart"
        
        db = client[db_name]
        
        # List collections
        collections = await db.list_collection_names()
        print(f"Database: {db_name}")
        print(f"Collections: {collections if collections else '(none yet - will be created on first use)'}")
        print()
        
        # Test write operation
        print("Testing write operation...")
        test_doc = {"test": "connection", "timestamp": "2025-10-20"}
        await db.test_collection.insert_one(test_doc)
        print("✅ Write operation successful!")
        
        # Test read operation
        print("Testing read operation...")
        result = await db.test_collection.find_one({"test": "connection"})
        print(f"✅ Read operation successful! Document: {result}")
        
        # Cleanup test
        await db.test_collection.delete_one({"test": "connection"})
        print("✅ Cleanup successful!")
        print()
        
        # Close connection
        client.close()
        
        print("=" * 70)
        print("🎉 All Tests Passed! MongoDB is working correctly!")
        print("=" * 70)
        print()
        print("Your MongoDB connection is ready to use.")
        print("Restart your backend server to connect with database.")
        
    except ConnectionFailure as e:
        print(f"❌ Connection Failed: {e}")
        print()
        print("Possible Solutions:")
        print("  1. Check Network Access in MongoDB Atlas")
        print("     - Go to MongoDB Atlas → Network Access")
        print("     - Click 'Add IP Address'")
        print("     - Add your current IP or use 0.0.0.0/0 for testing")
        print()
        print("  2. Verify MongoDB Atlas cluster is ACTIVE")
        print("     - Go to MongoDB Atlas → Database")
        print("     - Check if cluster shows green 'Active' status")
        print("     - If paused, click 'Resume'")
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Server Selection Timeout: {e}")
        print()
        print("Possible Solutions:")
        print("  1. MongoDB Atlas cluster may be paused - Resume it")
        print("  2. Firewall/Antivirus blocking connection")
        print("  3. VPN interfering with connection - Try disconnecting")
        print("  4. Wrong connection string - Verify in MongoDB Atlas")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print(f"Error Type: {type(e).__name__}")

# Run async test
try:
    asyncio.run(test_mongo_connection())
except Exception as e:
    print(f"❌ Failed to run async test: {e}")
    print()
    print("Make sure motor and pymongo are installed:")
    print("  pip install motor pymongo")
