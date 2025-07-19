#!/usr/bin/env python3
"""
Debug script to identify Slack integration issues
"""

import os
import sys
import requests
import json
from datetime import datetime

def check_environment_variables():
    """Check if required environment variables are set"""
    print("🔍 Checking Environment Variables...")
    print("=" * 50)
    
    env_vars = [
        'SLACK_BOT_TOKEN',
        'SLACK_APP_TOKEN', 
        'SLACK_SIGNING_SECRET',
        'SLACK_CLIENT_SECRET',
        'SLACK_WEBHOOK_URL'
    ]
    
    missing_vars = []
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * (len(value) - 8)}{value[-8:] if len(value) > 8 else value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    return missing_vars

def check_slack_webhook():
    """Test Slack webhook connectivity"""
    print("\n📡 Testing Slack Webhook...")
    print("=" * 50)
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL not configured")
        return False
    
    # Test message
    test_payload = {
        "text": f"🧪 Test notification from OptiGenix Debug - {datetime.now().strftime('%H:%M:%S')}"
    }
    
    try:
        response = requests.post(webhook_url, json=test_payload, timeout=10)
        if response.status_code == 200:
            print("✅ Webhook test successful")
            return True
        else:
            print(f"❌ Webhook failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return False

def check_slack_bot_api():
    """Test Slack Bot API connectivity"""
    print("\n🤖 Testing Slack Bot API...")
    print("=" * 50)
    
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN not configured")
        return False
    
    headers = {
        "Authorization": f"Bearer {bot_token}",
        "Content-Type": "application/json"
    }
    
    # Test auth
    try:
        response = requests.get("https://slack.com/api/auth.test", 
                               headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                print(f"✅ Bot API connected - Team: {data.get('team')}, User: {data.get('user')}")
                return True
            else:
                print(f"❌ Bot API failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Bot API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bot API error: {e}")
        return False

def check_local_flask_server():
    """Check if Flask server is running and accessible"""
    print("\n🌐 Testing Local Flask Server...")
    print("=" * 50)
    
    ports_to_test = [5000, 8080, 10000]
    flask_running = False
    
    for port in ports_to_test:
        try:
            response = requests.get(f"http://localhost:{port}/", timeout=3)
            if response.status_code == 200:
                print(f"✅ Flask server running on port {port}")
                flask_running = True
                
                # Test Slack notification endpoint
                try:
                    test_data = {
                        "volume_utilization": 85.5,
                        "items_packed": 25,
                        "total_items": 30,
                        "cost_savings": 5000,
                        "user_name": "Debug Test"
                    }
                    
                    notify_response = requests.post(
                        f"http://localhost:{port}/slack/notify/optimization-complete",
                        json=test_data,
                        timeout=5
                    )
                    
                    if notify_response.status_code == 200:
                        result = notify_response.json()
                        print(f"✅ Notification endpoint accessible: {result}")
                    else:
                        print(f"❌ Notification endpoint failed: {notify_response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Notification endpoint error: {e}")
                
                break
        except Exception:
            continue
    
    if not flask_running:
        print("❌ Flask server not running on common ports")
    
    return flask_running

def generate_env_file():
    """Generate a sample .env file with placeholders"""
    print("\n📝 Generating .env template...")
    print("=" * 50)
    
    env_content = """# OptiGenix Slack Integration Configuration
# Copy this to .env and fill in your actual values

# Bot token from https://api.slack.com/apps/A096HEE7TGD/oauth
SLACK_BOT_TOKEN=xoxb-your-bot-token-here

# App-level token for Socket Mode from https://api.slack.com/apps/A096HEE7TGD/general
SLACK_APP_TOKEN=xapp-1-your-app-token-here

# Signing secret from https://api.slack.com/apps/A096HEE7TGD/general
SLACK_SIGNING_SECRET=your-signing-secret-here

# Client secret from https://api.slack.com/apps/A096HEE7TGD/general
SLACK_CLIENT_SECRET=your-client-secret-here

# Webhook URL from https://api.slack.com/apps/A096HEE7TGD/incoming-webhooks
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env.template file")
    print("📋 Next steps:")
    print("   1. Copy .env.template to .env")
    print("   2. Fill in your actual Slack credentials")
    print("   3. Restart the Flask application")

def main():
    """Main debug function"""
    print("🔧 OptiGenix Slack Integration Debugger")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check environment
    missing_vars = check_environment_variables()
    
    # Test webhook if configured
    webhook_working = check_slack_webhook()
    
    # Test bot API if configured  
    bot_working = check_slack_bot_api()
    
    # Test Flask server
    flask_working = check_local_flask_server()
    
    # Summary
    print("\n📋 Summary")
    print("=" * 50)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        generate_env_file()
    else:
        print("✅ All environment variables configured")
    
    if webhook_working:
        print("✅ Slack webhook working")
    else:
        print("❌ Slack webhook not working")
    
    if bot_working:
        print("✅ Slack bot API working")
    else:
        print("❌ Slack bot API not working")
        
    if flask_working:
        print("✅ Flask server accessible")
    else:
        print("❌ Flask server not accessible")
    
    # Recommendations
    print("\n💡 Recommendations")
    print("=" * 50)
    
    if missing_vars:
        print("1. Configure missing environment variables using .env file")
    
    if not webhook_working and not bot_working:
        print("2. Set up Slack app credentials properly")
        print("   - Go to https://api.slack.com/apps/A096HEE7TGD")
        print("   - Get bot token, webhook URL, and signing secret")
    
    if not flask_working:
        print("3. Start Flask server: python app_modular.py")
    
    if webhook_working or bot_working:
        print("4. Test optimization to trigger notifications")

if __name__ == "__main__":
    main()
