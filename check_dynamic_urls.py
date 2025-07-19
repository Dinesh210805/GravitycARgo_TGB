#!/usr/bin/env python3
"""
🔗 Dynamic Slack URL Checker
=============================
Check current URLs and get update instructions
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*50}")
    print(f"🔗 {title}")
    print(f"{'='*50}")

def check_flask_server():
    """Check if Flask server is running"""
    try:
        response = requests.get("http://localhost:5000/", timeout=3)
        return response.status_code == 200
    except:
        return False

def get_current_urls():
    """Get current dynamic URLs from Flask app"""
    try:
        response = requests.get("http://localhost:5000/slack/urls", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"❌ Error getting URLs: {e}")
        return None

def show_update_instructions(url_data):
    """Show instructions for updating Slack app"""
    print_header("SLACK APP UPDATE INSTRUCTIONS")
    
    urls = url_data.get('urls', {})
    instructions = url_data.get('instructions', {})
    ngrok_info = url_data.get('ngrok', {})
    
    print(f"🌐 Current Base URL: {urls.get('base_url')}")
    print(f"⚡ Slack Commands URL: {urls.get('slack_commands')}")
    print(f"📱 Mobile Ready: {'✅ Yes' if ngrok_info.get('ready_for_mobile') else '❌ No (localhost only)'}")
    
    if ngrok_info.get('active'):
        print(f"\n🎉 ngrok is active! Your app is mobile-ready!")
    else:
        print(f"\n⚠️  Running on localhost only - not accessible from mobile")
        print(f"   💡 Run 'python start_dynamic_slack.py' for mobile support")
    
    print(f"\n📋 UPDATE THESE SLACK COMMANDS:")
    print(f"🔗 Go to: {instructions.get('slack_app_url')}")
    
    for cmd in instructions.get('commands_to_update', []):
        print(f"   • {cmd['command']} → {cmd['new_url']}")

def main():
    """Main function"""
    print_header("DYNAMIC SLACK URL CHECKER")
    
    # Check if Flask is running
    if not check_flask_server():
        print("❌ Flask server not running!")
        print("   Start with: python app_modular.py")
        print("   Or use: python start_dynamic_slack.py (for auto-ngrok)")
        return
    
    print("✅ Flask server is running")
    
    # Get current URLs
    url_data = get_current_urls()
    
    if url_data:
        show_update_instructions(url_data)
        
        # Save URLs for easy reference
        print(f"\n💾 Quick Reference:")
        print(f"Command URL: {url_data['urls']['slack_commands']}")
        
        # Show copy-paste command for easy use
        command_url = url_data['urls']['slack_commands']
        print(f"\n📋 COPY THIS URL FOR SLACK COMMANDS:")
        print(f"   {command_url}")
        
    else:
        print("❌ Could not get dynamic URLs from Flask app")

if __name__ == "__main__":
    main()
