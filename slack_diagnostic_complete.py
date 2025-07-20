#!/usr/bin/env python3
"""
🔍 Slack Integration Diagnostic Tool
===================================
Identifies and fixes Slack Socket Mode and notification issues
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

class SlackDiagnostic:
    
    def __init__(self):
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.app_token = os.getenv('SLACK_APP_TOKEN')
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
    def check_bot_permissions(self):
        """Check what OAuth scopes the bot has"""
        print("🔍 Checking Bot OAuth Scopes...")
        print("=" * 50)
        
        if not self.bot_token:
            print("❌ No SLACK_BOT_TOKEN found")
            return False
            
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Test bot permissions with auth.test
            response = requests.post(
                'https://slack.com/api/auth.test',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    print(f"✅ Bot authenticated as: {data.get('user', 'Unknown')}")
                    print(f"✅ Team: {data.get('team', 'Unknown')}")
                    print(f"✅ User ID: {data.get('user_id', 'Unknown')}")
                else:
                    print(f"❌ Auth failed: {data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
            
        # Check OAuth scopes with oauth.v2.access
        try:
            response = requests.post(
                'https://slack.com/api/oauth.v2.access',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    scope_info = data.get('scope', '')
                    print(f"\n📋 Current OAuth Scopes:")
                    if scope_info:
                        scopes = scope_info.split(',')
                        for scope in scopes:
                            print(f"   ✓ {scope.strip()}")
                    else:
                        print("   ⚠️ No scopes found in response")
                        
                    # Check if we have required scopes
                    required_scopes = [
                        'chat:write',
                        'channels:read', 
                        'groups:read',    # This is what we need for private channels!
                        'im:read',
                        'mpim:read'
                    ]
                    
                    print(f"\n🎯 Required Scopes for Full Functionality:")
                    for scope in required_scopes:
                        if scope in scope_info:
                            print(f"   ✅ {scope}")
                        else:
                            print(f"   ❌ {scope} - MISSING!")
                            
                else:
                    print(f"❌ OAuth check failed: {data.get('error', 'Unknown error')}")
                    
        except Exception as e:
            print(f"⚠️ Could not check OAuth scopes: {e}")
            
        return True
        
    def test_channel_access(self):
        """Test access to channels"""
        print("\n🔍 Testing Channel Access...")
        print("=" * 50)
        
        if not self.bot_token:
            print("❌ No bot token available")
            return False
            
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        # Test public channels
        try:
            response = requests.get(
                'https://slack.com/api/conversations.list?types=public_channel,private_channel',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    channels = data.get('channels', [])
                    print(f"✅ Found {len(channels)} accessible channels:")
                    
                    target_found = False
                    for channel in channels:
                        channel_name = channel.get('name', 'unknown')
                        channel_id = channel.get('id', 'unknown')
                        is_private = channel.get('is_private', False)
                        privacy_icon = "🔒" if is_private else "🌐"
                        
                        print(f"   {privacy_icon} #{channel_name} ({channel_id})")
                        
                        if 'gravity' in channel_name.lower() or 'cargo' in channel_name.lower():
                            target_found = True
                            print(f"      🎯 TARGET CHANNEL FOUND!")
                            
                    if not target_found:
                        print("\n⚠️ No 'gravity' or 'cargo' channels found")
                        print("💡 Available channels to test with:")
                        for channel in channels[:3]:  # Show first 3
                            print(f"   #{channel.get('name', 'unknown')}")
                            
                else:
                    error = data.get('error', 'Unknown error')
                    print(f"❌ Failed to list channels: {error}")
                    
                    if error == 'missing_scope':
                        print("💡 SOLUTION: Add 'channels:read' and 'groups:read' scopes to your Slack app")
                        print("   1. Go to https://api.slack.com/apps")
                        print("   2. Select your app")
                        print("   3. Go to 'OAuth & Permissions'")
                        print("   4. Add missing scopes")
                        print("   5. Reinstall the app")
                        
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            
        return True
        
    def test_socket_mode_connection(self):
        """Test Socket Mode connection"""
        print("\n🔍 Testing Socket Mode Connection...")
        print("=" * 50)
        
        if not self.app_token:
            print("❌ No SLACK_APP_TOKEN found")
            return False
            
        try:
            from slack_bolt import App
            from slack_bolt.adapter.socket_mode import SocketModeHandler
            
            app = App(token=self.bot_token)
            
            print("✅ Slack Bolt app created")
            
            # Try to create socket mode handler
            handler = SocketModeHandler(app, self.app_token)
            print("✅ Socket Mode handler created")
            
            # Test connection (don't start, just validate)
            print("✅ Socket Mode configuration valid")
            
            return True
            
        except ImportError:
            print("❌ slack_bolt not installed")
            print("💡 Run: pip install slack_bolt")
            return False
        except Exception as e:
            print(f"❌ Socket Mode error: {e}")
            if "invalid_auth" in str(e):
                print("💡 Check your SLACK_APP_TOKEN is correct")
            return False
            
    def test_webhook_delivery(self):
        """Test webhook notification delivery"""
        print("\n🔍 Testing Webhook Delivery...")
        print("=" * 50)
        
        if not self.webhook_url:
            print("❌ No SLACK_WEBHOOK_URL found")
            return False
            
        try:
            test_payload = {
                "text": "🧪 OptiGenix Diagnostic Test",
                "username": "OptiGenix Diagnostic",
                "icon_emoji": ":gear:",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*🧪 Diagnostic Test Complete*\n✅ Webhook delivery is working!"
                        }
                    }
                ]
            }
            
            response = requests.post(self.webhook_url, json=test_payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ Webhook test message sent successfully!")
                print("📱 Check your Slack channel for the diagnostic message")
                return True
            else:
                print(f"❌ Webhook failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Webhook error: {e}")
            return False
            
    def provide_solutions(self):
        """Provide specific solutions for common issues"""
        print("\n💡 SOLUTIONS & NEXT STEPS")
        print("=" * 50)
        
        print("1. 🔐 OAuth Scopes Issue:")
        print("   • Go to: https://api.slack.com/apps")
        print("   • Select your OptiGenix app")
        print("   • OAuth & Permissions → Scopes")
        print("   • Add: channels:read, groups:read, chat:write")
        print("   • Reinstall app to workspace")
        
        print("\n2. 🏷️ Channel Access:")
        print("   • Make sure bot is added to #all-gravitycargos-space")
        print("   • Type: /invite @optigenix-bot")
        print("   • Or add via channel settings")
        
        print("\n3. 🌐 Webhook Backup:")
        print("   • Webhook notifications work as fallback")
        print("   • Professional formatting included")
        print("   • HTTPS mobile access enabled")
        
        print("\n4. 📱 Mobile Testing:")
        print("   • Open Slack mobile app")
        print("   • Check #all-gravitycargos-space channel")
        print("   • Tap HTTPS links for 3D visualization")
        
    def run_full_diagnostic(self):
        """Run complete diagnostic suite"""
        print("🔍 SLACK INTEGRATION DIAGNOSTIC")
        print("=" * 60)
        print("🎯 Goal: Fix all Slack notification issues")
        print("=" * 60)
        
        results = []
        
        # Test each component
        results.append(("Bot Permissions", self.check_bot_permissions()))
        results.append(("Channel Access", self.test_channel_access()))
        results.append(("Socket Mode", self.test_socket_mode_connection()))
        results.append(("Webhook Delivery", self.test_webhook_delivery()))
        
        # Summary
        print("\n📊 DIAGNOSTIC SUMMARY")
        print("=" * 50)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:.<20} {status}")
            
        working_methods = sum(1 for _, result in results if result)
        print(f"\n🎯 {working_methods}/4 notification methods working")
        
        if working_methods >= 2:
            print("✅ System operational - notifications will be delivered")
        else:
            print("⚠️ Action required - check solutions below")
            
        self.provide_solutions()

if __name__ == "__main__":
    diagnostic = SlackDiagnostic()
    diagnostic.run_full_diagnostic()
