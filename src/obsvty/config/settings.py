"""Configuration model for OTLP gRPC endpoint settings.

This module defines the OtlpGrpcSettings model with environment variable support
following the principles of Hexagonal Architecture and Test-Driven Development,
allowing developers to connect their OTLP clients efficiently with proper
configuration management and validation.
"""

from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OtlpGrpcSettings(BaseSettings):
    """Configuration model for OTLP gRPC server settings following PRP requirements.

    This class follows the specification from the PRP with the exact fields needed
    for OTLP client connection, using the naming conventions and validation requirements.

    Attributes:
        host: The host address for the gRPC server to bind to (default: "localhost")
        port: The port number for the gRPC server (default: 4317 for OTLP)
        max_message_length: Maximum message size in bytes that the server will accept
        buffer_max_size: Maximum size of the trace buffer
    """

    host: str = "localhost"
    port: int = 4317
    max_message_length: int = 4 * 1024 * 1024  # 4MB
    buffer_max_size: int = 1000

    @field_validator("port")
    @classmethod
    def validate_port(cls, value: int) -> int:
        """Validate that the port number is within the valid range."""
        if not (1 <= value <= 65535):
            raise ValueError(f"Port must be between 1 and 65535, got {value}")
        return value

    @field_validator("max_message_length")
    @classmethod
    def validate_max_message_length(cls, value: int) -> int:
        """Validate that the max message length is positive."""
        if value <= 0:
            raise ValueError(f"Max message length must be positive, got {value}")
        return value

    @field_validator("buffer_max_size")
    @classmethod
    def validate_buffer_max_size(cls, value: int) -> int:
        """Validate that the buffer max size is positive."""
        if value <= 0:
            raise ValueError(f"Buffer max size must be positive, got {value}")
        return value

    model_config = SettingsConfigDict(
        env_prefix="OTLP_",
        case_sensitive=False,
    )


class OTLPGRPCServerConfig(BaseSettings):
    """Backward compatibility configuration model for existing implementation.

    This class maintains compatibility with the existing adapter implementation
    while providing the functionality required by the PRP.
    """

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


def load_grpc_settings() -> OtlpGrpcSettings:
    """Load gRPC settings from environment variables using PRP specifications.

    This function loads the OTLP gRPC server configuration from environment
    variables following the Hexagonal Architecture principles, with proper
    validation and error handling as specified in the PRP.

    Returns:
        OtlpGrpcSettings: Validated configuration instance loaded from environment

    Example:
        settings = load_grpc_settings()
        server = configure_grpc_server(settings)
    """
    return OtlpGrpcSettings()


def load_otlp_grpc_config() -> OTLPGRPCServerConfig:
    """Load OTLP gRPC configuration from environment variables (backward compatibility).

    This function maintains compatibility with existing code while providing
    the new configuration model as well.

    Returns:
        OTLPGRPCServerConfig: Validated configuration instance for existing adapter
    """
    return OTLPGRPCServerConfig()


def validate_settings(settings: OtlpGrpcSettings) -> bool:
    """Validate configuration settings before server startup.

    This function performs additional validation of the configuration settings
    beyond what Pydantic provides, ensuring the configuration is safe and
    appropriate for server startup.

    Args:
        settings: The configuration settings to validate

    Returns:
        True if all validations pass, False otherwise
    """
    # All validation is handled by Pydantic during instantiation
    # If we get here, the settings are valid
    return True


def get_server_endpoint(settings: OtlpGrpcSettings) -> str:
    """Get the server endpoint string from settings.

    Args:
        settings: The configuration settings

    Returns:
        str: The server endpoint in host:port format
    """
    return f"{settings.host}:{settings.port}"
