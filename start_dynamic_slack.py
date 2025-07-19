#!/usr/bin/env python3
"""
🚀 Dynamic Slack Integration - AUTO UPDATER
===========================================
Automatically starts Flask + ngrok and provides update URLs
"""

import os
import subprocess
import time
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import requests
import json
import threading
from dotenv import load_dotenv

load_dotenv()

class NgrokManager:
    """Manages ngrok tunnel automatically"""
    
    def __init__(self):
        self.ngrok_process = None
        self.public_url = None
        self.is_running = False
        
    def start_ngrok(self, port=5000):
        """Start ngrok tunnel and get public URL"""
        print("🌐 Starting ngrok tunnel...")
        
        try:
            # Start ngrok in background
            self.ngrok_process = subprocess.Popen(
                ['ngrok', 'http', str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
            
            # Wait for ngrok to start
            time.sleep(3)
            
            # Get ngrok URL from API
            self.public_url = self._get_ngrok_url()
            
            if self.public_url:
                print(f"✅ ngrok tunnel started: {self.public_url}")
                self.is_running = True
                return self.public_url
            else:
                print("❌ Failed to get ngrok URL")
                return None
                
        except Exception as e:
            print(f"❌ Failed to start ngrok: {e}")
            return None
    
    def _get_ngrok_url(self):
        """Get public URL from ngrok API"""
        try:
            # ngrok exposes API on localhost:4040
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            if response.status_code == 200:
                tunnels = response.json()
                for tunnel in tunnels.get('tunnels', []):
                    if tunnel.get('proto') == 'https':
                        return tunnel.get('public_url')
            return None
        except Exception as e:
            print(f"Warning: Could not get ngrok URL from API: {e}")
            return None
    
    def stop_ngrok(self):
        """Stop ngrok tunnel"""
        if self.ngrok_process:
            self.ngrok_process.terminate()
            self.ngrok_process = None
            self.is_running = False
            print("🔴 ngrok tunnel stopped")
    
    def get_slack_command_url(self):
        """Get the URL for Slack commands"""
        if self.public_url:
            return f"{self.public_url}/slack/commands"
        return "http://localhost:5000/slack/commands"

class SlackAppUpdater:
    """Updates Slack app URLs dynamically"""
    
    def __init__(self):
        self.app_id = "A096HEE7TGD"
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
        
    def update_slash_commands(self, new_url):
        """Update slash command URLs in Slack app"""
        print(f"🔧 Updating Slack app URLs to: {new_url}")
        
        # Note: Slack doesn't provide API to update slash commands programmatically
        # This would require manual update, but we can provide instructions
        self._show_update_instructions(new_url)
    
    def _show_update_instructions(self, new_url):
        """Show instructions for updating Slack app URLs"""
        print("\n📋 SLACK APP UPDATE REQUIRED:")
        print("=" * 50)
        print(f"🔗 Go to: https://api.slack.com/apps/{self.app_id}/slash-commands")
        print(f"📝 Update Request URLs to: {new_url}")
        print("   • /optigenix-status")
        print("   • /optigenix-optimize")
        print("💾 Click 'Save' for each command")

def start_with_ngrok():
    """Start Flask app with automatic ngrok tunnel"""
    
    # Initialize managers
    ngrok = NgrokManager()
    slack_updater = SlackAppUpdater()
    
    print("🚀 OPTIGENIX - AUTO-START WITH NGROK")
    print("=" * 50)
    
    # Start ngrok tunnel
    public_url = ngrok.start_ngrok(5000)
    
    if public_url:
        command_url = ngrok.get_slack_command_url()
        
        # Show current configuration
        print(f"\n✅ DYNAMIC URLS READY:")
        print(f"🌐 Public URL: {public_url}")
        print(f"⚡ Slack Commands: {command_url}")
        print(f"📱 Mobile Ready: Yes")
        
        # Update Slack app (show instructions)
        slack_updater.update_slash_commands(command_url)
        
        # Save URLs to environment for Flask app
        os.environ['NGROK_PUBLIC_URL'] = public_url
        os.environ['DYNAMIC_SLACK_URL'] = command_url
        
        print(f"\n🎯 READY FOR DEMO!")
        print(f"📱 Test commands in Slack mobile app")
        print(f"⚠️  Keep this terminal open during demo")
        
        # Now start Flask app
        print(f"\n🚀 Starting Flask application...")
        start_flask_app()
        
    else:
        print("❌ Failed to start ngrok. Starting in local mode...")
        start_flask_app()

def start_flask_app():
    """Start the Flask application"""
    try:
        from app_modular import create_app, create_socketio
        
        app = create_app()
        socketio = create_socketio(app)
        
        print("🚛 OptiGenix Flask app starting...")
        socketio.run(app, 
                    host='0.0.0.0',  # Allow external connections
                    port=5000, 
                    debug=False)
                    
    except KeyboardInterrupt:
        print("\n🔴 Shutting down...")
        # Cleanup will be handled by atexit
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")

def cleanup():
    """Cleanup function"""
    print("🧹 Cleaning up...")

if __name__ == "__main__":
    import atexit
    atexit.register(cleanup)
    
    start_with_ngrok()
