#!/usr/bin/env python3
"""
🚀 OptiGenix Professional Notifier - Fixed Version
=================================================
Prioritizes webhook notifications for guaranteed delivery
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

class OptiGenixSlackNotifierFixed:
    """Professional Slack notification system - Fixed for reliability"""
    
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
                            "text": "📱 View 3D Visualization"
                        },
                        "url": https_url,
                        "style": "primary"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"📱 *Mobile Access:* {https_url}"
                    }
                ]
            }
        ]
        
        return blocks
    
    def send_webhook_notification(self, optimization_data):
        """Send notification via webhook - Primary method"""
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
    
    def send_socket_mode_notification_safe(self, optimization_data):
        """Send notification via Socket Mode with timeout protection"""
        try:
            # Import with timeout protection
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Socket Mode timeout")
            
            # Set 10-second timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(10)
            
            try:
                from slack_bolt import App
                
                if not self.bot_token:
                    print("❌ Missing Socket Mode bot token")
                    return False
                
                app = App(token=self.bot_token)
                
                # Try to find a channel quickly
                channels_response = app.client.conversations_list(
                    types="public_channel,private_channel",
                    limit=20
                )
                
                target_channel = None
                if channels_response.get("ok"):
                    for channel in channels_response.get("channels", []):
                        channel_name = channel.get("name", "").lower()
                        if any(keyword in channel_name for keyword in ["gravity", "cargo", "general", "random"]):
                            target_channel = channel.get("id")
                            print(f"✅ Found channel: #{channel.get('name')}")
                            break
                
                if not target_channel:
                    print("❌ No accessible channel found")
                    return False
                
                # Send message
                blocks = self.create_rich_slack_blocks(optimization_data)
                response = app.client.chat_postMessage(
                    channel=target_channel,
                    blocks=blocks,
                    text=self.format_professional_message(optimization_data)
                )
                
                if response.get("ok"):
                    print("✅ Socket Mode notification sent successfully")
                    return True
                else:
                    print(f"❌ Socket Mode failed: {response.get('error', 'Unknown error')}")
                    return False
                    
            finally:
                signal.alarm(0)  # Cancel timeout
                
        except TimeoutError:
            print("⏰ Socket Mode timeout - using webhook fallback")
            return False
        except ImportError:
            print("⚠️ slack_bolt not available - using webhook fallback")
            return False
        except Exception as e:
            print(f"❌ Socket Mode error: {e}")
            return False
    
    def send_optimization_complete_notification(self, optimization_data):
        """Send professional optimization complete notification with fallback"""
        
        print("📱 SENDING PROFESSIONAL SLACK NOTIFICATION")
        print("=" * 50)
        
        # Try webhook first (most reliable)
        print("🔗 Attempting webhook notification...")
        webhook_success = self.send_webhook_notification(optimization_data)
        
        if webhook_success:
            print("🎉 Webhook notification delivered successfully!")
            
            # Also try Socket Mode as bonus (with timeout)
            print("🔗 Attempting Socket Mode as bonus...")
            socket_success = self.send_socket_mode_notification_safe(optimization_data)
            
            if socket_success:
                print("🎉 Socket Mode notification also delivered!")
            else:
                print("⚠️ Socket Mode failed, but webhook succeeded")
                
            return True
        else:
            # Webhook failed, try Socket Mode as backup
            print("⚠️ Webhook failed, trying Socket Mode backup...")
            socket_success = self.send_socket_mode_notification_safe(optimization_data)
            
            if socket_success:
                print("🎉 Socket Mode backup notification delivered!")
                return True
            else:
                print("❌ Both notification methods failed")
                return False

def test_notifications():
    """Test the notification system"""
    print("🧪 TESTING PROFESSIONAL NOTIFICATIONS")
    print("=" * 50)
    
    notifier = OptiGenixSlackNotifierFixed()
    
    test_data = {
        'volume_utilization': 87.3,
        'items_packed': 15,
        'total_weight': 523.7,
        'remaining_volume': 1.8,
        'user_name': 'Test Engineer',
        'algorithm_used': 'Genetic Algorithm'
    }
    
    success = notifier.send_optimization_complete_notification(test_data)
    
    if success:
        print("\n🎉 SUCCESS! Professional notifications working!")
        print(f"📱 Mobile access: https://{notifier.local_ip}:{notifier.https_port}/optimize")
    else:
        print("\n❌ FAILED! Check your Slack configuration")
        
    return success

if __name__ == "__main__":
    test_notifications()
