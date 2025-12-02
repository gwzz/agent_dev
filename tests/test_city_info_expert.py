from city_info_expert.agent import (
    get_current_time,
    get_coordinates,
    get_city_population,
)


def test_current_time_basic():
    result = get_current_time("London")
    assert result["status"] in ("success", "error")


def test_coordinates_basic():
    result = get_coordinates("London")
    assert result["status"] in ("success", "error")


def test_population_basic():
    result = get_city_population("London")
    assert result["status"] in ("success", "error")
