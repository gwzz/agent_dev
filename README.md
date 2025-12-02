# Agent Development Project

This is a comprehensive AI agent development platform featuring multiple specialized agents for different domains. The project is structured with a backend server handling AI agent logic and a frontend interface for user interaction.

## Project Structure

- `backend/`: Contains the AI agent server and various specialized agents
  - `city_info_expert/`: High-level exports for the city information expert agent
  - `crypto_expert/`: Cryptocurrency analysis and trading agent
  - `agent_tools/`: Shared tools for various agent capabilities
    - `services/weather.py`: OpenWeatherMap client utilities
    - `services/time.py`: Timezone calculations and time management
    - `services/timezones.py`: Timezone data and conversions
    - `services/location.py`: Coordinate lookups via OpenStreetMap
    - `services/population.py`: Wikipedia-based population scraping
  - `main.py`: Entry point for the backend application
  - `pyproject.toml`: Project dependencies and configuration
- `frontend/`: Next.js-based web interface for interacting with agents
  - Built with Next.js, TypeScript, and modern web technologies

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

## Tech Stack

### Backend
- Python 3.11+
- Google Agent Development Kit (ADK)
- LiteLLM
- Requests
- Geopy
- Wikipedia API

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS

## Setup

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set up API keys for external services:
   - For weather data, you need an OpenWeatherMap API key
   - Create a `.env` file in `agent_tools/services/` with your API keys:
   ```
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

### Backend API Service
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set up API keys (as needed):
   - Create a `.env` file with your API keys (GOOGLE_API_KEY, OPENWEATHER_API_KEY)

4. Run the FastAPI service:
   ```bash
   python main.py api
   # or use uvicorn directly:
   uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```

5. Access the API at [http://localhost:8000](http://localhost:8000) with endpoints:
   - `/city-info` - City information expert agent
   - `/crypto` - Cryptocurrency expert agent
   - `/weather/{city}` - Direct weather lookup
   - `/time/{city}` - Direct time lookup
   - `/coordinates/{city}` - Direct coordinates lookup
   - `/population/{city}` - Direct population lookup
   - `/crypto-price/{crypto}` - Direct crypto price lookup
   - `/docs` - Interactive API documentation (Swagger UI)
   - `/redoc` - Alternative API documentation (ReDoc)

## Development

### Running Backend Tests
```bash
cd backend
pytest
```

### Debugging Scripts
The backend includes several debugging scripts:
- `debug_detailed.py`: Script for detailed agent debugging
- `debug_population.py`: Script for testing population lookup functionality
- `test_crypto_agent.py`: Tests for cryptocurrency agent functionality
- `test_crypto.py`: Additional cryptocurrency tests
- `test_multiple_cities.py`: Tests for multi-city operations

## Architecture

This project demonstrates a modular approach to AI agent development:
- **Modular Agents**: Each agent is designed for specific domain expertise
- **Shared Tools**: Common service utilities available to all agents
- **Scalable Design**: Easy to add new agents and tools
- **Web Interface**: Next.js frontend for easy interaction

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

Add your license information here.