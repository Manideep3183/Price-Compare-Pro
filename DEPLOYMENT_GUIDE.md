# 🚀 Complete Authentication System Deployment Guide

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Testing Guide](#testing-guide)
6. [Features Overview](#features-overview)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

**PriceCompare Pro** now includes a complete modern authentication system with:

### ✨ Features Implemented
- ✅ Email/Password Registration & Login
- ✅ Google Sign-In (OAuth)
- ✅ Secure Password Generation (14-character)
- ✅ Password Strength Meter
- ✅ Forgot Password Flow
- ✅ User Profile Management
- ✅ Search History Tracking
- ✅ Activity Logging
- ✅ Protected Routes
- ✅ Firebase Authentication Backend
- ✅ MongoDB User Data Storage

### 🏗️ Tech Stack
**Frontend:**
- React 18.3.1 + TypeScript
- Firebase SDK 10.x
- Axios (API client with auto token injection)
- React Router 6.x
- Shadcn UI Components
- Purple-Pink-Blue Gradient Theme

**Backend:**
- FastAPI (Python)
- Firebase Admin SDK (token verification)
- Motor (MongoDB async driver)
- MongoDB Atlas

---

## 📦 Prerequisites

### ✅ Checklist
- [x] Python 3.8+ installed
- [x] Node.js 18+ installed
- [x] Firebase project created (smartcart2025-75899)
- [x] Firebase service account JSON downloaded
- [x] MongoDB Atlas cluster created (SmartCart)
- [x] MongoDB connection string obtained
- [x] All dependencies installed

---

## 🚀 Quick Start

### Step 1: Start Backend Server

```powershell
# Navigate to project root
cd c:\python\projects\PriceComparePro-master

# Activate virtual environment (if you have one)
# .\venv\Scripts\Activate.ps1

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
MongoDB connected successfully!
Database indexes created.
```

### Step 2: Start Frontend Server

```powershell
# Open new terminal
cd c:\python\projects\PriceComparePro-master\frontend

# Start Vite dev server
npm run dev
```

**Expected Output:**
```
  VITE v5.4.19  ready in 324 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 3: Access Application

Open your browser and navigate to:
```
http://localhost:5173
```

You should be redirected to the **Login Page** (since the app requires authentication).

---

## 🔧 Detailed Setup

### Backend Configuration

#### 1. Environment Variables (.env)
Located at: `c:\python\projects\PriceComparePro-master\.env`

```env
MONGO_URL=mongodb+srv://smartcart2025:smartcart2025@smartcart.gh9rs42.mongodb.net/smartcart?retryWrites=true&w=majority&appName=SmartCart
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
```

#### 2. Firebase Service Account
File: `firebase-service-account.json` (in project root)
- Already placed in your project
- Contains Firebase Admin SDK credentials
- Used for backend token verification

#### 3. Database Collections
MongoDB automatically creates these collections:
- `searches` - User search history
- `activity` - User activity logs
- Indexes are auto-created on startup

### Frontend Configuration

#### 1. Environment Variables (frontend/.env)
Located at: `c:\python\projects\PriceComparePro-master\frontend\.env`

```env
VITE_FIREBASE_API_KEY=AIzaSyDfmqxTCXWd7z-rMbKMr5mDf4O9yaDOmvE
VITE_FIREBASE_AUTH_DOMAIN=smartcart2025-75899.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=smartcart2025-75899
VITE_FIREBASE_STORAGE_BUCKET=smartcart2025-75899.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=350653091551
VITE_FIREBASE_APP_ID=1:350653091551:web:04b7e28f3e7f16de8d24b2
VITE_API_BASE_URL=http://127.0.0.1:8000
```

#### 2. Dependencies Installed
```json
{
  "firebase": "^10.x",
  "axios": "^1.x",
  "react-icons": "^5.x"
}
```

---

## 🧪 Testing Guide

### 1. Test User Registration

1. Navigate to http://localhost:5173
2. You'll be redirected to `/login`
3. Click **"Don't have an account? Sign up"**
4. On signup page, fill in:
   - **Name:** Test User
   - **Email:** test@example.com
   - **Password:** Click "Generate Secure Password" button
   - **Confirm Password:** Copy the generated password
5. Observe the password strength meter (should show "Strong" in green)
6. Click **"Create Account"**
7. You should be redirected to the home page

### 2. Test Google Sign-In

1. On login page, click **"Continue with Google"**
2. Select your Google account
3. Grant permissions
4. You should be redirected to home page
5. Check user profile dropdown in top-right corner

### 3. Test Password Reset

1. On login page, click **"Forgot Password?"**
2. Enter your email address
3. Click **"Send Reset Link"**
4. Check your email for password reset link
5. Success message should appear

### 4. Test Protected Routes

1. Open browser in **Incognito Mode**
2. Navigate to http://localhost:5173
3. You should be immediately redirected to `/login`
4. Login with credentials
5. You should now see the main app

### 5. Test User Profile Dropdown

1. After logging in, click your avatar in top-right corner
2. Dropdown should show:
   - Your name and email
   - Profile option
   - Search History option
   - Activity Log option
   - Log out button
3. Click **"Log out"**
4. You should be redirected to `/login`

### 6. Test Search History Tracking

1. Login to the app
2. Perform a search (e.g., "iPhone 15")
3. Open MongoDB Compass or Atlas
4. Navigate to `smartcart` database → `searches` collection
5. You should see a new document with:
   ```json
   {
     "uid": "firebase_user_id",
     "email": "test@example.com",
     "query": "iPhone 15",
     "results_count": 12,
     "created_at": "2025-06-15T10:30:00Z"
   }
   ```

### 7. Test API Authentication

#### Test Protected Endpoint (Should Fail Without Token)
```powershell
curl http://localhost:8000/api/v1/searches
```
**Expected Response:** `401 Unauthorized`

#### Test Protected Endpoint (With Token)
1. Login to the app
2. Open browser DevTools → Console
3. Run:
   ```javascript
   const user = firebase.auth().currentUser;
   const token = await user.getIdToken();
   console.log(token);
   ```
4. Copy the token
5. Test with curl:
   ```powershell
   curl http://localhost:8000/api/v1/searches `
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```
**Expected Response:** JSON array of searches

---

## 🎨 Features Overview

### 1. Authentication Pages

#### Login Page (`/login`)
- **Email/Password Login**
- **Google Sign-In Button**
- **Password Visibility Toggle**
- **Forgot Password Link**
- **Sign Up Link**
- **Purple-Pink-Blue Gradient Theme**
- **Glassmorphism Effects**

#### Signup Page (`/signup`)
- **Name, Email, Password Fields**
- **Password Generator Button** (14-char secure passwords)
- **Password Strength Meter** (color-coded: red→yellow→green)
- **Password Validation Feedback**
- **Confirm Password Field**
- **Google Sign-In Option**
- **Login Link**

#### Forgot Password Page (`/forgot-password`)
- **Email Input**
- **Send Reset Link Button**
- **Success State with Checkmark**
- **"Try Again" Functionality**
- **Back to Login Link**

### 2. Main App Features

#### User Profile Dropdown
- **Avatar** (initials or Google profile picture)
- **User Name & Email Display**
- **Profile Option** (placeholder)
- **Search History** (placeholder)
- **Activity Log** (placeholder)
- **Logout Button**

#### Protected Routes
- **Automatic Redirect** to `/login` if not authenticated
- **Loading Spinner** during auth state check
- **Redirect to Home** if authenticated user tries to access `/login`, `/signup`, or `/forgot-password`

### 3. Backend API Endpoints

#### Authentication
- **Firebase Token Verification** (all protected routes)
- **Bearer Token Required** in Authorization header

#### User Activity Endpoints

**Save Search**
```http
POST /api/v1/searches
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "iPhone 15",
  "results_count": 12
}
```

**Get Search History**
```http
GET /api/v1/searches?limit=20
Authorization: Bearer <token>
```

**Log Activity**
```http
POST /api/v1/activity
Authorization: Bearer <token>
Content-Type: application/json

{
  "event": "page_view",
  "payload": {"page": "/search"}
}
```

**Get Activity History**
```http
GET /api/v1/activity?limit=50&event_type=page_view
Authorization: Bearer <token>
```

**Get User Profile**
```http
GET /api/v1/profile
Authorization: Bearer <token>
```

Response:
```json
{
  "uid": "firebase_user_id",
  "email": "test@example.com",
  "name": "Test User",
  "picture": "https://...",
  "email_verified": true,
  "total_searches": 25,
  "recent_searches": [
    {
      "id": "...",
      "query": "iPhone 15",
      "results_count": 12,
      "created_at": "2025-06-15T10:30:00Z"
    }
  ]
}
```

---

## 🛠️ Troubleshooting

### Issue 1: Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'firebase_admin'`

**Solution:**
```powershell
pip install firebase-admin motor python-dotenv
```

---

### Issue 2: Frontend Shows "Firebase Error"

**Error:** `Firebase: Error (auth/configuration-not-found)`

**Solution:**
1. Check `frontend/.env` file exists
2. Verify all `VITE_FIREBASE_*` variables are set
3. Restart Vite dev server:
   ```powershell
   cd frontend
   npm run dev
   ```

---

### Issue 3: 401 Unauthorized on API Calls

**Error:** API returns `{"detail": "Authorization header missing"}`

**Solution:**
1. Verify user is logged in
2. Check browser console for errors
3. Check `frontend/src/lib/api.ts` token injection:
   ```typescript
   apiClient.interceptors.request.use(async (config) => {
     const token = await AuthAPI.getIdToken();
     if (token) {
       config.headers.Authorization = `Bearer ${token}`;
     }
     return config;
   });
   ```

---

### Issue 4: MongoDB Connection Failed

**Error:** `MongoNetworkError: connect ECONNREFUSED`

**Solution:**
1. Check MongoDB Atlas cluster is active
2. Verify IP whitelist in MongoDB Atlas:
   - Login to MongoDB Atlas
   - Navigate to Network Access
   - Add your IP address or use `0.0.0.0/0` (for testing only)
3. Verify connection string in `.env` file
4. Test connection manually:
   ```python
   from motor.motor_asyncio import AsyncIOMotorClient
   client = AsyncIOMotorClient("your_connection_string")
   await client.admin.command('ping')
   ```

---

### Issue 5: Google Sign-In Not Working

**Error:** Google popup closes without logging in

**Solution:**
1. Verify Firebase Console settings:
   - Go to Firebase Console → Authentication → Sign-in method
   - Ensure Google provider is enabled
2. Add authorized domains:
   - Firebase Console → Authentication → Settings → Authorized domains
   - Add `localhost`
3. Check browser console for CORS errors

---

### Issue 6: Password Generator Not Working

**Error:** Password field doesn't populate

**Solution:**
1. Check `frontend/src/lib/password.ts` exists
2. Verify import in SignUp page:
   ```typescript
   import { generateSecurePassword } from '@/lib/password';
   ```
3. Check browser console for errors

---

## 📊 Database Schema

### searches Collection
```json
{
  "_id": ObjectId("..."),
  "uid": "firebase_user_id",
  "email": "test@example.com",
  "query": "iPhone 15",
  "results_count": 12,
  "created_at": ISODate("2025-06-15T10:30:00Z")
}
```

**Indexes:**
- `{ "uid": 1, "created_at": -1 }`
- `{ "created_at": -1 }`

### activity Collection
```json
{
  "_id": ObjectId("..."),
  "uid": "firebase_user_id",
  "email": "test@example.com",
  "event": "page_view",
  "payload": {
    "page": "/search",
    "timestamp": "2025-06-15T10:30:00Z"
  },
  "created_at": ISODate("2025-06-15T10:30:00Z")
}
```

**Indexes:**
- `{ "uid": 1, "created_at": -1 }`
- `{ "event": 1, "created_at": -1 }`
- `{ "created_at": -1 }`

---

## 🎉 Success Checklist

After completing setup, you should have:

- ✅ Backend server running on http://localhost:8000
- ✅ Frontend server running on http://localhost:5173
- ✅ MongoDB connected successfully
- ✅ Firebase authentication working
- ✅ User can register with email/password
- ✅ User can login with Google
- ✅ User can reset password
- ✅ Protected routes redirect to login
- ✅ User profile dropdown shows user info
- ✅ Search history is saved to MongoDB
- ✅ API calls include Bearer token automatically

---

## 📞 Support

If you encounter issues not covered in this guide, check:
1. `AUTH_SETUP_GUIDE.md` - Firebase and MongoDB setup instructions
2. Browser DevTools Console - Frontend errors
3. Backend Terminal - API errors
4. MongoDB Atlas Logs - Database connection issues

---

## 🚀 Next Steps

Consider adding:
1. **Search History Page** - Full UI for browsing past searches
2. **Activity Dashboard** - Visual analytics of user behavior
3. **Email Verification** - Require email verification on signup
4. **User Profile Editing** - Allow users to update name, photo
5. **Password Change** - In-app password change functionality
6. **Social Logins** - Add Facebook, Twitter, GitHub OAuth
7. **Two-Factor Authentication** - Enhanced security with 2FA
8. **Session Management** - Show active sessions, logout all devices

---

**Happy Coding! 🎨✨**
