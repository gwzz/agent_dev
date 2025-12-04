"""Agent Manager for Google ADK-based agents."""

import logging
import uuid
from typing import Dict, Any, Optional
from google.adk.agents import Agent, InvocationContext
from google.adk.agents.run_config import RunConfig
from google.adk.sessions import Session, InMemorySessionService
from google.adk.events import Event
from google.genai.types import Content, Part
from pydantic import BaseModel, Field, ConfigDict

from city_info_expert.agent import root_agent as city_info_agent
from crypto_expert.agent import root_agent as crypto_agent
from law_expert.agent import root_agent as law_agent


logger = logging.getLogger(__name__)


class AgentResponse(BaseModel):
    """Standardized response format for agent results."""
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=False
    )
    
    status: str = Field(..., description="Status of the agent execution ('success' or 'error')")
    content: Optional[str] = Field(default=None, description="Main content of the agent response")
    usage: Optional[Dict[str, int]] = Field(default=None, description="Token usage information")
    error_message: Optional[str] = Field(default=None, description="Error message if status is 'error'")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class AgentManager:
    """Manager class to handle multiple Google ADK agents."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization of singleton
        if hasattr(self, '_initialized'):
            return
        
        self._agents: Dict[str, Agent] = {
            "city_info": city_info_agent,
            "crypto": crypto_agent,
            "law": law_agent,
        }
        # Initialize session service for agent invocations
        self._session_service = InMemorySessionService()
        self._initialized = True
        logger.info(f"Initialized AgentManager with {len(self._agents)} agents")
    
    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """Get an agent by name."""
        return self._agents.get(agent_name)
    
    def get_available_agents(self) -> list:
        """Get list of available agent names."""
        return list(self._agents.keys())
    
    async def run_agent(self, agent_name: str, query: str) -> AgentResponse:
        """Run an agent with the given query and return a standardized response."""
        # Validate inputs
        if not query or not query.strip():
            return AgentResponse(
                status="error",
                error_message="Query cannot be empty or whitespace only",
            )

        if len(query.strip()) > 1000:  # Reasonable query length limit
            return AgentResponse(
                status="error",
                error_message="Query is too long. Please keep it under 1000 characters.",
            )

        agent = self.get_agent(agent_name)

        if not agent:
            return AgentResponse(
                status="error",
                error_message=f"Agent '{agent_name}' not found. Available agents: {list(self._agents.keys())}",
            )

        try:
            logger.info(f"Running agent '{agent_name}' with query: {query[:100]}...")

            # Create a user message content
            user_content = Content(
                parts=[Part(text=query.strip())],
                role="user"
            )
            
            # Create a user event with the query
            user_event = Event(
                content=user_content,
                author="user"
            )
            
            # Create a session for this invocation with the user query
            session = Session(
                id=str(uuid.uuid4()),
                appName="agent_api",
                userId="api_user",
                events=[user_event]
            )
            
            # Create invocation context
            ctx = InvocationContext(
                session_service=self._session_service,
                invocation_id=str(uuid.uuid4()),
                agent=agent,
                session=session,
                run_config=RunConfig(response_modalities=["TEXT"])
            )

            # Run the agent - this returns an async generator
            result = agent.run_async(ctx)

            # Handle the async generator by collecting all chunks
            full_content = ""
            usage_info = None
            metadata_info = None

            # Collect the async generator results
            async for chunk in result:
                # Handle string chunks directly
                if isinstance(chunk, str):
                    full_content += chunk
                # Handle objects with text or content attributes
                elif hasattr(chunk, 'text') and isinstance(chunk.text, str):
                    full_content += chunk.text
                elif hasattr(chunk, 'content') and isinstance(chunk.content, str):
                    full_content += chunk.content
                # Handle dictionary chunks
                elif isinstance(chunk, dict):
                    if 'content' in chunk:
                        full_content += str(chunk['content'])
                    elif 'text' in chunk:
                        full_content += str(chunk['text'])
                    if 'usage' in chunk and isinstance(chunk['usage'], dict):
                        usage_info = chunk['usage']
                    # Store any additional metadata (only non-empty dicts)
                    other_metadata = {k: v for k, v in chunk.items() if k not in ['content', 'text', 'usage']}
                    if other_metadata:
                        if metadata_info is None:
                            metadata_info = {}
                        metadata_info.update(other_metadata)
                # Fallback to string conversion
                else:
                    full_content += str(chunk)

            # Create response with the collected content
            # Only include fields if they have actual values
            try:
                response = AgentResponse(
                    status="success",
                    content=full_content if full_content else None,
                    usage=usage_info if isinstance(usage_info, dict) else None,
                    metadata=metadata_info if isinstance(metadata_info, dict) and metadata_info else None
                )
            except Exception as response_error:
                logger.error(f"Error creating AgentResponse: {str(response_error)}")
                logger.error(f"  content type: {type(full_content)}, value: {repr(full_content[:100] if full_content else None)}")
                logger.error(f"  usage type: {type(usage_info)}, value: {repr(usage_info)}")
                logger.error(f"  metadata type: {type(metadata_info)}, value: {repr(metadata_info)}")
                raise

            logger.info(f"Agent '{agent_name}' completed successfully")
            return response

        except Exception as e:
            logger.error(f"Error running agent '{agent_name}': {str(e)}", exc_info=True)
            return AgentResponse(
                status="error",
                error_message=str(e),
            )

    async def run_city_info_agent(self, query: str) -> AgentResponse:
        """Convenience method to run the city info agent."""
        return await self.run_agent("city_info", query)

    async def run_crypto_agent(self, query: str) -> AgentResponse:
        """Convenience method to run the crypto agent."""
        return await self.run_agent("crypto", query)

    async def run_law_agent(self, query: str) -> AgentResponse:
        """Convenience method to run the law agent."""
        return await self.run_agent("law", query)


def get_agent_manager() -> AgentManager:
    """Dependency injection function for FastAPI."""
    return AgentManager()


# Global instance of the agent manager
agent_manager = AgentManager()