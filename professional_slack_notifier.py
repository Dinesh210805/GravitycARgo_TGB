#!/usr/bin/env python3
"""
📱 Professional Slack Notification System
=========================================
Sends professionally formatted Slack messages with HTTPS links
"""

import os
import sys
import time
import socket
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OptiGenixSlackNotifier:
    """Professional Slack notification system for OptiGenix"""
    
    def __init__(self):
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.app_token = os.getenv('SLACK_APP_TOKEN')
        self.local_ip = self.get_local_ip()
        self.https_port = 5443
        
    def get_local_ip(self):
        """Get the local IP address for network access"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "localhost"
    
    def format_professional_message(self, optimization_data):
        """Format the optimization results into a professional Slack message"""
        
        # Extract data with defaults
        volume_utilization = optimization_data.get('volume_utilization', 0)
        items_packed = optimization_data.get('items_packed', 0)
        total_weight = optimization_data.get('total_weight', 0)
        remaining_volume = optimization_data.get('remaining_volume', 0)
        user_name = optimization_data.get('user_name', 'System')
        algorithm = optimization_data.get('algorithm_used', 'Standard')
        
        # Generate HTTPS URL for mobile access
        https_url = f"https://{self.local_ip}:{self.https_port}/optimize"
        
        # Create professional message format
        message = f"""OptiGenix Bot:
✅ *Optimization Complete!*

📊 *{volume_utilization:.1f}%* Volume Utilization  
📦 *{items_packed}* Items Packed  
⚖️ *{total_weight:.1f} kg* Total Weight  
📏 *{remaining_volume:.2f} m³* Space Remaining  

📋 *View Full Report:* <{https_url}|Open 3D Visualization>

👤 *Completed by:* {user_name}
🤖 *Algorithm:* {algorithm}
⏰ *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        return message
    
    def create_rich_slack_blocks(self, optimization_data):
        """Create rich Slack block format for better presentation"""
        
        volume_utilization = optimization_data.get('volume_utilization', 0)
        items_packed = optimization_data.get('items_packed', 0)
        total_weight = optimization_data.get('total_weight', 0)
        remaining_volume = optimization_data.get('remaining_volume', 0)
        user_name = optimization_data.get('user_name', 'System')
        algorithm = optimization_data.get('algorithm_used', 'Standard')
        
        https_url = f"https://{self.local_ip}:{self.https_port}/optimize"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🎉 Container Optimization Complete!"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"📊 *Volume Utilization:*\n{volume_utilization:.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"📦 *Items Packed:*\n{items_packed}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"⚖️ *Total Weight:*\n{total_weight:.1f} kg"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"📏 *Space Remaining:*\n{remaining_volume:.2f} m³"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"👤 *Completed by:* {user_name}\n🤖 *Algorithm:* {algorithm}\n⏰ *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📱 Open 3D Visualization"
                        },
                        "url": https_url,
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📋 View Dashboard"
                        },
                        "url": f"https://{self.local_ip}:{self.https_port}/"
                    }
                ]
            }
        ]
        
        return blocks
    
    def send_webhook_notification(self, optimization_data):
        """Send notification via webhook URL"""
        if not self.webhook_url:
            print("❌ No webhook URL configured")
            return False
        
        try:
            message = self.format_professional_message(optimization_data)
            
            payload = {
                "text": message,
                "username": "OptiGenix Bot",
                "icon_emoji": ":truck:",
                "blocks": self.create_rich_slack_blocks(optimization_data)
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ Professional Slack notification sent via webhook")
                print(f"📱 Mobile link: https://{self.local_ip}:{self.https_port}/optimize")
                return True
            else:
                print(f"❌ Webhook failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Webhook error: {e}")
            return False
    
    def send_socket_mode_notification(self, optimization_data):
        """Send notification via Socket Mode"""
        try:
            from slack_bolt import App
            
            if not self.bot_token or not self.app_token:
                print("❌ Missing Socket Mode tokens")
                return False
            
            app = App(token=self.bot_token)
            
            # Find target channel
            target_channel = self.discover_target_channel(app)
            if not target_channel:
                print("❌ No accessible channel found for Socket Mode")
                return False
            
            # Send rich message
            blocks = self.create_rich_slack_blocks(optimization_data)
            
            response = app.client.chat_postMessage(
                channel=target_channel,
                blocks=blocks,
                text=self.format_professional_message(optimization_data)  # Fallback text
            )
            
            if response["ok"]:
                print("✅ Professional Slack notification sent via Socket Mode")
                print(f"📱 Mobile link: https://{self.local_ip}:{self.https_port}/optimize")
                return True
            else:
                print(f"❌ Socket Mode failed: {response.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ Socket Mode error: {e}")
            return False
    
    def discover_target_channel(self, app):
        """Discover the best channel to send notifications to"""
        try:
            channels_response = app.client.conversations_list(
                types="public_channel,private_channel",
                limit=50
            )
            
            if channels_response["ok"]:
                for channel in channels_response["channels"]:
                    if channel.get("is_member", False) or not channel.get("is_private", True):
                        # Prefer specific channels
                        if channel["name"] in ["all-gravitycargos-space", "general", "random"]:
                            return channel["id"]
                
                # Fallback to first available
                for channel in channels_response["channels"]:
                    if channel.get("is_member", False) or not channel.get("is_private", True):
                        return channel["id"]
            
            return None
            
        except Exception as e:
            print(f"❌ Channel discovery error: {e}")
            return None
    
    def send_optimization_complete_notification(self, optimization_data):
        """Send optimization complete notification using best available method"""
        print("📱 SENDING PROFESSIONAL SLACK NOTIFICATION")
        print("=" * 50)
        
        notification_sent = False
        
        # Method 1: Try Socket Mode first (rich formatting)
        if self.bot_token and self.app_token:
            print("🔗 Attempting Socket Mode notification...")
            notification_sent = self.send_socket_mode_notification(optimization_data)
        
        # Method 2: Fallback to webhook
        if not notification_sent and self.webhook_url:
            print("📨 Attempting webhook notification...")
            notification_sent = self.send_webhook_notification(optimization_data)
        
        if notification_sent:
            print("🎉 Professional notification delivered successfully!")
            print(f"📱 Users can access: https://{self.local_ip}:{self.https_port}/optimize")
        else:
            print("❌ Failed to send notification - check Slack configuration")
        
        return notification_sent

def test_notification_system():
    """Test the professional notification system"""
    print("🧪 TESTING PROFESSIONAL SLACK NOTIFICATIONS")
    print("=" * 50)
    
    notifier = OptiGenixSlackNotifier()
    
    # Test data matching your example
    test_data = {
        'volume_utilization': 2.9,
        'items_packed': 64,
        'total_weight': 4691.0,
        'remaining_volume': 38.60,
        'user_name': 'Test User',
        'algorithm_used': 'Genetic Algorithm'
    }
    
    print("📊 Test optimization data:")
    for key, value in test_data.items():
        print(f"   {key}: {value}")
    
    print(f"\n📱 Mobile access URL: https://{notifier.local_ip}:{notifier.https_port}/optimize")
    
    # Send test notification
    success = notifier.send_optimization_complete_notification(test_data)
    
    if success:
        print("\n✅ Test completed successfully!")
        print("📱 Check your Slack app for the professional notification")
    else:
        print("\n❌ Test failed - check your Slack configuration")

if __name__ == "__main__":
    test_notification_system()
