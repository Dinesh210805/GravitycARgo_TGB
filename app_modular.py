"""
Alternative entry point for the container packing application
This module uses the new optigenix_module structure while maintaining
the same functionality as the original app.py
"""
from flask import Flask, jsonify, request, current_app, render_template
from flask_cors import CORS
import os
import sys
import json
import time
import logging
import subprocess
import psutil
import signal
import threading
import http.server
import socketserver
import socket
import glob
import shutil
import requests
import hmac
import hashlib
from urllib.parse import parse_qs
from logging.handlers import RotatingFileHandler
from flask_socketio import SocketIO, emit
import multiprocessing
import numpy as np
from pathlib import Path
from routing.Server import app as route_temp_app

# Socket Mode integration imports
try:
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    SOCKET_MODE_AVAILABLE = True
except ImportError:
    SOCKET_MODE_AVAILABLE = False
    print("📢 Socket Mode not available. Install with: pip install slack-bolt")

# Update imports to use the new package structure

# Import configuration from config.py
from config import UPLOAD_FOLDER, PLANS_FOLDER, MAX_CONTENT_LENGTH, SECRET_KEY

# Configuration constants - moved from hardcoded values
class AppConfig:
    STANDARD_JSON_FILENAME = "latest_container_plan.json"
    NGROK_DOMAIN = os.getenv('NGROK_DOMAIN', "destined-mammoth-flowing.ngrok-free.app")
    JSON_SERVER_PORT = int(os.getenv('JSON_SERVER_PORT', '8000'))
    ROUTE_TEMP_PORT = int(os.getenv('ROUTE_TEMP_PORT', '5001'))
    MAIN_APP_PORT = int(os.getenv('MAIN_APP_PORT', '5000'))
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', str(1024 * 1024)))  # 1MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '10'))
    
    # Dynamic ngrok support
    _ngrok_process = None
    _ngrok_url = None
    
    @staticmethod
    def get_ngrok_url():
        """Get current ngrok URL or localhost fallback"""
        # First check environment variable (set by start_dynamic_slack.py)
        if os.getenv('NGROK_PUBLIC_URL'):
            return os.getenv('NGROK_PUBLIC_URL')
        
        # Try to get from ngrok API
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=2)
            if response.status_code == 200:
                tunnels = response.json()
                for tunnel in tunnels.get('tunnels', []):
                    if tunnel.get('proto') == 'https':
                        AppConfig._ngrok_url = tunnel.get('public_url')
                        return AppConfig._ngrok_url
        except:
            pass
        
        # Fallback to localhost
        return f"http://localhost:{AppConfig.MAIN_APP_PORT}"
    
    @staticmethod
    def get_slack_command_url():
        """Get dynamic URL for Slack commands"""
        base_url = AppConfig.get_ngrok_url()
        return f"{base_url}/slack/commands"
    
    # Production configuration helpers
    @staticmethod
    def is_production():
        """Check if running in production environment"""
        return os.environ.get('FLASK_ENV') == 'production'
    
    @staticmethod
    def get_port():
        """Get port from environment variable (Render sets PORT)"""
        return int(os.environ.get('PORT', AppConfig.MAIN_APP_PORT))

# Slack Configuration
class SlackConfig:
    """Slack app configuration"""
    CLIENT_ID = "9220170300022.9221490265557"
    CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET', "ac2f422216c0682f10278d2550f9f902")
    SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET', "e2475a30a09640d4055a5d5efa834084")
    BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', "")  # You'll set this after installation
    WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', "")  # Optional for notifications

