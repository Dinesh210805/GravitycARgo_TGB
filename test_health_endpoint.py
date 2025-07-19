#!/usr/bin/env python3
"""
Test script to verify the route server health endpoint
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test the route server directly
from routing.Server import app
import json

def test_health_endpoint():
    """Test the health endpoint directly"""
    print("🔧 Testing Route Server Health Endpoint")
    print("=" * 50)
    
    with app.test_client() as client:
        try:
            response = client.get('/health')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Health endpoint responds: {response.status_code}")
                print(f"✅ Response data: {json.dumps(data, indent=2)}")
                
                # Check required fields
                required_fields = ['status', 'service', 'timestamp', 'port']
                all_present = all(field in data for field in required_fields)
                
                if all_present and data['status'] == 'healthy':
                    print("✅ All required fields present and status is healthy")
                    return True
                else:
                    print("❌ Missing required fields or status not healthy")
                    return False
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Health endpoint test error: {e}")
            return False

if __name__ == "__main__":
    success = test_health_endpoint()
    print("\n" + "=" * 50)
    if success:
        print("🎉 Route server health endpoint is working correctly!")
        print("✅ The missing health endpoint has been successfully added")
        print("✅ System verification should now show 6/6 tests passing")
    else:
        print("❌ Route server health endpoint test failed")
    
    print("\nTo run full system verification:")
    print("1. Start the main server: python app_modular.py")
    print("2. Run verification: python final_verification.py")
