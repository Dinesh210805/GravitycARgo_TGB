#!/usr/bin/env python3
"""
🔧 OptiGenix Slack Diagnostic Tool
=================================
Diagnoses and fixes Slack integration issues
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_slack_configuration():
    """Check Slack app configuration and tokens"""
    print("🔧 SLACK CONFIGURATION DIAGNOSTIC")
    print("=" * 50)
    
    # Check environment variables
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    app_token = os.getenv('SLACK_APP_TOKEN')
    signing_secret = os.getenv('SLACK_SIGNING_SECRET')
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    print("📋 Environment Variables:")
    print(f"   SLACK_BOT_TOKEN: {'✅ Present' if bot_token else '❌ Missing'}")
    if bot_token:
        print(f"      Format: {'✅ Correct (xoxb-)' if bot_token.startswith('xoxb-') else '❌ Wrong format'}")
    
    print(f"   SLACK_APP_TOKEN: {'✅ Present' if app_token else '❌ Missing'}")
    if app_token:
        print(f"      Format: {'✅ Correct (xapp-)' if app_token.startswith('xapp-') else '❌ Wrong format'}")
    
    print(f"   SLACK_SIGNING_SECRET: {'✅ Present' if signing_secret else '❌ Missing'}")
    print(f"   SLACK_WEBHOOK_URL: {'✅ Present' if webhook_url else '❌ Missing'}")
    
    return bot_token, app_token, signing_secret

def test_slack_connection():
    """Test Slack API connection"""
    print("\n🔗 SLACK API CONNECTION TEST")
    print("=" * 50)
    
    try:
        from slack_bolt import App
        
        bot_token, app_token, signing_secret = check_slack_configuration()
        
        if not bot_token or not app_token:
            print("❌ Cannot test - Missing required tokens")
            return False
        
        # Create Slack app
        app = App(token=bot_token, signing_secret=signing_secret)
        
        # Test auth
        print("Testing bot authentication...")
        try:
            auth_response = app.client.auth_test()
            if auth_response["ok"]:
                print(f"✅ Bot authenticated successfully")
                print(f"   Bot User ID: {auth_response['user_id']}")
                print(f"   Bot Name: {auth_response.get('user', 'Unknown')}")
                print(f"   Team: {auth_response.get('team', 'Unknown')}")
            else:
                print(f"❌ Bot authentication failed: {auth_response.get('error')}")
                return False
        except Exception as e:
            print(f"❌ Bot authentication error: {e}")
            return False
        
        # Test app token for Socket Mode
        print("\nTesting Socket Mode capability...")
        try:
            from slack_bolt.adapter.socket_mode import SocketModeHandler
            handler = SocketModeHandler(app, app_token)
            print("✅ Socket Mode handler created successfully")
            
            # Don't actually start it, just test creation
            return True
            
        except Exception as e:
            print(f"❌ Socket Mode error: {e}")
            return False
            
    except ImportError:
        print("❌ slack-bolt not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "slack-bolt"])
        return test_slack_connection()  # Retry after installation
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def check_slack_app_settings():
    """Check Slack app configuration requirements"""
    print("\n📱 SLACK APP CONFIGURATION CHECKLIST")
    print("=" * 50)
    print("To fix slash command issues, verify these settings in your Slack app:")
    print()
    print("1. ✅ Socket Mode:")
    print("   - Go to https://api.slack.com/apps")
    print("   - Select your OptiGenix app")
    print("   - Go to 'Socket Mode' in sidebar")
    print("   - Enable Socket Mode")
    print("   - Generate App-Level Token with 'connections:write' scope")
    print()
    print("2. ✅ Slash Commands:")
    print("   - Go to 'Slash Commands' in sidebar")
    print("   - Create commands:")
    print("     /optigenix-status - Check system status")
    print("     /optigenix-optimize - Start optimization")
    print("   - Leave Request URL BLANK (Socket Mode handles this)")
    print()
    print("3. ✅ OAuth & Permissions:")
    print("   - Go to 'OAuth & Permissions'")
    print("   - Add these Bot Token Scopes:")
    print("     - app_mentions:read")
    print("     - channels:history")
    print("     - channels:read")
    print("     - chat:write")
    print("     - commands")
    print("     - users:read")
    print()
    print("4. ✅ Event Subscriptions:")
    print("   - Go to 'Event Subscriptions'")
    print("   - Enable Events")
    print("   - Subscribe to bot events: app_mention")
    print("   - Leave Request URL BLANK (Socket Mode handles this)")
    print()
    print("5. ✅ Install App:")
    print("   - Go to 'Install App'")
    print("   - Click 'Reinstall to Workspace'")
    print("   - Copy Bot User OAuth Token (starts with xoxb-)")
    print("   - Copy App-Level Token (starts with xapp-)")

def fix_slash_commands():
    """Attempt to fix slash command registration"""
    print("\n🔧 SLASH COMMAND FIX ATTEMPT")
    print("=" * 50)
    
    try:
        from slack_bolt import App
        
        bot_token, app_token, signing_secret = check_slack_configuration()
        
        if not all([bot_token, app_token, signing_secret]):
            print("❌ Cannot fix - Missing tokens")
            return False
        
        # The issue is likely that slash commands need to be manually registered
        # in the Slack app dashboard, not programmatically
        print("ℹ️  Slash commands must be registered in Slack App dashboard")
        print("   Socket Mode apps cannot register slash commands programmatically")
        print("   Please follow the checklist above to register them manually")
        
        return True
        
    except Exception as e:
        print(f"❌ Fix attempt failed: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🚀 OPTIGENIX SLACK DIAGNOSTIC TOOL")
    print("=" * 60)
    print()
    
    # Step 1: Check configuration
    bot_token, app_token, signing_secret = check_slack_configuration()
    
    # Step 2: Test connection
    connection_ok = test_slack_connection()
    
    # Step 3: Show configuration checklist
    check_slack_app_settings()
    
    # Step 4: Attempt to fix
    fix_slash_commands()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if bot_token and app_token and connection_ok:
        print("✅ Tokens are valid and connection works")
        print("❓ If slash commands still fail:")
        print("   1. Check Slack app dashboard configuration")
        print("   2. Ensure slash commands are registered")
        print("   3. Reinstall app to workspace")
        print("   4. Try /optigenix-status in a channel where bot is added")
    else:
        print("❌ Configuration issues found")
        print("   Please fix the issues above and run this tool again")
    
    print("\n🎯 Next Steps:")
    if not bot_token or not app_token:
        print("   1. Fix missing tokens in .env file")
        print("   2. Follow Slack app setup guide")
    else:
        print("   1. Check Slack app dashboard configuration")
        print("   2. Ensure bot is added to channels")
        print("   3. Test slash commands in Slack")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