# Socket Mode Integration
class SlackSocketMode:
    """100% Automated Slack integration using Socket Mode"""
    
    def __init__(self):
        self.bot_app = None
        self.handler = None
        self.is_running = False
        
        if not SOCKET_MODE_AVAILABLE:
            print("⚠️ Socket Mode not available. Run: pip install slack-bolt")
            return
            
        # Initialize Socket Mode app
        try:
            self.bot_app = App(
                token=os.getenv("SLACK_BOT_TOKEN"),
                signing_secret=os.getenv("SLACK_SIGNING_SECRET")
            )
            
            self.app_token = os.getenv("SLACK_APP_TOKEN")
            
            if not all([self.bot_app.client.token, self.app_token]):
                print("⚠️ Missing Socket Mode tokens. Check SLACK_APP_TOKEN in .env")
                return
                
            self.setup_commands()
            self.setup_events()
            print("✅ Socket Mode initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize Socket Mode: {e}")
    
    def setup_commands(self):
        """Setup slash commands for Socket Mode"""
        if not self.bot_app:
            return
            
        @self.bot_app.command("/optigenix-status")
        def handle_status_command(ack, command, say, logger):
            """Handle /optigenix-status command"""
            ack()
            
            try:
                # Get system status from existing SlackCommandHandler
                handler = SlackCommandHandler()
                response = handler.handle_status_command()
                
                say(blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": response.get("text", "🚛 OptiGenix Status: All systems operational!")
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "🚀 Quick Optimize"},
                                "value": "start_optimization",
                                "action_id": "quick_optimize"
                            },
                            {
                                "type": "button", 
                                "text": {"type": "plain_text", "text": "📊 Dashboard"},
                                "value": "view_dashboard",
                                "action_id": "open_dashboard"
                            }
                        ]
                    }
                ])
                
            except Exception as e:
                logger.error(f"Error in Socket Mode status command: {e}")
                say(f"❌ Error getting status: {str(e)}")
        
        @self.bot_app.command("/optigenix-optimize")
        def handle_optimize_command(ack, command, say, logger):
            """Handle /optigenix-optimize command"""
            ack()
            
            try:
                text = command.get("text", "").strip()
                user_name = command.get("user_name", "Unknown")
                
                # Use existing SlackCommandHandler
                handler = SlackCommandHandler()
                response = handler.handle_optimize_command(text, user_name)
                
                say(response.get("text", f"🚀 Optimization started by {user_name}!"))
                
            except Exception as e:
                logger.error(f"Error in Socket Mode optimize command: {e}")
                say(f"❌ Error starting optimization: {str(e)}")
    
    def setup_events(self):
        """Setup event handlers for Socket Mode"""
        if not self.bot_app:
            return
            
        @self.bot_app.event("app_mention")
        def handle_mentions(event, say, logger):
            """Handle @OptiGenix mentions"""
            try:
                text = event.get("text", "").lower()
                
                if "status" in text:
                    handler = SlackCommandHandler()
                    response = handler.handle_status_command()
                    say(response.get("text", "🚛 OptiGenix: All systems operational!"))
                elif "help" in text:
                    say("""🚛 *OptiGenix Bot Help*

**Commands:**
• `/optigenix-status` - Check system status
• `/optigenix-optimize [priority]` - Start optimization

**Mentions:**
• `@OptiGenix status` - Quick status check
• `@OptiGenix help` - Show this help

🎯 *Ready to optimize your containers!*""")
                else:
                    say("👋 Hi! Try `/optigenix-status` or `/optigenix-optimize` or mention me with 'help'")
                    
            except Exception as e:
                logger.error(f"Error in mention handler: {e}")
                say("❌ Sorry, I encountered an error.")
        
        @self.bot_app.action("quick_optimize")
        def handle_quick_optimize(ack, body, say):
            """Handle quick optimize button"""
            ack()
            user_name = body.get("user", {}).get("name", "Unknown")
            
            handler = SlackCommandHandler()
            response = handler.handle_optimize_command("normal", user_name)
            say(f"🚀 Quick optimization started by {user_name}!")
        
        @self.bot_app.action("open_dashboard")
        def handle_dashboard(ack, say):
            """Handle dashboard button"""
            ack()
            base_url = AppConfig.get_ngrok_url()
            say(f"📊 Dashboard: {base_url}/")
    
    def start_socket_mode(self):
        """Start Socket Mode in background thread"""
        if not self.bot_app or not self.app_token:
            print("❌ Socket Mode not properly configured")
            return False
            
        if self.is_running:
            print("✅ Socket Mode already running")
            return True
            
        try:
            def run_socket_mode():
                self.handler = SocketModeHandler(self.bot_app, self.app_token)
                print("🔗 Socket Mode: Starting connection...")
                self.handler.start()
            
            # Start in background thread
            socket_thread = threading.Thread(target=run_socket_mode, daemon=True)
            socket_thread.start()
            
            self.is_running = True
            print("✅ Socket Mode started successfully!")
            print("🔗 No URLs to configure - fully automated!")
            print("📱 Ready for Slack commands on mobile and desktop")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Socket Mode: {e}")
            return False
    
    def stop_socket_mode(self):
        """Stop Socket Mode"""
        if self.handler:
            try:
                self.handler.close()
                self.is_running = False
                print("🔴 Socket Mode stopped")
            except Exception as e:
                print(f"Error stopping Socket Mode: {e}")

# Global Socket Mode instance
_socket_mode_instance = None

def get_socket_mode():
    """Get or create Socket Mode instance"""
    global _socket_mode_instance
    if _socket_mode_instance is None:
        _socket_mode_instance = SlackSocketMode()
    return _socket_mode_instance

# Import other modules
from modules.handlers import (
    landing_handler, start_handler, optimize_handler, download_report_handler,
    view_report_handler, preview_csv_handler,
    get_container_stats_handler, get_item_details_handler, get_container_status_handler,
    clear_container_handler, handle_socketio_update_request, generate_alternative_plan_handler,
    download_ar_apk
)
from modules.handlers import bp

