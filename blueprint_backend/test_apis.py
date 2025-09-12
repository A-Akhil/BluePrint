#!/usr/bin/env python
"""
Test script for Blueprint Backend APIs
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def test_api_endpoints():
    print("🧪 Testing Blueprint Backend APIs...")
    print("=" * 50)
    
    # Test Expeditions endpoint
    print("\n📋 Testing Expeditions API:")
    try:
        response = requests.get(f"{BASE_URL}/expeditions/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data['results']) if 'results' in data else len(data)} expeditions")
            if data.get('results'):
                print(f"First expedition: {data['results'][0]['name']}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Sampling Locations endpoint
    print("\n🗺️  Testing Sampling Locations API:")
    try:
        response = requests.get(f"{BASE_URL}/sampling-locations/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data['results']) if 'results' in data else len(data)} sampling locations")
            if data.get('results'):
                location = data['results'][0]
                print(f"First location: {location['name']} at ({location['latitude']}, {location['longitude']})")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Samples endpoint
    print("\n🧪 Testing Samples API:")
    try:
        response = requests.get(f"{BASE_URL}/samples/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data['results']) if 'results' in data else len(data)} samples")
            if data.get('results'):
                sample = data['results'][0]
                print(f"First sample: {sample['sample_id']} ({sample['sample_type']})")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Taxonomic Assignments endpoint
    print("\n🧬 Testing Taxonomic Assignments API:")
    try:
        response = requests.get(f"{BASE_URL}/taxonomic-assignments/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data['results']) if 'results' in data else len(data)} taxonomic assignments")
            if data.get('results'):
                taxa = data['results'][0]
                print(f"First assignment: {taxa['kingdom']} > {taxa['phylum']} > {taxa['class_name']}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Species Search endpoint
    print("\n🔍 Testing Species Search API:")
    try:
        response = requests.get(f"{BASE_URL}/species/search/?q=Copepoda")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Search results for 'Copepoda': {len(data) if isinstance(data, list) else 'N/A'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Biodiversity Analytics endpoint
    print("\n📊 Testing Biodiversity Analytics API:")
    try:
        response = requests.get(f"{BASE_URL}/biodiversity/analytics/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Analytics data keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Visualization endpoints
    print("\n📈 Testing Visualization APIs:")
    viz_endpoints = [
        "diversity-heatmap",
        "species-distribution",
        "taxonomic-composition",
        "environmental-correlation"
    ]
    
    for endpoint in viz_endpoints:
        try:
            response = requests.get(f"{BASE_URL}/visualization/{endpoint}/")
            print(f"  {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"  {endpoint}: Error - {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("🌐 Access admin at: http://127.0.0.1:8001/admin/")
    print("📚 API documentation at: http://127.0.0.1:8001/api/v1/")
    print("🔑 Login credentials: hariharan / admin123")

if __name__ == "__main__":
    test_api_endpoints()
