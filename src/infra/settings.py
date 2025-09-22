"""
Configuration settings for the baseline solver.

This module provides configuration management using pydantic.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
import os


class SolverSettings(BaseModel):
    """Solver configuration settings."""
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8080, description="Server port")
    
    # Solver settings
    solver_name: str = Field(default="baseline", description="Solver name")
    solver_version: str = Field(default="1.0.0", description="Solver version")
    default_solver_route: str = Field(default="baseline", description="Default solver route (baseline|mysolver)")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format")
    
    # Metrics settings
    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    metrics_port: int = Field(default=9090, description="Metrics server port")
    
    # Database settings (if needed)
    database_url: Optional[str] = Field(default=None, description="Database URL")
    
    # External service settings
    ethereum_rpc_url: Optional[str] = Field(default=None, description="Ethereum RPC URL")
    ethereum_chain_id: int = Field(default=1, description="Ethereum chain ID")
    
    # Solver-specific settings
    max_orders_per_auction: int = Field(default=1000, description="Maximum orders per auction")
    max_tokens_per_auction: int = Field(default=100, description="Maximum tokens per auction")
    max_liquidity_sources: int = Field(default=50, description="Maximum liquidity sources")
    
    # Performance settings
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    max_concurrent_requests: int = Field(default=100, description="Maximum concurrent requests")
    
    # Security settings
    allowed_origins: List[str] = Field(default=["*"], description="Allowed CORS origins")
    api_key: Optional[str] = Field(default=None, description="API key for authentication")


def get_settings() -> SolverSettings:
    """
    Get settings with environment variable support.
    
    Returns:
        Settings instance
    """
    # Read from environment variables
    return SolverSettings(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        solver_name=os.getenv("SOLVER_NAME", "baseline"),
        solver_version=os.getenv("SOLVER_VERSION", "1.0.0"),
        default_solver_route=os.getenv("DEFAULT_SOLVER_ROUTE", "baseline"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        metrics_enabled=os.getenv("METRICS_ENABLED", "true").lower() == "true",
        database_url=os.getenv("DATABASE_URL"),
        ethereum_rpc_url=os.getenv("ETHEREUM_RPC_URL"),
        ethereum_chain_id=int(os.getenv("ETHEREUM_CHAIN_ID", "1")),
        max_orders_per_auction=int(os.getenv("MAX_ORDERS_PER_AUCTION", "1000")),
        max_tokens_per_auction=int(os.getenv("MAX_TOKENS_PER_AUCTION", "100")),
        max_liquidity_sources=int(os.getenv("MAX_LIQUIDITY_SOURCES", "50")),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
        max_concurrent_requests=int(os.getenv("MAX_CONCURRENT_REQUESTS", "100")),
        api_key=os.getenv("API_KEY")
    )


# Global settings instance
settings = get_settings()