# Slack Integration Classes
class SlackService:
    """Service for handling Slack interactions"""
    
    def __init__(self):
        self.client_id = SlackConfig.CLIENT_ID
        self.client_secret = SlackConfig.CLIENT_SECRET
        self.signing_secret = SlackConfig.SIGNING_SECRET
        self.bot_token = SlackConfig.BOT_TOKEN
        
    def verify_slack_signature(self, request_body, timestamp, signature):
        """Verify that requests come from Slack"""
        if not self.signing_secret:
            return True  # Skip verification if no signing secret
            
        # Create signature
        sig_basestring = f"v0:{timestamp}:{request_body}"
        my_signature = 'v0=' + hmac.new(
            self.signing_secret.encode(),
            sig_basestring.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(my_signature, signature)
    
    def send_message(self, channel, text, blocks=None):
        """Send message to Slack channel"""
        if not self.bot_token:
            print("No Slack bot token configured")
            return False
            
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "channel": channel,
            "text": text
        }
        
        if blocks:
            payload["blocks"] = blocks
            
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            return response.status_code == 200 and response.json().get("ok", False)
        except Exception as e:
            print(f"Failed to send Slack message: {e}")
            return False
    
    def send_webhook_notification(self, message):
        """Send notification via webhook"""
        if not SlackConfig.WEBHOOK_URL:
            return False
            
        payload = {"text": message}
        
        try:
            response = requests.post(SlackConfig.WEBHOOK_URL, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send webhook notification: {e}")
            return False

class SlackCommandHandler:
    """Handle Slack slash commands"""
    
    def __init__(self):
        self.slack_service = SlackService()
    
    def handle_status_command(self):
        """Handle /optigenix-status command"""
        try:
            # Check main server status
            main_status = "🟢 Running"
            
            # Check JSON server status
            json_service = JSONServerService.get_instance()
            json_status = "🟢 Running" if json_service.is_running() else "🔴 Stopped"
            json_url = json_service.get_url() if json_service.is_running() else "Not available"
            
            # Check route temperature server
            route_status = "🟢 Running" if is_port_in_use(AppConfig.ROUTE_TEMP_PORT) else "🔴 Stopped"
            
            # Get environment info
            env = "Production" if AppConfig.is_production() else "Development"
            port = AppConfig.get_port()
            
            # Get recent optimization stats
            stats = self._get_optimization_stats()
            
            status_message = f"""🚛 *OptiGenix Container Optimizer Status*

📊 *System Status:*
• Main Server: {main_status} (Port: {port})
• JSON Server: {json_status}
• Route Server: {route_status} (Port: {AppConfig.ROUTE_TEMP_PORT})
• Environment: {env}

📈 *Recent Activity:*
• Total Optimizations: {stats['total_optimizations']}
• Average Efficiency: {stats['avg_efficiency']:.1f}%
• Last Optimization: {stats['last_optimization']}

🔗 *AR Visualization URL:*
`{json_url}`

💡 *Available Commands:*
• `/optigenix-status` - Check server status
• `/optigenix-optimize [urgent|normal]` - Start optimization"""
            
            return {
                "response_type": "in_channel",
                "text": status_message
            }
            
        except Exception as e:
            return {
                "response_type": "ephemeral",
                "text": f"❌ Error checking status: {str(e)}"
            }
    
    def handle_optimize_command(self, text, user_name):
        """Handle /optigenix-optimize command"""
        try:
            priority = text.strip().lower() if text else "normal"
            
            if priority not in ["urgent", "normal"]:
                return {
                    "response_type": "ephemeral",
                    "text": "❌ Usage: `/optigenix-optimize [urgent|normal]`"
                }
            
            # Check if we have data to optimize
            script_dir = os.path.dirname(os.path.abspath(__file__))
            upload_dir = os.path.join(script_dir, "uploads")
            csv_files = glob.glob(os.path.join(upload_dir, "*.csv"))
            
            if not csv_files:
                return {
                    "response_type": "ephemeral",
                    "text": "❌ No CSV files found. Please upload data first via the web interface."
                }
            
            # Get latest file info
            latest_file = max(csv_files, key=os.path.getmtime)
            file_name = os.path.basename(latest_file)
            
            # Return immediate response
            response_text = f"""🚀 *Optimization Started by {user_name}!*

📊 *Details:*
• Priority: {priority.upper()}
• Data File: {file_name}
• Estimated Time: 2-5 minutes
• Status: Processing...

⏳ *I'll notify the team when complete!*"""
            
            # In a real implementation, you would trigger optimization here
            # For demo purposes, we'll simulate success
            
            return {
                "response_type": "in_channel",
                "text": response_text
            }
            
        except Exception as e:
            return {
                "response_type": "ephemeral",
                "text": f"❌ Error starting optimization: {str(e)}"
            }
    
    def _get_optimization_stats(self):
        """Get optimization statistics"""
        try:
            # Get container plans directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            plans_dir = os.path.join(script_dir, "container_plans")
            
            json_files = glob.glob(os.path.join(plans_dir, "*.json"))
            
            if not json_files:
                return {
                    "total_optimizations": 0,
                    "avg_efficiency": 0.0,
                    "last_optimization": "Never"
                }
            
            # Get stats from recent files
            total_files = len(json_files)
            latest_file = max(json_files, key=os.path.getmtime)
            
            # Try to read efficiency from latest file
            avg_efficiency = 85.0  # Default value
            try:
                with open(latest_file, 'r') as f:
                    data = json.load(f)
                    if 'container_info' in data and 'volume_utilization' in data['container_info']:
                        avg_efficiency = data['container_info']['volume_utilization']
            except:
                pass
            
            # Get last modification time
            last_mod = os.path.getmtime(latest_file)
            last_optimization = time.strftime("%Y-%m-%d %H:%M", time.localtime(last_mod))
            
            return {
                "total_optimizations": total_files,
                "avg_efficiency": avg_efficiency,
                "last_optimization": last_optimization
            }
            
        except Exception as e:
            print(f"Error getting optimization stats: {e}")
            return {
                "total_optimizations": 0,
                "avg_efficiency": 0.0,
                "last_optimization": "Unknown"
            }

# Integrated JSON Server implementation
class JSONServerService:
    """
    Manages an integrated JSON server for AR visualization.
    Runs a local HTTP server and ngrok tunnel directly within the Flask application.
    """
    _instance = None
    _server = None
    _server_thread = None
    _ngrok_process = None
    _ngrok_url = f"https://{AppConfig.NGROK_DOMAIN}/{AppConfig.STANDARD_JSON_FILENAME}"
    _is_running = False
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = JSONServerService()
        return cls._instance
    
    def __init__(self):
        """Initialize the JSONServerService"""
        # Setup static paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.script_dir, "container_plans")
        self.staging_dir = os.path.join(self.script_dir, "serving")
        self.json_path = os.path.join(self.staging_dir, AppConfig.STANDARD_JSON_FILENAME)
        
        # Prepare the staging directory
        os.makedirs(self.staging_dir, exist_ok=True)
        
        # Create handler for serving JSON
        self.handler_class = self._create_handler()
    
    def _create_handler(self):
        """Create a handler class for the HTTP server"""
        json_path = self.json_path
        
        class SingleJSONHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                # Redirect logs to Flask logger
                try:
                    current_app.logger.debug(f"JSONServer: {format % args}")
                except:
                    pass
                return
                
            def end_headers(self):
                # Enable CORS for Unity
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                self.send_header('Content-Type', 'application/json')
                return super().end_headers()
                
            def do_OPTIONS(self):
                self.send_response(200)
                self.end_headers()
            
            def do_GET(self):
                try:
                    current_app.logger.debug(f"JSONServer received request: {self.path}")
                except:
                    print(f"JSONServer received request: {self.path}")
                
                # For any path, serve the JSON file
                self.send_response(200)
                self.end_headers()
                
                try:
                    # Read and serve the JSON file
                    with open(json_path, 'rb') as file:
                        self.wfile.write(file.read())
                except Exception as e:
                    try:
                        current_app.logger.error(f"Error serving JSON: {e}")
                    except:
                        print(f"Error serving JSON: {e}")
        
        return SingleJSONHandler
    
    def update_json_file(self):
        """Update the JSON file with the latest container plan"""
        try:
            # Find the latest JSON file
            json_files = glob.glob(os.path.join(self.data_dir, "*.json"))
            if not json_files:
                print(f"ERROR: No JSON files found in {self.data_dir}")
                return False
                
            # Sort files by modification time, newest first
            latest_json = max(json_files, key=os.path.getmtime)
            print(f"Found latest JSON file: {os.path.basename(latest_json)}")
                
            # Copy to staging directory
            shutil.copy2(latest_json, self.json_path)
            print(f"Copied to staging as: {AppConfig.STANDARD_JSON_FILENAME}")
            return True
        except Exception as e:
            print(f"ERROR copying JSON file: {e}")
            return False
    
    def is_port_in_use(self, port):
        """Check if a port is already in use"""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
            
    def find_available_port(self, start_port, max_attempts=10):
        """Find an available port starting from start_port"""
        port = start_port
        for _ in range(max_attempts):
            if not self.is_port_in_use(port):
                return port
            port += 1
        return None
    
    def start_server(self):
        """Start the integrated JSON server"""
        # In production, disable ngrok and use direct server URL
        if AppConfig.is_production():
            return self._start_production_server()
        
        # Original development implementation with ngrok
        return self._start_development_server()
    
    def _start_production_server(self):
        """Start server for production environment without ngrok"""
        with self._lock:
            if self._is_running:
                print("JSON server is already running")
                return True
                
            try:
                # Update the JSON file first
                if not self.update_json_file():
                    return False
                
                port_to_use = AppConfig.JSON_SERVER_PORT
                if self.is_port_in_use(port_to_use):
                    port_to_use = self.find_available_port(port_to_use + 1)
                    if port_to_use is None:
                        raise Exception("Could not find an available port to start the JSON server")
                
                # Start the HTTP server
                print(f"Starting production JSON server on port {port_to_use}...")
                self._server = socketserver.TCPServer(("", port_to_use), self.handler_class)
                
                # Run in a thread
                self._server_thread = threading.Thread(target=self._server.serve_forever)
                self._server_thread.daemon = True
                self._server_thread.start()
                  # Set production URL (use the main app URL)
                # Try to detect Render URL automatically
                render_service_name = os.environ.get('RENDER_SERVICE_NAME')
                if render_service_name:
                    # Construct Render URL from service name
                    base_url = f"https://{render_service_name}.onrender.com"
                else:
                    # Fallback to manual environment variable or localhost
                    base_url = os.environ.get('RENDER_EXTERNAL_URL', f'http://localhost:{AppConfig.get_port()}')
                
                self._ngrok_url = f"{base_url}/api/container_plan.json"
                
                self._is_running = True
                print(f"Production JSON server is running. URL: {self._ngrok_url}")
                return True
                
            except Exception as e:
                print(f"Failed to start production JSON server: {e}")
                self.stop_server()
                return False
    
    def _start_development_server(self):
        """Original development server implementation with ngrok"""
        with self._lock:
            if self._is_running:
                print("JSON server is already running")
                return True
                
            try:
                # Update the JSON file first
                if not self.update_json_file():
                    return False
                
                # Check if the default port is in use
                port_to_use = AppConfig.JSON_SERVER_PORT
                if self.is_port_in_use(port_to_use):
                    print(f"Port {port_to_use} is already in use!")
                    
                    # Try to find an available port
                    port_to_use = self.find_available_port(port_to_use + 1)
                    if port_to_use is None:
                        raise Exception("Could not find an available port to start the JSON server")
                    print(f"Using alternative port: {port_to_use}")
                
                # Start the HTTP server
                print(f"Starting local HTTP server on port {port_to_use}...")
                self._server = socketserver.TCPServer(("", port_to_use), self.handler_class)
                
                # Run in a thread
                self._server_thread = threading.Thread(target=self._server.serve_forever)
                self._server_thread.daemon = True
                self._server_thread.start()
                print("HTTP server started successfully")
                
                # Start ngrok in another thread
                ngrok_thread = threading.Thread(target=lambda: self._start_ngrok(port_to_use))
                ngrok_thread.daemon = True
                ngrok_thread.start()
                
                # Wait for ngrok to start                time.sleep(5)
                
                self._is_running = True
                print(f"JSON server is running. URL: {self._ngrok_url}")
                return True
                
            except Exception as e:
                print(f"Failed to start JSON server: {e}")
                self.stop_server()  # Clean up if partially started
                return False
    
    def _start_ngrok(self, port=None):
        """Start ngrok tunnel"""
        if port is None:
            port = AppConfig.JSON_SERVER_PORT
            
        try:
            # Check if ngrok is installed
            result = subprocess.run(["ngrok", "version"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True)
            if result.returncode != 0:
                print("Warning: ngrok is not installed or not in PATH")
                print("The JSON server will run locally only.")
                print("For Unity AR access, you can:")
                print("1. Install ngrok from https://ngrok.com/")
                print("2. Use local network access if on same network")
                print(f"3. Access directly at http://localhost:{port}/{AppConfig.STANDARD_JSON_FILENAME}")
                
                # Set local URL instead of ngrok URL
                self._ngrok_url = f"http://localhost:{port}/{AppConfig.STANDARD_JSON_FILENAME}"
                return True  # Consider this successful for local development
                
            # Start ngrok with the specified domain
            cmd = f"ngrok http {port} --domain={AppConfig.NGROK_DOMAIN}"
            print(f"Starting ngrok: {cmd}")
            
            # Try to terminate any existing ngrok processes first
            self._kill_existing_ngrok()
            
            self._ngrok_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            
            # Check if process started successfully
            if self._ngrok_process.poll() is not None:
                stderr = self._ngrok_process.stderr.read().decode('utf-8')
                print(f"Failed to start ngrok: {stderr}")
                print("Falling back to local server only")
                self._ngrok_url = f"http://localhost:{port}/{AppConfig.STANDARD_JSON_FILENAME}"
                return True  # Fallback to local
                
            print(f"ngrok started successfully with URL: {self._ngrok_url}")
            return True
            
        except FileNotFoundError:
            print("Warning: ngrok not found in system PATH")
            print("The JSON server will run locally only.")
            print("To enable external access:")
            print("1. Install ngrok: https://ngrok.com/download")
            print("2. Add ngrok to your system PATH")
            print(f"3. For now, use local URL: http://localhost:{port}/{AppConfig.STANDARD_JSON_FILENAME}")
            
            # Set local URL as fallback
            self._ngrok_url = f"http://localhost:{port}/{AppConfig.STANDARD_JSON_FILENAME}"
            return True
            
        except Exception as e:
            print(f"Error with ngrok setup: {e}")
            print("Falling back to local server only")
            self._ngrok_url = f"http://localhost:{port}/{AppConfig.STANDARD_JSON_FILENAME}"
            return True
            
    def _kill_existing_ngrok(self):
        """Attempt to kill any existing ngrok processes"""
        try:
            if os.name == 'nt':  # Windows
                # Try to kill any existing ngrok processes
                os.system("taskkill /f /im ngrok.exe 2>nul")
            else:  # Unix/Linux/Mac
                os.system("pkill ngrok 2>/dev/null")
            
            # Give it a moment to terminate
            time.sleep(1)
        except Exception as e:
            print(f"Warning: Could not kill existing ngrok processes: {e}")
            # Continue anyway
    
    def stop_server(self):
        """Stop the JSON server"""
        with self._lock:
            if not self._is_running:
                return True
                
            try:
                # Stop ngrok
                if self._ngrok_process:
                    print("Stopping ngrok...")
                    self._ngrok_process.terminate()
                    try:
                        self._ngrok_process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self._ngrok_process.kill()
                    self._ngrok_process = None
                
                # Stop HTTP server
                if self._server:
                    print("Stopping HTTP server...")
                    self._server.shutdown()
                    self._server.server_close()
                    self._server = None
                    self._server_thread = None
                
                self._is_running = False
                print("JSON server stopped")
                return True
                
            except Exception as e:
                print(f"Error stopping JSON server: {e}")
                return False
    
    def is_running(self):
        """Check if the server is running"""
        with self._lock:
            if not self._is_running:
                return False
                
            # Additional check - if ngrok process died
            if self._ngrok_process and self._ngrok_process.poll() is not None:
                print("ngrok process has died unexpectedly")
                self._is_running = False
                return False
                
            return True
    
    def get_url(self):
        """Get the ngrok URL for the JSON server"""
        return self._ngrok_url

# JSON server process management for AR visualization (legacy class kept for compatibility)
class JsonServerManager:
    """Legacy class for backwards compatibility"""
    _process = None
    _server_url = None
    _lock = threading.Lock()
    
    @classmethod
    def start_server(cls):
        """Start the JSON server process"""
        service = JSONServerService.get_instance()
        result = service.start_server()
        if result:
            cls._server_url = service.get_url()
        return result
    
    @classmethod
    def stop_server(cls):
        """Stop the JSON server process"""
        service = JSONServerService.get_instance()
        result = service.stop_server()
        if result:
            cls._server_url = None
        return result
    
    @classmethod
    def is_server_running(cls):
        """Check if the JSON server process is running"""
        service = JSONServerService.get_instance()
        return service.is_running()
    
    @classmethod
    def get_server_url(cls):
        """Get the URL of the JSON server"""
        service = JSONServerService.get_instance()
        return service.get_url()

# JSON encoder for numpy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.float32):
            return float(obj)
        return super(NumpyEncoder, self).default(obj)

def create_app():
    """
    Create and configure the Flask application.
    This function initializes a Flask application with necessary configurations
    including upload directories, secret key, and JSON encoder. It sets up all
    route handlers, registers blueprints, configures error handlers, and
    establishes logging infrastructure.
    """
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Enable CORS for all domains (needed for local HTML files)
    CORS(app, origins=['*'], methods=['GET', 'POST', 'OPTIONS'], 
         allow_headers=['Content-Type', 'Authorization'])
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.secret_key = SECRET_KEY
    app.json_encoder = NumpyEncoder

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Ensure container plans directory exists
    os.makedirs(PLANS_FOLDER, exist_ok=True)
    
    # Set up routes
    app.route('/')(landing_handler)
    app.route('/start')(start_handler)
    app.route('/optimize', methods=['POST'])(optimize_handler)
    app.route('/download_report')(download_report_handler)
    app.route('/view_report')(view_report_handler)
    app.route('/preview_csv', methods=['POST'])(preview_csv_handler)
    app.route('/api/container/stats')(get_container_stats_handler)
    app.route('/api/items/<item_name>')(get_item_details_handler)
    app.route('/status')(get_container_status_handler)
    app.route('/clear', methods=['POST'])(clear_container_handler)
    app.route('/generate_alternative_plan')(generate_alternative_plan_handler)
    app.route('/download_ar_apk')(download_ar_apk)
    
    # Container Visualization Route
    @app.route('/visualization')
    def container_visualization():
        """Serve the container visualization page"""
        return render_template('container_visualization.html')
    
    # Slack Integration Routes
    @app.route('/slack/commands', methods=['POST'])
    def handle_slack_command():
        """Handle Slack slash commands"""
        try:
            # Get request data
            form_data = request.form
            request_body = request.get_data(as_text=True)
            
            # Verify Slack signature (optional but recommended)
            slack_signature = request.headers.get('X-Slack-Signature', '')
            slack_timestamp = request.headers.get('X-Slack-Request-Timestamp', '')
            
            slack_service = SlackService()
            if slack_signature and slack_timestamp:
                if not slack_service.verify_slack_signature(request_body, slack_timestamp, slack_signature):
                    app.logger.warning("Invalid Slack signature")
                    return jsonify({"text": "Unauthorized"}), 401
            
            # Parse command data
            command = form_data.get('command', '')
            text = form_data.get('text', '')
            user_name = form_data.get('user_name', 'Unknown')
            channel_id = form_data.get('channel_id', '')
            
            app.logger.info(f"Slack command received: {command} from {user_name}")
            
            # Handle commands
            handler = SlackCommandHandler()
            
            if command == '/optigenix-status':
                return jsonify(handler.handle_status_command())
            elif command == '/optigenix-optimize':
                return jsonify(handler.handle_optimize_command(text, user_name))
            else:
                return jsonify({
                    "response_type": "ephemeral",
                    "text": f"❌ Unknown command: {command}"
                })
                
        except Exception as e:
            app.logger.error(f"Error handling Slack command: {str(e)}")
            return jsonify({
                "response_type": "ephemeral",
                "text": "❌ Sorry, there was an error processing your command."
            })
    
    @app.route('/slack/oauth', methods=['GET'])
    def slack_oauth():
        """Handle Slack OAuth callback"""
        try:
            code = request.args.get('code')
            if not code:
                return "Missing authorization code", 400
            
            # Exchange code for token
            oauth_url = "https://slack.com/api/oauth.v2.access"
            payload = {
                "client_id": SlackConfig.CLIENT_ID,
                "client_secret": SlackConfig.CLIENT_SECRET,
                "code": code
            }
            
            response = requests.post(oauth_url, data=payload)
            oauth_data = response.json()
            
            if oauth_data.get("ok"):
                bot_token = oauth_data.get("access_token")
                app.logger.info(f"Slack OAuth successful. Bot token: {bot_token[:10]}...")
                return "✅ OptiGenix Bot installed successfully! You can now use slash commands."
            else:
                app.logger.error(f"Slack OAuth failed: {oauth_data}")
                return f"❌ OAuth failed: {oauth_data.get('error', 'Unknown error')}", 400
                
        except Exception as e:
            app.logger.error(f"Error in Slack OAuth: {str(e)}")
            return f"❌ OAuth error: {str(e)}", 500
    
    @app.route('/slack/test', methods=['POST'])
    def test_slack_integration():
        """Test endpoint for Slack integration"""
        try:
            slack_service = SlackService()
            
            # Test sending a message
            test_message = """🧪 *OptiGenix Bot Test*
            
✅ Bot is connected and working!
🚛 Container optimization system ready
💡 Try `/optigenix-status` to check system status"""
            
            # For testing, we'll return the message instead of sending
            return jsonify({
                "status": "success",
                "message": "Slack integration test successful",
                "test_message": test_message,
                "config": {
                    "client_id": SlackConfig.CLIENT_ID,
                    "has_bot_token": bool(SlackConfig.BOT_TOKEN),
                    "has_webhook": bool(SlackConfig.WEBHOOK_URL)
                }
            })
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500
    
    # Slack notification endpoint (called when optimization completes)
    @app.route('/slack/notify/optimization-complete', methods=['POST'])
    def notify_optimization_complete():
        """Send Slack notification when optimization completes"""
        try:
            data = request.get_json() or {}
            
            # Extract results
            efficiency = data.get('volume_utilization', 0)
            items_packed = data.get('items_packed', 0)
            total_items = data.get('total_items', 0)
            cost_savings = data.get('cost_savings', 0)
            user_name = data.get('user_name', 'System')
            
            # Create notification message
            message = f"""🎉 *Container Optimization Complete!*

👤 *Requested by:* {user_name}
📊 *Results:*
• Efficiency: {efficiency:.1f}%
• Items Packed: {items_packed}/{total_items}
• Estimated Savings: ₹{cost_savings:,}

🔗 *View Details:* Check the OptiGenix dashboard
⏰ *Completed:* {time.strftime('%Y-%m-%d %H:%M:%S')}"""
            
            # Send via webhook if available
            slack_service = SlackService()
            success = slack_service.send_webhook_notification(message)
            
            return jsonify({
                "success": success,
                "message": "Notification sent" if success else "Failed to send notification"
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # Dynamic URL information endpoint
    @app.route('/slack/urls', methods=['GET'])
    def get_slack_urls():
        """Get current dynamic URLs for Slack configuration"""
        try:
            base_url = AppConfig.get_ngrok_url()
            command_url = AppConfig.get_slack_command_url()
            
            # Check if ngrok is running
            is_ngrok = "ngrok" in base_url
            
            return jsonify({
                "status": "success",
                "urls": {
                    "base_url": base_url,
                    "slack_commands": command_url,
                    "slack_oauth": f"{base_url}/slack/oauth",
                    "slack_test": f"{base_url}/slack/test"
                },
                "ngrok": {
                    "active": is_ngrok,
                    "ready_for_mobile": is_ngrok
                },
                "instructions": {
                    "slack_app_url": "https://api.slack.com/apps/A096HEE7TGD/slash-commands",
                    "commands_to_update": [
                        {
                            "command": "/optigenix-status",
                            "new_url": command_url
                        },
                        {
                            "command": "/optigenix-optimize", 
                            "new_url": command_url
                        }
                    ]
                }
            })
            
        except Exception as e:
            app.logger.error(f"Error getting dynamic URLs: {str(e)}")
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500
    
    # JSON server control routes for AR visualization
    @app.route('/start_json_server', methods=['POST'])
    def start_json_server_handler():
        """Start the integrated JSON server for AR visualization"""
        try:
            # Use our integrated JSONServerService
            service = JSONServerService.get_instance()
            result = service.start_server()
            
            if result:
                # Return the fixed ngrok URL
                return jsonify({
                    'success': True,
                    'url': service.get_url(),
                    'message': 'JSON server started successfully'
                })
            else:
                raise Exception("Failed to start JSON server")
        except Exception as e:
            app.logger.error(f"Failed to start JSON server: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/stop_json_server', methods=['POST'])
    def stop_json_server_handler():
        """Stop the JSON server for AR visualization"""
        try:
            service = JSONServerService.get_instance()
            success = service.stop_server()
            return jsonify({
                'success': success
            })
        except Exception as e:
            app.logger.error(f"Error stopping JSON server: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/check_json_server_status')
    def check_json_server_status_handler():
        """Check the status of the JSON server for AR visualization"""
        service = JSONServerService.get_instance()
        is_running = service.is_running()
        response = {
            'running': is_running
        }
        
        if is_running:
            response['url'] = service.get_url()
        
        return jsonify(response)

    @app.route('/check_local_server', methods=['GET'])
    def check_local_server_handler():
        """Check if the local JSON server is running directly"""
        try:
            import requests
            
            # Try to connect to the local server using configured port
            local_url = f"http://localhost:{AppConfig.JSON_SERVER_PORT}/{AppConfig.STANDARD_JSON_FILENAME}"
            try:
                response = requests.get(local_url, timeout=2)
                if response.status_code == 200:
                    return jsonify({
                        'success': True,
                        'url': local_url,
                        'running': True
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': f"Server returned status code {response.status_code}",
                        'running': False
                    })
            except requests.RequestException as e:
                return jsonify({
                    'success': False,
                    'error': str(e),
                    'running': False
                })
        except Exception as e:
            app.logger.error(f"Error checking local server: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
                'running': False
            })    # Health check endpoint for Render
    @app.route('/health')
    def health_check():
        """Health check endpoint for deployment monitoring"""
        return jsonify({
            'status': 'healthy',
            'timestamp': time.time(),
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'version': '1.0.0'
        })
    
    # Server configuration endpoint for frontend
    @app.route('/api/server-config')
    def get_server_config():
        """Get server configuration for frontend"""
        render_service_name = os.environ.get('RENDER_SERVICE_NAME')
        if render_service_name:
            base_url = f"https://{render_service_name}.onrender.com"
        else:
            render_url = os.environ.get('RENDER_EXTERNAL_URL')
            if render_url:
                base_url = render_url
            else:
                port = AppConfig.get_port()
                base_url = f'http://localhost:{port}'
        
        return jsonify({
            'base_url': base_url,
            'is_production': AppConfig.is_production(),
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'port': AppConfig.get_port()
        })
    
    # Production API route for serving container plan JSON
    @app.route('/api/container_plan.json')
    def serve_container_plan():
        """Serve the latest container plan JSON for production"""
        try:
            service = JSONServerService.get_instance()
            service.update_json_file()
            
            # Read and return the JSON file
            with open(service.json_path, 'r') as file:
                data = json.load(file)
            
            return jsonify(data)
        except FileNotFoundError:
            return jsonify({'error': 'No container plan available'}), 404
        except Exception as e:
            app.logger.error(f"Error serving container plan: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    # Register blueprint
    app.register_blueprint(bp)
    
    # Error handlers
    @app.errorhandler(413)
    def too_large(e):
        return jsonify({
            'error': 'File is too large. Maximum size is 16MB'
        }), 413

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'error': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            'error': 'Internal server error occurred'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f'Unhandled exception: {str(e)}')
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500
        
    # Set up logging
    if not app.debug:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        # Set up file handler
        file_handler = RotatingFileHandler(
            'logs/container_packing.log', 
            maxBytes=AppConfig.LOG_MAX_BYTES,
            backupCount=AppConfig.LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Container Packing Web App startup with optigenix_module')
        
    return app

def create_socketio(app):
    """Create and configure SocketIO for the application"""
    socketio = SocketIO(app, async_mode='threading')
    
    @socketio.on('request_update')
    def handle_update_request():
        update_data = handle_socketio_update_request()
        if update_data:
            emit('container_update', update_data)
    
    @socketio.on('connect')
    def handle_connect():
        app.logger.info('Client connected to Socket.IO')
        emit('connection_status', {'status': 'connected'})
    
    @socketio.on('error')
    def handle_error(error):
        app.logger.error(f'Socket.IO error: {error}')
        emit('error', {'message': 'An error occurred with the realtime connection'})
            
    return socketio

import socket

def is_port_in_use(port):
    """Check if a port is already in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_route_temp_server():
    """Start the route temperature calculation server"""
    try:
        if not is_port_in_use(AppConfig.ROUTE_TEMP_PORT):
            route_temp_app.run(host='0.0.0.0', port=AppConfig.ROUTE_TEMP_PORT, debug=False, use_reloader=False)
        else:
            print(f"Route temperature server already running on port {AppConfig.ROUTE_TEMP_PORT}")
    except Exception as e:
        print(f"Failed to start route temperature server: {e}")

if __name__ == '__main__':
    app = create_app()
    socketio = create_socketio(app)
    
    # Get port from environment (Render requirement)
    port = AppConfig.get_port()
    
    # Initialize Socket Mode for 100% automated Slack integration
    print("🔗 Initializing Slack Socket Mode...")
    socket_mode = get_socket_mode()
    if socket_mode.bot_app and socket_mode.app_token:
        socket_mode.start_socket_mode()
        print("🎉 Socket Mode active - Zero manual URL configuration!")
    else:
        print("⚠️ Socket Mode not configured. Using HTTP endpoints.")
        print("💡 For 100% automation, set SLACK_APP_TOKEN in .env")
    
    try:
        # In production, don't start additional processes
        if not AppConfig.is_production():
            # Only start route temp server in development
            if not is_port_in_use(AppConfig.ROUTE_TEMP_PORT):
                try:
                    route_temp_process = multiprocessing.Process(target=start_route_temp_server)
                    route_temp_process.daemon = True
                    route_temp_process.start()
                    print(f"Route temperature server started at http://localhost:{AppConfig.ROUTE_TEMP_PORT}")
                except Exception as e:
                    print(f"Warning: Could not start route temperature server: {e}")
        
        # Run main application
        debug_mode = not AppConfig.is_production()
        print(f"Starting application on port {port}")
        if AppConfig.is_production():
            print("Running in production mode")
        else:
            print("Enhanced with LLM-powered dynamic fitness function and adaptive mutation")
        
        print("\n🚀 OptiGenix Ready!")
        print("=" * 50)
        print(f"📊 Web Dashboard: http://localhost:{port}")
        if socket_mode.is_running:
            print("⚡ Slack Commands: Ready (100% automated)")
        else:
            print(f"⚡ Slack Commands: {AppConfig.get_slack_command_url()}")
        print("📱 Mobile: Ready for testing")
        print("⚠️  Keep terminal open during demo")
        
        socketio.run(app, debug=debug_mode, host='0.0.0.0', port=port, use_reloader=False)
    except Exception as e:
        print(f"Failed to start application: {e}")
        raise