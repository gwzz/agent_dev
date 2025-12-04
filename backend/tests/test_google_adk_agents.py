"""Tests for the Google ADK agent endpoints."""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.agent_manager import agent_manager


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert data["message"] == "AI Agent Experts API"


def test_city_info_agent_endpoint(client):
    """Test the city info agent endpoint."""
    # Test with a simple query
    response = client.post("/city-info/", json={"query": "What is the current weather in London?"})

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] in ["success", "error"]  # Both are valid responses

    if data["status"] == "success":
        assert "result" in data
        assert "content" in data["result"]


def test_crypto_agent_endpoint(client):
    """Test the crypto agent endpoint."""
    # Test with a query about cryptocurrency
    response = client.post("/crypto/", json={"query": "What is the current price of Bitcoin?"})

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] in ["success", "error"]

    if data["status"] == "success":
        assert "result" in data
        assert "content" in data["result"]


def test_law_agent_endpoint(client):
    """Test the law agent endpoint."""
    # Test with a legal question
    response = client.post("/law/", json={"query": "What is due process?"})

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] in ["success", "error"]

    if data["status"] == "success":
        assert "result" in data
        assert "content" in data["result"]


def test_empty_query_validation(client):
    """Test that empty queries are properly handled."""
    # Test with an empty query for city-info
    response = client.post("/city-info/", json={"query": ""})
    assert response.status_code == 400  # Should now return 400 for validation errors
    data = response.json()
    assert "detail" in data

    # Test with whitespace-only query
    response = client.post("/city-info/", json={"query": "   "})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_long_query_validation(client):
    """Test that very long queries are properly handled."""
    # Create a very long query
    long_query = "A" * 1001  # More than 1000 characters
    response = client.post("/city-info/", json={"query": long_query})

    assert response.status_code == 400  # Should now return 400 for validation errors
    data = response.json()
    assert "detail" in data


def test_weather_service_endpoint(client):
    """Test the weather service endpoint."""
    response = client.get("/city-info/weather/London")
    # This endpoint may return 400 if API key is not configured, but it should not crash
    assert response.status_code in [200, 400]


def test_available_agents(client):
    """Test that the agent manager has the expected agents."""
    expected_agents = {"city_info", "crypto", "law"}
    available_agents = set(agent_manager.get_available_agents())
    
    assert expected_agents.issubset(available_agents)


def test_agent_manager_functionality():
    """Test the agent manager directly."""
    # Test that we can get an agent
    agent = agent_manager.get_agent("city_info")
    assert agent is not None
    
    # Test that requesting a non-existent agent returns None
    agent = agent_manager.get_agent("non_existent_agent")
    assert agent is None


if __name__ == "__main__":
    pytest.main()