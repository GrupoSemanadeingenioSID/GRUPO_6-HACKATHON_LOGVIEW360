#!/usr/bin/env python3

import os
import sys
import subprocess
from utils.config import API_HOST, API_PORT

def clean_environment():
    """Clean potentially problematic environment variables."""
    problematic_vars = [
        'ELECTRON_RUN_AS_NODE',
        'ELECTRON_NO_ATTACH_CONSOLE',
        'CHROME_DESKTOP',
        'CHROME_VERSION'
    ]
    for var in problematic_vars:
        if var in os.environ:
            del os.environ[var]

def setup_environment():
    """Setup the Python path and environment variables."""
    # Clean environment first
    clean_environment()
    
    # Add the current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

def main():
    """Main entry point for the application."""
    setup_environment()
    
    # Build the uvicorn command
    cmd = [
        "uvicorn",
        "api.core.app:app",
        "--host", API_HOST,
        "--port", str(API_PORT),
        "--reload"
    ]
    
    try:
        # Execute uvicorn directly
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 