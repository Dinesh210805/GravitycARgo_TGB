#!/usr/bin/env python3
"""
🚀 OptiGenix Slack Bot Setup Checker
====================================
Quick checker for Socket Mode integration in app_modular.py
"""

import os
from dotenv import load_dotenv

def check_socket_mode_setup():
    """Check if Socket Mode is properly configured"""
    load_dotenv()
    
    print("🔍 Checking Socket Mode Configuration...")
    print("=" * 50)
    
    # Check required tokens
    tokens = {
        "SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN"),
        "SLACK_APP_TOKEN": os.getenv("SLACK_APP_TOKEN"), 
        "SLACK_SIGNING_SECRET": os.getenv("SLACK_SIGNING_SECRET")
    }
    
    missing = []
    configured = []
    
    for name, value in tokens.items():
        if not value or "YOUR-" in value.upper():
            missing.append(name)
            print(f"❌ {name}: Missing or placeholder")
        else:
            configured.append(name)
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {name}: {masked}")
    
    # Check slack-bolt package
    try:
        import slack_bolt
        print("✅ slack-bolt package: Installed")
        bolt_available = True
    except ImportError:
        print("❌ slack-bolt package: Not installed")
        bolt_available = False
    
    print("\n📋 STATUS SUMMARY:")
    print("=" * 50)
    
    if len(configured) == 3 and bolt_available:
        print("🎉 PERFECT! Socket Mode is ready!")
        print("✅ All tokens configured")
        print("✅ Package installed")
        print("\n🚀 RUN YOUR APP:")
        print("   python app_modular.py")
        print("\n💡 RESULT:")
        print("   • 100% automated Slack integration")
        print("   • No manual URL updates needed")
        print("   • Works instantly on mobile")
        return True
        
    elif len(configured) > 0:
        print("⚠️ PARTIAL SETUP - Almost there!")
        if missing:
            print(f"❌ Missing: {', '.join(missing)}")
        if not bolt_available:
            print("❌ Missing: slack-bolt package")
        print("\n📋 NEXT STEPS:")
        print_setup_instructions(missing, not bolt_available)
        return False
        
    else:
        print("❌ NOT CONFIGURED")
        print("📋 Socket Mode tokens not found")
        print("\n🔧 SETUP REQUIRED:")
        print_setup_instructions(missing, not bolt_available)
        return False

def print_setup_instructions(missing_tokens, need_package):
    """Print setup instructions"""
    
    if need_package:
        print("\n1️⃣ INSTALL PACKAGE:")
        print("   pip install slack-bolt")
    
    if "SLACK_APP_TOKEN" in missing_tokens:
        print("\n2️⃣ GET APP-LEVEL TOKEN:")
        print("   • Go to: https://api.slack.com/apps/A096HEE7TGD/general")
        print("   • Find 'App-Level Tokens' section")
        print("   • Click 'Generate Token and Scopes'")
        print("   • Name: 'OptiGenix Socket Mode'")
        print("   • Add scope: 'connections:write'")
        print("   • Copy the xapp-... token")
    
    if missing_tokens:
        print("\n3️⃣ UPDATE .ENV FILE:")
        for token in missing_tokens:
            if token == "SLACK_APP_TOKEN":
                print(f"   {token}=xapp-your-generated-token-here")
            else:
                print(f"   {token}=your-existing-token")
    
    print("\n4️⃣ ENABLE SOCKET MODE:")
    print("   • Go to: https://api.slack.com/apps/A096HEE7TGD/socket-mode")
    print("   • Toggle 'Enable Socket Mode' to ON")
    print("   • Save Changes")
    
    print("\n5️⃣ TEST:")
    print("   python app_modular.py")

# Legacy function for compatibility
def check_slack_app_config():
    """Legacy function - redirects to Socket Mode check"""
    return check_socket_mode_setup()

def main():
    """Main function"""
    print("🚛 OptiGenix - Socket Mode Setup Checker")
    print("=" * 50)
    
    is_ready = check_socket_mode_setup()
    
    if is_ready:
        print("\n🎯 YOUR APP IS READY FOR 100% AUTOMATION!")
    else:
        print("\n⚡ Complete setup for perfect automation!")
    
    return 0 if is_ready else 1

