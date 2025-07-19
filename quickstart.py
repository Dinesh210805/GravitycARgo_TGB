#!/usr/bin/env python3
"""
🎯 OptiGenix Quick Start
=======================
One-click solution to start everything
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def main():
    """Quick start everything"""
    print("🚀 OptiGenix Quick Start")
    print("=" * 40)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("📁 Working directory:", script_dir)
    print("🔍 Starting auto-starter...")
    print()
    
    try:
        # Start the auto-starter
        subprocess.run([sys.executable, "auto_start.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutdown requested")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print("\n💡 Try running manually: python auto_start.py")
    except FileNotFoundError:
        print("❌ auto_start.py not found")
        print("💡 Make sure you're in the correct directory")

if __name__ == "__main__":
    main()
