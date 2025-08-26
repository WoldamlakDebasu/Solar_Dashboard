#!/usr/bin/env python3
"""
SolarSense Pro - Automated Setup Script
This script automates the installation and setup of the Solar IoT Dashboard.
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

def print_banner():
    """Print the SolarSense Pro banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    SolarSense Pro                            ║
    ║                Solar IoT Dashboard                           ║
    ║                                                              ║
    ║              Professional Setup Assistant                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def check_system_requirements():
    """Check system requirements."""
    print("\n🔍 Checking system requirements...")
    
    # Check operating system
    os_name = platform.system()
    print(f"✅ Operating System: {os_name} {platform.release()}")
    
    # Check available disk space (simplified check)
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        free_gb = free // (1024**3)
        if free_gb < 1:
            print("⚠️  Warning: Less than 1GB free disk space available")
        else:
            print(f"✅ Available disk space: {free_gb}GB")
    except:
        print("⚠️  Could not check disk space")

def create_virtual_environment():
    """Create and activate virtual environment."""
    print("\n🔧 Setting up virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return str(venv_path)
    
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created successfully")
        return str(venv_path)
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        sys.exit(1)

def get_pip_command(venv_path):
    """Get the pip command for the virtual environment."""
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "pip")
    else:
        return os.path.join(venv_path, "bin", "pip")

def install_dependencies(venv_path):
    """Install Python dependencies."""
    print("\n📦 Installing dependencies...")
    
    pip_cmd = get_pip_command(venv_path)
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ Error: {requirements_file} not found")
        sys.exit(1)
    
    try:
        # Upgrade pip first
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True, capture_output=True)
        print("✅ pip upgraded successfully")
        
        # Install requirements
        result = subprocess.run([pip_cmd, "install", "-r", requirements_file], 
                              check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        sys.exit(1)

def setup_database():
    """Initialize the database."""
    print("\n🗄️  Setting up database...")
    
    db_dir = Path("src/database")
    db_dir.mkdir(exist_ok=True)
    
    # Database will be created automatically when the app starts
    print("✅ Database directory prepared")

def create_startup_scripts():
    """Create convenient startup scripts."""
    print("\n📝 Creating startup scripts...")
    
    # Create start script for Unix-like systems
    if platform.system() != "Windows":
        start_script = """#!/bin/bash
echo "Starting SolarSense Pro..."
cd "$(dirname "$0")"
source venv/bin/activate
python src/main.py
"""
        with open("start.sh", "w") as f:
            f.write(start_script)
        os.chmod("start.sh", 0o755)
        print("✅ Created start.sh")
    
    # Create start script for Windows
    start_bat = """@echo off
echo Starting SolarSense Pro...
cd /d "%~dp0"
call venv\\Scripts\\activate
python src\\main.py
pause
"""
    with open("start.bat", "w") as f:
        f.write(start_bat)
    print("✅ Created start.bat")

def run_initial_test():
    """Run a quick test to ensure everything is working."""
    print("\n🧪 Running initial tests...")
    
    try:
        # Test import of main modules
        sys.path.insert(0, 'src')
        
        # Test Flask import
        import flask
        print("✅ Flask import successful")
        
        # Test other critical imports
        import sqlite3
        print("✅ SQLite3 available")
        
        print("✅ All critical components available")
        
    except ImportError as e:
        print(f"⚠️  Warning: Some components may not be properly installed: {e}")
    except Exception as e:
        print(f"⚠️  Warning: Test failed: {e}")

def print_completion_message():
    """Print setup completion message with next steps."""
    message = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                 🎉 Setup Complete! 🎉                        ║
    ║                                                              ║
    ║  SolarSense Pro is now ready to use!                        ║
    ║                                                              ║
    ║  Next Steps:                                                 ║
    ║  1. Start the application:                                   ║
    """
    
    if platform.system() == "Windows":
        message += """    ║     • Double-click start.bat                                ║
    ║     • Or run: python src/main.py                            ║"""
    else:
        message += """    ║     • Run: ./start.sh                                       ║
    ║     • Or run: python src/main.py                            ║"""
    
    message += """
    ║                                                              ║
    ║  2. Open your browser and go to:                            ║
    ║     http://localhost:5000                                    ║
    ║                                                              ║
    ║  3. Explore the dashboard features:                          ║
    ║     • Real-time solar monitoring                             ║
    ║     • AI-powered insights                                    ║
    ║     • Energy analytics                                       ║
    ║     • System health monitoring                               ║
    ║                                                              ║
    ║  For help and documentation:                                 ║
    ║  • README.md - Complete user guide                          ║
    ║  • DEPLOYMENT.md - Deployment instructions                  ║
    ║                                                              ║
    ║  Support: support@solarsense.ae                             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(message)

def main():
    """Main setup function."""
    print_banner()
    
    try:
        # Check system requirements
        check_python_version()
        check_system_requirements()
        
        # Setup virtual environment
        venv_path = create_virtual_environment()
        
        # Install dependencies
        install_dependencies(venv_path)
        
        # Setup database
        setup_database()
        
        # Create startup scripts
        create_startup_scripts()
        
        # Run tests
        run_initial_test()
        
        # Print completion message
        print_completion_message()
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        print("\nPlease check the error message above and try again.")
        print("If the problem persists, contact support@solarsense.ae")
        sys.exit(1)

if __name__ == "__main__":
    main()

