#!/usr/bin/env python3
"""
OptiGenix Simple Starter (Windows Compatible)
============================================
Simple launcher that starts the Flask app directly
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def log(message, level="INFO"):
    """Simple logging without emojis"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def check_tokens():
    """Check if Slack tokens are configured"""
    log("Checking Slack configuration...")
    
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    app_token = os.getenv('SLACK_APP_TOKEN')
    
    if not bot_token:
        log("Missing SLACK_BOT_TOKEN in .env", "WARNING")
        return False
        
    if not app_token:
        log("Missing SLACK_APP_TOKEN in .env", "WARNING")
        log("Socket Mode won't be available", "WARNING")
        return False
        
    log("Slack tokens configured", "SUCCESS")
    return True

def setup_auto_notifications():
    """Setup automatic notification triggers"""
    log("Setting up automatic notifications...")
    
    # Set environment variable to enable auto-notifications
    os.environ['OPTIGENIX_AUTO_NOTIFICATIONS'] = 'true'
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if webhook_url:
        log("Webhook notifications configured", "SUCCESS")
    else:
        log("No webhook URL - relying on Socket Mode", "INFO")

def start_flask_app():
    """Start the Flask application"""
    try:
        # Import Flask app modules
        from app_modular import create_app, create_socketio, get_socket_mode
        
        # Create Flask app and SocketIO
        app = create_app()
        socketio = create_socketio(app)
        
        log("Flask app created successfully", "SUCCESS")
        
        # Start Socket Mode for Slack integration
        socket_mode = get_socket_mode()
        if socket_mode:
            # Start Socket Mode in background thread
            import threading
            def start_socket_mode():
                try:
                    socket_mode.start_socket_mode()
                    log("Socket Mode started successfully", "SUCCESS")
                except Exception as e:
                    log(f"Socket Mode failed to start: {e}", "WARNING")
            
            socket_thread = threading.Thread(target=start_socket_mode, daemon=True)
            socket_thread.start()
            log("Socket Mode integration loaded", "SUCCESS")
        else:
            log("Socket Mode not available", "WARNING")
        
        log("Starting Flask server on http://localhost:5000", "INFO")
        
        # Start Flask app
        socketio.run(app, 
                    host='0.0.0.0',
                    port=5000, 
                    debug=False,
                    use_reloader=False)  # Disable reloader for cleaner startup
                    
    except KeyboardInterrupt:
        log("Shutting down by user request...", "INFO")
    except Exception as e:
        log(f"Error starting Flask app: {e}", "ERROR")
        return False
        
    return True

def main():
    """Main entry point"""
    print("=" * 50)
    print("OPTIGENIX SIMPLE STARTER")
    print("=" * 50)
    print()
    
    try:
        # 1. Check configuration
        tokens_ok = check_tokens()
        
        # 2. Setup notifications
        setup_auto_notifications()
        
        # 3. Start Flask app
        log("Starting OptiGenix services...", "INFO")
        if start_flask_app():
            log("Startup complete!", "SUCCESS")
            return True
        else:
            log("Failed to start services", "ERROR")
            return False
            
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
        return False
    except Exception as e:
        print(f"\nError during startup: {e}")
        return False

if __name__ == "__main__":
    # Set UTF-8 encoding for Windows
    if sys.platform == "win32":
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    success = main()
    if not success:
        sys.exit(1)
