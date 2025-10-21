# 🛒 SmartCart - AI-Powered Price Comparison Platform

**SmartCart** is a comprehensive full-stack web application that helps users find the best deals across multiple Indian e-commerce platforms. Built with **React + TypeScript** frontend and **Python FastAPI** backend, it provides real-time product price comparison with AI-powered recommendations, user authentication, and detailed analytics.

---

## � Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Firebase Setup](#firebase-setup)
  - [MongoDB Setup](#mongodb-setup)
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
- **Multi-Platform Results**: Get prices from Amazon, Flipkart, Croma, JioMart, Myntra, Nykaa, and 50+ Indian retailers
- **Real-Time Search**: Fast API responses using Google Shopping API via SerpAPI
- **First 12 Products**: Displays the first 12 products from API response in original order
- **Accurate Pricing**: All prices in Indian Rupees (₹) with discount information
- **Direct Retailer Links**: Quick access to search directly on major platforms

### 🤖 **AI-Powered Recommendations**
- **Smart Best Deal Detection**: Selects best product from items with rating > 3.5
- **Intelligent Scoring**: 70% price weight + 30% rating weight algorithm
- **Quality Filtering**: Ensures recommended products meet minimum quality standards
- **Transparent Recommendations**: Detailed logs showing why a product was selected

### 👤 **User Management**
- **Firebase Authentication**: Email/Password and Google OAuth sign-in
- **User Profiles**: Store and manage user information
- **Search History**: Track all searches with IST timestamps
- **Activity Tracking**: Monitor user interactions and engagement
- **Cascade Delete**: Automatic cleanup of all user data on account deletion
- **Google Re-signup Flow**: Two-step process for previously deleted Google accounts

### � **Analytics Dashboard**
- **Search Statistics**: View total searches and recent activity
- **User Activity Tracking**: Monitor clicks, searches, and interactions
- **IST Timezone**: All timestamps displayed in Indian Standard Time
- **Profile Management**: Separate account page for user details
- **Activity History**: Comprehensive view of user actions

### 🎨 **Modern User Interface**
- **Gradient Theme**: Beautiful purple-pink-blue gradient design
- **Dark/Light Mode**: Toggle between themes
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Floating particles and smooth transitions
- **Loading States**: Skeleton loaders for better UX
- **Error Handling**: User-friendly error messages

### 🔒 **Security & Privacy**
- **Firebase Admin SDK**: Secure backend authentication
- **MongoDB Atlas**: Cloud-hosted database with encryption
- **Environment Variables**: Sensitive data protection
- **CORS Protection**: Configured for authorized origins only
- **Input Validation**: Server-side validation for all inputs

---

## 🛠️ Tech Stack

### **Frontend**
- **Framework**: React 18.3.1 with TypeScript
- **Build Tool**: Vite 5.4.19
- **UI Library**: shadcn/ui components
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios
- **Authentication**: Firebase Auth SDK
- **State Management**: React Context API
- **Icons**: Lucide React

### **Backend**
- **Framework**: FastAPI (Python 3.12)
- **Server**: Uvicorn with auto-reload
- **Database**: MongoDB Atlas (Motor async driver)
- **Authentication**: Firebase Admin SDK
- **API Integration**: SerpAPI for Google Shopping
- **Validation**: Pydantic models
- **CORS**: FastAPI CORS middleware
- **Environment**: python-dotenv

### **Database & Services**
- **Primary Database**: MongoDB Atlas (Mumbai region)
- **Authentication**: Firebase Authentication
- **Product Data**: SerpAPI (Google Shopping API)
- **Deployment**: Vercel (Frontend & Backend)
- **Version Control**: Git & GitHub

---

## 🏗️ Architecture

### **System Design**
```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │────────▶│   Backend    │────────▶│   MongoDB   │
│  React+TS   │  HTTP   │   FastAPI    │  Async  │    Atlas    │
│  (Port 8082)│◀────────│  (Port 8000) │◀────────│             │
└─────────────┘         └──────────────┘         └─────────────┘
       │                       │
       │                       │
       ▼                       ▼
┌─────────────┐         ┌──────────────┐
│   Firebase  │         │   SerpAPI    │
│    Auth     │         │   (Google)   │
└─────────────┘         └──────────────┘
```

### **Backend Services**
- **google_shopping_service.py**: Product search, filtering, scoring, and best deal selection
- **recommendation_service.py**: Additional recommendation logic
- **product_filter.py**: Product quality filtering
- **firebase.py**: Authentication middleware and user verification
- **mongo.py**: Database connection and operations

### **Frontend Components**
- **SearchForm**: Product search input with validation
- **ResultsDisplay**: Product grid with retailer grouping
- **ProductCard**: Individual product display with details
- **AIRecommendation**: Best deal highlighting
- **UserProfileDropdown**: User menu and account access
- **Analytics**: User statistics and activity tracking

---

## 📦 Prerequisites

Before setting up SmartCart, ensure you have:

- **Python 3.12+** (with pip)
- **Node.js 16+** and npm
- **Git** for version control
- **MongoDB Atlas Account** (free tier available)
- **Firebase Project** (free tier available)
- **SerpAPI Account** (free tier: 100 searches/month)
- **Code Editor** (VS Code recommended)

---

## 🚀 Installation & Setup

### **1. Clone the Repository**

```bash
git clone https://github.com/Manideep3183/Price-Compare-Pro.git
cd Price-Compare-Pro
```

---

### **Backend Setup**

1. **Create Python Virtual Environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Backend `.env` File**:
   
   Create a `.env` file in the root directory with:
   
   ```env
   # SerpAPI Configuration
   SERPAPI_API_KEY=your_serpapi_key_here
   SERPAPI_KEY=your_serpapi_key_here
   
   # MongoDB Configuration
   MONGODB_URI=your_mongodb_connection_string
   MONGO_URL=your_mongodb_connection_string
   
   # Firebase Admin SDK
   FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
   
   # Application Settings
   ENVIRONMENT=development
   DEBUG=True
   ```

4. **Get SerpAPI Key**:
   - Sign up at [SerpAPI](https://serpapi.com/)
   - Get your API key from dashboard
   - Free tier: 100 searches/month
   - Add to `.env` file

---

### **Frontend Setup**

1. **Navigate to Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Node Dependencies**:
   ```bash
   npm install
   ```

3. **Create Frontend `.env` File**:
   
   Create `frontend/.env` with:
   
   ```env
   # Firebase Configuration
   VITE_FIREBASE_API_KEY=your_firebase_api_key
   VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=your_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   VITE_FIREBASE_APP_ID=your_app_id
   
   # Backend API URL
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

---

### **Firebase Setup**

1. **Create Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project"
   - Enter project name (e.g., "SmartCart")
   - Disable Google Analytics (optional)
   - Click "Create project"

2. **Enable Authentication**:
   - Go to Authentication → Sign-in method
   - Enable "Email/Password"
   - Enable "Google" sign-in provider
   - Add your domain to authorized domains

3. **Get Firebase Config**:
   - Go to Project Settings → General
   - Scroll to "Your apps" section
   - Click "Add app" → Web
   - Register app and copy the config values
   - Add to `frontend/.env`

4. **Generate Service Account Key**:
   - Go to Project Settings → Service accounts
   - Click "Generate new private key"
   - Download the JSON file
   - Rename to `firebase-service-account.json`
   - Place in root directory (it's already in `.gitignore`)

---

### **MongoDB Setup**

1. **Create MongoDB Atlas Account**:
   - Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free cluster (M0)
   - Choose region (Mumbai recommended for India)

2. **Configure Database**:
   - Database name: `SmartCart`
   - Collections will be created automatically:
     - `users` - User profiles
     - `searches` - Search history
     - `activity` - User activity tracking

3. **Get Connection String**:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database password
   - Add to `.env` as `MONGODB_URI`

4. **Configure Network Access**:
   - Go to Network Access
   - Click "Add IP Address"
   - For development: "Allow Access from Anywhere" (0.0.0.0/0)
   - For production: Add specific IPs

---

## ▶️ Running the Application

### **Start Backend Server**

```bash
# From root directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### **Start Frontend Development Server**

```bash
# From frontend directory
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:8082**

### **Using the Quick Start Script** (Optional)

Linux/macOS:
```bash
chmod +x start.sh
./start.sh
```

Windows:
```powershell
# Start backend
python -m uvicorn app.main:app --reload --port 8000

# In another terminal, start frontend
cd frontend
npm run dev
```

---

## 🚀 Deployment

### **Deploy to Vercel**

Complete deployment guides available:
- **Quick Start**: See `DEPLOYMENT_QUICK_START.md`
- **Detailed Guide**: See `VERCEL_DEPLOYMENT.md`
- **Troubleshooting**: See `VERCEL_TROUBLESHOOTING.md`

**Quick Deploy Steps**:

1. Push code to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Configure:
   - Project name: `smartcart-app` (use hyphens)
   - Framework: Vite
   - Root directory: `frontend`
   - Build command: `npm run build`
   - Output directory: `dist`

5. Add environment variables (all from above)
6. Deploy!

**After deployment**:
- Update `VITE_API_URL` with your Vercel URL
- Add Vercel domain to Firebase authorized domains
- Configure MongoDB to allow Vercel IPs

---

## 🔐 Environment Variables

### **Backend (.env)**

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `MONGODB_URI` | MongoDB connection string | Yes | `mongodb+srv://user:pass@cluster...` |
| `SERPAPI_API_KEY` | SerpAPI key for product search | Yes | `abc123...` |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Path to Firebase credentials | Yes | `./firebase-service-account.json` |
| `ENVIRONMENT` | Application environment | No | `development` / `production` |
| `DEBUG` | Enable debug mode | No | `True` / `False` |

### **Frontend (frontend/.env)**

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_BASE_URL` | Backend API URL | Yes |
| `VITE_FIREBASE_API_KEY` | Firebase API key | Yes |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase auth domain | Yes |
| `VITE_FIREBASE_PROJECT_ID` | Firebase project ID | Yes |
| `VITE_FIREBASE_STORAGE_BUCKET` | Firebase storage bucket | Yes |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging sender ID | Yes |
| `VITE_FIREBASE_APP_ID` | Firebase app ID | Yes |

---

## 📁 Project Structure

```
Price-Compare-Pro/
├── app/                          # Backend application
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── api/                      # API routes
│   │   ├── products.py           # Product search endpoints
│   │   └── activity.py           # User activity & profile endpoints
│   ├── auth/                     # Authentication
│   │   └── firebase.py           # Firebase admin & middleware
│   ├── db/                       # Database
│   │   └── mongo.py              # MongoDB connection & operations
│   └── services/                 # Business logic
│       ├── google_shopping_service.py  # Product search & scoring
│       ├── recommendation_service.py   # Recommendation logic
│       └── product_filter.py           # Product filtering
├── api/                          # Vercel serverless functions
│   └── index.py                  # Entry point for Vercel
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── main.tsx              # App entry point
│   │   ├── App.tsx               # Root component
│   │   ├── components/           # React components
│   │   │   ├── SearchForm.tsx    # Product search input
│   │   │   ├── ResultsDisplay.tsx # Search results grid
│   │   │   ├── ProductCard.tsx   # Product display card
│   │   │   ├── AIRecommendation.tsx # Best deal highlight
│   │   │   ├── UserProfileDropdown.tsx # User menu
│   │   │   └── ui/               # shadcn/ui components
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx   # Firebase auth context
│   │   ├── lib/
│   │   │   ├── api.ts            # API client
│   │   │   ├── firebase.ts       # Firebase SDK config
│   │   │   └── utils.ts          # Utility functions
│   │   ├── pages/
│   │   │   ├── Index.tsx         # Home/search page
│   │   │   ├── Login.tsx         # Login page
│   │   │   ├── SignUp.tsx        # Signup page
│   │   │   ├── Account.tsx       # User account page
│   │   │   └── Analytics.tsx     # Analytics dashboard
│   │   └── types/
│   │       └── product.ts        # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── requirements.txt              # Python dependencies
├── vercel.json                   # Vercel configuration
├── .env                          # Backend environment variables
├── .gitignore
├── README.md
├── DEPLOYMENT_QUICK_START.md     # Quick deployment guide
├── VERCEL_DEPLOYMENT.md          # Detailed deployment guide
└── VERCEL_TROUBLESHOOTING.md     # Deployment troubleshooting
```

---

## 🎯 Key Features Explained

### **Product Search Algorithm**

1. **Query Processing**: User search query sent to SerpAPI
2. **API Response**: Fetch products from Google Shopping
3. **First 12 Selection**: Take first 12 products in original order
4. **Score Calculation**: Calculate recommendation score for each product
   - 70% weight on price (lower is better)
   - 30% weight on rating (higher is better)
5. **Grouping**: Group products by retailer
6. **Best Deal Selection**: 
   - Filter products with rating > 3.5
   - Select product with highest score
   - Fall back to all products if none meet criteria

### **Best Deal Scoring Formula**

```python
price_score = 1 - ((price - min_price) / (max_price - min_price))
rating_score = rating / 5.0
final_score = (0.7 * price_score) + (0.3 * rating_score)
```

### **User Authentication Flow**

1. User signs up/logs in via Firebase
2. Frontend gets Firebase ID token
3. Token sent to backend with each request
4. Backend verifies token using Firebase Admin SDK
5. User data stored/retrieved from MongoDB
6. IST timezone applied to all timestamps

### **Search Persistence**

- Search results saved to `sessionStorage`
- Persists across navigation (Home ↔ Analytics)
- Cleared on browser close or manual logout
- Includes: products, query, timestamp, AI recommendation

---

## 📚 API Documentation

### **Search Products**

```http
POST /api/v1/search
Content-Type: application/json
Authorization: Bearer <firebase_token>

{
  "query": "laptop",
  "limit": 100
}
```

**Response**:
```json
{
  "platforms": [
    {
      "platform": "Amazon",
      "products": [
        {
          "product_name": "MacBook Air M2",
          "price": 99999.0,
          "rating": 4.8,
          "product_url": "https://amazon.in/...",
          "image_url": "https://...",
          "retailer": "Amazon",
          "final_score": 0.98,
          "recommendation": "Excellent Deal! Buy Now",
          "discount": "10% off"
        }
      ],
      "price_low": 99999.0,
      "price_avg": 105000.0,
      "price_high": 115000.0
    }
  ],
  "price_low": 99999.0,
  "price_avg": 105000.0,
  "price_high": 115000.0,
  "ai_recommendation": "🎯 **Best Deal Found**: MacBook Air M2 at ₹99,999 from Amazon (Rating: 4.8/5.0, Score: 0.98)"
}
```

### **Save Search**

```http
POST /api/v1/save-search
Content-Type: application/json
Authorization: Bearer <firebase_token>

{
  "query": "laptop",
  "results_count": 12,
  "best_deal": {
    "product_name": "MacBook Air M2",
    "price": 99999.0,
    "retailer": "Amazon"
  }
}
```

### **Get User Profile**

```http
GET /api/v1/user/profile
Authorization: Bearer <firebase_token>
```

### **Track Activity**

```http
POST /api/v1/track-activity
Content-Type: application/json
Authorization: Bearer <firebase_token>

{
  "event": "search",
  "metadata": {
    "query": "laptop",
    "results_count": 12
  }
}
```

### **Get User Searches**

```http
GET /api/v1/user/searches?limit=10
Authorization: Bearer <firebase_token>
```

### **Delete User Account**

```http
DELETE /api/v1/user/delete
Authorization: Bearer <firebase_token>
```

---

## 🐛 Troubleshooting

### **Backend Issues**

**MongoDB Connection Failed**:
```bash
# Check connection string in .env
# Ensure IP is whitelisted in MongoDB Atlas
# Test connection:
python -c "from pymongo import MongoClient; client = MongoClient('your_connection_string'); print(client.server_info())"
```

**SerpAPI Errors**:
```bash
# Verify API key in .env
# Check quota: https://serpapi.com/dashboard
# Test API key:
curl "https://serpapi.com/search?engine=google_shopping&q=laptop&api_key=your_key"
```

**Firebase Authentication Failed**:
```bash
# Ensure firebase-service-account.json exists
# Check file path in .env
# Verify Firebase project is active
```

### **Frontend Issues**

**Build Errors**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Firebase Config Errors**:
```bash
# Verify all VITE_FIREBASE_* variables in frontend/.env
# Check Firebase console for correct values
```

**CORS Errors**:
```bash
# Backend must allow frontend origin
# Check app/main.py CORS configuration
# Ensure both servers are running
```

### **Deployment Issues**

See `VERCEL_TROUBLESHOOTING.md` for complete deployment troubleshooting guide.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## 📧 Contact & Support

- **Repository**: [github.com/Manideep3183/Price-Compare-Pro](https://github.com/Manideep3183/Price-Compare-Pro)
- **Issues**: [GitHub Issues](https://github.com/Manideep3183/Price-Compare-Pro/issues)

---

## 🙏 Acknowledgments

- **SerpAPI** for Google Shopping API access
- **Firebase** for authentication services
- **MongoDB Atlas** for database hosting
- **Vercel** for deployment platform
- **shadcn/ui** for beautiful UI components
- **Tailwind CSS** for styling utilities

---

## 📝 Additional Documentation

- **Quick Deployment Guide**: `DEPLOYMENT_QUICK_START.md`
- **Vercel Deployment**: `VERCEL_DEPLOYMENT.md`
- **Troubleshooting**: `VERCEL_TROUBLESHOOTING.md`
- **User Profile Implementation**: `USER_PROFILE_IMPLEMENTATION.md`
- **Analytics Implementation**: `ANALYTICS_IMPLEMENTATION.md`
- **Cascade Delete Guide**: `CASCADE_DELETE_GUIDE.md`
- **Google Re-signup Flow**: `GOOGLE_RESIGNUP_FLOW.md`

---

**🎉 Happy Coding! Build something amazing with SmartCart!**

**Response**:
```json
{
  "locations": [
    {"value": "India", "label": "India"},
    {"value": "United States", "label": "United States"},
    {"value": "United Kingdom", "label": "United Kingdom"}
  ]
}
```

## 🎯 Key Improvements Over Previous Version

### ✅ Replaced Crawl4AI + OpenAI with Google Shopping API
- **Better Data Quality**: Direct access to Google Shopping results
- **Higher Success Rate**: No more broken scrapers or blocked requests
- **Real-time Pricing**: Always up-to-date product information
- **Multiple Sources**: Access to 50+ retailers in one API call

### ✅ Enhanced User Experience
- **Location Selection**: Choose your preferred shopping region
- **Platform Grouping**: Results organized by retailer for easy comparison
- **Smart Recommendations**: AI-powered scoring for best value products
- **Modern Interface**: Beautiful, responsive design with loading states

### ✅ Improved Performance
- **Faster Response Times**: Single API call vs multiple scraping operations
- **Reduced Complexity**: Simplified architecture without browser automation
- **Better Error Handling**: Graceful failures with meaningful error messages
- **Scalable**: Supports multiple concurrent users without browser limitations

## � Direct Retailer Search Links

After searching for a product, the application displays direct links to major Indian retailers, allowing you to search for the same product directly on their websites:

### Supported Direct Search Links:
- **🛒 Amazon India** - Direct search on Amazon.in
- **🛍️ Flipkart** - Search on Flipkart.com
- **🏪 JioMart** - Browse JioMart's product catalog
- **📱 Croma** - Electronics search on Croma.com
- **🖥️ Reliance Digital** - Digital products on RelianceDigital.in
- **📞 93mobiles** - Mobile phone comparisons
- **👕 Myntra** - Fashion and lifestyle products
- **💄 Nykaa** - Beauty and cosmetics
- **🛒 Tata CLiQ** - Multi-category marketplace

### How It Works:
1. Enter your search query (e.g., "iPhone 16")
2. View aggregated results from our API
3. Click on any retailer link below the search bar
4. Get redirected to that retailer's search results for your query
5. Compare prices across different platforms manually

This feature ensures you can always verify prices directly on retailer websites and discover additional product variants or deals.

## �🔧 Testing

Run the included test script to verify everything is working:

```bash
# With virtual environment activated
python test_api.py
```

## 🌟 Supported Indian Retailers

The platform supports 50+ Indian retailers including:
- **Major E-commerce**: Amazon India, Flipkart, Myntra, Ajio, Snapdeal
- **Electronics**: Croma, Reliance Digital, Vijay Sales, Sangeetha Mobiles
- **Brand Stores**: Apple India, Samsung India, Dell India, HP India, Asus Store
- **Mobile Specialists**: 93Mobiles, GoGizmo Mobiles, and more
- **Local Retailers**: Regional stores and authorized dealers

## 🚀 Usage Examples

### Search for Laptops
```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "gaming laptop", "limit": 8}'
```

### Search for Smartphones
```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "iPhone", "limit": 7}'
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Credits

- **Developers**: Rohan Pagadala, Manideep Reddy P, Vineeth V
- **Support**: miniprojectpricecomparepro@gmail.com
- **API Provider**: SerpAPI for Google Shopping results
- **UI Framework**: React + TypeScript + shadcn/ui
- **Backend**: FastAPI + Python

---

**Happy Shopping! 🛍️** Get the best deals across multiple platforms with AI-powered recommendations!
