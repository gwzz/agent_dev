#!/usr/bin/env python3
"""
API Documentation Enhancement Test

This script demonstrates the enhanced API documentation with examples and detailed descriptions.
After running the API with `python -m uvicorn api.main:app --reload`, 
visit http://localhost:8000/docs to see the improved documentation.
"""

import json
from api.main import QueryRequest

def show_api_examples():
    print("Enhanced API Documentation Examples")
    print("=" * 50)
    
    # Example for city-info endpoint
    print("\n1. City Info Expert Agent Endpoint")
    print("   POST /city-info")
    print("   Content-Type: application/json")
    print("   Request body example:")
    city_request = QueryRequest(query="What is the weather in London?")
    print(f"   {city_request.model_dump()}")
    print("\n   This endpoint will process your query about cities (weather, time, coordinates, population)")
    
    # Example for crypto endpoint  
    print("\n2. Cryptocurrency Expert Agent Endpoint")
    print("   POST /crypto")
    print("   Content-Type: application/json")
    print("   Request body example:")
    crypto_request = QueryRequest(query="What is the price of Bitcoin?")
    print(f"   {crypto_request.model_dump()}")
    print("\n   This endpoint will process your queries about cryptocurrency prices and market data")
    
    # Examples for direct service endpoints
    print("\n3. Direct Service Endpoints")
    print("   GET /weather/{city} - e.g., /weather/London")
    print("   GET /time/{city} - e.g., /time/New York")
    print("   GET /coordinates/{city} - e.g., /coordinates/Paris")
    print("   GET /population/{city} - e.g., /population/Tokyo")
    print("   GET /crypto-price/{crypto} - e.g., /crypto-price/bitcoin")
    
    print("\nThe API now includes:")
    print("• Detailed endpoint summaries and descriptions")
    print("• Request/response examples for each endpoint")
    print("• Input/output models with field descriptions")
    print("• Status code documentation with example responses")
    print("• Interactive API documentation at /docs")
    print("• Alternative documentation at /redoc")

if __name__ == "__main__":
    show_api_examples()