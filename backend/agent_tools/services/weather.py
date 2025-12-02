"""Weather lookup utilities backed by OpenWeatherMap."""

from __future__ import annotations

import os
from typing import Any

import requests


def get_weather(city: str) -> dict[str, Any]:
    """Fetch the current weather report for ``city`` using OpenWeatherMap."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "Weather API key not configured. Please set OPENWEATHER_API_KEY.",
        }

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        error_msg = _format_weather_error(exc)
        return {"status": "error", "error_message": error_msg}

    data = response.json()
    weather_desc = data["weather"][0]["description"]
    temp_celsius = round(data["main"]["temp"], 1)
    temp_fahrenheit = round((temp_celsius * 9 / 5) + 32, 1)
    humidity = data["main"]["humidity"]
    feels_like = round(data["main"]["feels_like"], 1)

    report = (
        f"The current weather in {city} is {weather_desc} with a temperature of "
        f"{temp_celsius}°C ({temp_fahrenheit}°F). It feels like {feels_like}°C. "
        f"Humidity is {humidity}%."
    )
    return {
        "status": "success",
        "report": report,
        "temperature_celsius": temp_celsius,
        "temperature_fahrenheit": temp_fahrenheit,
        "description": weather_desc,
        "humidity": humidity,
        "feels_like": feels_like,
    }


def _format_weather_error(exc: requests.exceptions.RequestException) -> str:
    """Return a readable error message for OpenWeatherMap failures."""
    if exc.response is None:
        return f"Failed to retrieve weather data: {exc}"

    try:
        details = exc.response.json().get("message")
    except Exception:  # noqa: BLE001 - fallback to default message
        details = None

    if details:
        return f"OpenWeatherMap API Error: {details} (Status: {exc.response.status_code})"

    return f"Failed to retrieve weather data: {exc} (Status: {exc.response.status_code})"
