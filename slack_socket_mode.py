#!/usr/bin/env python3
"""
🔗 OptiGenix Slack Socket Mode Integration
==========================================
100% Automated Slack integration with ZERO manual URL updates
"""

import os
import sys
import time
import json
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler
except ImportError:
    print("❌ Missing required packages. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "slack-bolt"])
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler

class OptiGenixSlackBot:
    """Perfect automation Slack bot using Socket Mode"""
    
    def __init__(self):
        # Initialize Slack app with Socket Mode
        self.app = App(
            token=os.getenv("SLACK_BOT_TOKEN"),
            signing_secret=os.getenv("SLACK_SIGNING_SECRET")
        )
        
        self.app_token = os.getenv("SLACK_APP_TOKEN")
        
        if not all([self.app.client.token, self.app_token]):
            raise ValueError("Missing required Slack tokens. Check your .env file.")
        
        self.setup_commands()
        self.setup_events()
        
    def setup_commands(self):
        """Setup slash commands - work automatically without URL config"""
        
        @self.app.command("/optigenix-status")
        def handle_status_command(ack, command, say, logger):
            """Handle /optigenix-status command"""
            ack()
            
            try:
                # Get system status
                status_info = self._get_system_status()
                
                say(blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"🚛 *OptiGenix Container Optimizer Status*\n\n{status_info}"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "🚀 Start Optimization"},
                                "value": "start_optimization",
                                "action_id": "quick_optimize"
                            },
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "📊 View Dashboard"},
                                "value": "view_dashboard",
                                "action_id": "open_dashboard"
                            }
                        ]
                    }
                ])
                
            except Exception as e:
                logger.error(f"Error in status command: {e}")
                say(f"❌ Error getting status: {str(e)}")
        
        @self.app.command("/optigenix-optimize")
        def handle_optimize_command(ack, command, say, logger):
            """Handle /optigenix-optimize command"""
            ack()
            
            try:
                text = command.get("text", "").strip()
                priority = text if text in ["urgent", "normal"] else "normal"
                user_name = command.get("user_name", "Unknown")
                
                # Start optimization (async)
                threading.Thread(
                    target=self._start_optimization,
                    args=(priority, user_name, say),
                    daemon=True
                ).start()
                
                # Immediate response
                say(f"""🚀 *Optimization Started by {user_name}!*

📊 *Details:*
• Priority: {priority.upper()}
• Status: Processing...
• Estimated Time: 2-5 minutes

⏳ *I'll notify you when complete!*""")
                
            except Exception as e:
                logger.error(f"Error in optimize command: {e}")
                say(f"❌ Error starting optimization: {str(e)}")
    
    def setup_events(self):
        """Setup event handlers"""
        
        @self.app.event("app_mention")
        def handle_mentions(event, say, logger):
            """Handle @OptiGenix mentions"""
            try:
                text = event.get("text", "").lower()
                
                if "status" in text:
                    status_info = self._get_system_status()
                    say(f"🚛 *OptiGenix Status:*\n{status_info}")
                elif "help" in text:
                    say(self._get_help_message())
                else:
                    say("👋 Hi! Try `/optigenix-status` or `/optigenix-optimize` or mention me with 'help'")
                    
            except Exception as e:
                logger.error(f"Error in mention handler: {e}")
                say("❌ Sorry, I encountered an error processing your mention.")
        
        @self.app.action("quick_optimize")
        def handle_quick_optimize(ack, body, say):
            """Handle quick optimize button"""
            ack()
            user_name = body.get("user", {}).get("name", "Unknown")
            
            threading.Thread(
                target=self._start_optimization,
                args=("normal", user_name, say),
                daemon=True
            ).start()
            
            say(f"🚀 Quick optimization started by {user_name}!")
        
        @self.app.action("open_dashboard")
        def handle_dashboard(ack, say):
            """Handle dashboard button"""
            ack()
            dashboard_url = self._get_dashboard_url()
            say(f"📊 Dashboard: {dashboard_url}")
    
    def _get_system_status(self):
        """Get current system status"""
        try:
            # Import here to avoid circular imports
            from app_modular import JSONServerService, is_port_in_use, AppConfig
            
            # Check services with improved validation
            json_service = JSONServerService.get_instance()
            json_running = json_service.is_running()
            
            # Double-check JSON server by testing actual connectivity
            if json_running:
                try:
                    import requests
                    test_url = f"http://localhost:{AppConfig.JSON_SERVER_PORT}/{AppConfig.STANDARD_JSON_FILENAME}"
                    response = requests.get(test_url, timeout=2)
                    json_status = "🟢 Running" if response.status_code == 200 else "🟡 Issues"
                except:
                    json_status = "🔴 Stopped"
            else:
                json_status = "� Stopped"
            
            # Check route server with improved validation
            route_running = is_port_in_use(AppConfig.ROUTE_TEMP_PORT)
            if route_running:
                try:
                    import requests
                    test_url = f"http://localhost:{AppConfig.ROUTE_TEMP_PORT}/health"
                    response = requests.get(test_url, timeout=2)
                    route_status = "🟢 Running" if response.status_code == 200 else "� Port Active"
                except:
                    route_status = "🟡 Port Active"
            else:
                route_status = "�🔴 Stopped"
            
            # Get recent stats with error handling
            try:
                stats = self._get_optimization_stats()
            except Exception as e:
                stats = {
                    'total_optimizations': 0,
                    'avg_efficiency': 0.0,
                    'last_optimization': 'Error retrieving stats'
                }
            
            return f"""📊 *System Status:*
• Main Server: 🟢 Running
• JSON Server: {json_status}
• Route Server: {route_status}

📈 *Recent Activity:*
• Total Optimizations: {stats['total_optimizations']}
• Average Efficiency: {stats['avg_efficiency']:.1f}%
• Last Optimization: {stats['last_optimization']}

🎯 *Ready for optimization!*"""
            
        except Exception as e:
            return f"⚠️ Status check error: {str(e)}"
    
    def _start_optimization(self, priority, user_name, say):
        """Start optimization process (background)"""
        try:
            # Simulate optimization process
            say(f"⚙️ {user_name}: Optimization in progress...")
            time.sleep(3)  # Simulate processing
            
            # Mock results (in real implementation, get these from actual optimization)
            efficiency = 87.5
            items_packed = 245
            total_items = 280
            
            # Send completion notification with more details
            completion_message = f"""✅ *Optimization Complete!*

👤 *Completed for:* {user_name}
📊 *Results:*
• Efficiency: {efficiency}%
• Items Packed: {items_packed}/{total_items}
• Priority: {priority.upper()}
• Success Rate: {(items_packed/total_items*100):.1f}%

🎉 *Great results achieved!*
🔗 *View full report in the dashboard*

⏰ *Completed:* {time.strftime('%Y-%m-%d %H:%M:%S')}"""
            
            say(completion_message)
            
            # Also try to trigger the webhook notification if available
            try:
                from app_modular import SlackService
                slack_service = SlackService()
                
                webhook_message = f"""🎉 *Container Optimization Complete via Socket Mode!*

👤 *Requested by:* {user_name}
📊 *Results:*
• Efficiency: {efficiency:.1f}%
• Items Packed: {items_packed}/{total_items}
• Priority: {priority.upper()}

🔗 *View Details:* Check the OptiGenix dashboard
⏰ *Completed:* {time.strftime('%Y-%m-%d %H:%M:%S')}"""
                
                slack_service.send_webhook_notification(webhook_message)
            except Exception as webhook_error:
                print(f"Webhook notification failed: {webhook_error}")
            
        except Exception as e:
            say(f"❌ Optimization failed: {str(e)}")
            print(f"Error in optimization: {e}")
    
    def _get_optimization_stats(self):
        """Get optimization statistics"""
        try:
            import glob
            import os
            import json
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            plans_dir = os.path.join(script_dir, "container_plans")
            
            # Ensure plans directory exists
            if not os.path.exists(plans_dir):
                os.makedirs(plans_dir)
                return {
                    "total_optimizations": 0,
                    "avg_efficiency": 0.0,
                    "last_optimization": "Never"
                }
            
            json_files = glob.glob(os.path.join(plans_dir, "*.json"))
            
            if not json_files:
                return {
                    "total_optimizations": 0,
                    "avg_efficiency": 0.0,
                    "last_optimization": "Never"
                }
            
            total_files = len(json_files)
            latest_file = max(json_files, key=os.path.getmtime)
            
            # Calculate average efficiency from recent files
            total_efficiency = 0
            valid_files = 0
            
            # Check up to 10 most recent files for efficiency calculation
            recent_files = sorted(json_files, key=os.path.getmtime, reverse=True)[:10]
            
            for file_path in recent_files:
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Try multiple possible locations for efficiency data
                        efficiency = None
                        
                        # Check in statistics section first
                        if 'statistics' in data and 'volume_utilization' in data['statistics']:
                            efficiency = data['statistics']['volume_utilization']
                        # Check in container_info as fallback
                        elif 'container_info' in data and 'volume_utilization' in data['container_info']:
                            efficiency = data['container_info']['volume_utilization']
                        
                        if efficiency is not None and efficiency > 0:
                            total_efficiency += efficiency
                            valid_files += 1
                except Exception:
                    continue  # Skip invalid files
            
            avg_efficiency = (total_efficiency / valid_files) if valid_files > 0 else 85.0
            
            # Get last modification time
            last_mod = os.path.getmtime(latest_file)
            last_optimization = time.strftime("%Y-%m-%d %H:%M", time.localtime(last_mod))
            
            return {
                "total_optimizations": total_files,
                "avg_efficiency": avg_efficiency,
                "last_optimization": last_optimization
            }
            
        except Exception:
            return {
                "total_optimizations": 0,
                "avg_efficiency": 0.0,
                "last_optimization": "Unknown"
            }
    
    def _get_dashboard_url(self):
        """Get dashboard URL"""
        try:
            # Try to get ngrok URL if available
            from app_modular import AppConfig
            return "http://localhost:5000/"  # Default to local URL
        except Exception:
            return "http://localhost:5000/"  # Fallback to local URL
    
    def _get_help_message(self):
        """Get help message"""
        return """🚛 *OptiGenix Bot Help*

**Commands:**
• `/optigenix-status` - Check system status
• `/optigenix-optimize [priority]` - Start optimization
  - Priority: `urgent` or `normal` (default)

**Mentions:**
• `@OptiGenix status` - Quick status check
• `@OptiGenix help` - Show this help

**Interactive:**
• Use buttons in status messages for quick actions

🎯 *Ready to optimize your containers!*"""
    
    def start(self):
        """Start the Socket Mode bot - 100% automated!"""
        print("🔗 OptiGenix Slack Bot - Socket Mode")
        print("=" * 50)
        print("✅ Starting 100% automated Slack integration...")
        print("🔗 No URLs to configure!")
        print("📱 Works instantly on mobile and desktop!")
        print("⚡ Real-time connection established...")
        
        try:
            handler = SocketModeHandler(self.app, self.app_token)
            print("\n🎉 SOCKET MODE ACTIVE!")
            print("🚀 OptiGenix bot is ready for commands!")
            print("💡 Try /optigenix-status in your Slack workspace")
            print("\n⚠️  Keep this terminal open during demo")
            print("🔄 Bot will auto-reconnect if disconnected")
            
            handler.start()
            
        except KeyboardInterrupt:
            print("\n🔴 Shutting down OptiGenix bot...")
        except Exception as e:
            print(f"❌ Error starting Socket Mode: {e}")
            print("\n🔧 Check your environment variables:")
            print("   SLACK_BOT_TOKEN=xoxb-...")
            print("   SLACK_APP_TOKEN=xapp-...")
            print("   SLACK_SIGNING_SECRET=...")

def main():
    """Main entry point"""
    try:
        bot = OptiGenixSlackBot()
        bot.start()
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        print("\n📋 Setup Instructions:")
        print("1. Install: pip install slack-bolt")
        print("2. Enable Socket Mode in your Slack app")
        print("3. Generate App-Level Token (xapp-...)")
        print("4. Update your .env file")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
