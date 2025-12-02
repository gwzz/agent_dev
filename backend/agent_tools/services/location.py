"""Location and geocoding utilities."""

from __future__ import annotations

from typing import Any

from geopy.geocoders import Nominatim

_geolocator = Nominatim(user_agent="agent-dev-project")


def get_coordinates(city: str) -> dict[str, Any]:
    """Return latitude/longitude for ``city`` using OpenStreetMap data."""
    try:
        location = _geolocator.geocode(city)
    except Exception as exc:  # noqa: BLE001 - propagate as user-readable error
        return {
            "status": "error",
            "error_message": f"An error occurred while retrieving coordinates for {city}: {exc}",
        }

    if not location:
        return {
            "status": "error",
            "error_message": f"Could not find coordinates for city '{city}'.",
        }

    return {
        "status": "success",
        "city": city,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "address": location.address,
    }
