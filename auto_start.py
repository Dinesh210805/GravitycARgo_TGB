#!/usr/bin/env python3
"""
🚀 OptiGenix Auto-Starter
========================
Automatically starts all services and notifications in the correct order
"""

import os
import sys
import time
import threading
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OptiGenixAutoStarter:
    """Automated startup manager for OptiGenix"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.services = {}
        self.startup_complete = False
        
    def log(self, message, level="INFO"):
        """Simple logging"""
        timestamp = time.strftime("%H:%M:%S")
        icon = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "STARTUP": "🚀"
        }.get(level, "•")
        print(f"[{timestamp}] {icon} {message}")
        
    def check_tokens(self):
        """Check if required Slack tokens are configured"""
        self.log("Checking Slack configuration...", "INFO")
        
        bot_token = os.getenv('SLACK_BOT_TOKEN')
        app_token = os.getenv('SLACK_APP_TOKEN')
        signing_secret = os.getenv('SLACK_SIGNING_SECRET')
        
        if not bot_token:
            self.log("Missing SLACK_BOT_TOKEN in .env", "WARNING")
            return False
            
        if not app_token:
            self.log("Missing SLACK_APP_TOKEN in .env", "WARNING")
            self.log("Socket Mode won't be available - notifications will use webhook fallback", "WARNING")
            return False
            
        if not signing_secret:
            self.log("Missing SLACK_SIGNING_SECRET in .env", "WARNING")
            
        self.log("Slack tokens configured ✓", "SUCCESS")
        return True
        
    def start_main_service(self):
        """Start the main Flask application with Socket Mode"""
        self.log("Starting main OptiGenix service...", "STARTUP")
        
        try:
            # Set environment variables for auto-notifications
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            os.environ['OPTIGENIX_AUTO_NOTIFICATIONS'] = 'true'
            
            self.log("Loading OptiGenix Flask application...", "INFO")
            
            # Import and start the Flask app directly (no subprocess)
            from app_modular import create_app, create_socketio, get_socket_mode
            
            app = create_app()
            socketio = create_socketio(app)
            
            self.log("Flask app created successfully", "SUCCESS")
            
            # Initialize and start Socket Mode integration
            socket_mode = get_socket_mode()
            if socket_mode:
                self.log("Socket Mode integration loaded", "INFO")
                
                # Start Socket Mode in background
                socket_mode_started = socket_mode.start_socket_mode()
                if socket_mode_started:
                    self.log("Socket Mode started successfully", "SUCCESS")
                else:
                    self.log("Socket Mode failed to start", "WARNING")
            else:
                self.log("Socket Mode not available", "WARNING")
            
            # Start Flask in background thread
            def run_flask():
                try:
                    self.log("Starting Flask server on http://localhost:5000", "INFO")
                    socketio.run(app, 
                                host='0.0.0.0',
                                port=5000, 
                                debug=False,
                                use_reloader=False,  # Disable reloader for cleaner startup
                                log_output=False)    # Reduce verbose logging
                except Exception as e:
                    self.log(f"Flask server error: {e}", "ERROR")
            
            # Start HTTPS server for mobile access
            def run_https_server():
                try:
                    self.log("Starting HTTPS server for mobile access...", "INFO")
                    import subprocess
                    import sys
                    https_process = subprocess.Popen([
                        sys.executable, 
                        str(self.script_dir / "https_server.py")
                    ], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)
                    self.services['https'] = https_process
                    self.log("HTTPS server started for mobile access", "SUCCESS")
                except Exception as e:
                    self.log(f"HTTPS server error: {e}", "WARNING")
            
            # Start Flask in background thread
            flask_thread = threading.Thread(target=run_flask, daemon=True)
            flask_thread.start()
            
            # Start HTTPS server in background thread 
            https_thread = threading.Thread(target=run_https_server, daemon=True)
            https_thread.start()
            
            # Give servers time to start
            time.sleep(5)
            
            # Store thread reference instead of process
            self.services['main'] = flask_thread
            
            self.log("Main service started successfully", "SUCCESS")
            return True
                
        except Exception as e:
            self.log(f"Error starting main service: {e}", "ERROR")
            return False
            
    def wait_for_service(self, url, service_name, max_wait=30):
        """Wait for a service to be ready"""
        self.log(f"Waiting for {service_name} to be ready...", "INFO")
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.log(f"{service_name} is ready ✓", "SUCCESS")
                    return True
            except requests.RequestException:
                pass
                
            time.sleep(1)
            
        self.log(f"{service_name} not ready after {max_wait}s", "WARNING")
        return False
        
    def check_services_health(self):
        """Check health of all services"""
        self.log("Checking service health...", "INFO")
        
        services_status = {}
        
        # Check main Flask app
        try:
            response = requests.get("http://localhost:5000/health", timeout=3)
            services_status['main_app'] = response.status_code == 200
        except:
            services_status['main_app'] = False
            
        # Check JSON server (if running)
        try:
            response = requests.get("http://localhost:8000", timeout=3)
            services_status['json_server'] = response.status_code in [200, 404]  # 404 is OK for JSON server
        except:
            services_status['json_server'] = False
            
        # Check route server
        try:
            response = requests.get("http://localhost:5001/health", timeout=3)
            services_status['route_server'] = response.status_code == 200
        except:
            services_status['route_server'] = False
            
        # Report status
        for service, status in services_status.items():
            status_icon = "✅" if status else "❌"
            self.log(f"{service}: {status_icon}", "INFO")
            
        return services_status
        
    def setup_auto_notifications(self):
        """Setup automatic notification triggers"""
        self.log("Setting up automatic notifications...", "INFO")
        
        # Set environment variable to enable auto-notifications
        os.environ['OPTIGENIX_AUTO_NOTIFICATIONS'] = 'true'
        
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if webhook_url:
            self.log("Webhook notifications configured ✓", "SUCCESS")
        else:
            self.log("No webhook URL - relying on Socket Mode", "INFO")
            
    def send_startup_notification(self):
        """Send notification that system is ready"""
        try:
            # Try to import and use Socket Mode
            from app_modular import get_socket_mode
            socket_mode = get_socket_mode()
            
            if socket_mode and socket_mode.bot_app and socket_mode.is_running:
                startup_message = f"""🚀 *OptiGenix System Started!*

