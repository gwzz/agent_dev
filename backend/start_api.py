#!/usr/bin/env python3
"""Script to start the FastAPI service."""

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
    
    # Start the FastAPI server
    print("Starting FastAPI server...")
    subprocess.run([sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"], check=True)

if __name__ == "__main__":
    main()