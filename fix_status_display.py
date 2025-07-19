#!/usr/bin/env python3
"""
Quick fix for server status display issues
"""

import re

def fix_status_display():
    """Fix encoding issues in server status display"""
    
    # Read the current file
    with open('app_modular.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the route status issues
    content = content.replace('� Issues"', '🟡 Issues"')
    content = content.replace('�🔴 Stopped"', '🔴 Stopped"')
    
    # Write back the file
    with open('app_modular.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed server status display issues")

if __name__ == "__main__":
    fix_status_display()
