"""Time utilities built on Python's ZoneInfo."""

from __future__ import annotations

import datetime as _dt
from typing import Any
from zoneinfo import ZoneInfo

from .timezones import resolve_timezone


def get_current_time(city: str) -> dict[str, Any]:
    """Return the current local time for ``city`` if a timezone is known."""
    tz_name = resolve_timezone(city)
    if not tz_name:
        return {
            "status": "error",
            "error_message": f"Timezone not found for city '{city}'. Please use a major city name.",
        }

    tz = ZoneInfo(tz_name)
    now = _dt.datetime.now(tz)
    report = f"The current time in {city.title()} is {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    return {
        "status": "success",
        "report": report,
        "timezone": tz_name,
        "datetime": now.isoformat(),
    }


def convert_time_between_cities(
    source_city: str,
    destination_city: str,
    time_str: str | None = None,
) -> dict[str, Any]:
    """Convert ``time_str`` from ``source_city`` to ``destination_city``."""
    source_tz_name = resolve_timezone(source_city)
    dest_tz_name = resolve_timezone(destination_city)

    if not source_tz_name:
        return {
            "status": "error",
            "error_message": f"Could not determine timezone for source city '{source_city}'.",
        }

    if not dest_tz_name:
        return {
            "status": "error",
            "error_message": f"Could not determine timezone for destination city '{destination_city}'.",
        }

    source_tz = ZoneInfo(source_tz_name)
    dest_tz = ZoneInfo(dest_tz_name)

    if time_str:
        time_obj = _dt.datetime.strptime(time_str, "%H:%M").time()
        current_date = _dt.date.today()
        dt_source = _dt.datetime.combine(current_date, time_obj, tzinfo=source_tz)
    else:
        dt_source = _dt.datetime.now(source_tz)

    dt_dest = dt_source.astimezone(dest_tz)
    report = (
        f"Time in {source_city} ({source_tz_name}): {dt_source.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        f"Time in {destination_city} ({dest_tz_name}): {dt_dest.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )

    return {
        "status": "success",
        "report": report,
        "source_time": dt_source.isoformat(),
        "destination_time": dt_dest.isoformat(),
        "source_timezone": source_tz_name,
        "destination_timezone": dest_tz_name,
    }
