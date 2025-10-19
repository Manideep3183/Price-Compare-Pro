#!/usr/bin/env python3
"""
Test script for the Google Shopping API implementation
"""
import requests
import json

# Test the locations endpoint
print("Testing locations endpoint...")
try:
    response = requests.get("http://localhost:8000/api/v1/locations")
    if response.status_code == 200:
        locations = response.json()
        print(f"✅ Locations endpoint working: {len(locations['locations'])} locations available")
        print(f"   Available locations: {[loc['label'] for loc in locations['locations'][:3]]}...")
    else:
        print(f"❌ Locations endpoint failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error testing locations: {e}")

print("\n" + "="*50 + "\n")

# Test the search endpoint
print("Testing search endpoint...")
test_queries = [
    {"query": "headphones", "location": "India", "limit": 7},
    {"query": "gaming laptop", "location": "India", "limit": 8},
]

for test_data in test_queries:
    print(f"Testing: {test_data['query']} in India (INR)")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/search",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            total_products = sum(len(platform['products']) for platform in data['platforms'])
            platforms = [platform['platform'] for platform in data['platforms']]
            
            print("✅ Search successful:")
            print(f"   Products found: {total_products}")
            print(f"   Platforms: {', '.join(platforms[:3])}{'...' if len(platforms) > 3 else ''}")
            print(f"   Price range: ₹{data['price_low']:.0f} - ₹{data['price_high']:.0f}")
            
            if data['ai_recommendation']:
                print("   AI recommendation available: ✅")
        else:
            print(f"❌ Search failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing search: {e}")
    
    print()

print("Test complete!")
