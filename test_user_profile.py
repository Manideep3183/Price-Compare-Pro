"""
Test script for user profile endpoints
Run this after signing up a test user
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# You'll need to replace this with an actual Firebase ID token after signing up
# To get the token, check the browser console after signing up
TEST_TOKEN = "YOUR_FIREBASE_ID_TOKEN_HERE"

def test_create_user_profile():
    """Test creating a user profile"""
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Test email signup user
    data = {
        "display_name": "Test User",
        "auth_provider": "email"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/users/create-or-update",
        headers=headers,
        json=data
    )
    
    print(f"Create Profile Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
def test_get_user_profile():
    """Test getting user profile from MongoDB"""
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}",
    }
    
    response = requests.get(
        f"{BASE_URL}/api/v1/users/me",
        headers=headers
    )
    
    print(f"\nGet Profile Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=" * 50)
    print("Testing User Profile Endpoints")
    print("=" * 50)
    print("\nNOTE: Update TEST_TOKEN variable with actual Firebase ID token")
    print("You can get this from browser console after signing up\n")
    
    if TEST_TOKEN == "YOUR_FIREBASE_ID_TOKEN_HERE":
        print("⚠️  Please update TEST_TOKEN in the script first!")
    else:
        test_create_user_profile()
        test_get_user_profile()
