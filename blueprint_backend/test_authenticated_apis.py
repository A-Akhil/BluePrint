#!/usr/bin/env python3
"""
Enhanced API testing script with authentication for Blueprint Backend
"""
import requests
import json
import sys
import os
from datetime import datetime

BASE_URL = "http://127.0.0.1:8001/api/v1"
TOKEN_FILE = "/tmp/blueprint_auth_token.txt"

def save_token(token):
    """Save auth token to temporary file"""
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)
    print(f"🔑 Token saved to {TOKEN_FILE}")

def load_token():
    """Load auth token from temporary file"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    return None

def get_auth_headers():
    """Get authorization headers with token"""
    token = load_token()
    if token:
        return {"Authorization": f"Token {token}"}
    return {}

def test_login():
    """Test login API with existing superuser"""
    print("🔐 Testing Login API...")
    
    # Test with existing superuser credentials
    login_data = {
        "username": "hariharan",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful!")
            print(f"   User: {data['user']['username']} ({data['user']['email']})")
            
            # Save token for future use
            save_token(data['token'])
            return data['token']
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_signup():
    """Test signup API with a new user"""
    print("👤 Testing Signup API...")
    
    # Create a test user
    signup_data = {
        "username": f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup/", json=signup_data)
        print(f"Signup Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Signup successful!")
            print(f"   New User: {data['user']['username']} ({data['user']['email']})")
            print(f"   Token: {data['token'][:20]}...")
            return data['token']
        else:
            print(f"❌ Signup failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Signup error: {e}")
        return None

def test_api_endpoint(endpoint, name, method='GET', params=None):
    """Test an API endpoint with authentication"""
    headers = get_auth_headers()
    
    try:
        if method == 'GET':
            response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(f"{BASE_URL}/{endpoint}", headers=headers, json=params)
        
        print(f"  {name}: Status {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict):
                    if 'results' in data:
                        print(f"    ✅ {len(data['results'])} records found")
                        if data['results']:
                            print(f"    📝 Sample: {list(data['results'][0].keys())}")
                    elif 'count' in data:
                        print(f"    ✅ Count: {data['count']}")
                    else:
                        print(f"    ✅ Keys: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"    ✅ {len(data)} items")
                    if data:
                        print(f"    📝 Sample keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Non-dict items'}")
            except:
                print(f"    ✅ Response received (non-JSON)")
        elif response.status_code == 403:
            print(f"    ❌ Authentication required")
        elif response.status_code == 404:
            print(f"    ❌ Endpoint not found")
        else:
            print(f"    ⚠️  Unexpected status")
            
    except Exception as e:
        print(f"  {name}: Error - {e}")

def main():
    print("🧪 Enhanced Blueprint Backend API Testing with Authentication")
    print("=" * 70)
    
    # Step 1: Test authentication
    token = test_login()
    
    if not token:
        print("\n❌ Cannot proceed without authentication token")
        sys.exit(1)
    
    print(f"\n✅ Authentication successful! Token: {token[:20]}...")
    
    # Optional: Test signup with new user
    print("\n" + "-" * 50)
    test_signup()
    
    # Step 2: Test authenticated endpoints
    print("\n" + "-" * 50)
    print("🧪 Testing Authenticated API Endpoints...")
    
    print("\n📋 Core Data APIs:")
    test_api_endpoint("expeditions/", "Expeditions")
    test_api_endpoint("locations/", "Sampling Locations")  
    test_api_endpoint("samples/", "Samples")
    test_api_endpoint("taxonomy/", "Taxonomic Assignments")
    
    print("\n🔍 Search & Analytics:")
    test_api_endpoint("species/search/", "Species Search", params={"q": "Copepoda"})
    test_api_endpoint("biodiversity/analytics/", "Biodiversity Analytics")
    
    print("\n🗺️  Location-based APIs:")
    test_api_endpoint("locations/nearby/", "Nearby Locations", params={"lat": 15.5, "lng": 68.75, "radius": 50})
    test_api_endpoint("locations/diversity_hotspots/", "Diversity Hotspots")
    
    print("\n📊 Visualization APIs:")
    visualization_endpoints = [
        ("visualization/diversity-heatmap/", "Diversity Heatmap"),
        ("visualization/species-distribution/", "Species Distribution"),
        ("visualization/taxonomic-composition/", "Taxonomic Composition"),
        ("visualization/environmental-correlation/", "Environmental Correlation")
    ]
    
    for endpoint, name in visualization_endpoints:
        test_api_endpoint(endpoint, name)
    
    print("\n📤 Export API:")
    test_api_endpoint("export/", "Data Export", method='POST', params={"format": "json"})
    
    # Step 3: Test logout
    print("\n" + "-" * 50)
    print("🚪 Testing Logout...")
    headers = get_auth_headers()
    try:
        response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
        print(f"Logout Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Logout successful!")
            # Remove token file
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE)
                print(f"🗑️  Token file removed")
        else:
            print(f"❌ Logout failed: {response.text}")
    except Exception as e:
        print(f"❌ Logout error: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 API testing completed!")
    print(f"🌐 Access admin at: http://127.0.0.1:8001/admin/")
    print(f"📚 API documentation at: http://127.0.0.1:8001/api/v1/")
    print(f"🔑 Login credentials: hariharan / admin123")

if __name__ == "__main__":
    main()
