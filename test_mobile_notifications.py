#!/usr/bin/env python3
"""
🧪 Quick Slack Notification Test
================================
Test if Slack notifications work on your mobile
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_webhook_notification():
    """Test webhook notification directly"""
    print("📱 Testing Slack Webhook Notification...")
    print("=" * 50)
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL not found in .env")
        print("🔧 Add this to your .env file:")
        print("SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL")
        return False
    
    # Test message
    test_message = f"""🧪 **Mobile Notification Test** 📱

⏰ Time: {time.strftime('%H:%M:%S')}
📍 Source: OptiGenix Test Script
🎯 Purpose: Testing mobile notifications

🔔 *If you see this on your mobile, notifications are working!*"""
    
    try:
        response = requests.post(webhook_url, json={"text": test_message}, timeout=10)
        if response.status_code == 200:
            print("✅ Webhook test successful!")
            print("📱 Check your mobile Slack app now!")
            return True
        else:
            print(f"❌ Webhook failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_socket_mode_notification():
    """Test Socket Mode notification"""
    print("\n🔗 Testing Socket Mode Notification...")
    print("=" * 50)
    
    try:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
        
        bot_token = os.getenv('SLACK_BOT_TOKEN')
        app_token = os.getenv('SLACK_APP_TOKEN')
        
        if not bot_token or not app_token:
            print("❌ Missing Slack tokens")
            print("🔧 Required in .env:")
            print("SLACK_BOT_TOKEN=xoxb-...")
            print("SLACK_APP_TOKEN=xapp-...")
            return False
        
        # Create app
        app = App(token=bot_token)
        
        # Method 1: Try to send to #general (most common)
        target_channel = "general"
        
        test_message = f"""🔗 **Socket Mode Test** 📱

⏰ Time: {time.strftime('%H:%M:%S')}
📍 Source: OptiGenix Socket Mode
🎯 Purpose: Testing Socket Mode notifications

✨ *Socket Mode is working if you see this!*"""
        
        try:
            response = app.client.chat_postMessage(
                channel=target_channel,
                text=test_message
            )
            
            if response["ok"]:
                print("✅ Socket Mode test successful!")
                print(f"📤 Message sent to #{target_channel}")
                return True
            else:
                print(f"❌ Failed to send: {response.get('error', 'Unknown error')}")
                
                # Method 2: Try to find bot's own DM channel
                print("🔄 Trying alternative method...")
                try:
                    # Get bot's user ID
                    auth_response = app.client.auth_test()
                    if auth_response["ok"]:
                        bot_user_id = auth_response["user_id"]
                        
                        # Open a DM conversation with the bot (for testing)
                        dm_response = app.client.conversations_open(users=[bot_user_id])
                        if dm_response["ok"]:
                            dm_channel = dm_response["channel"]["id"]
                            
                            # Send to DM
                            dm_message_response = app.client.chat_postMessage(
                                channel=dm_channel,
                                text="🧪 Socket Mode DM test - this should work!"
                            )
                            
                            if dm_message_response["ok"]:
                                print("✅ DM method successful!")
                                return True
                            else:
                                print(f"❌ DM also failed: {dm_message_response.get('error')}")
                                
                except Exception as dm_error:
                    print(f"❌ DM method error: {dm_error}")
                
                # Method 3: List and try accessible channels
                print("🔄 Checking accessible channels...")
                try:
                    channels_response = app.client.conversations_list(
                        types="public_channel",
                        limit=20
                    )
                    
                    if channels_response["ok"]:
                        for channel in channels_response["channels"]:
                            if channel.get("is_member", False):
                                try:
                                    test_response = app.client.chat_postMessage(
                                        channel=channel["id"],
                                        text="🧪 Socket Mode working!"
                                    )
                                    
                                    if test_response["ok"]:
                                        print(f"✅ Success with #{channel['name']}")
                                        return True
                                except:
                                    continue
                                    
                        print("❌ No accessible channels found")
                    else:
                        print("❌ Cannot list channels")
                        
                except Exception as list_error:
                    print(f"❌ Channel listing error: {list_error}")
                
                return False
                
        except Exception as e:
            print(f"❌ Socket Mode error: {e}")
            return False
            
    except ImportError:
        print("❌ slack-bolt not installed")
        print("� Install with: pip install slack-bolt")
        return False
    except Exception as e:
        print(f"❌ General error: {e}")
        return False
    except Exception as e:
        print(f"❌ Socket Mode error: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 SLACK MOBILE NOTIFICATION TEST")
    print("=" * 60)
    print("🎯 Goal: Get notifications on your mobile Slack app")
    print()
    
    # Test both methods
    webhook_works = test_webhook_notification()
    socket_works = test_socket_mode_notification()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"📨 Webhook Notifications: {'✅ Working' if webhook_works else '❌ Failed'}")
    print(f"🔗 Socket Mode Notifications: {'✅ Working' if socket_works else '❌ Failed'}")
    
    if webhook_works or socket_works:
        print("\n🎉 SUCCESS! At least one notification method works.")
        print("📱 Check your mobile Slack app for test messages.")
        print("\n🔔 When you run optimizations, you should now get notifications!")
        return True
    else:
        print("\n❌ ISSUE: No notification methods are working.")
        print("\n🔧 QUICK FIXES:")
        print("1. Check your .env file has correct tokens")
        print("2. Ensure your Slack app has 'chat:write' permission")
        print("3. Verify you're in the #general channel")
        print("4. Try adding a webhook URL to .env")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
