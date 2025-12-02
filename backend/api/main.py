"""FastAPI service for AI agent experts."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.adk.agents import Agent
import os
import asyncio
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

# Load environment variables from .env file if present
load_dotenv()

import google.generativeai as genai

# Set up Google API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Import agent experts
from city_info_expert.agent import root_agent as city_info_agent
from crypto_expert.agent import root_agent as crypto_agent
from law_expert.agent import root_agent as law_agent

class QueryRequest(BaseModel):
    query: str

class CityInfoResponse(BaseModel):
    status: str
    result: dict

class CryptoResponse(BaseModel):
    status: str
    result: dict

class LawResponse(BaseModel):
    status: str
    result: dict

app = FastAPI(
    title="AI Agent Experts API",
    description="API service for multiple AI agent experts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",
         summary="API Root",
         description="Returns basic information about the API and available endpoints")
async def root():
    """
    Root endpoint for the API.

    Returns:
        - message: Welcome message
        - endpoints: Available API endpoints
    """
    return {
        "message": "AI Agent Experts API",
        "endpoints": {
            "/city-info": "City information expert agent",
            "/crypto": "Cryptocurrency expert agent",
            "/law": "Legal expert agent",
            "/docs": "Interactive API documentation (Swagger UI)",
            "/redoc": "Alternative API documentation (ReDoc)"
        },
        "description": "This API provides access to AI agents for city information, cryptocurrency data, and legal expertise."
    }

@app.post("/city-info",
          summary="City Information Expert Agent",
          description="Query the city information expert agent for weather, time, coordinates, and population data for cities",
          responses={
              200: {
                  "description": "Successfully processed the query",
                  "content": {
                      "application/json": {
                          "example": {
                              "status": "success",
                              "result": {
                                  "content": "The current weather in London is clear sky with a temperature of 18.5°C (65.3°F). It feels like 18.5°C. Humidity is 65%.",
                                  "usage": {"prompt_tokens": 50, "completion_tokens": 120, "total_tokens": 170}
                              }
                          }
                      }
                  }
              }
          })
async def city_info_agent_endpoint(request: QueryRequest):
    """
    Endpoint for the city information expert agent.

    This agent can answer questions about:
    - Weather information for cities
    - Current time in cities
    - Time conversion between cities
    - Geographic coordinates
    - City population data

    Args:
        query (str): The query to send to the city information expert agent

    Returns:
        dict: The agent's response

    Example:
        Input: {"query": "What is the weather in London?"}
        Output: {"status": "success", "result": {...}}
    """
    try:
        # Run the agent with the query
        result = city_info_agent.run(request.query)
        return CityInfoResponse(status="success", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running city info agent: {str(e)}")

@app.post("/crypto",
          summary="Cryptocurrency Expert Agent",
          description="Query the cryptocurrency expert agent for cryptocurrency prices and market information",
          responses={
              200: {
                  "description": "Successfully processed the query",
                  "content": {
                      "application/json": {
                          "example": {
                              "status": "success",
                              "result": {
                                  "content": "The current price of Bitcoin (bitcoin) is $43,567.89 USD.",
                                  "usage": {"prompt_tokens": 40, "completion_tokens": 100, "total_tokens": 140}
                              }
                          }
                      }
                  }
              }
          })
async def crypto_agent_endpoint(request: QueryRequest):
    """
    Endpoint for the cryptocurrency expert agent.

    This agent can answer questions about:
    - Cryptocurrency prices
    - Market trends
    - Price comparisons

    Args:
        query (str): The query to send to the cryptocurrency expert agent

    Returns:
        dict: The agent's response

    Example:
        Input: {"query": "What is the price of Bitcoin?"}
        Output: {"status": "success", "result": {...}}
    """
    try:
        # Run the agent with the query
        result = crypto_agent.run(request.query)
        return CryptoResponse(status="success", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running crypto agent: {str(e)}")

@app.post("/law",
          summary="Legal Expert Agent",
          description="Query the legal expert agent for information about jurisdictions, statutes, recent cases, and legal definitions",
          responses={
              200: {
                  "description": "Successfully processed the query",
                  "content": {
                      "application/json": {
                          "example": {
                              "status": "success",
                              "result": {
                                  "content": "Based on legal information, the jurisdiction of federal courts includes matters involving federal law, constitutional issues, and interstate commerce. The federal court system consists of Supreme Court, Circuit Courts of Appeal, and District Courts.",
                                  "usage": {"prompt_tokens": 60, "completion_tokens": 140, "total_tokens": 200}
                              }
                          }
                      }
                  }
              }
          })
async def law_agent_endpoint(request: QueryRequest):
    """
    Endpoint for the legal expert agent.

    This agent can answer questions about:
    - Legal jurisdictions and court systems
    - Specific statutes and laws
    - Recent significant legal cases
    - Legal definitions and terminology

    Args:
        query (str): The query to send to the legal expert agent

    Returns:
        dict: The agent's response

    Example:
        Input: {"query": "What is due process?"}
        Output: {"status": "success", "result": {...}}
    """
    try:
        # Run the agent with the query
        result = law_agent.run(request.query)
        return LawResponse(status="success", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running law agent: {str(e)}")

# Individual service endpoints for direct access to tools
@app.get("/weather/{city}",
         summary="Get Weather Information",
         description="Get current weather information for a specific city",
         responses={
             200: {
                 "description": "Weather information for the requested city",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "report": "The current weather in London is clear sky with a temperature of 18.5°C (65.3°F). It feels like 18.5°C. Humidity is 65%.",
                             "temperature_celsius": 18.5,
                             "temperature_fahrenheit": 65.3,
                             "description": "clear sky",
                             "humidity": 65,
                             "feels_like": 18.5
                         }
                     }
                 }
             },
             400: {
                 "description": "Error retrieving weather information",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "error_message": "Weather API key not configured. Please set OPENWEATHER_API_KEY."
                         }
                     }
                 }
             }
         })
async def get_weather(city: str):
    """
    Get weather information for a specific city.

    Args:
        city (str): The name of the city to get weather for

    Returns:
        dict: Weather information for the city

    Example:
        Input: city = "London"
        Output: {
            "status": "success",
            "report": "The current weather in London is clear sky with a temperature of 18.5°C (65.3°F)...",
            "temperature_celsius": 18.5,
            "temperature_fahrenheit": 65.3,
            "description": "clear sky",
            "humidity": 65,
            "feels_like": 18.5
        }
    """
    try:
        from agent_tools.services import get_weather
        result = get_weather(city)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving weather: {str(e)}")

@app.get("/time/{city}",
         summary="Get Current Time",
         description="Get current local time for a specific city",
         responses={
             200: {
                 "description": "Current time information for the requested city",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "report": "The current time in London is 2023-06-15 14:30:45 BST",
                             "timezone": "Europe/London",
                             "datetime": "2023-06-15T14:30:45+01:00"
                         }
                     }
                 }
             }
         })
async def get_time(city: str):
    """
    Get current time for a specific city.

    Args:
        city (str): The name of the city to get time for

    Returns:
        dict: Time information for the city

    Example:
        Input: city = "London"
        Output: {
            "status": "success",
            "report": "The current time in London is 2023-06-15 14:30:45 BST",
            "timezone": "Europe/London",
            "datetime": "2023-06-15T14:30:45+01:00"
        }
    """
    try:
        from agent_tools.services import get_current_time
        result = get_current_time(city)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving time: {str(e)}")

@app.get("/coordinates/{city}",
         summary="Get Geographic Coordinates",
         description="Get latitude and longitude for a specific city",
         responses={
             200: {
                 "description": "Coordinates information for the requested city",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "city": "London",
                             "latitude": 51.5074,
                             "longitude": -0.1278,
                             "address": "London, Greater London, England, UK"
                         }
                     }
                 }
             }
         })
async def get_coordinates(city: str):
    """
    Get geographic coordinates for a specific city.

    Args:
        city (str): The name of the city to get coordinates for

    Returns:
        dict: Latitude and longitude for the city

    Example:
        Input: city = "London"
        Output: {
            "status": "success",
            "city": "London",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "address": "London, Greater London, England, UK"
        }
    """
    try:
        from agent_tools.services import get_coordinates
        result = get_coordinates(city)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving coordinates: {str(e)}")

@app.get("/population/{city}",
         summary="Get Population Information",
         description="Get population information for a specific city from Wikipedia",
         responses={
             200: {
                 "description": "Population information for the requested city",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "city": "London",
                             "population": "9 million",
                             "summary_text": "London is the capital and largest city of England and the United Kingdom, with a population of approximately 9 million..."
                         }
                     }
                 }
             }
         })
async def get_population(city: str):
    """
    Get population information for a specific city.

    Args:
        city (str): The name of the city to get population for

    Returns:
        dict: Population information for the city

    Example:
        Input: city = "London"
        Output: {
            "status": "success",
            "city": "London",
            "population": "9 million",
            "summary_text": "London is the capital and largest city of England and the United Kingdom..."
        }
    """
    try:
        from agent_tools.services import get_city_population
        result = get_city_population(city)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving population: {str(e)}")

@app.get("/crypto-price/{crypto}",
         summary="Get Cryptocurrency Price",
         description="Get current price for a specific cryptocurrency in USD",
         responses={
             200: {
                 "description": "Price information for the requested cryptocurrency",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "report": "The current price of bitcoin (bitcoin) is $43,567.89 USD.",
                             "crypto": "bitcoin",
                             "crypto_id": "bitcoin",
                             "price_usd": 43567.89
                         }
                     }
                 }
             }
         })
async def get_crypto_price(crypto: str):
    """
    Get current price for a specific cryptocurrency.

    Args:
        crypto (str): The name or symbol of the cryptocurrency (e.g., 'bitcoin', 'btc', 'ethereum', 'eth')

    Returns:
        dict: Price information for the cryptocurrency

    Example:
        Input: crypto = "bitcoin"
        Output: {
            "status": "success",
            "report": "The current price of bitcoin (bitcoin) is $43,567.89 USD.",
            "crypto": "bitcoin",
            "crypto_id": "bitcoin",
            "price_usd": 43567.89
        }
    """
    try:
        from crypto_tools.services import get_crypto_price
        result = get_crypto_price(crypto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving crypto price: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)