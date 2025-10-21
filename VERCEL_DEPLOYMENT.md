# SmartCart Deployment Guide - Vercel

## Overview
This guide will help you deploy the SmartCart application to Vercel. The application consists of:
- **Frontend**: React + TypeScript (Vite) - Deployed to Vercel
- **Backend**: FastAPI (Python) - Deployed to Vercel Serverless Functions

---

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be pushed to GitHub (✅ Already done)
3. **Environment Variables**: Prepare all required environment variables

---

## Part 1: Prepare Backend for Vercel

### Step 1: Create `vercel.json` in Root Directory

Create a file `vercel.json` in the root directory (`c:\python\projects\PriceComparePro-master\`):

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

### Step 2: Update `requirements.txt`

Ensure your `requirements.txt` includes all dependencies:

```txt
fastapi==0.115.4
uvicorn[standard]==0.32.0
pydantic==2.9.2
requests==2.32.3
pymongo==4.10.1
firebase-admin==6.5.0
python-dotenv==1.0.1
```

### Step 3: Create `api` Directory (Optional but Recommended)

For better organization, you can create an `api` directory:

```
mkdir api
```

Then move your FastAPI app or create a wrapper file `api/index.py`:

```python
from app.main import app

# Vercel requires the app to be named 'app' or exposed at module level
handler = app
```

---

## Part 2: Prepare Frontend for Vercel

### Step 1: Update Frontend Environment Variables

Create `frontend/.env.production`:

```env
VITE_API_URL=https://your-backend-domain.vercel.app
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

### Step 2: Update API Base URL in Frontend

Modify `frontend/src/lib/api.ts` to use environment variable:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

---

## Part 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended for First Time)

#### 1. **Import Project**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Project"
   - Select your GitHub repository: `Manideep3183/Price-Compare-Pro`

#### 2. **Configure Project**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

#### 3. **Add Environment Variables**
   Click on "Environment Variables" and add:

   **Frontend Environment Variables:**
   - `VITE_API_URL` = `https://your-app-name.vercel.app/api`
   - `VITE_FIREBASE_API_KEY` = (from Firebase Console)
   - `VITE_FIREBASE_AUTH_DOMAIN` = (from Firebase Console)
   - `VITE_FIREBASE_PROJECT_ID` = (from Firebase Console)
   - `VITE_FIREBASE_STORAGE_BUCKET` = (from Firebase Console)
   - `VITE_FIREBASE_MESSAGING_SENDER_ID` = (from Firebase Console)
   - `VITE_FIREBASE_APP_ID` = (from Firebase Console)

   **Backend Environment Variables:**
   - `MONGODB_URI` = (your MongoDB connection string)
   - `SERPAPI_API_KEY` = (your SerpAPI key)
   - `FIREBASE_CREDENTIALS` = (paste entire firebase-service-account.json content)

#### 4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (usually 2-3 minutes)
   - You'll get a URL like: `https://your-app-name.vercel.app`

---

### Option B: Deploy via Vercel CLI

#### 1. **Install Vercel CLI**

```bash
npm install -g vercel
```

#### 2. **Login to Vercel**

```bash
vercel login
```

#### 3. **Deploy Frontend**

```bash
cd frontend
vercel --prod
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? *Select your account*
- Link to existing project? **N**
- What's your project name? **smartcart-frontend**
- In which directory is your code located? **./**
- Override settings? **Y**
  - Build Command: `npm run build`
  - Output Directory: `dist`
  - Development Command: `npm run dev`

#### 4. **Deploy Backend**

```bash
cd ..
vercel --prod
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? *Select your account*
- Link to existing project? **N**
- What's your project name? **smartcart-backend**
- In which directory is your code located? **./**

---

## Part 4: Configure Backend Environment Variables

### Via Vercel Dashboard:

1. Go to your project dashboard
2. Click on "Settings" > "Environment Variables"
3. Add the following:

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/SmartCart?retryWrites=true&w=majority
SERPAPI_API_KEY=your_serpapi_key
FIREBASE_CREDENTIALS={"type":"service_account","project_id":"..."}
```

**Important**: For `FIREBASE_CREDENTIALS`, copy the entire content of `firebase-service-account.json` as a single-line JSON string.

### Via Vercel CLI:

```bash
vercel env add MONGODB_URI
vercel env add SERPAPI_API_KEY
vercel env add FIREBASE_CREDENTIALS
```

---

## Part 5: Update Frontend API URL

After deploying the backend, update the frontend's API URL:

1. Go to Frontend project settings in Vercel
2. Navigate to "Environment Variables"
3. Update `VITE_API_URL` to your backend URL: `https://your-backend.vercel.app`
4. Redeploy the frontend

---

## Part 6: Configure CORS

Update `app/main.py` to allow your Vercel frontend domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8082",
        "https://your-frontend.vercel.app",  # Add your Vercel frontend URL
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Part 7: Setup Custom Domain (Optional)

### 1. **Add Custom Domain**
   - Go to Project Settings > Domains
   - Click "Add"
   - Enter your domain (e.g., `smartcart.com`)

### 2. **Configure DNS**
   - Add the DNS records provided by Vercel to your domain registrar
   - Wait for DNS propagation (up to 48 hours)

### 3. **SSL Certificate**
   - Vercel automatically provisions SSL certificates
   - Your site will be available on HTTPS

---

## Part 8: Continuous Deployment

Vercel automatically deploys:
- **Production**: When you push to `main` branch
- **Preview**: When you create a pull request

To disable auto-deployment:
1. Go to Project Settings > Git
2. Toggle off "Auto-deploy"

---

## Troubleshooting

### Issue 1: "Module not found" Error

**Solution**: Ensure all dependencies are in `requirements.txt` and rebuild.

### Issue 2: Backend Timeout

**Solution**: Vercel serverless functions have a 10-second timeout on Hobby plan. Consider:
- Upgrading to Pro plan (60s timeout)
- Optimizing slow API calls
- Implementing caching

### Issue 3: Environment Variables Not Working

**Solution**:
- Ensure variables are added to correct environment (Production/Preview/Development)
- Redeploy after adding environment variables
- Check variable names match exactly

### Issue 4: CORS Errors

**Solution**: Update `allow_origins` in `app/main.py` to include your Vercel URL.

### Issue 5: Firebase Authentication Issues

**Solution**: 
- Add Vercel domain to Firebase authorized domains
- Go to Firebase Console > Authentication > Settings > Authorized domains
- Add `your-app.vercel.app`

---

## Performance Optimization

### 1. **Enable Edge Caching**

Add to `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=60, stale-while-revalidate"
        }
      ]
    }
  ]
}
```

### 2. **Use Vercel Analytics**

Add to `frontend/src/main.tsx`:

```typescript
import { inject } from '@vercel/analytics';

inject();
```

Install package:
```bash
npm install @vercel/analytics
```

---

## Monitoring

### 1. **Vercel Dashboard**
   - View deployment logs
   - Monitor function invocations
   - Check bandwidth usage

### 2. **MongoDB Atlas Monitoring**
   - Monitor database performance
   - Set up alerts for connection issues
   - Track query performance

### 3. **Firebase Console**
   - Monitor authentication events
   - Check for errors in Firebase logs

---

## Cost Estimation

### Vercel Hobby Plan (Free):
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Serverless function execution: 100 GB-hours
- ⚠️ 10-second function timeout
- ⚠️ No commercial use

### Vercel Pro Plan ($20/month):
- ✅ Commercial use allowed
- ✅ 1TB bandwidth/month
- ✅ 1000 GB-hours serverless execution
- ✅ 60-second function timeout
- ✅ Advanced analytics
- ✅ Password protection

---

## Next Steps After Deployment

1. ✅ Test all features on production
2. ✅ Set up monitoring and alerts
3. ✅ Configure custom domain
4. ✅ Enable analytics
5. ✅ Set up error tracking (Sentry)
6. ✅ Implement rate limiting
7. ✅ Add SEO optimization
8. ✅ Set up backup strategy

---

## Important Notes

⚠️ **Firebase Service Account**: Never commit `firebase-service-account.json` to GitHub (already in `.gitignore`)

⚠️ **API Keys**: Store all API keys in Vercel environment variables, never in code

⚠️ **MongoDB**: Ensure MongoDB Atlas allows connections from Vercel IPs (use 0.0.0.0/0 for testing, restrict in production)

⚠️ **Rate Limiting**: Implement rate limiting to prevent API abuse (SerpAPI has request limits)

---

## Support Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI on Vercel](https://vercel.com/guides/using-fastapi-with-vercel)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html#vercel)

---

## Quick Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create `vercel.json` configuration
- [ ] Set up environment variables in Vercel
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Update frontend API URL
- [ ] Configure CORS
- [ ] Add Firebase authorized domains
- [ ] Test all features
- [ ] Set up monitoring
- [ ] Configure custom domain (optional)

---

**🎉 Your SmartCart application is now live on Vercel!**

For any issues, check the deployment logs in Vercel Dashboard or contact Vercel support.
