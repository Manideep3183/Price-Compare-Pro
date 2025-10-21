# Vercel Deployment Quick Start Guide

## 🚀 Quick Deployment Steps

### 1. Prerequisites Checklist
- [x] Code pushed to GitHub (Repository: `Manideep3183/Price-Compare-Pro`)
- [x] `vercel.json` created in root directory
- [x] `.env.production` created with Firebase config
- [x] CORS updated to allow Vercel domains
- [x] API client updated to support production URL

### 2. Get Your Credentials Ready

Before deploying, gather these:

**MongoDB Connection String:**
- Go to MongoDB Atlas → Database → Connect
- Copy your connection string (e.g., `mongodb+srv://username:password@cluster...`)

**SerpAPI Key:**
- Your SerpAPI key from the backend `.env` or SerpAPI dashboard

**Firebase Service Account JSON:**
- Open `firebase-service-account.json` (local file only, not in git)
- Copy the entire JSON content

### 3. Deploy to Vercel (Dashboard Method)

#### Step 1: Go to Vercel
Visit: https://vercel.com/new

#### Step 2: Import Repository
- Click "Import Git Repository"
- Select: `Manideep3183/Price-Compare-Pro`
- Click "Import"

#### Step 3: Configure Project Settings
```
Project Name: smartcart-app (or your preferred name)
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

#### Step 4: Add Environment Variables

Click "Environment Variables" and add these **one by one**:

**For All Environments (Production, Preview, Development):**

```
VITE_API_URL = https://smartcart-app.vercel.app
VITE_FIREBASE_API_KEY = AIzaSyCjAwwlW24nb66DC8Z0C6gFJZUt_0B-BtQ
VITE_FIREBASE_AUTH_DOMAIN = smartcart2025-75899.firebaseapp.com
VITE_FIREBASE_PROJECT_ID = smartcart2025-75899
VITE_FIREBASE_STORAGE_BUCKET = smartcart2025-75899.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID = 7264623509
VITE_FIREBASE_APP_ID = 1:7264623509:web:ecb7709d21039eca12349c
MONGODB_URI = [Your MongoDB connection string]
SERPAPI_API_KEY = [Your SerpAPI key]
FIREBASE_CREDENTIALS = [Paste entire firebase-service-account.json content as single line]
```

**Note:** For `FIREBASE_CREDENTIALS`, copy the entire JSON from `firebase-service-account.json` and paste it as a single-line string.

#### Step 5: Deploy
- Click "Deploy"
- Wait 2-3 minutes for deployment
- You'll get a URL like: `https://smartcart-app.vercel.app`

### 4. After First Deployment

#### Update Frontend API URL:
1. Note your Vercel URL (e.g., `https://smartcart-app.vercel.app`)
2. Go to Project Settings → Environment Variables
3. Update `VITE_API_URL` to: `https://your-actual-url.vercel.app`
4. Click "Redeploy" from the Deployments tab

#### Add Domain to Firebase:
1. Go to Firebase Console
2. Navigate to: Authentication → Settings → Authorized domains
3. Click "Add domain"
4. Add: `your-app.vercel.app`
5. Save

### 5. Test Your Deployment

Visit your Vercel URL and test:
- ✅ Homepage loads
- ✅ Firebase authentication works (Login/Signup)
- ✅ Product search returns results
- ✅ Analytics dashboard shows data
- ✅ User profile updates save

### 6. Monitor Your Deployment

**Check Logs:**
- Vercel Dashboard → Your Project → Deployments → Latest → View Logs
- Look for any errors or warnings

**Check Function Logs:**
- Vercel Dashboard → Your Project → Functions
- Monitor serverless function invocations

### 7. Troubleshooting Common Issues

**Issue: "Failed to fetch" or CORS errors**
- Solution: Ensure your Vercel URL is in the CORS `allow_origins` in `app/main.py`
- Redeploy after updating

**Issue: Firebase authentication not working**
- Solution: Add Vercel domain to Firebase authorized domains
- Check if Firebase credentials environment variable is set correctly

**Issue: MongoDB connection timeout**
- Solution: In MongoDB Atlas, go to Network Access
- Add IP: `0.0.0.0/0` (allow from anywhere) for testing
- Later, add specific Vercel IPs for production

**Issue: Environment variables not working**
- Solution: Ensure variables are added to all environments
- Redeploy after adding variables
- Check variable names match exactly (case-sensitive)

**Issue: Build fails**
- Solution: Check the build logs in Vercel
- Ensure all dependencies are in `package.json` and `requirements.txt`
- Try building locally first: `cd frontend && npm run build`

### 8. Optional: Custom Domain

If you have a custom domain:

1. Go to Project Settings → Domains
2. Click "Add"
3. Enter your domain (e.g., `smartcart.com`)
4. Follow DNS configuration instructions
5. Wait for SSL certificate provisioning (automatic)

### 9. Enable Continuous Deployment

Vercel automatically deploys on:
- **Push to `main`** → Production deployment
- **Pull Requests** → Preview deployments

To customize:
- Go to Project Settings → Git
- Configure deployment branches
- Set up deployment protection (optional)

---

## 📝 Post-Deployment Checklist

- [ ] Deployment successful
- [ ] Frontend loads without errors
- [ ] Backend API responds correctly
- [ ] Firebase authentication works
- [ ] Product search returns results
- [ ] MongoDB connection working
- [ ] Environment variables configured
- [ ] Firebase authorized domains updated
- [ ] CORS configured correctly
- [ ] Custom domain configured (if applicable)
- [ ] Analytics tracking enabled
- [ ] Error monitoring set up

---

## 🎯 Next Steps

1. **Set up monitoring**: Add Vercel Analytics or Sentry
2. **Optimize performance**: Enable edge caching, optimize images
3. **Security**: Implement rate limiting, add input validation
4. **SEO**: Add meta tags, sitemap, robots.txt
5. **Backup**: Set up MongoDB backup strategy

---

## 📞 Support

If you encounter issues:
- Check Vercel deployment logs
- Review MongoDB Atlas logs
- Check Firebase Console for auth errors
- Refer to: VERCEL_DEPLOYMENT.md for detailed troubleshooting

**Vercel Support:** https://vercel.com/support
**Documentation:** https://vercel.com/docs

---

**🎉 Congratulations! Your SmartCart app is now live on Vercel!**
