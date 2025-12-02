# Agent Development Backend

This backend project demonstrates the development of AI agents using the Google ADK (Agent Development Kit). It includes multiple specialized agents with different capabilities for handling user queries. The system now includes both the original ADK-based agents and a FastAPI service for web-based access.

## Project Structure

- `city_info_expert/`: High-level exports for the city information expert agent
- `crypto_expert/`: Cryptocurrency analysis and trading agent
- `agent_tools/`: Shared tools for various agent capabilities
  - `services/weather.py`: OpenWeatherMap client utilities
  - `services/time.py`: Timezone calculations and time management
  - `services/timezones.py`: Timezone data and conversions
  - `services/location.py`: Coordinate lookups via OpenStreetMap
  - `services/population.py`: Wikipedia-based population scraping
- `crypto_tools/`: Tools for cryptocurrency analysis
  - `services/price.py`: Cryptocurrency price lookup via CoinGecko API
- `api/`: FastAPI service implementation
  - `main.py`: Main FastAPI application with endpoints for all agent experts
- `main.py`: Entry point for both ADK and FastAPI services
- `pyproject.toml`: Project dependencies and configuration
- `agent_dev.egg-info/`: Package information
- `debug_detailed.py`: Detailed agent debugging script
- `debug_population.py`: Population lookup debugging script
- `test_crypto_agent.py`: Tests for cryptocurrency agent
- `test_crypto.py`: Additional cryptocurrency tests
- `test_multiple_cities.py`: Tests for multi-city operations

## Features

### City Information Expert
- **Real-time Weather Information**: Get current weather for any city worldwide
  - Temperature (Celsius/Fahrenheit)
  - Weather description
  - Humidity
  - "Feels like" temperature
- **Current Time in Any City**: Accurate time with timezone information
- **Time Conversion**: Convert time between different cities/regions
  - Current time conversion
  - Specific time conversion (HH:MM format)
- **Geographical Coordinates**: Get latitude and longitude for any city
  - Returns precise coordinates
  - Includes full address information
- **Population Lookup**: Retrieve approximate population information for major cities using Wikipedia parsing

### Cryptocurrency Expert
- **Cryptocurrency Analysis**: Real-time cryptocurrency market data
- **Price Tracking**: Detailed price information for various cryptocurrencies
- **Market Trends**: Insights into market movements and trends

### General Agent Tools
- **Weather Services**: Integration with OpenWeatherMap API
- **Time Services**: Accurate timezone conversion and time calculations
- **Location Services**: Coordinate lookups via OpenStreetMap
- **Population Services**: City population data from Wikipedia

## Setup

1. **Install dependencies**:
   ```bash
   pip install -e .
   ```

2. **Set up API keys**:
   - For weather data, you need an OpenWeatherMap API key
   - For Google AI services, you need a Google API key
   - Create a `.env` file in the backend directory with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

## Running the Service

### Using the Main Entry Point

The main entry point supports both the original ADK server and the new FastAPI service:

- To run the original ADK server:
  ```bash
  python main.py adk
  ```

- To run the FastAPI service:
  ```bash
  python main.py api
  # or
  python main.py fastapi
  ```

### Using Dedicated Scripts

- To run the FastAPI service directly:
  ```bash
  python start_api.py
  ```

- To run the FastAPI service in development mode with auto-reload:
  ```bash
  python start_dev.py
  ```

- Using the batch scripts:
  - For production: `start_api.bat`
  - For development: `start_dev.bat`

### Direct Uvicorn Command

- To run with uvicorn directly:
  ```bash
  uvicorn api.main:app --host 0.0.0.0 --port 8000
  ```

- For development with auto-reload:
  ```bash
  uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
  ```

## FastAPI Endpoints

When running the FastAPI service, the following endpoints are available:

- `GET /` - API root information
- `POST /city-info` - Query the city information expert agent
- `POST /crypto` - Query the cryptocurrency expert agent
- `GET /weather/{city}` - Get weather for a specific city
- `GET /time/{city}` - Get current time for a specific city
- `GET /coordinates/{city}` - Get coordinates for a specific city
- `GET /population/{city}` - Get population for a specific city
- `GET /crypto-price/{crypto}` - Get current price for a cryptocurrency
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Example API Usage

1. Query the city info expert:
   ```bash
   curl -X POST "http://localhost:8000/city-info" -H "Content-Type: application/json" -d '{"query": "What is the weather in London?"}'
   ```

2. Get weather directly:
   ```bash
   curl "http://localhost:8000/weather/London"
   ```

3. Query the crypto expert:
   ```bash
   curl -X POST "http://localhost:8000/crypto" -H "Content-Type: application/json" -d '{"query": "What is the price of Bitcoin?"}'
   ```

4. Get crypto price directly:
   ```bash
   curl "http://localhost:8000/crypto-price/bitcoin"
   ```

### Enhanced API Documentation

The API includes comprehensive documentation with the following features:
- Detailed endpoint summaries and descriptions
- Request/response examples for each endpoint
- Input/output models with field descriptions
- Status code documentation with example responses
- Interactive API playground at `/docs`
- Alternative documentation at `/redoc`

To access the interactive API documentation:
1. Start the service: `python main.py api`
2. Visit `http://localhost:8000/docs` in your browser
3. Use the interactive interface to test endpoints

## Architecture

The backend follows a modular architecture:
- **Agent Modules**: Separate modules for different agent specializations
- **Service Layer**: Common tools available to all agents
- **Agent Development Kit**: Google ADK for creating and running agents
- **FastAPI Service Layer**: Web API for frontend integration
- **External Service Integration**: APIs for weather, location, and data services

## Testing

Run the full test suite:

```bash
pytest
```

Run specific tests:
```bash
# For cryptocurrency agent tests
python test_crypto_agent.py

# For population lookup tests
python debug_population.py

# For multi-city tests
python test_multiple_cities.py
```

## Requirements

- Python 3.11+
- Google ADK
- Google Generative AI
- FastAPI
- Uvicorn
- Requests
- Geopy
- Wikipedia API

## Debugging

Several debugging scripts are available:
- `debug_detailed.py`: For detailed agent debugging and testing
- `debug_population.py`: For testing population lookup functionality
- `test_crypto_agent.py`: For testing cryptocurrency agent functionality

## Development

To add new tools:
1. Create the service in `agent_tools/services/` or `crypto_tools/services/`
2. Add the necessary imports to the module's `__init__.py` file
3. Consider how the new tool might be used by the existing agents

To add new agents:
1. Create a new agent module similar to `city_info_expert` or `crypto_expert`
2. Define the agent's capabilities and tools
3. Export the agent's main interface in the module's `__init__.py`
4. Add endpoints to the FastAPI service in `api/main.py`

## License

Add your license information here.