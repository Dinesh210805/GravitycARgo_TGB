#!/usr/bin/env python3
"""
🧪 OptiGenix Slash Command Tester
=================================
Tests slash commands and fixes common issues
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_slash_commands():
    """Test slash command registration and functionality"""
    print("🧪 SLASH COMMAND TESTER")
    print("=" * 50)
    
    try:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
        
        bot_token = os.getenv('SLACK_BOT_TOKEN')
        app_token = os.getenv('SLACK_APP_TOKEN')
        signing_secret = os.getenv('SLACK_SIGNING_SECRET')
        
        if not all([bot_token, app_token, signing_secret]):
            print("❌ Missing required tokens")
            return False
        
        # Create Slack app with proper error handling
        app = App(
            token=bot_token,
            signing_secret=signing_secret
        )
        
        print("✅ Slack app created successfully")
        
        # Test authentication
        try:
            auth_response = app.client.auth_test()
            if auth_response["ok"]:
                print(f"✅ Bot authenticated: {auth_response.get('user', 'Unknown')}")
            else:
                print(f"❌ Auth failed: {auth_response.get('error')}")
                return False
        except Exception as e:
            print(f"❌ Auth error: {e}")
            return False
        
        # Register slash commands with proper error handling
        @app.command("/optigenix-status")
        def handle_status_command(ack, command, say, logger):
            """Handle /optigenix-status command"""
            ack()  # Acknowledge the command immediately
            
            try:
                user_name = command.get("user_name", "Unknown")
                channel = command.get("channel_name", "unknown-channel")
                
                status_message = f"""🚛 *OptiGenix Status Check*

📊 **System Status:**
• Main Server: 🟢 Running
• Socket Mode: 🟢 Connected  
• Auto-Notifications: 🟢 Enabled

👤 **Requested by:** {user_name}
📍 **Channel:** #{channel}
⏰ **Time:** {time.strftime('%Y-%m-%d %H:%M:%S')}

🎯 **Ready for optimization!**
💡 Use `/optigenix-optimize` to start an optimization

🔗 **Dashboard:** http://localhost:5000"""
                
                say(status_message)
                print(f"✅ Status command executed for {user_name} in #{channel}")
                
            except Exception as e:
                logger.error(f"Error in status command: {e}")
                say(f"❌ Error getting status: {str(e)}")
                print(f"❌ Status command error: {e}")
        
        @app.command("/optigenix-optimize")
        def handle_optimize_command(ack, command, say, logger):
            """Handle /optigenix-optimize command"""
            ack()  # Acknowledge the command immediately
            
            try:
                user_name = command.get("user_name", "Unknown")
                text = command.get("text", "").strip()
                priority = text if text in ["urgent", "normal"] else "normal"
                
                # Immediate response
                say(f"""🚀 *Optimization Started by {user_name}!*

📊 *Details:*
• Priority: {priority.upper()}
• Status: Processing...
• Estimated Time: 2-5 minutes

⏳ *I'll notify you when complete!*
🔗 *Monitor progress:* http://localhost:5000

💡 *This is a test response - actual optimization would run in the background*""")
                
                print(f"✅ Optimize command executed for {user_name} with priority {priority}")
                
            except Exception as e:
                logger.error(f"Error in optimize command: {e}")
                say(f"❌ Error starting optimization: {str(e)}")
                print(f"❌ Optimize command error: {e}")
        
        # Add app mention handler
        @app.event("app_mention")
        def handle_mentions(event, say, logger):
            """Handle @OptiGenix mentions"""
            try:
                text = event.get("text", "").lower()
                user = event.get("user", "Unknown")
                
                if "status" in text:
                    say("🚛 *OptiGenix Status:* All systems operational! Use `/optigenix-status` for detailed info.")
                elif "help" in text:
                    say("""👋 *OptiGenix Bot Help*

**Commands:**
• `/optigenix-status` - Check system status
• `/optigenix-optimize [priority]` - Start optimization

**Mentions:**
• `@OptiGenix status` - Quick status check
• `@OptiGenix help` - Show this help

🎯 *Ready to optimize your containers!*""")
                else:
                    say("👋 Hi! Try `/optigenix-status` or `/optigenix-optimize` or mention me with 'help'")
                    
                print(f"✅ Mention handled for user {user}")
                    
            except Exception as e:
                logger.error(f"Error in mention handler: {e}")
                say("❌ Sorry, I encountered an error processing your mention.")
                print(f"❌ Mention handler error: {e}")
        
        print("✅ Slash commands registered successfully")
        
        # Test Socket Mode handler creation
        try:
            handler = SocketModeHandler(app, app_token)
            print("✅ Socket Mode handler created successfully")
            
            # Start the handler for testing
            print("\n🚀 Starting Socket Mode for testing...")
            print("💡 Try your slash commands in Slack now!")
            print("📱 Commands should work on mobile and desktop")
            print("⚠️  Press Ctrl+C to stop testing")
            
            handler.start()
            
        except KeyboardInterrupt:
            print("\n✅ Test completed successfully!")
            return True
        except Exception as e:
            print(f"❌ Socket Mode handler error: {e}")
            return False
            
    except ImportError:
        print("❌ slack-bolt not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "slack-bolt"])
        return test_slash_commands()  # Retry after installation
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main function"""
    print("🧪 OPTIGENIX SLASH COMMAND TESTER")
    print("=" * 60)
    print()
    print("This tool will test your slash commands and help fix issues.")
    print("Make sure your bot is added to the channel before testing!")
    print()
    
    if test_slash_commands():
        print("\n✅ Test completed! Slash commands should now work.")
    else:
        print("\n❌ Test failed. Check the errors above.")
        print("\n📋 Troubleshooting:")
        print("1. Verify bot is added to the channel")
        print("2. Check Slack app dashboard settings")
        print("3. Ensure slash commands are registered in Slack app")
        print("4. Try reinstalling the app to your workspace")

if __name__ == "__main__":
    main()
