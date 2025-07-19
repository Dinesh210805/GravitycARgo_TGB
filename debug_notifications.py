#!/usr/bin/env python3
"""
Test Slack notification functionality
"""

import os
import sys
import requests
import time
import json
from datetime import datetime

# Load environment variables if .env file exists
if os.path.exists('.env'):
    print("📁 Loading .env file...")
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
                print(f"   {key} = {'*' * (len(value) - 4)}{value[-4:] if len(value) > 4 else value}")

def test_webhook_directly():
    """Test Slack webhook directly"""
    print("\n🧪 Testing Slack Webhook Directly...")
    print("=" * 50)
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL not set")
        return False
    
    test_message = f"""🔧 *Direct Webhook Test*

📊 *Test Results:*
• Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Source: debug_notifications.py
• Status: Testing webhook connectivity

🎯 *This is a test notification to verify Slack integration is working!*"""
    
    payload = {"text": test_message}
    
    try:
        print(f"📤 Sending to: {webhook_url[:50]}...")
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        print(f"📨 Response Status: {response.status_code}")
        print(f"📝 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
            return True
        else:
            print(f"❌ Webhook failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return False

def test_flask_notification_endpoint():
    """Test the Flask notification endpoint"""
    print("\n🌐 Testing Flask Notification Endpoint...")
    print("=" * 50)
    
    # Try different ports
    ports = [5000, 8080, 10000]
    
    for port in ports:
        try:
            # First check if server is running
            response = requests.get(f"http://localhost:{port}/", timeout=3)
            print(f"✅ Flask server found on port {port}")
            
            # Test the notification endpoint
            test_data = {
                "volume_utilization": 87.5,
                "items_packed": 28,
                "total_items": 32,
                "cost_savings": 7500,
                "user_name": "Debug Test User"
            }
            
            notify_url = f"http://localhost:{port}/slack/notify/optimization-complete"
            print(f"📤 Testing: {notify_url}")
            
            notify_response = requests.post(notify_url, json=test_data, timeout=10)
            
            print(f"📨 Status: {notify_response.status_code}")
            print(f"📝 Response: {notify_response.text}")
            
            if notify_response.status_code == 200:
                result = notify_response.json()
                print(f"✅ Notification endpoint test: {result}")
                return True
            else:
                print(f"❌ Notification endpoint failed: {notify_response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ No server on port {port}")
            continue
        except Exception as e:
            print(f"❌ Error testing port {port}: {e}")
            continue
    
    print("❌ Flask server not found on any common port")
    return False

def test_bot_api():
    """Test Slack Bot API"""
    print("\n🤖 Testing Slack Bot API...")
    print("=" * 50)
    
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN not set")
        return False
    
    headers = {
        "Authorization": f"Bearer {bot_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test auth
        response = requests.get("https://slack.com/api/auth.test", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                print(f"✅ Bot authenticated - Team: {data.get('team')}, User: {data.get('user')}")
                
                # Test sending a message to a channel
                message_payload = {
                    "channel": "#general",  # or use channel ID
                    "text": f"🧪 Bot API Test - {datetime.now().strftime('%H:%M:%S')}"
                }
                
                msg_response = requests.post("https://slack.com/api/chat.postMessage", 
                                           json=message_payload, headers=headers, timeout=10)
                
                if msg_response.status_code == 200:
                    msg_data = msg_response.json()
                    if msg_data.get("ok"):
                        print("✅ Bot message sent successfully")
                        return True
                    else:
                        print(f"❌ Bot message failed: {msg_data.get('error')}")
                        return False
                else:
                    print(f"❌ Bot message request failed: {msg_response.status_code}")
                    return False
            else:
                print(f"❌ Bot auth failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Bot API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Bot API error: {e}")
        return False

def main():
    """Main test function"""
    print("🔔 OptiGenix Slack Notification Tester")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test webhook
    webhook_success = test_webhook_directly()
    
    # Test Flask endpoint
    flask_success = test_flask_notification_endpoint()
    
    # Test bot API
    bot_success = test_bot_api()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    
    if webhook_success:
        print("✅ Slack webhook working")
    else:
        print("❌ Slack webhook not working")
        
    if flask_success:
        print("✅ Flask notification endpoint working")
    else:
        print("❌ Flask notification endpoint not working")
        
    if bot_success:
        print("✅ Slack bot API working")
    else:
        print("❌ Slack bot API not working")
    
    # Recommendations
    print("\n💡 Next Steps")
    print("=" * 50)
    
    if webhook_success and flask_success:
        print("🎉 Both webhook and Flask endpoint working!")
        print("   → Notifications should work during optimization")
        print("   → Test by running an actual container optimization")
    elif webhook_success and not flask_success:
        print("🔧 Webhook works but Flask endpoint doesn't")
        print("   → Start Flask server: python app_modular.py")
        print("   → Check if server is running on correct port")
    elif not webhook_success and flask_success:
        print("🔧 Flask endpoint works but webhook doesn't")
        print("   → Check SLACK_WEBHOOK_URL in .env file")
        print("   → Verify webhook URL in Slack app settings")
    else:
        print("🚨 Both webhook and Flask endpoint failing")
        print("   → Check all Slack credentials in .env file")
        print("   → Restart Flask server with: python app_modular.py")

if __name__ == "__main__":
    main()
