# 🛒 PriceComparePro - Intelligent E-Commerce Price Comparison Platform

**PriceComparePro** is a modern full-stack web application that helps users discover the best deals across 50+ Indian e-commerce retailers. Built with **React + TypeScript + Vite** frontend and **Python FastAPI** backend, it provides real-time product price comparison with intelligent scoring algorithms, Firebase authentication, and comprehensive user analytics.

---

## 🌐 Live Deployment

- **Frontend Application**: [https://smartcart-app.vercel.app](https://smartcart-app.vercel.app)
- **Backend API**: [https://price-compare-pro-1.onrender.com](https://price-compare-pro-1.onrender.com)
- **API Documentation**: [https://price-compare-pro-1.onrender.com/docs](https://price-compare-pro-1.onrender.com/docs)
- **GitHub Repository**: [https://github.com/Manideep3183/Price-Compare-Pro](https://github.com/Manideep3183/Price-Compare-Pro)

---

## 📑 Table of Contents

- [Live Deployment](#-live-deployment)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Deployment](#-deployment)
- [Environment Variables](#-environment-variables)
- [Project Structure](#-project-structure)
- [Key Features Explained](#-key-features-explained)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🛍️ **Product Search & Comparison**
- **Multi-Platform Results**: Search across 50+ Indian retailers including Amazon, Flipkart, Croma, JioMart, Myntra, Nykaa, and more
- **Real-Time Data**: Fast API responses powered by Google Shopping API via SerpAPI
- **Smart Product Display**: Shows first 12 most relevant products with complete details
- **Accurate Pricing**: All prices displayed in Indian Rupees (₹) with discount information
- **Direct Retailer Links**: One-click access to search on major e-commerce platforms
- **Product Images**: High-quality product images from retailers
- **Rating & Reviews**: Display product ratings and review counts

### 🤖 **Intelligent Product Ranking**
- **Smart Best Deal Detection**: Automatically identifies the best value product
- **Dual-Factor Scoring Algorithm**: 
  - 70% weight on price (lower is better)
  - 30% weight on rating (higher is better)
- **Quality Filtering**: Only recommends products with ratings > 3.5 stars
- **Transparent Recommendations**: Detailed scoring explanation for each product
- **Price Range Analysis**: Shows minimum, average, and maximum prices across all results

### 👤 **User Management & Authentication**
- **Firebase Authentication**: Secure email/password and Google OAuth sign-in
- **User Profiles**: Complete profile management with display names and contact info
- **Search History**: Automatic tracking of all searches with IST timestamps
- **Activity Tracking**: Monitor user interactions, clicks, and engagement
- **Account Deletion**: Cascade delete removes all user data securely
- **Google Re-signup Flow**: Seamless two-step process for returning users

### 📊 **Analytics Dashboard**
- **Search Statistics**: View total searches and activity trends
- **Recent Activity**: Track searches with timestamps and result counts
- **User Activity Log**: Comprehensive monitoring of all user interactions
- **IST Timezone**: All timestamps displayed in Indian Standard Time (UTC+5:30)
- **Profile Management**: Dedicated account page for user settings
- **Activity History**: Detailed view of search patterns and behaviors

### 🎨 **Modern User Interface**
- **Beautiful Gradient Theme**: Stunning purple-pink-blue color scheme
- **Dark/Light Mode**: Toggle between themes with persistent preferences
- **Fully Responsive Design**: Perfect experience on mobile, tablet, and desktop
- **Smooth Animations**: Floating particles, smooth transitions, and micro-interactions
- **Loading States**: Elegant skeleton loaders for better perceived performance
- **Error Handling**: User-friendly error messages with actionable solutions
- **Toast Notifications**: Real-time feedback for user actions
- **Logo Selection**: Custom logo chooser for personalized experience

### 🔒 **Security & Privacy**
- **Firebase Admin SDK**: Backend authentication with token verification
- **MongoDB Atlas**: Cloud-hosted database with encryption at rest
- **Environment Variables**: Secure configuration management
- **CORS Protection**: Configured for authorized origins only
- **Input Validation**: Comprehensive server-side validation with Pydantic
- **Secure API Keys**: Protected API credentials and service accounts

---

## 🛠️ Tech Stack

### **Frontend**
- **Framework**: React 18.3.1 with TypeScript 5.6.2
- **Build Tool**: Vite 5.4.19 (Lightning-fast HMR)
- **UI Components**: shadcn/ui (Built on Radix UI primitives)
- **Styling**: Tailwind CSS 3.4.17 with custom configuration
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios 1.12.2
- **Authentication**: Firebase Auth SDK 12.4.0
- **State Management**: React Context API + Hooks
- **Icons**: Lucide React
- **Form Handling**: React Hook Form + Zod validation
- **Animations**: Framer Motion + CSS transitions
- **Date Handling**: date-fns 3.6.0

### **Backend**
- **Framework**: FastAPI 0.100.1 (Python 3.12+)
- **ASGI Server**: Uvicorn 0.22.0 with auto-reload
- **Database**: MongoDB Atlas (Motor 3.3.2 async driver)
- **Authentication**: Firebase Admin SDK 6.4.0
- **Product Data API**: SerpAPI (Google Shopping)
- **Validation**: Pydantic models
- **CORS**: FastAPI CORS middleware
- **Environment**: python-dotenv 1.0.0
- **HTTP Requests**: requests 2.31.0

### **Database & Services**
- **Primary Database**: MongoDB Atlas (Cloud-hosted, Mumbai region)
- **Authentication Provider**: Firebase Authentication
- **Product Data Source**: SerpAPI (Google Shopping API)
- **Frontend Deployment**: Vercel
- **Backend Deployment**: Render.com
- **Version Control**: Git & GitHub

---

## 🏗️ Architecture

### **System Design**

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Frontend      │────────▶│   Backend API    │────────▶│   MongoDB       │
│  React+TS+Vite  │  HTTP   │   FastAPI        │  Async  │    Atlas        │
│  (Vercel)       │◀────────│  (Render.com)    │◀────────│   (Cloud)       │
└─────────────────┘         └──────────────────┘         └─────────────────┘
       │                            │
       │                            │
       ▼                            ▼
┌─────────────────┐         ┌──────────────────┐
│   Firebase      │         │   SerpAPI        │
│  Authentication │         │ (Google Shopping)│
└─────────────────┘         └──────────────────┘
```

### **Backend Services**
- **main.py**: FastAPI application entry point with CORS configuration
- **google_shopping_service.py**: Product search, price extraction, scoring, and best deal selection
- **firebase.py**: Authentication middleware, token verification, and user management
- **mongo.py**: Database connection, operations, and query management
- **products.py**: Product search API endpoints
- **activity.py**: User activity tracking, search history, and profile management

### **Frontend Components**
- **SearchForm**: Product search input with validation and submit
- **ResultsDisplay**: Responsive product grid with retailer grouping
- **ProductCard**: Individual product display with image, price, rating, and actions
- **AIRecommendation**: Best deal highlighting with scoring explanation
- **UserProfileDropdown**: User menu, account access, and logout
- **Analytics**: Dashboard with statistics, search history, and activity tracking
- **ThemeToggle**: Dark/light mode switcher with persistent preferences
- **RetailerLinks**: Direct search links to major e-commerce platforms

### **Data Flow**
1. User enters search query in SearchForm
2. Frontend sends authenticated request to Backend API
3. Backend validates Firebase token
4. Backend calls SerpAPI for product data
5. Backend processes, scores, and ranks products
6. Backend saves search history to MongoDB
7. Backend returns structured response with best deal
8. Frontend displays results with recommendations
9. User interactions tracked and saved to database

---

## 📦 Prerequisites

Before setting up PriceComparePro, ensure you have:

- **Python 3.12+** (with pip package manager)
- **Node.js 16+** and npm (or yarn/pnpm)
- **Git** for version control
- **MongoDB Atlas Account** (Free tier available - M0)
- **Firebase Project** (Free Spark plan available)
- **SerpAPI Account** (Free tier: 100 searches/month)
- **Code Editor** (VS Code recommended)
- **Terminal/Command Prompt** access

---

## 🚀 Installation & Setup

### **1. Clone the Repository**

```bash
git clone https://github.com/Manideep3183/Price-Compare-Pro.git
cd Price-Compare-Pro
```

---

### **Backend Setup**

#### **1. Create Python Virtual Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
venv\Scripts\Activate.ps1

# On Windows CMD:
venv\Scripts\activate.bat

# On macOS/Linux:
source venv/bin/activate
```

#### **2. Install Python Dependencies**

```bash
pip install -r requirements.txt
```

#### **3. Create Backend `.env` File**

Create a `.env` file in the **root directory** with the following:

```env
# SerpAPI Configuration (Required)
SERPAPI_API_KEY=your_serpapi_key_here
SERPAPI_KEY=your_serpapi_key_here

# MongoDB Configuration (Required)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/pricecomparepro?retryWrites=true&w=majority
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/pricecomparepro?retryWrites=true&w=majority

# Firebase Admin SDK (Required)
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json

# Application Settings (Optional)
ENVIRONMENT=development
DEBUG=True
```

#### **4. Get SerpAPI Key**

1. Sign up at [https://serpapi.com/](https://serpapi.com/)
2. Navigate to Dashboard → API Key
3. Copy your API key
4. Free tier provides 100 searches/month
5. Add to `.env` file as `SERPAPI_API_KEY`

---

### **Frontend Setup**

#### **1. Navigate to Frontend Directory**

```bash
cd frontend
```

#### **2. Install Node Dependencies**

```bash
npm install
```

#### **3. Create Frontend `.env` File**

Create `frontend/.env` with the following:

```env
# Backend API URL
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_API_URL=http://127.0.0.1:8000

# Firebase Configuration (Get from Firebase Console)
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

---

### **Firebase Setup**

#### **1. Create Firebase Project**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"**
3. Enter project name (e.g., "PriceComparePro")
4. Disable Google Analytics (optional for development)
5. Click **"Create project"**

#### **2. Enable Authentication Methods**

1. Navigate to **Authentication** → **Sign-in method**
2. Enable **Email/Password** authentication
3. Enable **Google** sign-in provider
   - Add your support email
   - Configure OAuth consent screen
4. Add authorized domains:
   - `localhost`
   - `smartcart-app.vercel.app` (for production)

#### **3. Get Firebase Web App Configuration**

1. Go to **Project Settings** → **General**
2. Scroll to **"Your apps"** section
3. Click **"Add app"** → Select **Web (</> icon)**
4. Register app with a nickname
5. Copy the `firebaseConfig` object values
6. Add each value to `frontend/.env` with `VITE_` prefix

#### **4. Generate Service Account Key (For Backend)**

1. Go to **Project Settings** → **Service accounts**
2. Click **"Generate new private key"**
3. Click **"Generate key"** to download JSON file
4. Rename file to `firebase-service-account.json`
5. Place in root directory (already in `.gitignore`)
6. **NEVER commit this file to version control**

---

### **MongoDB Setup**

#### **1. Create MongoDB Atlas Account**

1. Sign up at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster:
   - Choose **FREE** tier (M0)
   - Select **Mumbai (ap-south-1)** region (or closest to you)
   - Cluster name: `PriceComparePro`

#### **2. Configure Database Access**

1. Go to **Database Access**
2. Click **"Add New Database User"**
3. Choose **Password** authentication
4. Create username and strong password
5. Set role to **Atlas Admin** (for development)
6. Click **"Add User"**

#### **3. Configure Network Access**

1. Go to **Network Access**
2. Click **"Add IP Address"**
3. For development: Click **"Allow Access from Anywhere"** (0.0.0.0/0)
4. For production: Add specific server IP addresses
5. Click **"Confirm"**

#### **4. Get Connection String**

1. Click **"Connect"** on your cluster
2. Choose **"Connect your application"**
3. Select **Driver**: Python, **Version**: 3.12 or later
4. Copy the connection string
5. Replace `<password>` with your database user password
6. Replace `<dbname>` with `pricecomparepro`
7. Add to `.env` as `MONGODB_URI`

#### **5. Database Collections**

The following collections will be created automatically:

- **users**: User profiles and authentication data
- **searches**: Search history with timestamps
- **activity**: User activity tracking and analytics

---

## ▶️ Running the Application

### **Start Backend Server**

```bash
# Make sure you're in the root directory and virtual environment is activated
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- Main API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### **Start Frontend Development Server**

Open a **new terminal window**:

```bash
# Navigate to frontend directory
cd frontend

# Start Vite dev server
npm run dev
```

**Frontend will be available at:**
- Development server: `http://localhost:5173` (Vite default)
- Or: `http://localhost:8081` (if 5173 is busy)

### **Access the Application**

1. Open browser and navigate to frontend URL
2. Sign up for a new account or login
3. Search for products (e.g., "laptop", "iPhone 16", "headphones")
4. View results, best deals, and analytics

---

## 🚀 Deployment

### **Frontend Deployment (Vercel)**

#### **Option 1: Deploy via Vercel Dashboard**

1. Push your code to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository: `Manideep3183/Price-Compare-Pro`
4. Configure project:
   - **Project Name**: `smartcart-app`
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. Add Environment Variables (from `frontend/.env`):
   - `VITE_API_URL`: `https://price-compare-pro-1.onrender.com`
   - All `VITE_FIREBASE_*` variables

6. Click **"Deploy"**

#### **Option 2: Deploy via Vercel CLI**

```bash
cd frontend
npm i -g vercel
vercel login
vercel --prod
```

#### **Post-Deployment Steps**

1. Note your Vercel deployment URL (e.g., `smartcart-app.vercel.app`)
2. Add this domain to Firebase **Authorized Domains**:
   - Firebase Console → Authentication → Settings → Authorized domains
3. Update MongoDB Network Access if needed

---

### **Backend Deployment (Render.com)**

#### **1. Create Render Account**

1. Sign up at [https://render.com](https://render.com)
2. Connect your GitHub account

#### **2. Create New Web Service**

1. Click **"New +"** → **"Web Service"**
2. Connect to repository: `Manideep3183/Price-Compare-Pro`
3. Configure service:
   - **Name**: `price-compare-pro`
   - **Region**: Singapore or closest to Mumbai
   - **Branch**: `main`
   - **Root Directory**: Leave empty (uses root)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### **3. Add Environment Variables**

In Render dashboard, add:

```
MONGODB_URI=your_mongodb_connection_string
SERPAPI_API_KEY=your_serpapi_key
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
ENVIRONMENT=production
DEBUG=False
```

#### **4. Upload Firebase Service Account**

Since Render doesn't support file uploads via dashboard:

1. Encode your `firebase-service-account.json` to base64
2. Add as environment variable: `FIREBASE_SERVICE_ACCOUNT_BASE64`
3. Update `app/auth/firebase.py` to decode from env variable (optional)

**OR** use Firebase Admin SDK with credentials from environment variables instead of JSON file.

#### **5. Deploy**

1. Click **"Create Web Service"**
2. Wait for deployment to complete
3. Note your Render URL: `https://price-compare-pro-1.onrender.com`

#### **6. Update Frontend Configuration**

1. Update `frontend/.env.production`:
   ```env
   VITE_API_URL=https://price-compare-pro-1.onrender.com
   ```
2. Redeploy frontend on Vercel

---

## 🔐 Environment Variables

### **Backend (.env)**

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `MONGODB_URI` | MongoDB Atlas connection string | ✅ Yes | `mongodb+srv://user:pass@cluster...` |
| `MONGO_URL` | Alternative MongoDB URI | No | Same as MONGODB_URI |
| `SERPAPI_API_KEY` | SerpAPI key for Google Shopping | ✅ Yes | `abc123xyz...` |
| `SERPAPI_KEY` | Alternative SerpAPI key | No | Same as SERPAPI_API_KEY |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Path to Firebase credentials JSON | ✅ Yes | `./firebase-service-account.json` |
| `ENVIRONMENT` | Application environment | No | `development` / `production` |
| `DEBUG` | Enable debug logging | No | `True` / `False` |

### **Frontend (frontend/.env)**

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `VITE_API_BASE_URL` | Backend API URL (development) | ✅ Yes | `http://127.0.0.1:8000` |
| `VITE_API_URL` | Backend API URL (production) | ✅ Yes | `https://price-compare-pro-1.onrender.com` |
| `VITE_FIREBASE_API_KEY` | Firebase API key | ✅ Yes | `AIzaSy...` |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase auth domain | ✅ Yes | `project.firebaseapp.com` |
| `VITE_FIREBASE_PROJECT_ID` | Firebase project ID | ✅ Yes | `project-id` |
| `VITE_FIREBASE_STORAGE_BUCKET` | Firebase storage bucket | ✅ Yes | `project.firebasestorage.app` |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging sender ID | ✅ Yes | `1234567890` |
| `VITE_FIREBASE_APP_ID` | Firebase app ID | ✅ Yes | `1:1234:web:abc123` |

---

## 📁 Project Structure

```
Price-Compare-Pro/
│
├── app/                                    # Backend application (FastAPI)
│   ├── __init__.py                         # Package initializer
│   ├── main.py                             # FastAPI app entry point, CORS config
│   │
│   ├── api/                                # API route handlers
│   │   ├── __init__.py
│   │   ├── products.py                     # Product search endpoints
│   │   └── activity.py                     # User activity, profile, search history
│   │
│   ├── auth/                               # Authentication & authorization
│   │   ├── __init__.py
│   │   └── firebase.py                     # Firebase Admin SDK, token verification
│   │
│   ├── db/                                 # Database layer
│   │   ├── __init__.py
│   │   └── mongo.py                        # MongoDB connection, CRUD operations
│   │
│   └── services/                           # Business logic services
│       ├── __init__.py
│       └── google_shopping_service.py      # SerpAPI integration, product scoring
│
├── api/                                    # Vercel serverless functions
│   └── index.py                            # Entry point for Vercel deployment
│
├── frontend/                               # React frontend application
│   ├── public/                             # Static assets
│   │   ├── robots.txt
│   │   └── logos/                          # Logo options
│   │
│   ├── src/                                # Source code
│   │   ├── main.tsx                        # App entry point, React root
│   │   ├── App.tsx                         # Root component, routing setup
│   │   ├── App.css                         # Global styles
│   │   ├── index.css                       # Tailwind imports, base styles
│   │   ├── vite-env.d.ts                   # Vite TypeScript declarations
│   │   │
│   │   ├── components/                     # Reusable React components
│   │   │   ├── SearchForm.tsx              # Product search input form
│   │   │   ├── ResultsDisplay.tsx          # Product grid with results
│   │   │   ├── ProductCard.tsx             # Individual product card
│   │   │   ├── ProductSkeleton.tsx         # Loading skeleton for products
│   │   │   ├── AIRecommendation.tsx        # Best deal highlighting
│   │   │   ├── UserProfileDropdown.tsx     # User menu, profile, logout
│   │   │   ├── ThemeToggle.tsx             # Dark/light mode switcher
│   │   │   ├── ThemeProvider.tsx           # Theme context provider
│   │   │   ├── RetailerLinks.tsx           # Direct retailer search links
│   │   │   ├── FeaturedCarousel.tsx        # Featured products carousel
│   │   │   ├── FloatingParticles.tsx       # Animated background particles
│   │   │   ├── LogoOptions.tsx             # Logo selection component
│   │   │   ├── ViewMoreButton.tsx          # Load more button
│   │   │   └── ui/                         # shadcn/ui components
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       ├── input.tsx
│   │   │       ├── dialog.tsx
│   │   │       ├── dropdown-menu.tsx
│   │   │       ├── avatar.tsx
│   │   │       ├── badge.tsx
│   │   │       ├── skeleton.tsx
│   │   │       ├── toast.tsx
│   │   │       ├── toaster.tsx
│   │   │       └── ... (40+ UI components)
│   │   │
│   │   ├── contexts/                       # React context providers
│   │   │   └── AuthContext.tsx             # Firebase auth state management
│   │   │
│   │   ├── hooks/                          # Custom React hooks
│   │   │   ├── use-mobile.tsx              # Mobile device detection
│   │   │   └── use-toast.ts                # Toast notification hook
│   │   │
│   │   ├── lib/                            # Utility libraries
│   │   │   ├── api.ts                      # Axios HTTP client, interceptors
│   │   │   ├── firebase.ts                 # Firebase SDK configuration
│   │   │   ├── password.ts                 # Password validation utilities
│   │   │   └── utils.ts                    # Helper functions (cn, etc.)
│   │   │
│   │   ├── pages/                          # Page components (routes)
│   │   │   ├── Index.tsx                   # Home page with search
│   │   │   ├── Login.tsx                   # Login page
│   │   │   ├── SignUp.tsx                  # Sign up page
│   │   │   ├── ForgotPassword.tsx          # Password reset page
│   │   │   ├── Account.tsx                 # User account settings
│   │   │   ├── Analytics.tsx               # Analytics dashboard
│   │   │   ├── LogoSelection.tsx           # Logo picker page
│   │   │   └── NotFound.tsx                # 404 error page
│   │   │
│   │   └── types/                          # TypeScript type definitions
│   │       └── product.ts                  # Product, Platform, Search types
│   │
│   ├── .env                                # Environment variables (gitignored)
│   ├── .env.production                     # Production environment variables
│   ├── package.json                        # NPM dependencies and scripts
│   ├── tsconfig.json                       # TypeScript configuration
│   ├── tsconfig.app.json                   # App TypeScript config
│   ├── tsconfig.node.json                  # Node TypeScript config
│   ├── vite.config.ts                      # Vite build configuration
│   ├── tailwind.config.ts                  # Tailwind CSS configuration
│   ├── postcss.config.js                   # PostCSS configuration
│   ├── components.json                     # shadcn/ui configuration
│   ├── eslint.config.js                    # ESLint configuration
│   ├── vercel.json                         # Vercel deployment config
│   └── index.html                          # HTML entry point
│
├── .env                                    # Backend environment variables (gitignored)
├── .env.example                            # Example environment variables
├── .gitignore                              # Git ignore rules
├── requirements.txt                        # Python dependencies
├── vercel.json                             # Vercel backend config
├── firebase-service-account.json           # Firebase credentials (gitignored)
└── README.md                               # This file
```

---

## 🎯 Key Features Explained

### **Product Search Algorithm**

1. **User Input**: User enters search query (e.g., "gaming laptop")
2. **API Call**: Frontend sends authenticated request to backend
3. **SerpAPI Integration**: Backend calls Google Shopping API via SerpAPI
4. **Data Extraction**: Parse product name, price, rating, image, URL, retailer
5. **Price Normalization**: Convert USD to INR (1 USD = 83 INR), clean formatting
6. **Product Scoring**: Calculate recommendation score for each product
7. **Quality Filtering**: Filter products with rating > 3.5 for best deal
8. **Best Deal Selection**: Select product with highest score
9. **Response**: Return first 12 products with best deal highlighted

### **Intelligent Scoring Formula**

```python
# Normalize price (lower is better)
price_score = 1 - ((price - min_price) / (max_price - min_price))

# Normalize rating (higher is better)
rating_score = rating / 5.0

# Weighted combination
final_score = (0.7 * price_score) + (0.3 * rating_score)
```

**Example**:
- Product A: ₹50,000, 4.5★ → Score: 0.87
- Product B: ₹45,000, 4.0★ → Score: 0.92 ✅ Best Deal
- Product C: ₹55,000, 5.0★ → Score: 0.78

### **User Authentication Flow**

1. **Sign Up/Login**: User creates account or logs in (Email/Google)
2. **Firebase Auth**: Frontend authenticates with Firebase
3. **Get ID Token**: Firebase returns JWT token
4. **Store Token**: Token stored in memory (not localStorage for security)
5. **API Requests**: Token sent in Authorization header
6. **Backend Verification**: Firebase Admin SDK verifies token
7. **User Context**: User info extracted from token
8. **MongoDB Sync**: User profile created/updated in database

### **Search History Persistence**

- **SessionStorage**: Search results saved to sessionStorage
- **Cross-Page**: Persists across Home ↔ Analytics navigation
- **Auto-Clear**: Cleared on browser close or logout
- **Data Saved**: Products, query, timestamp, AI recommendation
- **Database**: Search history also saved to MongoDB for analytics

### **Activity Tracking**

Tracks the following user events:

- **search**: Product search performed
- **click**: Product card clicked
- **view**: Page viewed
- **profile_update**: User profile updated
- **logout**: User logged out

All events stored with:
- User ID (uid)
- Event type
- Timestamp (IST)
- Metadata (query, results count, etc.)

---

## 📚 API Documentation

### **Base URL**

- **Development**: `http://localhost:8000`
- **Production**: `https://price-compare-pro-1.onrender.com`

### **Authentication**

All protected endpoints require Firebase ID token:

```
Authorization: Bearer <firebase_id_token>
```

---

### **1. Search Products**

```http
POST /api/v1/search
Content-Type: application/json
Authorization: Bearer <token>

{
  "query": "gaming laptop",
  "location": "India",
  "limit": 12
}
```

**Response** (200 OK):

```json
{
  "platforms": [
    {
      "platform": "Amazon",
      "products": [
        {
          "product_name": "ASUS ROG Strix G15",
          "price": 89999.0,
          "rating": 4.5,
          "product_url": "https://amazon.in/...",
          "image_url": "https://...",
          "retailer": "Amazon",
          "final_score": 0.92,
          "recommendation": "Excellent Deal! Buy Now",
          "discount": "₹10,000 off"
        }
      ],
      "price_low": 89999.0,
      "price_avg": 95000.0,
      "price_high": 105000.0
    }
  ],
  "price_low": 89999.0,
  "price_avg": 95000.0,
  "price_high": 105000.0,
  "ai_recommendation": "🎯 **Best Deal**: ASUS ROG Strix G15 at ₹89,999 from Amazon (Rating: 4.5★, Score: 0.92)"
}
```

---

### **2. Save Search History**

```http
POST /api/v1/save-search
Content-Type: application/json
Authorization: Bearer <token>

{
  "query": "gaming laptop",
  "results_count": 12
}
```

**Response** (200 OK):

```json
{
  "message": "Search saved successfully",
  "search_id": "507f1f77bcf86cd799439011"
}
```

---

### **3. Get User Profile**

```http
GET /api/v1/user/profile
Authorization: Bearer <token>
```

**Response** (200 OK):

```json
{
  "uid": "abc123xyz",
  "email": "user@example.com",
  "display_name": "John Doe",
  "phone_number": "+91 98765 43210",
  "auth_provider": "email",
  "created_at": "2024-11-09T10:30:00+05:30",
  "updated_at": "2024-11-09T14:20:00+05:30"
}
```

---

### **4. Update User Profile**

```http
POST /api/v1/user/profile
Content-Type: application/json
Authorization: Bearer <token>

{
  "display_name": "John Smith",
  "phone_number": "+91 98765 43210"
}
```

**Response** (200 OK):

```json
{
  "message": "Profile updated successfully",
  "profile": {
    "uid": "abc123xyz",
    "email": "user@example.com",
    "display_name": "John Smith",
    "phone_number": "+91 98765 43210",
    "updated_at": "2024-11-09T14:45:00+05:30"
  }
}
```

---

### **5. Get Search History**

```http
GET /api/v1/user/searches?limit=10
Authorization: Bearer <token>
```

**Response** (200 OK):

```json
{
  "searches": [
    {
      "id": "507f1f77bcf86cd799439011",
      "query": "gaming laptop",
      "results_count": 12,
      "created_at": "2024-11-09T14:30:00+05:30"
    }
  ],
  "total": 25
}
```

---

### **6. Track User Activity**

```http
POST /api/v1/track-activity
Content-Type: application/json
Authorization: Bearer <token>

{
  "event": "search",
  "payload": {
    "query": "gaming laptop",
    "results_count": 12
  }
}
```

**Response** (200 OK):

```json
{
  "message": "Activity tracked successfully",
  "activity_id": "507f1f77bcf86cd799439011"
}
```

---

### **7. Get User Activity**

```http
GET /api/v1/user/activity?limit=20
Authorization: Bearer <token>
```

**Response** (200 OK):

```json
{
  "activities": [
    {
      "id": "507f1f77bcf86cd799439011",
      "event": "search",
      "payload": {
        "query": "gaming laptop",
        "results_count": 12
      },
      "created_at": "2024-11-09T14:30:00+05:30"
    }
  ],
  "total": 150
}
```

---

### **8. Delete User Account**

```http
DELETE /api/v1/user/delete
Authorization: Bearer <token>
```

**Response** (200 OK):

```json
{
  "message": "User account and all associated data deleted successfully",
  "deleted": {
    "profile": true,
    "searches": 25,
    "activities": 150
  }
}
```

---

### **9. Get Supported Locations**

```http
GET /api/v1/locations
```

**Response** (200 OK):

```json
{
  "locations": [
    {"value": "India", "label": "India"}
  ]
}
```

---

## 🐛 Troubleshooting

### **Backend Issues**

#### **MongoDB Connection Failed**

```bash
# Check connection string format
# mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>

# Verify credentials in MongoDB Atlas
# Check Network Access whitelist

# Test connection:
python -c "from pymongo import MongoClient; client = MongoClient('your_uri'); print(client.server_info())"
```

#### **SerpAPI Quota Exceeded**

```bash
# Check quota at https://serpapi.com/dashboard
# Free tier: 100 searches/month

# Test API key:
curl "https://serpapi.com/search?engine=google_shopping&q=laptop&api_key=YOUR_KEY"

# Consider upgrading plan or implement caching
```

#### **Firebase Authentication Failed**

```bash
# Ensure firebase-service-account.json exists
# Check file path in .env
# Verify Firebase project is active

# Test Firebase Admin:
python -c "import firebase_admin; from firebase_admin import credentials; cred = credentials.Certificate('./firebase-service-account.json'); print('Success')"
```

#### **Module Import Errors**

```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Or use virtual environment:
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### **Frontend Issues**

#### **Build Errors**

```bash
cd frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite

# Build
npm run build
```

#### **Environment Variables Not Loading**

```bash
# Vite requires VITE_ prefix
# Must restart dev server after changing .env

# Check loading:
npm run dev
# Should see: VITE v5.4.19 ready in XX ms
```

#### **Firebase Configuration Errors**

```bash
# Verify all VITE_FIREBASE_* variables exist
# Check values in Firebase Console → Project Settings

# Test Firebase config:
console.log(import.meta.env.VITE_FIREBASE_API_KEY)
```

#### **CORS Errors**

```bash
# Backend must allow frontend origin
# Check app/main.py:

allow_origins=[
    "http://localhost:5173",
    "http://localhost:8081",
    "https://smartcart-app.vercel.app",
]

# Ensure both servers are running
# Check browser console for exact error
```

---

### **Deployment Issues**

#### **Vercel Deployment Failed**

1. Check build logs in Vercel dashboard
2. Verify `frontend/.env.production` exists
3. Ensure all environment variables are set
4. Check `vercel.json` configuration
5. Verify `vite.config.ts` build settings

#### **Render Deployment Failed**

1. Check deployment logs in Render dashboard
2. Verify `requirements.txt` is correct
3. Ensure `uvicorn` start command is correct
4. Check environment variables are set
5. Verify Python version (3.12+)

#### **Database Connection in Production**

1. Update MongoDB Network Access for Render IPs
2. Check connection string has correct credentials
3. Verify database user has correct permissions
4. Test connection from Render shell

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### **1. Fork the Repository**

Click the "Fork" button at the top right of the GitHub page.

### **2. Clone Your Fork**

```bash
git clone https://github.com/YOUR_USERNAME/Price-Compare-Pro.git
cd Price-Compare-Pro
```

### **3. Create a Feature Branch**

```bash
git checkout -b feature/amazing-feature
```

### **4. Make Your Changes**

- Follow existing code style
- Add comments for complex logic
- Update documentation if needed
- Test your changes thoroughly

### **5. Commit Your Changes**

```bash
git add .
git commit -m "Add: Amazing new feature"
```

**Commit Message Format**:
- `Add:` New feature
- `Fix:` Bug fix
- `Update:` Update existing feature
- `Refactor:` Code refactoring
- `Docs:` Documentation changes

### **6. Push to Your Fork**

```bash
git push origin feature/amazing-feature
```

### **7. Create Pull Request**

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Provide detailed description of changes
4. Wait for review

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 PriceComparePro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📧 Contact & Support

- **GitHub Repository**: [https://github.com/Manideep3183/Price-Compare-Pro](https://github.com/Manideep3183/Price-Compare-Pro)
- **Issues**: [GitHub Issues](https://github.com/Manideep3183/Price-Compare-Pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Manideep3183/Price-Compare-Pro/discussions)
- **Email**: miniprojectpricecomparepro@gmail.com

---

## 🙏 Acknowledgments

### **Developers**
- **Manideep Reddy P** - [@Manideep3183](https://github.com/Manideep3183)
- **Rohan Pagadala**
- **Vineeth V**

### **Technologies & Services**
- **[SerpAPI](https://serpapi.com/)** - Google Shopping API access
- **[Firebase](https://firebase.google.com/)** - Authentication and hosting
- **[MongoDB Atlas](https://www.mongodb.com/cloud/atlas)** - Cloud database
- **[Vercel](https://vercel.com/)** - Frontend deployment platform
- **[Render](https://render.com/)** - Backend hosting
- **[shadcn/ui](https://ui.shadcn.com/)** - Beautiful UI components
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Vite](https://vitejs.dev/)** - Next generation frontend tooling

---

## 🌟 Supported Retailers

PriceComparePro searches across **50+ Indian e-commerce retailers** including:

### **Major E-Commerce Platforms**
- Amazon India, Flipkart, Myntra, Ajio, Snapdeal, Shopclues

### **Electronics Specialists**
- Croma, Reliance Digital, Vijay Sales, Sangeetha Mobiles, Poorvika Mobiles

### **Mobile & Tech**
- 93Mobiles, GoGizmo Mobiles, Samsung India, Apple India

### **Brand Stores**
- Dell India, HP India, Asus Store, Lenovo India, Acer Store

### **Fashion & Lifestyle**
- Tata CLiQ, Nykaa, Koovs, Lifestyle, Westside

### **Grocery & Essentials**
- JioMart, BigBasket, Grofers (Blinkit), Amazon Pantry

---

## 📊 Features Comparison

| Feature | Free Version | Premium (Future) |
|---------|--------------|------------------|
| Product Search | ✅ 100/month | ✅ Unlimited |
| Price Comparison | ✅ Yes | ✅ Yes |
| Best Deal Detection | ✅ Yes | ✅ Yes |
| Search History | ✅ 30 days | ✅ Unlimited |
| Price Alerts | ❌ No | ✅ Yes |
| Price History Graph | ❌ No | ✅ Yes |
| API Access | ❌ No | ✅ Yes |
| Priority Support | ❌ No | ✅ Yes |

---

## 🎉 Future Roadmap

- [ ] **Price Alerts**: Get notified when prices drop
- [ ] **Price History**: View price trends over time
- [ ] **Wishlist**: Save favorite products
- [ ] **Price Tracking**: Track specific products
- [ ] **Comparison Table**: Side-by-side comparison
- [ ] **Browser Extension**: Quick price checks
- [ ] **Mobile App**: Native iOS/Android apps
- [ ] **API Access**: Public API for developers
- [ ] **AI Recommendations**: ML-based suggestions
- [ ] **Social Features**: Share deals with friends

---

**🎉 Happy Shopping! Find the best deals with PriceComparePro! 🛍️**

*Built with ❤️ by the PriceComparePro Team*
