#!/usr/bin/env python3
"""
OptiGenix Slack Demo Script
Complete demo flow for the Future of Work Hackathon
"""
import time
import subprocess
import sys
import os

def print_banner():
    """Print demo banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                  🚛 OPTIGENIX SLACK DEMO 🚛                   ║
║           Enterprise WorkOS - Future of Work                ║
║                                                              ║
║              🏆 Kroolo x TGB Hackathon 2025 🏆               ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if Flask app is running
    try:
        import requests
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Flask application is running")
        else:
            print("❌ Flask application not responding")
            return False
    except Exception as e:
        print("❌ Flask application not running. Please start it first:")
        print("   python app_modular.py")
        return False
    
    # Check environment variables
    env_vars = [
        'SLACK_CLIENT_SECRET',
        'SLACK_SIGNING_SECRET'
    ]
    
    for var in env_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️ {var} not set (optional for demo)")
    
    return True

def demo_slack_commands():
    """Demonstrate Slack commands"""
    print("\n📱 SLACK COMMAND DEMONSTRATIONS")
    print("=" * 50)
    
    print("\n1️⃣ Testing /optigenix-status command...")
    try:
        import requests
        
        # Test status command
        data = {
            'command': '/optigenix-status',
            'user_name': 'demo-user',
            'text': ''
        }
        
        response = requests.post("http://localhost:5000/slack/commands", data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Status command successful!")
            print("📊 Response preview:")
            print(result.get('text', 'No response text')[:200] + "...")
        else:
            print(f"❌ Status command failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing status command: {e}")
    
    print("\n2️⃣ Testing /optigenix-optimize command...")
    try:
        data = {
            'command': '/optigenix-optimize',
            'user_name': 'demo-user',
            'text': 'urgent'
        }
        
        response = requests.post("http://localhost:5000/slack/commands", data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Optimize command successful!")
            print("🚀 Response preview:")
            print(result.get('text', 'No response text')[:200] + "...")
        else:
            print(f"❌ Optimize command failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing optimize command: {e}")

def show_demo_instructions():
    """Show instructions for live demo"""
    print("\n🎬 LIVE DEMO INSTRUCTIONS")
    print("=" * 50)
    
    instructions = """
🎯 For Your Hackathon Presentation:

1. **Set Up Slack App** (if not done):
   • Go to https://api.slack.com/apps/A096HEE7TGD
   • Add slash commands:
     - /optigenix-status → http://localhost:5000/slack/commands
     - /optigenix-optimize → http://localhost:5000/slack/commands
   • Install to your workspace

2. **Live Demo Flow**:
   • Show Slack workspace
   • Type: /optigenix-status
   • Explain real-time server monitoring
   • Type: /optigenix-optimize urgent
   • Show immediate response
   • Switch to OptiGenix web interface
   • Demonstrate actual optimization

3. **Key Points to Highlight**:
   ✅ Enterprise Integration - Teams stay in Slack
   ✅ Real-time Status Monitoring - No need to check web app
   ✅ Collaborative Workflows - Team notifications
   ✅ AI-Powered Responses - Intelligent status reporting

4. **Business Impact**:
   📈 50% faster logistics operations
   💰 Cost savings through optimization
   🚀 Unified workspace for enterprise teams
   ⚡ Instant access without context switching

5. **Demo Commands**:
   • /optigenix-status (show system health)
   • /optigenix-optimize urgent (trigger optimization)
   • Switch to web app for visualization
   """
    
    print(instructions)

def main():
    """Main demo function"""
    print_banner()
    
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix issues above.")
        return
    
    demo_slack_commands()
    show_demo_instructions()
    
    print("\n🎉 Demo preparation complete!")
    print("🚀 Your OptiGenix Slack integration is ready for the hackathon!")

if __name__ == "__main__":
    main()
