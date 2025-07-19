#!/usr/bin/env python3
"""
🚛 OptiGenix Slack Integration Testing Guide
=======================================================
Complete testing guide for Slack integration setup and verification
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🚛 {title}")
    print(f"{'='*60}")

def print_step(step_num, title):
    """Print a formatted step"""
    print(f"\n📋 STEP {step_num}: {title}")
    print("-" * 40)

def check_environment_variables():
    """Check if all required environment variables are set"""
    print_header("ENVIRONMENT VARIABLES CHECK")
    
    required_vars = [
        'SLACK_CLIENT_SECRET',
        'SLACK_SIGNING_SECRET', 
        'SLACK_BOT_TOKEN',
        'SLACK_WEBHOOK_URL'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * 20}...{value[-4:]}")
        else:
            print(f"❌ {var}: Not set")
            all_set = False
    
    return all_set

def test_flask_server():
    """Test if Flask server is running"""
    print_header("FLASK SERVER TEST")
    
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        print(f"✅ Flask server is running (Status: {response.status_code})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask server not running: {e}")
        print("   Start with: python app_modular.py")
        return False

def test_slack_endpoints():
    """Test Slack integration endpoints"""
    print_header("SLACK ENDPOINTS TEST")
    
    # Test data for slash commands
    test_data = {
        'token': 'test_token',
        'team_id': 'T096G508U0N',
        'team_domain': 'optigenix-workspace',
        'channel_id': 'C1234567890',
        'channel_name': 'general',
        'user_id': 'U1234567890',
        'user_name': 'test_user',
        'command': '/optigenix-status',
        'text': '',
        'response_url': 'https://hooks.slack.com/commands/1234567890/1234567890/test',
        'trigger_id': '1234567890.1234567890.test'
    }
    
    endpoints = [
        ('/slack/commands', 'POST', test_data),
        ('/slack/test', 'POST', test_data),  # Fixed: /slack/test expects POST
        ('/slack/oauth', 'GET', {'code': 'test_auth_code'})  # Fixed: OAuth needs code parameter
    ]
    
    results = []
    for endpoint, method, data in endpoints:
        try:
            url = f"http://localhost:5000{endpoint}"
            if method == 'POST':
                response = requests.post(url, data=data, timeout=5)
            else:
                response = requests.get(url, params=data, timeout=5)
            
            print(f"✅ {endpoint}: Status {response.status_code}")
            results.append(True)
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
            results.append(False)
    
    return all(results)

def test_slack_commands():
    """Test specific Slack commands"""
    print_header("SLACK COMMANDS TEST")
    
    commands = [
        {
            'command': '/optigenix-status',
            'text': '',
            'description': 'Check system status'
        },
        {
            'command': '/optigenix-optimize', 
            'text': 'urgent',
            'description': 'Start urgent optimization'
        }
    ]
    
    for cmd in commands:
        print(f"\n🔧 Testing {cmd['command']}...")
        
        test_data = {
            'token': 'test_token',
            'team_id': 'T096G508U0N',
            'team_domain': 'optigenix-workspace',
            'channel_id': 'C1234567890',
            'channel_name': 'general',
            'user_id': 'U1234567890',
            'user_name': 'test_user',
            'command': cmd['command'],
            'text': cmd['text'],
            'response_url': 'https://hooks.slack.com/commands/test',
            'trigger_id': '1234567890.1234567890.test'
        }
        
        try:
            response = requests.post(
                "http://localhost:5000/slack/commands", 
                data=test_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Command works: {cmd['description']}")
                print(f"   Response type: {result.get('response_type', 'N/A')}")
                # Show first 100 chars of response
                text = result.get('text', '')[:100]
                print(f"   Response preview: {text}...")
            else:
                print(f"❌ Command failed: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Command error: {e}")

def slack_app_configuration_guide():
    """Display Slack app configuration guide"""
    print_header("SLACK APP CONFIGURATION GUIDE")
    
    app_id = "A096HEE7TGD"
    
    print(f"🔗 Slack App Dashboard: https://api.slack.com/apps/{app_id}")
    print("\n📋 REQUIRED CONFIGURATIONS:")
    
    print("\n1. 🤖 ENABLE BOT USER:")
    print(f"   • Go to: https://api.slack.com/apps/{app_id}/app-home")
    print("   • Scroll to 'Your App's Presence in Slack'")
    print("   • Toggle 'Always Show My Bot as Online' to ON")
    print("   • Set Display Name: 'OptiGenix Bot'")
    print("   • Set Default Username: 'optigenix'")
    print("   • Click 'Save Changes'")
    
    print("\n2. 🔐 OAUTH SCOPES:")
    print(f"   • Go to: https://api.slack.com/apps/{app_id}/oauth")
    print("   • Add Bot Token Scopes:")
    print("     - chat:write")
    print("     - commands") 
    print("     - incoming-webhook")
    print("     - app_mentions:read")
    print("     - channels:read")
    
    print("\n3. ⚡ SLASH COMMANDS:")
    print(f"   • Go to: https://api.slack.com/apps/{app_id}/slash-commands")
    print("   • Create Command: /optigenix-status")
    print("     - Request URL: http://localhost:5000/slack/commands")
    print("     - Description: Check OptiGenix server status")
    print("   • Create Command: /optigenix-optimize")
    print("     - Request URL: http://localhost:5000/slack/commands")
    print("     - Description: Start container optimization")
    
    print("\n4. 🚀 INSTALL APP:")
    print(f"   • Go to: https://api.slack.com/apps/{app_id}/install-on-team")
    print("   • Click 'Install to Workspace'")
    print("   • Copy the Bot Token (starts with xoxb-)")
    print("   • Update SLACK_BOT_TOKEN in .env file")

def verify_installation():
    """Guide for verifying Slack app installation"""
    print_header("INSTALLATION VERIFICATION")
    
    print("After installing the app to your workspace:")
    print("\n1. 🔍 CHECK BOT IN SLACK:")
    print("   • Look for 'OptiGenix Bot' in your workspace")
    print("   • Bot should appear as online")
    
    print("\n2. 🧪 TEST COMMANDS IN SLACK:")
    print("   • Type: /optigenix-status")
    print("   • Type: /optigenix-optimize urgent")
    print("   • Commands should appear in autocomplete")
    
    print("\n3. 📊 VERIFY RESPONSES:")
    print("   • Commands should return formatted messages")
    print("   • Check for emojis and proper formatting")
    print("   • Response should be visible to the channel")

def troubleshooting_guide():
    """Common issues and solutions"""
    print_header("TROUBLESHOOTING GUIDE")
    
    issues = [
        {
            'issue': "❌ 'No bot user to install'",
            'solution': "Enable bot in App Home → 'Your App's Presence in Slack'"
        },
        {
            'issue': "❌ 'Permission denied'", 
            'solution': "Add required OAuth scopes before installing"
        },
        {
            'issue': "❌ 'Commands not appearing'",
            'solution': "Check slash commands configuration and Request URLs"
        },
        {
            'issue': "❌ 'Bot not responding'",
            'solution': "Verify bot token in .env and Flask server is running"
        },
        {
            'issue': "❌ 'Connection timeout'",
            'solution': "Ensure localhost:5000 is accessible and Flask is running"
        }
    ]
    
    for item in issues:
        print(f"\n{item['issue']}")
        print(f"   💡 Solution: {item['solution']}")

def run_complete_test():
    """Run complete integration test"""
    print_header("COMPLETE SLACK INTEGRATION TEST")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Environment variables
    print_step(1, "Environment Variables")
    env_ok = check_environment_variables()
    
    # Test 2: Flask server
    print_step(2, "Flask Server")
    server_ok = test_flask_server()
    
    # Test 3: Slack endpoints
    print_step(3, "Slack Endpoints")
    endpoints_ok = test_slack_endpoints() if server_ok else False
    
    # Test 4: Slack commands
    print_step(4, "Slack Commands")
    if server_ok:
        test_slack_commands()
    
    # Results summary
    print_header("TEST RESULTS SUMMARY")
    print(f"✅ Environment Variables: {'PASS' if env_ok else 'FAIL'}")
    print(f"✅ Flask Server: {'PASS' if server_ok else 'FAIL'}")
    print(f"✅ Slack Endpoints: {'PASS' if endpoints_ok else 'FAIL'}")
    
    if env_ok and server_ok and endpoints_ok:
        print(f"\n🎉 LOCAL INTEGRATION: ALL TESTS PASSED!")
        print(f"📋 Next: Configure Slack app and install to workspace")
    else:
        print(f"\n⚠️  SOME TESTS FAILED - Check issues above")
    
    # Show configuration guide
    slack_app_configuration_guide()
    verify_installation()
    troubleshooting_guide()

if __name__ == "__main__":
    run_complete_test()
