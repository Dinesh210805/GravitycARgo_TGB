#!/usr/bin/env python3
"""
🚀    if not app_token:
        print("ERROR: Missing SLACK_APP_TOKEN in .env file")
        print(">> See SOCKET_MODE_SETUP.env for setup instructions")
        returniGenix Socket Mode Launcher
================================
Simplified launcher that only uses Socket Mode (Method 1)
HTTP endpoints (Method 2) have been removed from the codebase.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def start_socket_mode_only():
    """Start Flask app with Socket Mode integration only"""
    
    print(">> OPTIGENIX - SOCKET MODE ONLY")
    print("=" * 50)
    print(">> Using 100% automated Socket Mode integration")
    print(">> No ngrok or URL configuration needed!")
    print(">> Works instantly on mobile and desktop")
    
    # Check for required Socket Mode tokens
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    app_token = os.getenv('SLACK_APP_TOKEN')
    
    if not bot_token:
        print("ERROR: Missing SLACK_BOT_TOKEN in .env file")
        return
        
    if not app_token:
        print("❌ Missing SLACK_APP_TOKEN in .env file")
        print("� See SOCKET_MODE_SETUP.env for setup instructions")
        return
    
    print("SUCCESS: Socket Mode tokens configured")
    print(">> Starting OptiGenix with Socket Mode...")
    
    # Start Flask app with Socket Mode
    start_flask_app()

def start_flask_app():
    """Start the Flask application with Socket Mode"""
    try:
        from app_modular import create_app, create_socketio
        
        app = create_app()
        socketio = create_socketio(app)
        
        print(">> OptiGenix Flask app starting...")
        print(">> Socket Mode will auto-connect to Slack")
        
        socketio.run(app, 
                    host='0.0.0.0',  # Allow external connections
                    port=5000, 
                    debug=False)
                    
    except KeyboardInterrupt:
        print("\n>> Shutting down...")
    except Exception as e:
        print(f"ERROR: Error starting Flask app: {e}")

if __name__ == "__main__":
    start_socket_mode_only()
