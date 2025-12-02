"""Utility helpers for resolving city names to IANA timezone identifiers."""

from __future__ import annotations

CITY_TIMEZONE_MAP: dict[str, str] = {
    # North America
    "new york": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "houston": "America/Chicago",
    "phoenix": "America/Phoenix",
    "philadelphia": "America/New_York",
    "san antonio": "America/Chicago",
    "san diego": "America/Los_Angeles",
    "dallas": "America/Chicago",
    "san jose": "America/Los_Angeles",
    "austin": "America/Chicago",
    "jacksonville": "America/New_York",
    "san francisco": "America/Los_Angeles",
    "indianapolis": "America/Indiana/Indianapolis",
    "seattle": "America/Los_Angeles",
    "denver": "America/Denver",
    "washington": "America/New_York",
    "boston": "America/New_York",
    "nashville": "America/Chicago",
    "baltimore": "America/New_York",
    # Europe
    "london": "Europe/London",
    "berlin": "Europe/Berlin",
    "paris": "Europe/Paris",
    "rome": "Europe/Rome",
    "madrid": "Europe/Madrid",
    "amsterdam": "Europe/Amsterdam",
    "brussels": "Europe/Brussels",
    "vienna": "Europe/Vienna",
    "stockholm": "Europe/Stockholm",
    "oslo": "Europe/Oslo",
    "copenhagen": "Europe/Copenhagen",
    "dublin": "Europe/Dublin",
    "athens": "Europe/Athens",
    "lisbon": "Europe/Lisbon",
    "helsinki": "Europe/Helsinki",
    "warsaw": "Europe/Warsaw",
    "prague": "Europe/Prague",
    "budapest": "Europe/Budapest",
    # Asia
    "tokyo": "Asia/Tokyo",
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "hong kong": "Asia/Hong_Kong",
    "singapore": "Asia/Singapore",
    "seoul": "Asia/Seoul",
    "bangkok": "Asia/Bangkok",
    "jakarta": "Asia/Jakarta",
    "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "kolkata": "Asia/Kolkata",
    "chennai": "Asia/Kolkata",
    "bengaluru": "Asia/Kolkata",
    "karachi": "Asia/Karachi",
    "lahore": "Asia/Karachi",
    "dubai": "Asia/Dubai",
    "riyadh": "Asia/Riyadh",
    # Oceania
    "sydney": "Australia/Sydney",
    "melbourne": "Australia/Melbourne",
    "brisbane": "Australia/Brisbane",
    "perth": "Australia/Perth",
    "adelaide": "Australia/Adelaide",
    "auckland": "Pacific/Auckland",
    "wellington": "Pacific/Auckland",
    # South America
    "sao paulo": "America/Sao_Paulo",
    "buenos aires": "America/Argentina/Buenos_Aires",
    "lima": "America/Lima",
    "santiago": "America/Santiago",
    "bogota": "America/Bogota",
    "caracas": "America/Caracas",
}


def resolve_timezone(city_name: str) -> str | None:
    """Return the timezone name for ``city_name`` if a close match exists."""
    if not city_name:
        return None

    city_key = city_name.lower().strip()
    if city_key in CITY_TIMEZONE_MAP:
        return CITY_TIMEZONE_MAP[city_key]

    for key, tz in CITY_TIMEZONE_MAP.items():
        if city_key in key or key in city_key:
            return tz
    return None
