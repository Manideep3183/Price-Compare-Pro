# Vercel Configuration Fix

## Issue
Build failing because Vercel is trying to build both frontend and backend together.

## Solution Options

### **Option 1: Frontend Only Deployment (Recommended)**

Deploy only the frontend to Vercel, and deploy backend separately.

**Steps:**

1. **Cancel Current Deployment**
   - Go to Vercel Dashboard → Your Project → Settings
   - Delete the project

2. **Redeploy with Correct Settings**
   - Go to https://vercel.com/new
   - Import repository: `Manideep3183/Price-Compare-Pro`
   - **IMPORTANT**: Set Root Directory to `frontend`
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

3. **Add Environment Variables** (in Vercel Dashboard):
   ```
   VITE_API_URL=https://your-backend-url.vercel.app
   VITE_FIREBASE_API_KEY=AIzaSyCjAwwlW24nb66DC8Z0C6gFJZUt_0B-BtQ
   VITE_FIREBASE_AUTH_DOMAIN=smartcart2025-75899.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=smartcart2025-75899
   VITE_FIREBASE_STORAGE_BUCKET=smartcart2025-75899.firebasestorage.app
   VITE_FIREBASE_MESSAGING_SENDER_ID=7264623509
   VITE_FIREBASE_APP_ID=1:7264623509:web:ecb7709d21039eca12349c
   ```

4. **Deploy Backend Separately** (Choose one):
   - **Railway.app**: Better for Python backends
   - **Render.com**: Free tier available
   - **Heroku**: Classic option
   - **PythonAnywhere**: Python-specific hosting

---

### **Option 2: Deploy Backend to Vercel (Separate Project)**

Deploy backend as a separate Vercel project:

1. **Create Second Vercel Project for Backend**
   - Go to https://vercel.com/new
   - Import same repository: `Manideep3183/Price-Compare-Pro`
   - Project name: `smartcart-backend`
   - **Root Directory**: Leave as `.` (root)
   - Override Build Settings: No
   
2. **Add Backend Environment Variables**:
   ```
   MONGODB_URI=mongodb+srv://smartcart2025:smartcart2025@smartcart.gh9rs42.mongodb.net/SmartCart?retryWrites=true&w=majority&appName=SmartCart
   SERPAPI_API_KEY=8583174e1f99fae5aa5dfbef52b8c70d4e3ee6fb419d0d5ae0e017d6bbfe8636
   FIREBASE_CREDENTIALS={"type":"service_account",...}
   ```

3. **Get Backend URL**
   - After deployment, note the URL (e.g., `https://smartcart-backend.vercel.app`)

4. **Update Frontend Environment Variables**
   - Go to frontend project
   - Settings → Environment Variables
   - Update `VITE_API_URL` to backend URL
   - Redeploy frontend

---

### **Option 3: Deploy Backend to Railway.app (Easiest)**

Railway is better suited for Python backends:

1. **Sign up at Railway.app**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Price-Compare-Pro`

3. **Configure Backend**
   - Root Directory: `.` (leave as root)
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Railway will auto-detect Python and use `requirements.txt`

4. **Add Environment Variables** (in Railway):
   ```
   MONGODB_URI=mongodb+srv://smartcart2025:smartcart2025@smartcart.gh9rs42.mongodb.net/SmartCart?retryWrites=true&w=majority&appName=SmartCart
   SERPAPI_API_KEY=8583174e1f99fae5aa5dfbef52b8c70d4e3ee6fb419d0d5ae0e017d6bbfe8636
   FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
   PORT=8000
   ```

5. **Deploy**
   - Railway will give you a URL like `https://smartcart-backend.railway.app`
   - Copy this URL

6. **Update Frontend on Vercel**
   - Deploy frontend only (Option 1)
   - Set `VITE_API_URL=https://smartcart-backend.railway.app`

---

## Quick Fix for Current Error

**Immediate Solution**:

1. **In Vercel Dashboard**:
   - Go to your project
   - Settings → General
   - **Root Directory**: Change to `frontend`
   - Save changes

2. **Redeploy**:
   - Go to Deployments
   - Click "..." on latest deployment
   - Click "Redeploy"

This will deploy only the frontend, and the build should succeed.

---

## Recommended Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  Vercel         │         │  Railway.app     │
│  (Frontend)     │────────▶│  (Backend)       │
│  smartcart.app  │  HTTP   │  api.smartcart   │
└─────────────────┘         └──────────────────┘
        │                           │
        │                           │
        ▼                           ▼
  ┌──────────┐              ┌─────────────┐
  │ Firebase │              │  MongoDB    │
  │   Auth   │              │   Atlas     │
  └──────────┘              └─────────────┘
```

**Why This Works Better**:
- Frontend: Static files, perfect for Vercel
- Backend: Python FastAPI, better on Railway/Render
- Separation of concerns
- Independent scaling
- Easier debugging

---

## Step-by-Step: Deploy Frontend Only (Fastest Solution)

1. **Delete Current Vercel Project** (optional but clean):
   - Settings → Advanced → Delete Project

2. **Redeploy**:
   ```
   Go to: https://vercel.com/new
   Import: Manideep3183/Price-Compare-Pro
   
   Configure:
   - Project Name: smartcart-app
   - Framework: Vite
   - Root Directory: frontend  ← CRITICAL!
   - Build Command: npm run build
   - Output Directory: dist
   - Install Command: npm install
   ```

3. **Add Environment Variables**:
   ```
   VITE_API_URL=http://localhost:8000  (temporarily, change after backend deploy)
   VITE_FIREBASE_API_KEY=AIzaSyCjAwwlW24nb66DC8Z0C6gFJZUt_0B-BtQ
   VITE_FIREBASE_AUTH_DOMAIN=smartcart2025-75899.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=smartcart2025-75899
   VITE_FIREBASE_STORAGE_BUCKET=smartcart2025-75899.firebasestorage.app
   VITE_FIREBASE_MESSAGING_SENDER_ID=7264623509
   VITE_FIREBASE_APP_ID=1:7264623509:web:ecb7709d21039eca12349c
   ```

4. **Deploy**: Click "Deploy" button

5. **Deploy Backend to Railway** (follow Option 3 above)

6. **Update Frontend API URL**:
   - After backend is deployed on Railway
   - Update `VITE_API_URL` in Vercel
   - Redeploy frontend

---

## Need Help?

If you want me to guide you through any specific option, let me know which one you prefer:
- **Option 1**: Frontend only on Vercel (fastest, needs separate backend)
- **Option 2**: Both on Vercel (2 projects)
- **Option 3**: Frontend on Vercel + Backend on Railway (recommended)

I'll provide detailed step-by-step instructions for your chosen option!
