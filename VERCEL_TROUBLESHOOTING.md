# Vercel Deployment Troubleshooting Guide

## Common Deployment Issues & Solutions

### Issue 1: "Build Failed" - Python Dependencies

**Error:** `Could not find a version that satisfies the requirement...`

**Solution:**
1. Ensure `requirements.txt` is in the root directory
2. Check for version conflicts
3. Use compatible versions:

```txt
fastapi==0.115.4
uvicorn[standard]==0.32.0
pydantic==2.9.2
requests==2.32.3
pymongo==4.10.1
firebase-admin==6.5.0
python-dotenv==1.0.1
motor==3.3.2
```

---

### Issue 2: "Module Not Found" Error

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
- Created `api/index.py` as entry point
- Updated `vercel.json` to point to `api/index.py`
- This structure works better with Vercel's Python runtime

---

### Issue 3: Environment Variables Not Working

**Error:** `MONGODB_URI not found` or similar

**Solution:**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add each variable individually (not in vercel.json)
3. Make sure to select "All" environments or "Production"
4. Redeploy after adding variables

**Required Environment Variables:**
```
MONGODB_URI
SERPAPI_API_KEY
FIREBASE_CREDENTIALS
VITE_API_URL
VITE_FIREBASE_API_KEY
VITE_FIREBASE_AUTH_DOMAIN
VITE_FIREBASE_PROJECT_ID
VITE_FIREBASE_STORAGE_BUCKET
VITE_FIREBASE_MESSAGING_SENDER_ID
VITE_FIREBASE_APP_ID
```

---

### Issue 4: "Invalid Project Name"

**Error:** `The name contains invalid characters`

**Solution:**
- Use only lowercase letters, numbers, and hyphens
- Don't use underscores
- Don't start with a number
- Valid examples: `smartcart-app`, `price-compare-pro`

---

### Issue 5: Frontend Build Fails

**Error:** Build fails in `npm run build`

**Solution:**
1. Check if you're setting the correct root directory: `frontend`
2. Ensure `package.json` has build script
3. Check for TypeScript errors:

```bash
cd frontend
npm install
npm run build
```

Fix any errors before deploying.

---

### Issue 6: CORS Errors After Deployment

**Error:** `Access to fetch blocked by CORS policy`

**Solution:**
Already fixed in `app/main.py` with:
```python
allow_origins=["https://*.vercel.app"]
```

If still having issues, add your specific domain:
```python
allow_origins=[
    "https://your-app.vercel.app",
    "https://*.vercel.app"
]
```

---

### Issue 7: MongoDB Connection Timeout

**Error:** `ServerSelectionTimeoutError`

**Solution:**
1. Go to MongoDB Atlas
2. Network Access → Add IP Address
3. Click "Allow Access from Anywhere" (0.0.0.0/0)
4. Wait 2-3 minutes for changes to propagate
5. Redeploy on Vercel

---

### Issue 8: Firebase Credentials Format Error

**Error:** `Failed to parse Firebase credentials`

**Solution:**
The `FIREBASE_CREDENTIALS` must be a single-line JSON string:

**Correct Format:**
```
{"type":"service_account","project_id":"smartcart2025-75899",...}
```

**Incorrect Format:**
```
{
  "type": "service_account",
  ...
}
```

To convert:
1. Copy your `firebase-service-account.json` content
2. Use this Python code to convert:

```python
import json
with open('firebase-service-account.json', 'r') as f:
    data = json.load(f)
print(json.dumps(data, separators=(',', ':')))
```

Or use online JSON minifier: https://www.minifier.org/

---

### Issue 9: API Routes Not Working

**Error:** `404 Not Found` for API endpoints

**Solution:**
1. Check if your API URL is correct in frontend
2. Should be: `https://your-app.vercel.app` (without `/api`)
3. Update `VITE_API_URL` environment variable in Vercel
4. Redeploy frontend

---

### Issue 10: Function Timeout

**Error:** `Function execution timeout`

**Solution:**
- Vercel Free tier: 10-second timeout
- Optimize slow API calls (SerpAPI requests)
- Consider upgrading to Pro ($20/month) for 60-second timeout
- Add caching to reduce repeated API calls

---

## Step-by-Step Deployment Checklist

### Pre-Deployment:
- [ ] All code pushed to GitHub
- [ ] `requirements.txt` is up to date
- [ ] `api/index.py` exists
- [ ] `vercel.json` is configured correctly
- [ ] Frontend builds locally: `cd frontend && npm run build`
- [ ] Backend runs locally: `python -m uvicorn app.main:app`

### During Deployment:
- [ ] Project name uses hyphens only (no underscores)
- [ ] Framework preset: Vite
- [ ] Root directory: `frontend`
- [ ] All environment variables added
- [ ] `FIREBASE_CREDENTIALS` is single-line JSON
- [ ] MongoDB allows connections from anywhere

### Post-Deployment:
- [ ] Update `VITE_API_URL` with actual Vercel URL
- [ ] Add Vercel domain to Firebase authorized domains
- [ ] Test authentication (login/signup)
- [ ] Test product search
- [ ] Check browser console for errors
- [ ] Check Vercel function logs for backend errors

---

## Alternative: Deploy Backend Separately

If Vercel deployment continues to fail, consider deploying backend elsewhere:

### Option A: Railway.app
1. Sign up at railway.app
2. Connect GitHub repo
3. Deploy from root directory
4. Add environment variables
5. Get backend URL and use in frontend

### Option B: Render.com
1. Sign up at render.com
2. New Web Service → Connect repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

### Option C: Heroku
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create smartcart-api
   heroku config:set MONGODB_URI=...
   git push heroku main
   ```

Then deploy only the frontend to Vercel.

---

## Getting Help

1. **Check Vercel Logs:**
   - Dashboard → Your Project → Deployments → Latest → View Logs
   - Look for specific error messages

2. **Check Function Logs:**
   - Dashboard → Your Project → Functions
   - View real-time function invocations

3. **Test Locally First:**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Test locally
   vercel dev
   ```

4. **Vercel Community:**
   - https://github.com/vercel/vercel/discussions
   - Discord: https://vercel.com/discord

---

## Quick Fix Commands

### Reset and Redeploy:
```bash
# Remove node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Test build
npm run build

# Commit and push
git add .
git commit -m "Fix deployment issues"
git push origin main
```

### Force Redeploy on Vercel:
1. Go to Vercel Dashboard
2. Deployments → Latest
3. Click "..." → Redeploy
4. Check "Use existing Build Cache" → Uncheck it
5. Redeploy

---

## Contact Support

If nothing works:
1. Vercel Support: support@vercel.com
2. Include deployment URL and error logs
3. Mention you're using Python FastAPI backend

---

**Remember:** Most deployment issues are due to:
1. ❌ Incorrect environment variables
2. ❌ MongoDB network access restrictions
3. ❌ Wrong project structure
4. ❌ Missing dependencies

Double-check these first! ✅
