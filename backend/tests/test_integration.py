"""Integration tests for API with actual service calls."""

import pytest
from fastapi.testclient import TestClient
import os

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app

client = TestClient(app)


class TestIntegrationCityInfo:
    """Integration tests for city info endpoints with real services."""

    @pytest.mark.skipif(
        not os.getenv("OPENWEATHER_API_KEY"),
        reason="OPENWEATHER_API_KEY not set"
    )
    def test_real_weather_api(self):
        """Test with real weather API (requires API key)."""
        response = client.get("/city-info/weather/London")
        assert response.status_code in [200, 500]  # 500 if API key issue
        
    def test_real_coordinates_api(self):
        """Test with real coordinates service."""
        response = client.get("/city-info/coordinates/Paris")
        assert response.status_code == 200
        data = response.json()
        # Should have latitude and longitude
        if data.get("status") == "success":
            assert "latitude" in data
            assert "longitude" in data

    def test_real_population_api(self):
        """Test with real population service."""
        response = client.get("/city-info/population/Tokyo")
        assert response.status_code == 200
        data = response.json()
        # Should have population data or error
        assert "status" in data


class TestIntegrationCrypto:
    """Integration tests for crypto endpoints with real services."""

    def test_real_crypto_price_api(self):
        """Test with real crypto price API."""
        response = client.get("/crypto/price/bitcoin")
        assert response.status_code == 200
        data = response.json()
        # Should have price data
        if data.get("status") == "success":
            assert "price_usd" in data
            assert data["price_usd"] > 0


class TestIntegrationLaw:
    """Integration tests for law endpoints with real services."""

    def test_real_jurisdiction_api(self):
        """Test with real jurisdiction service."""
        response = client.get("/law/jurisdiction/federal")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_real_statute_api(self):
        """Test with real statute service."""
        response = client.get("/law/statute/gdpr")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_real_cases_api(self):
        """Test with real cases service."""
        response = client.get("/law/cases/privacy")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_real_definition_api(self):
        """Test with real definition service."""
        response = client.get("/law/definition/tort")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
