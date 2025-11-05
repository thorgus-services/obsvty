"""Configuration model for OTLP gRPC endpoint settings."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OtlpGrpcSettings(BaseSettings):
    """Configuration model for OTLP gRPC server settings."""

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
    """Backward compatibility configuration model for existing implementation."""

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
    """Load gRPC settings from environment variables."""
    return OtlpGrpcSettings()


def load_otlp_grpc_config() -> OTLPGRPCServerConfig:
    """Load OTLP gRPC configuration from environment variables (backward compatibility)."""
    return OTLPGRPCServerConfig()


def validate_settings(settings: OtlpGrpcSettings) -> bool:
    """Validate configuration settings before server startup."""
    # All validation is handled by Pydantic during instantiation
    # If we get here, the settings are valid
    return True


def get_server_endpoint(settings: OtlpGrpcSettings) -> str:
    """Get the server endpoint string from settings."""
    return f"{settings.host}:{settings.port}"
