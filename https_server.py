#!/usr/bin/env python3
"""
🔒 HTTPS Flask Server for Mobile Access
======================================
Enables HTTPS access to the 3D visualization dashboard from mobile devices
"""

import os
import sys
import ssl
import socket
from pathlib import Path
from OpenSSL import SSL, crypto
from datetime import datetime, timedelta

def generate_self_signed_cert():
    """Generate self-signed SSL certificate for local HTTPS access"""
    cert_dir = Path("ssl_certs")
    cert_dir.mkdir(exist_ok=True)
    
    cert_file = cert_dir / "cert.pem"
    key_file = cert_dir / "key.pem"
    
    # Check if certificates already exist
    if cert_file.exists() and key_file.exists():
        print("✅ SSL certificates already exist")
        return str(cert_file), str(key_file)
    
    print("🔐 Generating self-signed SSL certificate for HTTPS access...")
    
    # Create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)
    
    # Create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "OptiGenix"
    cert.get_subject().L = "Container"
    cert.get_subject().O = "OptiGenix"
    cert.get_subject().OU = "Container Optimization"
    cert.get_subject().CN = get_local_ip()
    
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Valid for 1 year
    
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    
    # Save certificate and key
    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    
    print(f"✅ SSL certificate generated:")
    print(f"   📄 Certificate: {cert_file}")
    print(f"   🔑 Private Key: {key_file}")
    
    return str(cert_file), str(key_file)

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "localhost"

def create_https_context():
    """Create SSL context for HTTPS server"""
    cert_file, key_file = generate_self_signed_cert()
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    
    return context

def start_https_server():
    """Start the Flask app with HTTPS support"""
    try:
        # Import Flask app
        from app_modular import create_app
        
        app = create_app()
        
        # Get local IP for mobile access
        local_ip = get_local_ip()
        port = 5443  # HTTPS port (443 requires admin privileges)
        
        # Create SSL context
        context = create_https_context()
        
        print("🚀 STARTING OPTIGENIX HTTPS SERVER")
        print("=" * 50)
        print(f"🌐 Local Access: https://localhost:{port}")
        print(f"📱 Mobile Access: https://{local_ip}:{port}")
        print(f"🔒 SSL Certificate: Self-signed (browsers will show warning)")
        print("📋 Note: Accept the security warning on mobile browsers")
        print("⚠️  Keep this terminal open during operation")
        
        # Start the server
        app.run(
            host="0.0.0.0",  # Allow external connections
            port=port,
            ssl_context=context,
            debug=False,
            threaded=True
        )
        
    except ImportError:
        print("❌ Cannot import Flask app. Make sure app_modular.py exists.")
        return False
    except Exception as e:
        print(f"❌ Error starting HTTPS server: {e}")
        return False

if __name__ == "__main__":
    print("🔒 OptiGenix HTTPS Server Setup")
    print("=" * 40)
    
    # Check for required dependencies
    try:
        import OpenSSL
        print("✅ OpenSSL available")
    except ImportError:
        print("❌ OpenSSL not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyOpenSSL"])
        import OpenSSL
    
    start_https_server()
