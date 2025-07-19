#!/usr/bin/env python3
"""
🚀 Quick Mobile Testing Setup
=============================
The fastest way to test Slack integration on mobile
"""

import subprocess
import sys
import time
import requests

def print_step(num, title, description):
    print(f"\n📋 STEP {num}: {title}")
    print("─" * 40)
    print(description)

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ ngrok not found")
    return False

def main():
    print("🚀 OPTIGENIX SLACK MOBILE SETUP")
    print("=" * 40)
    
    print_step(1, "Check Flask Server", 
               "Verifying your OptiGenix server is running...")
    
    try:
        response = requests.get("http://localhost:5000/", timeout=3)
        print(f"✅ Flask server running (Status: {response.status_code})")
    except:
        print("❌ Flask server not running!")
        print("   Run: python app_modular.py")
        return
    
    print_step(2, "Check ngrok", 
               "Checking if ngrok tunnel tool is available...")
    
    if not check_ngrok_installed():
        print("\n💡 INSTALL NGROK:")
        print("1. Go to: https://ngrok.com/download")
        print("2. Download for Windows")
        print("3. Extract ngrok.exe to your project folder")
        print("4. Run this script again")
        return
    
    print_step(3, "Start ngrok Tunnel", 
               "Creating secure tunnel to your Flask server...")
    
    print("🌐 Starting ngrok tunnel...")
    print("Run this command in a NEW terminal window:")
    print("   ngrok http 5000")
    print("\n⚠️ Keep that terminal window open!")
    print("📋 Copy the HTTPS URL from ngrok (e.g., https://abc123.ngrok.io)")
    
    print_step(4, "Update Slack App", 
               "Configure your Slack app for mobile access...")
    
    print("🔧 Go to Slack App Dashboard:")
    print("   https://api.slack.com/apps/A096HEE7TGD/slash-commands")
    print("\n📝 Update Request URLs:")
    print("   Replace 'http://localhost:5000' with your ngrok HTTPS URL")
    print("   • /optigenix-status → https://YOUR-NGROK-URL/slack/commands")
    print("   • /optigenix-optimize → https://YOUR-NGROK-URL/slack/commands")
    
    print_step(5, "Install Slack Bot", 
               "Enable bot features and install to workspace...")
    
    print("🤖 Enable Bot User:")
    print("   https://api.slack.com/apps/A096HEE7TGD/app-home")
    print("   → Toggle 'Always Show My Bot as Online' to ON")
    print("\n🔐 Add OAuth Scopes:")
    print("   https://api.slack.com/apps/A096HEE7TGD/oauth")
    print("   → Add: chat:write, commands, incoming-webhook")
    print("\n🚀 Install to Workspace:")
    print("   https://api.slack.com/apps/A096HEE7TGD/install-on-team")
    
    print_step(6, "Test on Mobile", 
               "Try your Slack commands on mobile app...")
    
    print("📱 Open Slack mobile app and test:")
    print("   • Type: /optigenix-status")
    print("   • Type: /optigenix-optimize urgent")
    print("\n✅ Expected Results:")
    print("   • Commands appear in autocomplete")
    print("   • Bot responds with formatted messages")
    print("   • Emojis and stats display correctly")
    
    print("\n🎉 SUCCESS! Your OptiGenix bot is mobile-ready!")
    print("Perfect for hackathon demos and team collaboration!")

if __name__ == "__main__":
    main()
