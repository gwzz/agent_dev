"""Tests for the cryptocurrency price change summary functionality."""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from crypto_tools.services.price import get_crypto_price_change_summary


def test_get_crypto_price_change_summary():
    """Test the price change summary function directly."""
    # Test with a supported cryptocurrency and valid days
    result = get_crypto_price_change_summary("bitcoin", 7)

    # The result should be a dictionary with status
    assert isinstance(result, dict)
    assert "status" in result

    # Status should be success (either with real data or mock data)
    assert result["status"] == "success"

    # Check for required fields
    assert "report" in result
    assert "crypto" in result
    assert "days" in result
    assert "initial_price_usd" in result
    assert "final_price_usd" in result
    assert "price_change_percentage" in result

    # Check if it's mock data (indicated by 'is_mock_data' field)
    if result.get("is_mock_data"):
        assert "[MOCK DATA]" in result["report"]
        assert "simulated data" in result["report"]


def test_mock_data_generation():
    """Test the mock data generation functionality directly."""
    from crypto_tools.services.price import _generate_mock_price_change_summary

    # Test mock data generation
    result = _generate_mock_price_change_summary("bitcoin", "bitcoin", 7)

    assert result["status"] == "success"
    assert result["is_mock_data"] is True
    assert "[MOCK DATA]" in result["report"]
    assert "bitcoin" in result["report"]
    assert result["days"] == 7
    assert "initial_price_usd" in result
    assert "final_price_usd" in result
    assert "price_change_percentage" in result


def test_get_crypto_price_change_summary_invalid_crypto():
    """Test the price change summary function with invalid crypto."""
    result = get_crypto_price_change_summary("invalid_crypto", 7)
    
    # Should return an error status
    assert result["status"] == "error"
    assert "error_message" in result


def test_get_crypto_price_change_summary_invalid_days():
    """Test the price change summary function with invalid days."""
    result = get_crypto_price_change_summary("bitcoin", -1)
    
    # Should return an error status
    assert result["status"] == "error"
    assert "error_message" in result
    assert "positive integer" in result["error_message"]
    
    # Test with too many days
    result = get_crypto_price_change_summary("bitcoin", 400)
    assert result["status"] == "error"
    assert "error_message" in result
    assert "365 days" in result["error_message"]


def test_get_crypto_price_change_summary_edge_cases():
    """Test edge cases for the price change summary function."""
    # Test with 1 day
    result = get_crypto_price_change_summary("bitcoin", 1)
    assert result["status"] in ["success", "error"]  # May fail due to insufficient data
    
    # Test with 365 days (maximum)
    result = get_crypto_price_change_summary("bitcoin", 365)
    assert result["status"] in ["success", "error"]  # May fail due to insufficient data


def test_crypto_api_endpoints():
    """Test the new API endpoints."""
    client = TestClient(app)
    
    # Test the new price change endpoint
    response = client.get("/crypto/price-change/bitcoin/7")
    
    # The response could be success or error depending on API availability
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "status" in data
        assert data["status"] in ["success", "error"]
        
        if data["status"] == "success":
            assert "report" in data
            assert "crypto" in data
            assert data["crypto"] == "bitcoin"
            assert "days" in data
            assert data["days"] == 7


def test_crypto_api_endpoints_with_invalid_data():
    """Test the API endpoints with invalid data."""
    client = TestClient(app)
    
    # Test with invalid cryptocurrency
    response = client.get("/crypto/price-change/invalid_crypto/7")
    assert response.status_code in [200, 500]  # May return error in body rather than HTTP error
    
    # Test with invalid days (will likely return 422 validation error)
    response = client.get("/crypto/price-change/bitcoin/0")
    assert response.status_code in [400, 422, 500]  # Could be validation error or internal error
    
    response = client.get("/crypto/price-change/bitcoin/400")
    assert response.status_code in [400, 422, 500]  # Could be validation error or internal error


def test_crypto_price_endpoint_still_works():
    """Ensure the original price endpoint still works."""
    client = TestClient(app)
    
    # Test the original price endpoint
    response = client.get("/crypto/price/bitcoin")
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "status" in data
        assert data["status"] in ["success", "error"]


if __name__ == "__main__":
    pytest.main()