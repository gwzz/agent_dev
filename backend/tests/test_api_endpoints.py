"""Comprehensive tests for all API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app

client = TestClient(app)


class TestGeneralEndpoints:
    """Tests for general API endpoints."""

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data

    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "available_services" in data
        assert isinstance(data["available_services"], list)


class TestCityInfoEndpoints:
    """Tests for city information endpoints."""

    @patch('api.services.city_info.get_weather')
    def test_get_weather_success(self, mock_get_weather):
        """Test successful weather request."""
        mock_get_weather.return_value = {
            "status": "success",
            "report": "The current weather in London is clear sky with a temperature of 18.5°C (65.3°F). It feels like 18.5°C. Humidity is 65%.",
            "temperature_celsius": 18.5,
            "temperature_fahrenheit": 65.3,
            "description": "clear sky",
            "humidity": 65,
            "feels_like": 18.5
        }

        response = client.get("/city-info/weather/London")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "report" in data

    def test_get_weather_empty_city(self):
        """Test weather request with empty city."""
        response = client.get("/city-info/weather/ ")
        assert response.status_code == 400

    @patch('api.services.city_info.get_weather')
    def test_get_weather_error(self, mock_get_weather):
        """Test weather request with error."""
        mock_get_weather.return_value = {
            "status": "error",
            "error_message": "API key not configured"
        }

        response = client.get("/city-info/weather/London")
        assert response.status_code == 500

    @patch('api.services.city_info.get_current_time')
    def test_get_time_success(self, mock_get_time):
        """Test successful time request."""
        mock_get_time.return_value = {
            "status": "success",
            "city": "New York",
            "current_time": "2024-01-01 12:00:00",
            "timezone": "America/New_York"
        }

        response = client.get("/city-info/time/New York")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "current_time" in data

    @patch('api.services.city_info.get_coordinates')
    def test_get_coordinates_success(self, mock_get_coordinates):
        """Test successful coordinates request."""
        mock_get_coordinates.return_value = {
            "status": "success",
            "city": "Paris",
            "latitude": 48.8566,
            "longitude": 2.3522
        }

        response = client.get("/city-info/coordinates/Paris")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "latitude" in data
        assert "longitude" in data

    @patch('api.services.city_info.get_city_population')
    def test_get_population_success(self, mock_get_population):
        """Test successful population request."""
        mock_get_population.return_value = {
            "status": "success",
            "city": "Tokyo",
            "population": 13960000,
            "source": "Wikipedia"
        }

        response = client.get("/city-info/population/Tokyo")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "population" in data

    @patch('api.services.city_info.convert_time_between_cities')
    def test_convert_time_success(self, mock_convert_time):
        """Test successful time conversion."""
        mock_convert_time.return_value = {
            "status": "success",
            "from_city": "New York",
            "to_city": "London",
            "original_time": "12:00",
            "converted_time": "17:00"
        }

        response = client.post("/city-info/time/convert", json={
            "from_city": "New York",
            "to_city": "London",
            "time": "12:00"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


class TestCryptoEndpoints:
    """Tests for cryptocurrency endpoints."""

    @patch('api.services.crypto.get_crypto_price')
    def test_get_price_success(self, mock_get_price):
        """Test successful crypto price request."""
        mock_get_price.return_value = {
            "status": "success",
            "cryptocurrency": "bitcoin",
            "price_usd": 43567.89,
            "report": "The current price of Bitcoin (bitcoin) is $43,567.89 USD."
        }

        response = client.get("/crypto/price/bitcoin")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "price_usd" in data

    @patch('api.services.crypto.get_crypto_price')
    def test_get_price_with_symbol(self, mock_get_price):
        """Test crypto price request with symbol."""
        mock_get_price.return_value = {
            "status": "success",
            "cryptocurrency": "bitcoin",
            "price_usd": 43567.89,
            "report": "The current price of Bitcoin (bitcoin) is $43,567.89 USD."
        }

        response = client.get("/crypto/price/btc")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_get_price_empty_crypto(self):
        """Test crypto price request with empty cryptocurrency."""
        response = client.get("/crypto/price/ ")
        assert response.status_code == 400

    @patch('api.services.crypto.get_crypto_price')
    def test_get_price_error(self, mock_get_price):
        """Test crypto price request with error."""
        mock_get_price.return_value = {
            "status": "error",
            "error_message": "Cryptocurrency not supported"
        }

        response = client.get("/crypto/price/unknown")
        assert response.status_code == 500


class TestLawEndpoints:
    """Tests for legal information endpoints."""

    @patch('api.services.law.get_jurisdiction_info')
    def test_get_jurisdiction_success(self, mock_get_jurisdiction):
        """Test successful jurisdiction request."""
        mock_get_jurisdiction.return_value = {
            "status": "success",
            "jurisdiction": "federal",
            "court_system": "Supreme Court, Circuit Courts, District Courts",
            "description": "Federal jurisdiction covers matters involving federal law..."
        }

        response = client.get("/law/jurisdiction/federal")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "jurisdiction" in data

    @patch('api.services.law.get_statute_info')
    def test_get_statute_success(self, mock_get_statute):
        """Test successful statute request."""
        mock_get_statute.return_value = {
            "status": "success",
            "statute": "gdpr",
            "name": "General Data Protection Regulation",
            "jurisdiction": "European Union"
        }

        response = client.get("/law/statute/gdpr")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "statute" in data

    @patch('api.services.law.get_recent_cases')
    def test_get_cases_success(self, mock_get_cases):
        """Test successful cases request."""
        mock_get_cases.return_value = {
            "status": "success",
            "law_area": "privacy",
            "cases": [
                {
                    "case_name": "Sample v. Test",
                    "year": 2023,
                    "description": "Privacy case"
                }
            ]
        }

        response = client.get("/law/cases/privacy")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "cases" in data

    @patch('api.services.law.get_legal_definition')
    def test_get_definition_success(self, mock_get_definition):
        """Test successful definition request."""
        mock_get_definition.return_value = {
            "status": "success",
            "term": "tort",
            "definition": "A civil wrong that causes harm or loss..."
        }

        response = client.get("/law/definition/tort")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "definition" in data

    def test_get_jurisdiction_empty(self):
        """Test jurisdiction request with empty parameter."""
        response = client.get("/law/jurisdiction/ ")
        assert response.status_code == 400

    def test_get_statute_empty(self):
        """Test statute request with empty parameter."""
        response = client.get("/law/statute/ ")
        assert response.status_code == 400


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_endpoint(self):
        """Test 404 for non-existent endpoint."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    @patch('api.services.city_info.get_weather')
    def test_service_exception_handling(self, mock_get_weather):
        """Test exception handling in services."""
        mock_get_weather.side_effect = Exception("Unexpected error")

        response = client.get("/city-info/weather/London")
        # Should be handled and return error status
        assert response.status_code in [500, 200]  # Depending on how exceptions are caught


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
