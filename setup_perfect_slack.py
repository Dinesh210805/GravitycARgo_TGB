#!/usr/bin/env python3
"""
🚀 OptiGenix - Perfect Slack Automation Setup
==============================================
One-time setup script for 100% automated Slack integration
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "slack-bolt", "--quiet"])
        print("✅ slack-bolt installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_environment():
    """Check if all required environment variables are set"""
    load_dotenv()
    
    required_vars = {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_APP_TOKEN": "xapp-...",
        "SLACK_SIGNING_SECRET": "your-signing-secret"
    }
    
    missing_vars = []
    
    print("\n🔍 Checking environment variables...")
    for var, example in required_vars.items():
        value = os.getenv(var)
        if not value or "YOUR-" in value.upper():
            missing_vars.append((var, example))
            print(f"❌ {var}: Missing or placeholder")
        else:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {masked_value}")
    
    return missing_vars

def show_setup_instructions(missing_vars):
    """Show setup instructions for missing variables"""
    if not missing_vars:
        return
    
    print(f"\n📋 SETUP REQUIRED - Missing {len(missing_vars)} variables:")
    print("=" * 60)
    
    for var, example in missing_vars:
        if var == "SLACK_APP_TOKEN":
            print(f"\n🔗 {var}:")
            print(f"   1. Go to: https://api.slack.com/apps/A096HEE7TGD/general")
            print(f"   2. Scroll to 'App-Level Tokens'")
            print(f"   3. Click 'Generate Token and Scopes'")
            print(f"   4. Name: 'OptiGenix Socket Mode'")
            print(f"   5. Add scope: 'connections:write'")
            print(f"   6. Click 'Generate'")
            print(f"   7. Copy the {example} token")
            print(f"   8. Add to .env: {var}=your-token-here")
        else:
            print(f"\n✅ {var}: Already configured")
    
    print(f"\n🔧 ENABLE SOCKET MODE:")
    print(f"   1. Go to: https://api.slack.com/apps/A096HEE7TGD/socket-mode")
    print(f"   2. Toggle 'Enable Socket Mode' to ON")
    print(f"   3. Save Changes")

def test_socket_mode():
    """Test if Socket Mode can be initialized"""
    try:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
        
        load_dotenv()
        
        app = App(
            token=os.getenv("SLACK_BOT_TOKEN"),
            signing_secret=os.getenv("SLACK_SIGNING_SECRET")
        )
        
        app_token = os.getenv("SLACK_APP_TOKEN")
        
        if not app_token or "YOUR-" in app_token.upper():
            raise ValueError("SLACK_APP_TOKEN not properly configured")
        
        print("✅ Socket Mode configuration valid!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 OptiGenix - Perfect Slack Automation Setup")
    print("=" * 50)
    
    # Step 1: Install packages
    if not install_requirements():
        return 1
    
    # Step 2: Check environment
    missing_vars = check_environment()
    
    # Step 3: Show instructions if needed
    if missing_vars:
        show_setup_instructions(missing_vars)
        print(f"\n⚠️  Please complete setup and run this script again.")
        return 1
    
    # Step 4: Test configuration
    print(f"\n🧪 Testing Socket Mode configuration...")
    if not test_socket_mode():
        print(f"\n❌ Configuration test failed. Check your tokens.")
        return 1
    
    # Step 5: Success!
    print(f"\n🎉 SETUP COMPLETE!")
    print("=" * 50)
    print("✅ All requirements installed")
    print("✅ Environment variables configured")
    print("✅ Socket Mode ready")
    print(f"\n🚀 START YOUR 100% AUTOMATED SLACK BOT:")
    print("   python slack_socket_mode.py")
    print(f"\n💡 BENEFITS:")
    print("   • Zero manual URL updates")
    print("   • Works instantly on mobile")
    print("   • Real-time communication")
    print("   • Perfect for hackathon demos!")
    
    return 0

if __name__ == "__main__":
    exit(main())
