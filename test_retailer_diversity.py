#!/usr/bin/env python3

import requests

def test_search_api():
    """Test the search API with various queries"""
    base_url = "http://127.0.0.1:8000"
    endpoint = f"{base_url}/api/v1/search"
    
    test_queries = [
        "laptop",
        "headphones",
        "smartphone",
        "camera"
    ]
    
    print("🧪 Testing Search API with Retailer Diversity...")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        print("-" * 40)
        
        try:
            response = requests.post(endpoint, json={
                "query": query,
                "location": "India",
                "limit": 8
            }, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check number of platforms
                platforms = data.get("platforms", [])
                total_products = sum(len(platform.get("products", [])) for platform in platforms)
                
                print(f"✅ Found {total_products} products across {len(platforms)} platforms")
                
                # Check for Amazon and Flipkart specifically
                amazon_found = any("amazon" in platform.get("platform", "").lower() for platform in platforms)
                flipkart_found = any("flipkart" in platform.get("platform", "").lower() for platform in platforms)
                
                print(f"🛒 Amazon products: {'✅' if amazon_found else '❌'}")
                print(f"🛍️ Flipkart products: {'✅' if flipkart_found else '❌'}")
                
                # List all retailers found
                retailers = [platform.get("platform") for platform in platforms]
                print(f"🏪 Retailers found: {', '.join(retailers)}")
                
                # Check price range
                price_low = data.get("price_low")
                price_high = data.get("price_high")
                if price_low and price_high:
                    print(f"💰 Price range: ₹{price_low:,.0f} - ₹{price_high:,.0f}")
                
                # Check AI recommendation
                ai_rec = data.get("ai_recommendation")
                if ai_rec:
                    print(f"🤖 AI Recommendation available: {'✅' if len(ai_rec) > 50 else '❌'}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {e}")
            
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print("- API should return products from multiple retailers")
    print("- Amazon and Flipkart should be prioritized when available")
    print("- Price should be in INR")
    print("- AI recommendations should be provided")
    print("=" * 60)

if __name__ == "__main__":
    test_search_api()
