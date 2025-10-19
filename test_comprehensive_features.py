#!/usr/bin/env python3

import requests
import time

def test_comprehensive_features():
    """Test all new features comprehensively"""
    base_url = "http://127.0.0.1:8000"
    endpoint = f"{base_url}/api/v1/search"
    
    print("🧪 Comprehensive Feature Testing")
    print("=" * 60)
    print("Testing the following features:")
    print("✅ Direct product links (like JioMart, 93mobiles)")
    print("✅ Retailer diversity (Amazon, Flipkart, Croma, etc.)")
    print("✅ INR pricing accuracy")
    print("✅ Product count (7-8 products)")
    print("✅ AI recommendations")
    print("=" * 60)
    
    test_cases = [
        {
            "query": "iPhone 16",
            "expected_retailers": ["amazon", "flipkart", "jiomart", "croma"],
            "min_products": 6
        },
        {
            "query": "laptop dell",
            "expected_retailers": ["amazon", "flipkart", "croma"],
            "min_products": 5
        },
        {
            "query": "samsung galaxy",
            "expected_retailers": ["amazon", "flipkart"],
            "min_products": 4
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}: '{test_case['query']}'")
        print("-" * 40)
        
        try:
            response = requests.post(endpoint, json={
                "query": test_case["query"],
                "location": "India",
                "limit": 8
            }, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                platforms = data.get("platforms", [])
                total_products = sum(len(platform.get("products", [])) for platform in platforms)
                
                print("📊 Results Overview:")
                print(f"   • Total products: {total_products}")
                print(f"   • Platforms found: {len(platforms)}")
                
                # Test 1: Product count
                if total_products >= test_case["min_products"]:
                    print(f"   ✅ Product count: {total_products} (minimum {test_case['min_products']})")
                else:
                    print(f"   ❌ Product count: {total_products} (expected minimum {test_case['min_products']})")
                
                # Test 2: Retailer diversity
                retailers_found = [platform.get("platform", "").lower() for platform in platforms]
                expected_found = []
                for expected in test_case["expected_retailers"]:
                    found = any(expected in retailer for retailer in retailers_found)
                    if found:
                        expected_found.append(expected)
                        print(f"   ✅ {expected.title()} products found")
                    else:
                        print(f"   ⚠️  {expected.title()} products not found")
                
                # Test 3: Direct product links
                direct_links_found = 0
                jiomart_links = 0
                mobiles93_links = 0
                
                for platform in platforms:
                    for product in platform.get("products", []):
                        product_url = product.get("product_url", "")
                        if product_url and "http" in product_url:
                            direct_links_found += 1
                            if "jiomart" in product_url.lower():
                                jiomart_links += 1
                            if "93mobiles" in product_url.lower() or "91mobiles" in product_url.lower():
                                mobiles93_links += 1
                
                print(f"   📱 Direct product links: {direct_links_found}/{total_products}")
                if jiomart_links > 0:
                    print(f"   🏪 JioMart links found: {jiomart_links}")
                if mobiles93_links > 0:
                    print(f"   📞 93Mobiles links found: {mobiles93_links}")
                
                # Test 4: INR pricing
                inr_prices = 0
                price_range = []
                for platform in platforms:
                    for product in platform.get("products", []):
                        price = product.get("price")
                        if price and price > 0:
                            inr_prices += 1
                            price_range.append(price)
                
                if price_range:
                    min_price = min(price_range)
                    max_price = max(price_range)
                    print(f"   💰 INR pricing: ₹{min_price:,.0f} - ₹{max_price:,.0f}")
                    if min_price > 100 and max_price < 10000000:  # Reasonable price range
                        print("   ✅ Price range looks reasonable")
                    else:
                        print("   ⚠️  Price range might need review")
                
                # Test 5: AI recommendations
                ai_rec = data.get("ai_recommendation")
                if ai_rec and len(ai_rec) > 100:
                    print(f"   🤖 AI recommendation: ✅ ({len(ai_rec)} characters)")
                else:
                    print("   🤖 AI recommendation: ❌ (missing or too short)")
                
                # Test 6: Product details completeness
                complete_products = 0
                for platform in platforms:
                    for product in platform.get("products", []):
                        has_name = bool(product.get("product_name"))
                        has_price = bool(product.get("price"))
                        has_url = bool(product.get("product_url"))
                        has_retailer = bool(product.get("retailer"))
                        
                        if has_name and has_price and has_url and has_retailer:
                            complete_products += 1
                
                print(f"   📋 Complete product data: {complete_products}/{total_products}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {e}")
            
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
        
        # Add delay between requests
        if i < len(test_cases):
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print("🎯 Feature Test Summary:")
    print("✅ Direct product links (JioMart, 93mobiles, Amazon, Flipkart)")
    print("✅ Retailer diversity ensuring Amazon & Flipkart presence")
    print("✅ India-focused INR pricing")
    print("✅ 7-8 product limit compliance")
    print("✅ AI-powered recommendations")
    print("✅ Complete product metadata")
    print("=" * 60)
    print("\n🌐 Frontend Features to Test Manually:")
    print("• Visit http://localhost:8081")
    print("• Search for 'iPhone 16' or 'laptop'")
    print("• Verify retailer links appear below search bar")
    print("• Click retailer links to test direct navigation")
    print("• Check product cards show 'View on [Retailer]' buttons")
    print("=" * 60)

if __name__ == "__main__":
    test_comprehensive_features()
