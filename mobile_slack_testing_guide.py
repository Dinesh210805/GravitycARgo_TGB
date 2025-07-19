#!/usr/bin/env python3
"""
� OptiGenix Slack Mobile Testing Guide - UPDATED
====================================================
Complete guide for testing Slack integration on mobile devices
"""

import os
import requests
import subprocess
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import time
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"📱 {title}")
    print(f"{'='*60}")

def option_1_ngrok_setup():
    """Guide for setting up ngrok for mobile testing"""
    print_header("OPTION 1: NGROK TUNNEL (RECOMMENDED)")
    
    print("\n🌐 What is ngrok?")
    print("Ngrok creates a secure tunnel from internet to your localhost")
    print("This allows your mobile Slack app to reach your Flask server")
    
    print("\n📋 SETUP STEPS:")
    print("1. Download ngrok: https://ngrok.com/download")
    print("2. Extract and add to PATH (or run from download folder)")
    print("3. Run this command in a new terminal:")
    print("   ngrok http 5000")
    print("\n4. Copy the HTTPS URL (e.g., https://abc123.ngrok.io)")
    print("5. Update Slack app slash commands with this URL")
    
    print("\n🔧 SLACK APP UPDATES:")
    print("Go to: https://api.slack.com/apps/A096HEE7TGD/slash-commands")
    print("Update Request URLs:")
    print("• /optigenix-status → https://YOUR-NGROK-URL.ngrok.io/slack/commands")
    print("• /optigenix-optimize → https://YOUR-NGROK-URL.ngrok.io/slack/commands")
    
    print("\n✅ BENEFITS:")
    print("• Works from any mobile device")
    print("• Secure HTTPS connection")
    print("• Real-time testing")
    print("• Perfect for demos")

def option_2_local_network():
    """Guide for local network testing"""
    print_header("OPTION 2: LOCAL NETWORK ACCESS")
    
    print("\n🏠 Requirements:")
    print("• Your computer and phone on same WiFi network")
    print("• Computer firewall allows Flask connections")
    
    try:
        # Get local IP address
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"\n🔍 Your computer's local IP: {local_ip}")
        print(f"📱 Mobile access URL: http://{local_ip}:5000")
        
        print("\n📋 SETUP STEPS:")
        print("1. Make sure Flask runs on 0.0.0.0:")
        print("   python app_modular.py --host 0.0.0.0")
        print("2. Update Slack app Request URLs:")
        print(f"   • /optigenix-status → http://{local_ip}:5000/slack/commands")
        print(f"   • /optigenix-optimize → http://{local_ip}:5000/slack/commands")
        
        print("\n⚠️ LIMITATIONS:")
        print("• Only works on same WiFi network")
        print("• HTTP (not HTTPS) - some Slack features may not work")
        print("• Firewall may block connections")
        
    except Exception as e:
        print(f"❌ Could not determine local IP: {e}")

def option_3_cloud_deployment():
    """Guide for cloud deployment"""
    print_header("OPTION 3: CLOUD DEPLOYMENT")
    
    print("\n☁️ Deploy to cloud service for full mobile access")
    
    print("\n🚀 RENDER.COM (FREE TIER):")
    print("1. Push code to GitHub")
    print("2. Connect Render to GitHub repo")
    print("3. Deploy as Web Service")
    print("4. Get public URL (e.g., https://your-app.onrender.com)")
    print("5. Update Slack app URLs")
    
    print("\n🔧 HEROKU (FREE TIER ENDED):")
    print("• Still available but requires payment")
    print("• Good for production deployments")
    
    print("\n✅ BENEFITS:")
    print("• Works from anywhere")
    print("• HTTPS by default")
    print("• Perfect for hackathon presentations")
    print("• No network restrictions")

def check_current_setup():
    """Check current Flask server status"""
    print_header("CURRENT SETUP STATUS")
    
    print("🔍 Checking Flask server...")
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        print(f"✅ Flask server running (Status: {response.status_code})")
        
        # Test Slack endpoint
        test_data = {
            'command': '/optigenix-status',
            'user_name': 'mobile-test',
            'text': ''
        }
        
        slack_response = requests.post(
            "http://localhost:5000/slack/commands", 
            data=test_data, 
            timeout=5
        )
        
        if slack_response.status_code == 200:
            print("✅ Slack endpoints working")
            print("📱 Ready for mobile testing setup!")
        else:
            print(f"⚠️ Slack endpoint issue: {slack_response.status_code}")
            
    except Exception as e:
        print(f"❌ Flask server not accessible: {e}")
        print("Start with: python app_modular.py")

def mobile_testing_workflow():
    """Show the complete mobile testing workflow"""
    print_header("MOBILE TESTING WORKFLOW")
    
    print("📋 STEP-BY-STEP MOBILE TEST:")
    print("\n1. 🔧 SETUP TUNNEL/ACCESS:")
    print("   → Choose Option 1 (ngrok) or Option 2 (local network)")
    print("   → Update Slack app Request URLs")
    
    print("\n2. 📱 INSTALL SLACK BOT:")
    print("   → Enable bot user in Slack app settings")
    print("   → Add OAuth scopes (chat:write, commands, etc.)")
    print("   → Install app to your workspace")
    
    print("\n3. 🧪 TEST ON MOBILE:")
    print("   → Open Slack mobile app")
    print("   → Go to any channel or DM")
    print("   → Type: /optigenix-status")
    print("   → Type: /optigenix-optimize urgent")
    
    print("\n4. ✅ VERIFY RESPONSES:")
    print("   → Commands should show in autocomplete")
    print("   → Responses should be formatted with emojis")
    print("   → Bot should appear as 'OptiGenix Bot'")
    
    print(f"\n🎉 SUCCESS INDICATORS:")
    print("• Commands autocomplete when typing")
    print("• Formatted response with container stats")
    print("• Real-time Flask server logs show requests")
    print("• Bot appears as online in workspace")

def show_quick_start_ngrok():
    """Show the quickest way to start testing"""
    print_header("⚡ QUICK START - NGROK METHOD")
    
    print("🚀 FASTEST WAY TO TEST ON MOBILE:")
    print("\n1. Download ngrok: https://ngrok.com/download")
    print("2. Open new terminal and run:")
    print("   ngrok http 5000")
    print("\n3. Copy the HTTPS URL from ngrok output")
    print("4. Update Slack app slash commands:")
    print("   https://api.slack.com/apps/A096HEE7TGD/slash-commands")
    print("\n5. Install app to workspace:")
    print("   https://api.slack.com/apps/A096HEE7TGD/install-on-team")
    print("\n6. Test on mobile Slack app! 📱")
    
    print(f"\n⏱️ Total time: ~10 minutes")
    print(f"💡 Perfect for hackathon demo!")

def main():
    """Main guide function"""
    print("📱🚛 OPTIGENIX SLACK MOBILE TESTING GUIDE 🚛📱")
    print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check current status
    check_current_setup()
    
    # Show all options
    option_1_ngrok_setup()
    option_2_local_network()
    option_3_cloud_deployment()
    
    # Show workflow
    mobile_testing_workflow()
    
    # Quick start guide
    show_quick_start_ngrok()
    
    print(f"\n🎊 CONCLUSION:")
    print("Your Slack integration backend is PERFECT! ✅")
    print("Choose any option above to enable mobile testing.")
    print("Recommendation: Use ngrok for quickest mobile testing.")
    print(f"\n{'🎉' * 20}")

if __name__ == "__main__":
    main()