📊 **Status:**
• Main Application: ✅ Running (Port 5000)
• Socket Mode: ✅ Connected
• Auto-Notifications: ✅ Enabled

🎯 **Ready for:**
• Web optimizations at http://localhost:5000
• Slack commands: `/optigenix-status`, `/optigenix-optimize`
• Automatic completion notifications

💡 *System is fully operational!*"""
                
                try:
                    socket_mode.bot_app.client.chat_postMessage(
                        channel="#general",
                        text=startup_message
                    )
                    self.log("Startup notification sent via Socket Mode", "SUCCESS")
                except:
                    # Fall back to webhook
                    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
                    if webhook_url:
                        response = requests.post(webhook_url, json={"text": "🚀 OptiGenix System Started! Ready for optimizations."}, timeout=10)
                        if response.status_code == 200:
                            self.log("Startup notification sent via webhook", "SUCCESS")
            else:
                # Use webhook fallback
                webhook_url = os.getenv('SLACK_WEBHOOK_URL')
                if webhook_url:
                    response = requests.post(webhook_url, json={"text": "🚀 OptiGenix System Started! Ready for optimizations."}, timeout=10)
                    if response.status_code == 200:
                        self.log("Startup notification sent via webhook", "SUCCESS")
                        
        except Exception as e:
            self.log(f"Could not send startup notification: {e}", "WARNING")
            
    def cleanup_on_exit(self):
        """Cleanup processes on exit"""
        self.log("Cleaning up services...", "INFO")
        
        for service_name, service in self.services.items():
            if service:
                if hasattr(service, 'poll'):  # It's a process
                    if service.poll() is None:
                        self.log(f"Terminating {service_name}...", "INFO")
                        service.terminate()
                        try:
                            service.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            service.kill()
                elif hasattr(service, 'is_alive'):  # It's a thread
                    if service.is_alive():
                        self.log(f"Stopping {service_name}...", "INFO")
                        # For daemon threads, they'll stop when main process exits
                    
    def start_all(self):
        """Start all services automatically"""
        self.log("🚀 OPTIGENIX AUTO-STARTER", "STARTUP")
        self.log("=" * 50, "INFO")
        
        try:
            # 1. Check configuration
            tokens_ok = self.check_tokens()
            
            # 2. Setup auto-notifications
            self.setup_auto_notifications()
            
            # 3. Start main service
            if not self.start_main_service():
                self.log("Failed to start main service", "ERROR")
                return False
                
            # 4. Wait for main service to be ready
            if not self.wait_for_service("http://localhost:5000/health", "Main App"):
                self.log("Main app not responding", "WARNING")
                
            # 5. Check all service health
            time.sleep(3)  # Allow all services to fully start
            self.check_services_health()
            
            # 6. Send startup notification
            if tokens_ok:
                time.sleep(2)  # Give Socket Mode time to connect
                self.send_startup_notification()
                
            # 7. Final status
            self.startup_complete = True
            self.log("🎉 STARTUP COMPLETE!", "SUCCESS")
            self.log("=" * 50, "INFO")
            self.log("📊 Dashboard: http://localhost:5000", "INFO")
            if tokens_ok:
                self.log("⚡ Slack Commands: Ready", "INFO")
            self.log("🔔 Auto-Notifications: Enabled", "INFO")
            self.log("⚠️  Keep this terminal open during operation", "WARNING")
            self.log("", "INFO")
            self.log("Press Ctrl+C to stop all services", "INFO")
            
            return True
            
        except KeyboardInterrupt:
            self.log("Shutdown requested by user", "INFO")
            self.cleanup_on_exit()
            return False
        except Exception as e:
            self.log(f"Startup failed: {e}", "ERROR")
            self.cleanup_on_exit()
            return False
            
    def monitor_services(self):
        """Monitor services and restart if needed"""
        while self.startup_complete:
            try:
                time.sleep(30)  # Check every 30 seconds
                
                # Check if main service is still running
                main_service = self.services.get('main')
                if main_service:
                    if hasattr(main_service, 'is_alive'):  # It's a thread
                        if not main_service.is_alive():
                            self.log("Main service thread stopped unexpectedly", "WARNING")
                    elif hasattr(main_service, 'poll'):  # It's a process
                        if main_service.poll() is not None:
                            self.log("Main service process stopped unexpectedly", "WARNING")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log(f"Monitor error: {e}", "WARNING")
                
        self.cleanup_on_exit()

def main():
    """Main entry point"""
    starter = OptiGenixAutoStarter()
    
    # Handle Ctrl+C gracefully
    import signal
    def signal_handler(sig, frame):
        starter.log("Shutdown signal received", "INFO")
        starter.cleanup_on_exit()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start all services
    if starter.start_all():
        # Monitor services
        starter.monitor_services()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
