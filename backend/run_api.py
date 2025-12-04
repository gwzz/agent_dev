"""Improved startup script for the API service."""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


def main():
    """Start the FastAPI service with proper configuration."""
    import uvicorn
    from api.config import get_settings
    from api.logging_config import setup_logging
    
    # Setup logging first
    setup_logging()
    
    # Get settings
    settings = get_settings()
    
    # Check for required API keys
    if not settings.google_api_key:
        print("WARNING: GOOGLE_API_KEY not set in environment variables")
        print("Please set GOOGLE_API_KEY in your .env file or environment")
    
    if not settings.openweather_api_key:
        print("WARNING: OPENWEATHER_API_KEY not set in environment variables")
        print("Weather functionality may not work properly")
    
    # Run the server
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
