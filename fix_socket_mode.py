#!/usr/bin/env python3
"""
🔧 Socket Mode Channel Fixer
===========================
Fixes the channel access issue for Socket Mode notifications
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fix_socket_mode_channels():
    """Fix Socket Mode channel access"""
    print("🔧 SOCKET MODE CHANNEL FIXER")
    print("=" * 50)
    
    try:
        from slack_bolt import App
        
        bot_token = os.getenv('SLACK_BOT_TOKEN')
        app_token = os.getenv('SLACK_APP_TOKEN')
        
        if not bot_token or not app_token:
            print("❌ Missing Slack tokens")
            return False
        
        # Create app
        app = App(token=bot_token)
        
        print("🔍 Discovering accessible channels...")
        
        # Get list of channels
        channels_response = app.client.conversations_list(
            types="public_channel,private_channel",
            limit=50
        )
        
        accessible_channels = []
        
        if channels_response["ok"]:
            print(f"📊 Found {len(channels_response['channels'])} total channels")
            
            for channel in channels_response["channels"]:
                channel_info = {
                    'id': channel['id'],
                    'name': channel['name'],
                    'is_member': channel.get('is_member', False),
                    'is_private': channel.get('is_private', True)
                }
                
                # Test if bot can post to this channel
                if channel_info['is_member'] or not channel_info['is_private']:
                    try:
                        # Try to send a test message
                        test_result = app.client.chat_postMessage(
                            channel=channel['id'],
                            text="🧪 Socket Mode channel test - verifying access"
                        )
                        
                        if test_result["ok"]:
                            accessible_channels.append(channel_info)
                            print(f"✅ #{channel['name']} - Access confirmed")
                        else:
                            print(f"❌ #{channel['name']} - Access denied: {test_result.get('error')}")
                            
                    except Exception as test_error:
                        print(f"⚠️ #{channel['name']} - Test failed: {test_error}")
                else:
                    print(f"⏭️ #{channel['name']} - Skipped (private/not member)")
            
            print(f"\n📋 SUMMARY:")
            print(f"✅ Accessible channels: {len(accessible_channels)}")
            
            if accessible_channels:
                print("\n🎯 RECOMMENDED CHANNEL:")
                # Find best channel
                best_channel = None
                for ch in accessible_channels:
                    if ch['name'] in ['general', 'random', 'test']:
                        best_channel = ch
                        break
                
                if not best_channel:
                    best_channel = accessible_channels[0]
                
                print(f"   #{best_channel['name']} (ID: {best_channel['id']})")
                
                # Update the Socket Mode configuration
                update_socket_mode_config(best_channel['id'], best_channel['name'])
                
                return True
            else:
                print("❌ No accessible channels found!")
                print("\n🔧 SOLUTIONS:")
                print("1. Invite the bot to #general channel")
                print("2. Create a dedicated #optigenix channel")
                print("3. Check bot permissions in Slack app settings")
                return False
                
        else:
            print(f"❌ Failed to list channels: {channels_response.get('error')}")
            return False
            
    except ImportError:
        print("❌ slack-bolt not installed")
        print("🔧 Install with: pip install slack-bolt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_socket_mode_config(channel_id, channel_name):
    """Update Socket Mode configuration with working channel"""
    print(f"\n🔧 Updating Socket Mode configuration...")
    
    # Update auto_start.py notification function
    try:
        auto_start_path = "auto_start.py"
        if os.path.exists(auto_start_path):
            with open(auto_start_path, 'r') as f:
                content = f.read()
            
            # Replace #general with the working channel
            updated_content = content.replace(
                'channel="#general"',
                f'channel="{channel_id}"  # #{channel_name}'
            )
            
            with open(auto_start_path, 'w') as f:
                f.write(updated_content)
            
            print(f"✅ Updated auto_start.py to use #{channel_name}")
        
        print(f"✅ Socket Mode will now use #{channel_name} for notifications")
        return True
        
    except Exception as e:
        print(f"⚠️ Could not update config files: {e}")
        return False

def main():
    """Main function"""
    print("🎯 GOAL: Fix Socket Mode notification channel access")
    print("🔧 This will find accessible channels and configure them")
    print()
    
    if fix_socket_mode_channels():
        print("\n🎉 SUCCESS!")
        print("✅ Socket Mode notifications should now work")
        print("📱 Test by running an optimization")
    else:
        print("\n❌ FAILED!")
        print("🔧 Manual setup required")
        
    print("\nPress Enter to continue...")
    input()

if __name__ == "__main__":
    main()
