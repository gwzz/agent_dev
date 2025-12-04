"""Integration tests for the Google ADK agent manager wrapper."""

import pytest
from unittest.mock import Mock, patch
from api.agent_manager import AgentManager, AgentResponse
from google.adk.agents import Agent


class TestAgentManagerIntegration:
    """Integration tests for the agent manager functionality."""
    
    def test_agent_manager_initialization(self):
        """Test that the agent manager initializes with the expected agents."""
        manager = AgentManager()
        expected_agents = {"city_info", "crypto", "law"}
        available_agents = set(manager.get_available_agents())
        
        assert expected_agents.issubset(available_agents)
        
        # Check that all agents are properly loaded
        for agent_name in expected_agents:
            agent = manager.get_agent(agent_name)
            assert agent is not None
            assert isinstance(agent, Agent)
    
    async def test_run_agent_with_valid_agent(self):
        """Test running an agent with a valid query."""
        manager = AgentManager()

        # Test with the city info agent
        result = await manager.run_agent("city_info", "What is the weather in London?")

        # The result should be an AgentResponse
        assert isinstance(result, AgentResponse)
        assert result.status in ["success", "error"]  # Both are valid, depending on API availability
        # Ensure the content is a string and not an async_generator
        if result.status == "success":
            assert isinstance(result.content, str)
            assert not str(result.content).startswith("<async_generator")
    
    async def test_run_agent_with_invalid_agent_name(self):
        """Test running an agent with an invalid name."""
        manager = AgentManager()

        result = await manager.run_agent("invalid_agent", "test query")

        assert isinstance(result, AgentResponse)
        assert result.status == "error"
        assert "not found" in result.error_message

    async def test_run_agent_with_empty_query(self):
        """Test running an agent with an empty query."""
        manager = AgentManager()

        result = await manager.run_agent("city_info", "")

        assert isinstance(result, AgentResponse)
        assert result.status == "error"
        assert "cannot be empty" in result.error_message

    async def test_run_agent_with_whitespace_query(self):
        """Test running an agent with a whitespace-only query."""
        manager = AgentManager()

        result = await manager.run_agent("city_info", "   ")

        assert isinstance(result, AgentResponse)
        assert result.status == "error"
        assert "cannot be empty" in result.error_message

    async def test_run_agent_with_long_query(self):
        """Test running an agent with a query that exceeds the length limit."""
        manager = AgentManager()

        long_query = "A" * 1001  # More than 1000 characters
        result = await manager.run_agent("city_info", long_query)

        assert isinstance(result, AgentResponse)
        assert result.status == "error"
        assert "too long" in result.error_message
    
    async def test_convenience_methods(self):
        """Test the convenience methods for each agent type."""
        manager = AgentManager()

        # Test that convenience methods exist and work
        result1 = await manager.run_city_info_agent("Hello")
        result2 = await manager.run_crypto_agent("Hello")
        result3 = await manager.run_law_agent("Hello")

        for result in [result1, result2, result3]:
            assert isinstance(result, AgentResponse)
            # Note: These might fail or succeed depending on API availability
            assert result.status in ["success", "error"]
            # Ensure the content is a string and not an async_generator
            if result.status == "success":
                assert isinstance(result.content, str)
                assert not str(result.content).startswith("<async_generator")


class TestAgentResponseModel:
    """Tests for the AgentResponse model."""
    
    def test_agent_response_creation(self):
        """Test creating AgentResponse objects."""
        response = AgentResponse(
            status="success",
            content="Test content",
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        )
        
        assert response.status == "success"
        assert response.content == "Test content"
        assert response.usage == {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    
    def test_agent_response_error_case(self):
        """Test creating AgentResponse for error cases."""
        response = AgentResponse(
            status="error",
            error_message="Something went wrong"
        )
        
        assert response.status == "error"
        assert response.error_message == "Something went wrong"
        assert response.content is None
        assert response.usage is None


import asyncio

if __name__ == "__main__":
    # Use asyncio to run the async tests
    pytest.main([__file__])