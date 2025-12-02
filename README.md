# Agent Development Project

This project demonstrates the development of AI agents using the Google ADK (Agent Development Kit). It includes multiple agents with different capabilities for handling user queries.

## Project Structure

- `ask_agent/`: A simple agent with one tool for getting time in cities
- `city_info_expert/`: High-level exports for the city information expert agent
- `multi_tool_agent/`: Core toolkit broken into focused service modules
  - `services/weather.py`: OpenWeatherMap client utilities
  - `services/time.py`: Timezone calculations backed by `zoneinfo`
  - `services/location.py`: Coordinate lookups via OpenStreetMap
  - `services/population.py`: Wikipedia-based population scraping
  - `agent.py`: Wires the tools together and exposes `root_agent` for Google ADK
- `pyproject.toml`: Project dependencies and configuration
- `main.py`: Entry point for the application

## Features

### ask_agent
- Simple agent to get the current time in a specified city
- Uses Google's Gemini model through the ADK framework

### City Info Expert
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

## Setup

1. **Install dependencies**:
   ```bash
   pip install -e .
   ```

2. **Set up API keys**:
  - For `city_info_expert`, you need an OpenWeatherMap API key
   - Update `multi_tool_agent/.env` with your API key:
   ```
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

## Usage

Access tools directly from the package:

```python
from multi_tool_agent import get_coordinates, get_current_time, get_weather

print(get_coordinates("Paris"))
```

Or interact through the `city_info_expert` agent, which can:
- Answer questions about the weather in specific cities
- Provide the current time in different cities
- Convert time between different time zones
- Handle complex queries requiring multiple tools
- Retrieve population estimates for major cities

## Requirements

- Python 3.11+
- Google ADK
- LiteLLM
- Requests
- Geopy

## License

Add your license information here.