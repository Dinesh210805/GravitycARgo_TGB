#!/usr/bin/env python3
"""
🚀 OptiGenix Socket Mode Checker  
=================================
Check if integrated Socket Mode is ready
"""

import os
from dotenv import load_dotenv

def check_socket_mode_ready():
    """Check if Socket Mode is configured for app_modular.py"""
    load_dotenv()
    
    print("🔍 Socket Mode Configuration Check")
    print("=" * 40)
    
    # Check tokens
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    app_token = os.getenv("SLACK_APP_TOKEN") 
    signing_secret = os.getenv("SLACK_SIGNING_SECRET")
    
    print(f"✅ SLACK_BOT_TOKEN: {bot_token[:10] + '...' if bot_token else '❌ Missing'}")
    print(f"✅ SLACK_APP_TOKEN: {app_token[:10] + '...' if app_token else '❌ Missing'}")
    print(f"✅ SLACK_SIGNING_SECRET: {signing_secret[:10] + '...' if signing_secret else '❌ Missing'}")
    
    # Check package
    try:
        import slack_bolt
        print("✅ slack-bolt: Installed")
        package_ok = True
    except ImportError:
        print("❌ slack-bolt: Not installed")
        package_ok = False
    
    all_ready = all([bot_token, app_token, signing_secret, package_ok])
    
    print(f"\n📊 STATUS: {'🎉 READY' if all_ready else '⚠️ NEEDS SETUP'}")
    
    if all_ready:
        print("\n🚀 RUN COMMAND:")
        print("   python app_modular.py")
        print("\n✨ RESULT:")
        print("   • 100% automated Slack integration")
        print("   • No manual URL configuration")
        print("   • Instant mobile compatibility")
    else:
        print("\n🔧 SETUP NEEDED:")
        if not package_ok:
            print("   pip install slack-bolt")
        if not app_token:
            print("   • Get App-Level Token from Slack")
            print("   • https://api.slack.com/apps/A096HEE7TGD/general")
        print("   • Enable Socket Mode in Slack dashboard")
    
    return all_ready

if __name__ == "__main__":
    check_socket_mode_ready()