if __name__ == "__main__":
    exit(main())
    print("🔍 SLACK BOT CONFIGURATION CHECKER")
    print("=" * 50)
    
    app_id = "A096HEE7TGD"
    print(f"📱 Checking Slack App: {app_id}")
    print(f"🔗 App Dashboard: https://api.slack.com/apps/{app_id}")
    
    print("\n📋 CONFIGURATION CHECKLIST:")
    print("=" * 30)
    
    checklist = [
        "✅ 1. Enable Bot User in 'App Home' → 'Your App's Presence in Slack'",
        "✅ 2. Set Display Name: 'OptiGenix Bot'", 
        "✅ 3. Set Default Username: 'optigenix'",
        "✅ 4. Toggle 'Always Show My Bot as Online' to ON",
        "✅ 5. Add OAuth Scopes in 'OAuth & Permissions':",
        "   • chat:write",
        "   • commands", 
        "   • incoming-webhook",
        "   • app_mentions:read",
        "   • channels:read",
        "✅ 6. Create Slash Commands:",
        "   • /optigenix-status",
        "   • /optigenix-optimize",
        "✅ 7. Install App to Workspace",
        "✅ 8. Copy Bot Token (xoxb-...)"
    ]
    
    for item in checklist:
        print(item)
    
    print("\n🚨 COMMON ISSUES & FIXES:")
    print("=" * 30)
    
    issues = [
        "❌ 'No bot user to install' → Enable bot in App Home",
        "❌ 'Permission denied' → Add required OAuth scopes first",
        "❌ 'Commands not working' → Set correct Request URLs",
        "❌ 'Bot not responding' → Check bot token in .env file"
    ]
    
    for issue in issues:
        print(issue)
    
    print("\n🔧 NEXT STEPS:")
    print("=" * 15)
    print("1. Go to: https://api.slack.com/apps/A096HEE7TGD/general")
    print("2. Navigate to 'App Home' in sidebar")
    print("3. Scroll to 'Your App's Presence in Slack'")
    print("4. Toggle 'Always Show My Bot as Online' to ON")
    print("5. Fill in Display Name and Username")
    print("6. Save Changes")
    print("7. Go to 'OAuth & Permissions' and add scopes")
    print("8. Try installing to workspace again")

def check_environment_vars():
    """Check if environment variables are set"""
    print("\n🔧 ENVIRONMENT VARIABLES STATUS:")
    print("=" * 35)
    
    env_vars = {
        'SLACK_CLIENT_SECRET': os.getenv('SLACK_CLIENT_SECRET'),
        'SLACK_SIGNING_SECRET': os.getenv('SLACK_SIGNING_SECRET'), 
        'SLACK_BOT_TOKEN': os.getenv('SLACK_BOT_TOKEN'),
        'SLACK_WEBHOOK_URL': os.getenv('SLACK_WEBHOOK_URL')
    }
    
    for var, value in env_vars.items():
        if value and value != "xoxb-paste-your-actual-bot-token-here":
            status = "✅ Set"
            preview = value[:10] + "..." if len(value) > 10 else value
        else:
            status = "❌ Missing" 
            preview = "Not configured"
        
        print(f"{var}: {status} ({preview})")

def test_local_server():
    """Test if local Flask server is running"""
    print("\n🌐 LOCAL SERVER STATUS:")
    print("=" * 25)
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Flask server is running on localhost:5000")
            print("✅ Ready for Slack command testing")
        else:
            print("⚠️ Flask server responding but with issues")
    except Exception as e:
        print("❌ Flask server not running")
        print("   Start with: python app_modular.py")

if __name__ == "__main__":
    check_slack_app_config()
    check_environment_vars()
    test_local_server()
    
    print("\n🎯 QUICK FIX SUMMARY:")
    print("=" * 20)
    print("1. Enable bot user in Slack app settings")
    print("2. Add OAuth scopes before installing")
    print("3. Install app to get bot token")
    print("4. Update .env with bot token")
    print("5. Test with: python test_slack_integration.py")
