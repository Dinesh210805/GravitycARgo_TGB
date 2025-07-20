#!/usr/bin/env python3
"""
📱 Start HTTPS Server for Mobile Access
======================================
Quick launcher for HTTPS mobile access
"""

import os
import sys
import subprocess
from pathlib import Path

def start_https_server():
    """Start the HTTPS server for mobile access"""
    script_dir = Path(__file__).parent
    https_server_path = script_dir / "https_server.py"
    
    if not https_server_path.exists():
        print("❌ https_server.py not found!")
        return False
    
    print("🚀 Starting HTTPS server for mobile access...")
    print("📱 Mobile devices can access: https://10.1.3.41:5443/")
    print("💡 Make sure your mobile device is on the same network!")
    print()
    
    try:
        # Start HTTPS server
        subprocess.run([sys.executable, str(https_server_path)], check=True)
    except KeyboardInterrupt:
        print("\n👋 HTTPS server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_https_server()
