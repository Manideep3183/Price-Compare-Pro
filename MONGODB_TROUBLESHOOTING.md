# MongoDB Connection Troubleshooting Guide

## Current Error
```
⚠️  MongoDB initialization error: The DNS query name does not exist: _mongodb._tcp.cluster.mongodb.net.
```

## Root Cause
The DNS server cannot resolve the MongoDB Atlas cluster hostname `smartcart.gh9rs42.mongodb.net`.

---

## Solution 1: Verify MongoDB Atlas Cluster is Running

### Step 1: Login to MongoDB Atlas
1. Go to https://cloud.mongodb.com/
2. Login with your credentials
3. Select your **SmartCart** project

### Step 2: Check Cluster Status
1. Click on **"Database"** in left sidebar
2. Verify your cluster **SmartCart** shows as **"Active"** (green status)
3. If it shows **"Paused"** or **"Resuming"**, click **"Resume"** button
4. Wait 2-3 minutes for cluster to become active

### Step 3: Get Correct Connection String
1. Click **"Connect"** button on your cluster
2. Choose **"Connect your application"**
3. Select **Driver: Python**, **Version: 3.12 or later**
4. Copy the connection string
5. Replace `<password>` with your actual password: `smartcart2025`
6. The string should look like:
   ```
   mongodb+srv://smartcart2025:smartcart2025@smartcart.gh9rs42.mongodb.net/?retryWrites=true&w=majority&appName=SmartCart
   ```

### Step 4: Update .env File
Replace the MONGO_URL in `.env` with the new connection string:
```env
MONGO_URL=mongodb+srv://smartcart2025:smartcart2025@smartcart.gh9rs42.mongodb.net/?retryWrites=true&w=majority&appName=SmartCart
```

**Note:** Remove `/smartcart` from the connection string (database name should not be in the URL path for this setup).

---

## Solution 2: Update Network Access (IP Whitelist)

### Step 1: Check Network Access
1. In MongoDB Atlas, click **"Network Access"** in left sidebar
2. Check if your current IP address is whitelisted

### Step 2: Add Your IP Address
1. Click **"Add IP Address"** button
2. Choose one of these options:

   **Option A: Add Current IP (Recommended for Development)**
   - Click **"Add Current IP Address"**
   - This automatically detects and adds your IP
   
   **Option B: Allow All IPs (For Testing Only - Not Secure for Production)**
   - Click **"Allow Access from Anywhere"**
   - Enter: `0.0.0.0/0`
   - Click **"Confirm"**

3. Click **"Confirm"** and wait 1-2 minutes for changes to propagate

---

## Solution 3: Check Firewall/VPN/Antivirus

### Windows Firewall
1. Press `Win + R`, type `wf.msc`, press Enter
2. Check if MongoDB ports are blocked
3. Add exception for Python if needed

### VPN Issues
- Some VPNs block MongoDB Atlas connections
- **Try disconnecting VPN** temporarily to test
- If it works without VPN, configure VPN to allow MongoDB Atlas

### Antivirus
- Some antivirus software blocks database connections
- Add exception for:
  - Python executable
  - MongoDB Atlas domains (`*.mongodb.net`)

---

## Solution 4: Check DNS Resolution

### Test DNS Resolution
Open PowerShell and run:
```powershell
nslookup smartcart.gh9rs42.mongodb.net
```

**Expected Output:**
```
Server:  your-dns-server
Address:  x.x.x.x

Non-authoritative answer:
Name:    smartcart.gh9rs42.mongodb.net
Addresses:  multiple IP addresses should appear
```

**If it fails:**
1. Try using Google DNS:
   - Open Network Settings → Change Adapter Options
   - Right-click your network → Properties
   - Select IPv4 → Properties
   - Use these DNS servers:
     - Preferred: `8.8.8.8` (Google DNS)
     - Alternate: `8.8.4.4` (Google DNS)

2. Flush DNS cache:
   ```powershell
   ipconfig /flushdns
   ```

---

## Solution 5: Use Standard MongoDB Connection (Fallback)

If mongodb+srv continues to fail, you can use standard connection format:

### Step 1: Get Node Addresses
1. In MongoDB Atlas, click **"Connect"** → **"Connect your application"**
2. Scroll down to see individual node addresses

### Step 2: Update Connection String
Replace in `.env`:
```env
MONGO_URL=mongodb://smartcart2025:smartcart2025@ac-xxxxxx-shard-00-00.gh9rs42.mongodb.net:27017,ac-xxxxxx-shard-00-01.gh9rs42.mongodb.net:27017,ac-xxxxxx-shard-00-02.gh9rs42.mongodb.net:27017/smartcart?ssl=true&replicaSet=atlas-xxxxx-shard-0&authSource=admin&retryWrites=true&w=majority
```

---

## Solution 6: Test with pymongo Directly

Create a test file to verify connection:

**File: `test_mongodb.py`**
```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    MONGO_URL = os.getenv("MONGO_URL")
    print(f"Testing connection to: {MONGO_URL[:50]}...")
    
    try:
        client = AsyncIOMotorClient(
            MONGO_URL,
            serverSelectionTimeoutMS=10000
        )
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        dbs = await client.list_database_names()
        print(f"Available databases: {dbs}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
```

Run test:
```powershell
python test_mongodb.py
```

---

## Quick Fix Checklist

- [ ] MongoDB Atlas cluster is **Active** (not paused)
- [ ] Connection string has correct **password** (`smartcart2025`)
- [ ] Your **IP address is whitelisted** in Network Access
- [ ] **Firewall/Antivirus** allows MongoDB connections
- [ ] **VPN is disconnected** (for testing)
- [ ] **DNS can resolve** the cluster hostname
- [ ] `.env` file has **correct MONGO_URL**
- [ ] Backend server **restarted** after changing `.env`

---

## After Fixing

1. **Stop the backend server** (Ctrl+C in terminal)
2. **Restart the backend**:
   ```powershell
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. **Look for success message**:
   ```
   ✅ MongoDB connected successfully! Database: smartcart
   ✅ Database indexes created successfully
   ```

---

## Still Having Issues?

### Option A: Use Local MongoDB (Development Only)
Install MongoDB locally and use:
```env
MONGO_URL=mongodb://localhost:27017/smartcart
```

### Option B: Disable MongoDB Temporarily
The app will work without MongoDB - only search history won't persist.
Authentication and price comparison will work fine.

### Option C: Create New Cluster
1. Create a new free cluster in MongoDB Atlas
2. Use a different region (try US East or Europe)
3. Get new connection string
4. Update `.env`

---

## Need Help?
- MongoDB Atlas Support: https://www.mongodb.com/contact
- MongoDB Community Forums: https://www.mongodb.com/community/forums/
- Check MongoDB Atlas Status: https://status.cloud.mongodb.com/

