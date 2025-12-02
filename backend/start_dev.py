#!/usr/bin/env python3
"""Development script to start the FastAPI service with auto-reload."""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Change to the backend directory if needed
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Install the package in development mode
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
    
    # Start the FastAPI server in development mode with auto-reload
    print("Starting FastAPI server in development mode...")
    subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"], check=True)

if __name__ == "__main__":
    main()