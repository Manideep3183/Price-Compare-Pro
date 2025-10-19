# SmartKart Pro - AI-Powered Price Comparison Platform

A modern price comparison application that uses **Google Shopping API** to fetch products from multiple platforms including Amazon, Flipkart, Croma, JioMart, and many more. Get the best deals with AI-powered recommendations focused on the Indian market.

## 🚀 Key Features

- **🇮🇳 India-Focused Shopping**: Dedicated search for Indian market with accurate INR pricing
- **🛍️ Multi-Platform Results**: Get results from Amazon, Flipkart, Croma, JioMart, 93Mobiles, and 50+ Indian retailers
- **🔗 Direct Retailer Links**: Quick access to search directly on Amazon, Flipkart, Croma, JioMart, Myntra, Nykaa, and more
- **🤖 AI-Powered Recommendations**: Smart scoring system to find the best deals
- **📱 Modern UI**: Beautiful, responsive interface with dark/light themes
- **⚡ Real-time Search**: Fast API responses using Google Shopping API via SerpAPI
- **💰 Accurate Pricing**: All prices shown in Indian Rupees (INR) with discount information
- **🎯 Retailer Diversity**: Ensures products from major platforms like Amazon and Flipkart are includedPro - AI-Powered Price Comparison Platform

A modern price comparison application that uses **Google Shopping API** to fetch products from multiple platforms including Amazon, Flipkart, Croma, and many more. Get the best deals with AI-powered recommendations across different locations worldwide.

## 🚀 New Features

- **�🇳 India-Focused Shopping**: Dedicated search for Indian market with accurate INR pricing
- **🛍️ Multi-Platform Results**: Get results from Amazon, Flipkart, Croma, 93Mobiles, and 50+ Indian retailers
- **🤖 AI-Powered Recommendations**: Smart scoring system to find the best deals
- **📱 Modern UI**: Beautiful, responsive interface with dark/light themes
- **⚡ Real-time Search**: Fast API responses using Google Shopping API via SerpAPI
- **💰 Accurate Pricing**: All prices shown in Indian Rupees (INR) with discount information

## 🏗️ Architecture

### Backend (Python FastAPI)
- **Google Shopping Service**: Uses SerpAPI to fetch real-time product data
- **Smart Scoring Algorithm**: 70% price weight + 30% rating weight for recommendations
- **Multi-Platform Support**: Aggregates results by retailer for easy comparison
- **Location-Based Search**: Customizable search locations for better local results

### Frontend (React + TypeScript)
- **Modern UI Components**: Built with shadcn/ui and Tailwind CSS
- **Location Selection**: Choose your preferred shopping location
- **Responsive Design**: Works perfectly on desktop and mobile
- **Real-time Updates**: Live search with loading states and error handling

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone and navigate to the project**:
   ```bash
   cd smartkart-master
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your API key:
   ```
   SERPAPI_KEY=8583174e1f99fae5aa5dfbef52b8c70d4e3ee6fb419d0d5ae0e017d6bbfe8636
   ENVIRONMENT=development
   DEBUG=True
   ```

5. **Start the backend server**:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at: `http://localhost:8080`

## 📚 API Documentation

### Search Products
```bash
POST /api/v1/search
Content-Type: application/json

{
  "query": "laptop",
  "location": "India",
  "limit": 8
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
          "product_url": "https://...",
          "image_url": "https://...",
          "retailer": "Amazon",
          "final_score": 0.85,
          "recommendation": "Excellent Deal! Buy Now",
          "discount": null
        }
      ],
      "price_low": 99999.0,
      "price_avg": 99999.0,
      "price_high": 99999.0
    }
  ],
  "price_low": 99999.0,
  "price_avg": 99999.0,
  "price_high": 99999.0,
  "ai_recommendation": "🎯 **Best Deal Found**: MacBook Air M2..."
}
```

### Get Supported Locations
```bash
GET /api/v1/locations
```

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
