#!/usr/bin/env python3
"""
Startup script for Healo Mental Health Chatbot
Runs both the Flask API server and serves the frontend
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def start_api_server():
    """Start the Flask API server"""
    print("Starting AI Backend Server...")
    try:
        subprocess.run([sys.executable, "api_server.py"])
    except KeyboardInterrupt:
        print("\nShutting down API server...")

def open_browser():
    """Open browser after a short delay"""
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:5000")
        print("✓ Browser opened to http://localhost:5000")
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print("Please manually open http://localhost:5000 in your browser")

def main():
    """Main startup function"""
    print("=" * 60)
    print("🤖 HEALO - AI Mental Health Chatbot")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("api_server.py"):
        print("✗ Error: Please run this script from the Healo project directory")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("✗ Failed to install requirements. Please install manually:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🚀 Starting Healo Chatbot...")
    print("=" * 60)
    print("Frontend: http://localhost:5000")
    print("API: http://localhost:5000/api")
    print("Chatbot: http://localhost:5000/chatbot.html")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start browser in a separate thread
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the API server
    try:
        start_api_server()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Healo Chatbot...")
        print("Thank you for using Healo! Take care of your mental health. 💚")

if __name__ == "__main__":
    main()
