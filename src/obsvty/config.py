"""Configuration model for OTLP gRPC server settings.

Uses Pydantic for validation and environment-based configuration management
following the principles of dependency inversion and configuration as code.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OTLPGRPCServerConfig(BaseSettings):
    """Configuration model for the OTLP gRPC server."""

    model_config = SettingsConfigDict(
        env_prefix="OTLP_GRPC_",
        case_sensitive=False,
        frozen=True,  # Immutable configuration once created
    )

    host: str = Field(
        default="0.0.0.0", description="Host address for the gRPC server to bind to"
    )
    port: int = Field(
        default=4317,
        ge=1,
        le=65535,
        description="Port number for the gRPC server (default: 4317 for OTLP)",
    )
    max_buffer_size: int = Field(
        default=10000, ge=1, description="Maximum size of the trace buffer"
    )
    max_message_length: int = Field(
        default=4 * 1024 * 1024,  # 4MB
        description="Maximum message size in bytes that the server will accept",
    )
    enable_reflection: bool = Field(
        default=False, description="Enable gRPC server reflection for debugging tools"
    )
    enable_logs_service: bool = Field(
        default=False, description="Enable optional OTLP logs service alongside traces"
    )


def load_otlp_grpc_config() -> OTLPGRPCServerConfig:
    """Load OTLP gRPC configuration from environment variables.

    Returns:
        OTLPGRPCServerConfig: Validated configuration instance
    """
    return OTLPGRPCServerConfig()
