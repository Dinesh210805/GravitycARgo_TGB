#!/usr/bin/env python3
"""
🧪 Slack Notification Testing Script
====================================
Test the Slack notification system to ensure notifications are sent properly.
"""

import requests
import json
import time
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def test_flask_server():
    """Test if Flask server is running"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Flask server not accessible: {e}")
        return False

def test_optimization_notification():
    """Test the optimization complete notification"""
    print_header("TESTING OPTIMIZATION NOTIFICATION")
    
    if not test_flask_server():
        print("❌ Flask server is not running. Start it with: python app_modular.py")
        return False
    
    print("✅ Flask server is running")
    
    # Test data for notification
    test_data = {
        'volume_utilization': 87.5,
        'items_packed': 245,
        'total_items': 280,
        'cost_savings': 15000,
        'user_name': 'TestUser'
    }
    
    try:
        print("📤 Sending test notification...")
        response = requests.post(
            "http://localhost:5000/slack/notify/optimization-complete",
            json=test_data,
            timeout=10
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Notification Result: {result}")
            
            if result.get('success'):
                print("🎉 Slack notification sent successfully!")
                return True
            else:
                print(f"⚠️ Notification failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending notification: {e}")
        return False

def test_slack_status_command():
    """Test the Slack status command"""
    print_header("TESTING SLACK STATUS COMMAND")
    
    test_data = {
        'token': 'test-token',
        'team_id': 'T1234567890',
        'channel_id': 'C1234567890',
        'user_id': 'U1234567890',
        'user_name': 'test-user',
        'command': '/optigenix-status',
        'text': '',
        'response_url': 'https://hooks.slack.com/commands/test'
    }
    
    try:
        print("📤 Testing status command...")
        response = requests.post(
            "http://localhost:5000/slack/commands",
            data=test_data,
            timeout=10
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Status command working!")
            print(f"📊 Status response preview:")
            status_text = result.get('text', '')
            # Show first few lines
            lines = status_text.split('\n')[:8]
            for line in lines:
                print(f"   {line}")
            if len(status_text.split('\n')) > 8:
                print("   ... (truncated)")
            return True
        else:
            print(f"❌ Status command failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing status command: {e}")
        return False

def test_optimization_command():
    """Test the Slack optimization command"""
    print_header("TESTING SLACK OPTIMIZATION COMMAND")
    
    test_data = {
        'token': 'test-token',
        'team_id': 'T1234567890',
        'channel_id': 'C1234567890',
        'user_id': 'U1234567890',
        'user_name': 'test-user',
        'command': '/optigenix-optimize',
        'text': 'urgent',
        'response_url': 'https://hooks.slack.com/commands/test'
    }
    
    try:
        print("📤 Testing optimization command...")
        response = requests.post(
            "http://localhost:5000/slack/commands",
            data=test_data,
            timeout=10
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Optimization command working!")
            print(f"🚀 Response preview:")
            response_text = result.get('text', '')
            lines = response_text.split('\n')[:6]
            for line in lines:
                print(f"   {line}")
            return True
        else:
            print(f"❌ Optimization command failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing optimization command: {e}")
        return False

def check_webhook_configuration():
    """Check if webhook is configured"""
    print_header("CHECKING WEBHOOK CONFIGURATION")
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    
    if webhook_url:
        print(f"✅ Webhook URL configured: ...{webhook_url[-20:]}")
    else:
        print("⚠️ SLACK_WEBHOOK_URL not configured")
    
    if bot_token:
        print(f"✅ Bot token configured: ...{bot_token[-8:]}")
    else:
        print("⚠️ SLACK_BOT_TOKEN not configured")
    
    return bool(webhook_url or bot_token)

def show_summary(results):
    """Show test summary"""
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"📊 Tests run: {total_tests}")
    print(f"✅ Tests passed: {passed_tests}")
    print(f"❌ Tests failed: {total_tests - passed_tests}")
    
    print("\n📋 Detailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    if passed_tests == total_tests:
        print(f"\n🎉 All tests passed! Your Slack integration is working correctly.")
    else:
        print(f"\n⚠️ Some tests failed. Check the configuration and server status.")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Ensure Flask server is running: python app_modular.py")
        print(f"   2. Check environment variables in .env file")
        print(f"   3. Verify Slack webhook URL is correct")

def main():
    """Main test function"""
    print("🧪 OptiGenix Slack Notification Testing")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Run tests
    results["Webhook Configuration"] = check_webhook_configuration()
    results["Status Command"] = test_slack_status_command()
    results["Optimization Command"] = test_optimization_command()
    results["Optimization Notification"] = test_optimization_notification()
    
    # Show summary
    show_summary(results)
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
