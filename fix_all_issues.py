#!/usr/bin/env python3
"""
Complete fix for all identified issues:
1. CORS endpoint verification (correct URL)
2. Start JSON and Route Temperature servers
3. Verify Slack notifications
"""

import requests
import json
import time
import subprocess
import sys
import os

def test_cors_endpoint():
    """Test the correct CORS endpoint"""
    print("🔍 Testing CORS Endpoint...")
    try:
        # Test the correct endpoint: /visualization
        response = requests.get('http://localhost:5000/visualization', timeout=10)
        if response.status_code == 200:
            print("✅ CORS endpoint /visualization is accessible")
            print(f"   Response length: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ CORS endpoint failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS endpoint test failed: {e}")
        return False

def start_json_server():
    """Start the JSON server for AR visualization"""
    print("\n🔍 Starting JSON Server...")
    try:
        response = requests.post('http://localhost:5000/start_json_server', timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ JSON Server start result: {result}")
            return True
        else:
            print(f"❌ Failed to start JSON server: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ JSON server start failed: {e}")
        return False

def check_json_server_status():
    """Check JSON server status"""
    print("\n🔍 Checking JSON Server Status...")
    try:
        response = requests.get('http://localhost:5000/check_json_server_status', timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ JSON Server status: {result}")
            return result.get('running', False)
        else:
            print(f"❌ JSON server status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ JSON server status check failed: {e}")
        return False

def start_route_temp_server():
    """Start the route temperature server"""
    print("\n🔍 Starting Route Temperature Server...")
    try:
        # Check if route temp server is already running
        try:
            response = requests.get('http://localhost:5001/health', timeout=2)
            if response.status_code == 200:
                print("✅ Route temperature server already running")
                return True
        except:
            pass
        
        # Start the route temp server by importing and running it
        print("   Starting route temperature server in background...")
        
        # Use the app's built-in route temperature server starter
        import threading
        import sys
        sys.path.append('.')
        
        # Import the start function
        from app_modular import start_route_temp_server
        
        # Start in a thread
        server_thread = threading.Thread(target=start_route_temp_server, daemon=True)
        server_thread.start()
        
        # Wait a moment for startup
        time.sleep(3)
        
        # Test if it's now running
        try:
            response = requests.get('http://localhost:5001/health', timeout=2)
            if response.status_code == 200:
                print("✅ Route temperature server started successfully")
                return True
            else:
                print(f"❌ Route temperature server not responding properly")
                return False
        except Exception as e:
            print(f"❌ Route temperature server failed to start: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Route temperature server start failed: {e}")
        return False

def test_slack_notification():
    """Test Slack notification"""
    print("\n🔍 Testing Slack Notification...")
    try:
        test_data = {
            "message": "🔧 Testing all systems - CORS, JSON Server, and Route Server fixes applied!",
            "container_count": 42,
            "efficiency_improvement": 18.5
        }
        
        response = requests.post(
            'http://localhost:5000/slack/notify/optimization-complete',
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Slack notification sent: {result}")
            return True
        else:
            print(f"❌ Slack notification failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Slack notification test failed: {e}")
        return False

def check_server_status():
    """Check overall server status"""
    print("\n🔍 Checking Overall Server Status...")
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Main Flask server is healthy")
            
            # Get detailed status if available
            try:
                status_response = requests.get('http://localhost:5000/api/server-config', timeout=5)
                if status_response.status_code == 200:
                    config = status_response.json()
                    print(f"   Server config: {json.dumps(config, indent=2)}")
            except:
                pass
                
            return True
        else:
            print(f"❌ Main server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server health check failed: {e}")
        return False

def main():
    """Main fix and verification function"""
    print("🚀 OptiGeniX Complete System Fix & Verification")
    print("=" * 60)
    
    results = {}
    
    # 1. Check main server health first
    results['main_server'] = check_server_status()
    
    # 2. Test CORS endpoint (with correct URL)
    results['cors_endpoint'] = test_cors_endpoint()
    
    # 3. Start and verify JSON server
    results['json_server_start'] = start_json_server()
    time.sleep(2)  # Wait for startup
    results['json_server_status'] = check_json_server_status()
    
    # 4. Start and verify route temperature server
    results['route_server'] = start_route_temp_server()
    
    # 5. Test Slack notifications
    results['slack_notifications'] = test_slack_notification()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\nOverall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        print("\nNext steps:")
        print("• Access AR visualization at: http://localhost:5000/visualization")
        print("• JSON server is running for AR content")
        print("• Route temperature calculations are active")
        print("• Slack notifications are working")
    else:
        print("⚠️  Some issues remain. Check the failed tests above.")
        
    return total_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
