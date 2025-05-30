#!/usr/bin/env python3

import os
import sys
import uvicorn

def setup_environment():
    """Setup the Python path and environment variables."""
    # Add the current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

def main():
    """Main entry point for the application."""
    setup_environment()
    
    # Run the FastAPI application
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 