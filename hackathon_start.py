#!/usr/bin/env python3
"""
OptiGenix Hackathon Startup Script
Quick setup and demo script for the Future of Work Hackathon
"""

import os
import sys
import time
import webbrowser
from app_modular import create_app, create_socketio, AppConfig

def print_banner():
    """Print the hackathon banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                     🚛 OPTIGENIX WORKOS 🚛                    ║
║              AI-Powered Container Optimization               ║
║                                                              ║
║             🏆 Future of Work Hackathon 2025 🏆              ║
║                   Kroolo x TGB - Bengaluru                   ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)
    print("🚀 Starting OptiGenix - Enterprise Logistics WorkOS Platform")
    print("=" * 64)

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    # Check for Slack configuration
    slack_config = {
        "Bot Token": bool(os.getenv('SLACK_BOT_TOKEN')),
        "Client Secret": bool(os.getenv('SLACK_CLIENT_SECRET')),
        "Signing Secret": bool(os.getenv('SLACK_SIGNING_SECRET')),
        "Webhook URL": bool(os.getenv('SLACK_WEBHOOK_URL'))
    }
    
    print("\n📱 Slack Integration Status:")
    for key, value in slack_config.items():
        status = "✅" if value else "⚠️"
        print(f"   {status} {key}: {'Configured' if value else 'Not set'}")
    
    # Environment info
    env = "Production" if AppConfig.is_production() else "Development"
    port = AppConfig.get_port()
    
    print(f"\n🔧 Environment: {env}")
    print(f"📡 Port: {port}")
    
    # Show Slack setup instructions if not configured
    if not all(slack_config.values()):
        show_slack_setup_instructions()
    
    return True

def show_slack_setup_instructions():
    """Show Slack setup instructions for the hackathon"""
    print("\n📋 SLACK SETUP INSTRUCTIONS FOR HACKATHON:")
    print("=" * 55)
    
    instructions = """
🎯 **Quick Slack Integration Setup:**

1. **Create Slash Commands** in your Slack app (A096HEE7TGD):
   
   📍 Command 1: /optigenix-status
   • Request URL: http://localhost:5000/slack/commands
   • Description: Check OptiGenix server status and health
   • Usage Hint: No parameters needed
   
   📍 Command 2: /optigenix-optimize
   • Request URL: http://localhost:5000/slack/commands  
   • Description: Start container optimization process
   • Usage Hint: [urgent|normal]

2. **Install App to Your Workspace**:
   • Go to "Install App" in Slack app settings
   • Click "Install to Workspace" 
   • Copy Bot Token → Update .env file

3. **Test Integration**:
   • Run: python demo_slack.py
   • Test commands in Slack workspace

4. **Demo Flow**:
   🚀 Type /optigenix-status → Show system health
   🚀 Type /optigenix-optimize urgent → Trigger optimization
   🚀 Switch to web app for live visualization
    """
    
    print(instructions)

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    # Check for Slack configuration
    slack_config = {
        "Bot Token": bool(os.getenv('SLACK_BOT_TOKEN')),
        "Client Secret": bool(os.getenv('SLACK_CLIENT_SECRET')),
        "Signing Secret": bool(os.getenv('SLACK_SIGNING_SECRET')),
        "Webhook URL": bool(os.getenv('SLACK_WEBHOOK_URL'))
    }
    
    print("\n📱 Slack Integration Status:")
    for key, value in slack_config.items():
        status = "✅" if value else "⚠️"
        print(f"   {status} {key}: {'Configured' if value else 'Not set'}")
    
    # Environment info
    env = "Production" if AppConfig.is_production() else "Development"
    port = AppConfig.get_port()

def setup_demo_data():
    """Set up demo data for the hackathon"""
    print("\n📦 Setting up demo data...")
    
    # Check if demo data exists
    demo_files = [
        "uploads/demo_pharmaceutical_shipment.csv",
        "uploads/demo_electronics_export.csv",
        "uploads/demo_automotive_parts.csv"
    ]
    
    demo_data_exists = any(os.path.exists(f) for f in demo_files)
    
    if demo_data_exists:
        print("   ✅ Demo data already available")
    else:
        print("   ⚠️  Demo data not found - you can upload via web interface")
    
    return True

def show_demo_urls(port):
    """Show important URLs for the demo"""
    base_url = f"http://localhost:{port}"
    
    print(f"""
🌐 OPTIGENIX DEMO URLS:
══════════════════════════════════════════════════════════════
🏠 Main Application:     {base_url}
📊 Optimization Portal:  {base_url}/start
📈 Dashboard:            {base_url}/status
🔧 Health Check:         {base_url}/health

🤖 SLACK INTEGRATION:
══════════════════════════════════════════════════════════════
📝 Commands Endpoint:    {base_url}/slack/commands
🧪 Test Integration:     {base_url}/slack/test
🔗 OAuth Handler:        {base_url}/slack/oauth

💡 SLACK COMMANDS (Use in your Slack workspace):
══════════════════════════════════════════════════════════════
/optigenix-status        - Check server status
/optigenix-optimize      - Start optimization

🎯 HACKATHON DEMO FLOW:
══════════════════════════════════════════════════════════════
1. Show Slack commands working (/optigenix-status)
2. Upload CSV data via web interface
3. Trigger optimization via Slack (/optigenix-optimize urgent)
4. Show real-time results and notifications
5. Demonstrate AR visualization integration
══════════════════════════════════════════════════════════════
""")

def main():
    """Main hackathon startup function"""
    print_banner()
    
    # Check environment
    check_environment()
    
    # Setup demo data
    setup_demo_data()
    
    # Get port
    port = AppConfig.get_port()
    
    # Show demo information
    show_demo_urls(port)
    
    # Ask if user wants to start automatically
    print("\n🚀 Ready to launch OptiGenix!")
    start_auto = input("📝 Start automatically? (y/n): ").lower().strip()
    
    if start_auto in ['y', 'yes', '']:
        print("\n🎬 Starting OptiGenix for hackathon demo...")
        
        # Import and start the app
        try:
            app = create_app()
            socketio = create_socketio(app)
            
            print(f"✅ OptiGenix is running on http://localhost:{port}")
            print("\n💡 HACKATHON TIPS:")
            print("   • Open Slack and try /optigenix-status")
            print("   • Upload demo CSV files via the web interface")
            print("   • Show real-time optimization progress")
            print("   • Demonstrate team collaboration features")
            print("\n🏆 Good luck with your presentation!")
            print("   Press Ctrl+C to stop the server")
            
            # Open browser
            if not AppConfig.is_production():
                time.sleep(2)
                try:
                    webbrowser.open(f"http://localhost:{port}")
                except:
                    pass
            
            # Start the application
            socketio.run(
                app, 
                debug=not AppConfig.is_production(), 
                host='0.0.0.0', 
                port=port, 
                use_reloader=False
            )
            
        except KeyboardInterrupt:
            print("\n\n🛑 OptiGenix stopped by user")
            print("🏆 Thanks for using OptiGenix! Good luck in the hackathon!")
        except Exception as e:
            print(f"\n❌ Error starting OptiGenix: {e}")
            print("💡 Try running: python app_modular.py")
            return 1
    else:
        print("\n💻 To start manually, run: python app_modular.py")
        print("🔗 Or use this script: python hackathon_start.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
