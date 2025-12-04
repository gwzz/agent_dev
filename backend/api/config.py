"""Configuration management for the API service."""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # API Configuration
    app_name: str = "AI Agent Experts API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # CORS Configuration
    allowed_origins: str = "*"
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]
    expose_headers: List[str] = ["Access-Control-Allow-Origin"]
    allow_credentials: bool = True
    
    # Security Configuration
    allowed_hosts: str = "*"
    api_keys: str = "demo-key-123,test-key-456"
    require_api_key: bool = False  # Set to True in production
    
    # Rate Limiting Configuration
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # in seconds (1 hour)
    
    # Agent Configuration
    google_api_key: Optional[str] = None
    openweather_api_key: Optional[str] = None
    
    # Query Validation
    max_query_length: int = 1000
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse allowed origins from comma-separated string."""
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        """Parse allowed hosts from comma-separated string."""
        if self.allowed_hosts == "*":
            return ["*"]
        return [host.strip() for host in self.allowed_hosts.split(",")]
    
    @property
    def api_keys_set(self) -> set:
        """Parse API keys from comma-separated string."""
        if not self.api_keys:
            return set()
        return {key.strip() for key in self.api_keys.split(",") if key.strip()}
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
