"""Tests for Google ADK agent endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app
from api.agent_manager import AgentResponse

client = TestClient(app)


class TestCityInfoAgent:
    """Tests for city info agent endpoint."""

    @patch('api.agent_manager.AgentManager.run_city_info_agent')
    @pytest.mark.asyncio
    async def test_city_info_agent_success(self, mock_run_agent):
        """Test successful city info agent query."""
        mock_run_agent.return_value = AgentResponse(
            status="success",
            content="The current weather in London is clear sky with a temperature of 18.5°C. The current time in Tokyo is 2:30 AM JST.",
            usage={"prompt_tokens": 50, "completion_tokens": 150, "total_tokens": 200}
        )

        response = client.post("/city-info/agent", json={
            "query": "What's the weather in London and the time in Tokyo?"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "content" in data
        assert "London" in data["content"]
        assert "Tokyo" in data["content"]

    def test_city_info_agent_empty_query(self):
        """Test agent with empty query."""
        response = client.post("/city-info/agent", json={"query": ""})
        assert response.status_code == 422  # Pydantic validation error

    def test_city_info_agent_whitespace_query(self):
        """Test agent with whitespace query."""
        response = client.post("/city-info/agent", json={"query": "   "})
        assert response.status_code == 400


class TestCryptoAgent:
    """Tests for crypto agent endpoint."""

    @patch('api.agent_manager.AgentManager.run_crypto_agent')
    @pytest.mark.asyncio
    async def test_crypto_agent_success(self, mock_run_agent):
        """Test successful crypto agent query."""
        mock_run_agent.return_value = AgentResponse(
            status="success",
            content="Bitcoin is currently priced at $43,567.89 USD. Ethereum is at $2,345.67 USD.",
            usage={"prompt_tokens": 40, "completion_tokens": 120, "total_tokens": 160}
        )

        response = client.post("/crypto/agent", json={
            "query": "What's the price of Bitcoin and Ethereum?"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Bitcoin" in data["content"]
        assert "Ethereum" in data["content"]

    def test_crypto_agent_empty_query(self):
        """Test agent with empty query."""
        response = client.post("/crypto/agent", json={"query": ""})
        assert response.status_code == 422  # Pydantic validation error


class TestLawAgent:
    """Tests for law agent endpoint."""

    @patch('api.agent_manager.AgentManager.run_law_agent')
    @pytest.mark.asyncio
    async def test_law_agent_success(self, mock_run_agent):
        """Test successful law agent query."""
        mock_run_agent.return_value = AgentResponse(
            status="success",
            content="Federal jurisdiction covers matters involving federal law and constitutional issues. Recent privacy cases include...",
            usage={"prompt_tokens": 60, "completion_tokens": 180, "total_tokens": 240}
        )

        response = client.post("/law/agent", json={
            "query": "Tell me about federal jurisdiction and recent privacy cases"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "jurisdiction" in data["content"].lower()

    def test_law_agent_empty_query(self):
        """Test agent with empty query."""
        response = client.post("/law/agent", json={"query": ""})
        assert response.status_code == 422  # Pydantic validation error


class TestAgentErrorHandling:
    """Tests for agent error handling."""

    @patch('api.agent_manager.AgentManager.run_city_info_agent')
    @pytest.mark.asyncio
    async def test_agent_error_response(self, mock_run_agent):
        """Test agent error response."""
        mock_run_agent.return_value = AgentResponse(
            status="error",
            error_message="Agent execution failed"
        )

        response = client.post("/city-info/agent", json={
            "query": "test query"
        })
        
        assert response.status_code == 500

    @patch('api.agent_manager.AgentManager.run_crypto_agent')
    @pytest.mark.asyncio
    async def test_agent_exception(self, mock_run_agent):
        """Test agent exception handling."""
        mock_run_agent.side_effect = Exception("Unexpected error")

        response = client.post("/crypto/agent", json={
            "query": "test query"
        })
        
        assert response.status_code == 500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
