#!/usr/bin/env python3
"""
Quick Slack Command Debug Test
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_slack_tokens():
    """Test if Slack tokens are properly loaded"""
    print("🧪 Testing Slack Token Configuration")
    print("=" * 50)
    
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    app_token = os.getenv("SLACK_APP_TOKEN")
    signing_secret = os.getenv("SLACK_SIGNING_SECRET")
    
    print(f"SLACK_BOT_TOKEN: {'✅ Set' if bot_token else '❌ Missing'}")
    if bot_token:
        print(f"  - Starts with: {bot_token[:10]}...")
        
    print(f"SLACK_APP_TOKEN: {'✅ Set' if app_token else '❌ Missing'}")
    if app_token:
        print(f"  - Starts with: {app_token[:10]}...")
        
    print(f"SLACK_SIGNING_SECRET: {'✅ Set' if signing_secret else '❌ Missing'}")
    if signing_secret:
        print(f"  - Starts with: {signing_secret[:10]}...")
    
    return all([bot_token, app_token, signing_secret])

def test_slack_bolt():
    """Test if slack_bolt is properly installed"""
    print("\n🧪 Testing Slack Bolt Installation")
    print("=" * 50)
    
    try:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
        print("✅ slack_bolt is properly installed")
        return True
    except ImportError as e:
        print(f"❌ slack_bolt import error: {e}")
        print("💡 Install with: pip install slack-bolt")
        return False

def test_slack_connection():
    """Test basic Slack connection"""
    print("\n🧪 Testing Slack Connection")
    print("=" * 50)
    
    if not test_slack_bolt():
        return False
        
    if not test_slack_tokens():
        print("❌ Missing required tokens")
        return False
    
    try:
        from slack_bolt import App
        
        app = App(
            token=os.getenv("SLACK_BOT_TOKEN"),
            signing_secret=os.getenv("SLACK_SIGNING_SECRET")
        )
        
        print("✅ Slack App created successfully")
        
        # Test simple API call
        try:
            response = app.client.auth_test()
            print(f"✅ Bot authenticated as: {response['user']}")
            print(f"✅ Team: {response['team']}")
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Slack App creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 OptiGenix Slack Debug Tool")
    print("=" * 50)
    
    success = test_slack_connection()
    
    if success:
        print("\n🎉 All Slack tests passed!")
        print("💡 Your Slack integration should work properly.")
        print("🔄 Try restarting your app and test /optigenix-status again")
    else:
        print("\n❌ Slack tests failed!")
        print("🔧 Fix the issues above and try again")
        print("\n📋 Common fixes:")
        print("1. Regenerate Slack tokens at https://api.slack.com/apps")
        print("2. Update .env file with new tokens")
        print("3. Ensure Socket Mode is enabled in Slack app settings")
        print("4. Install slack-bolt: pip install slack-bolt")
