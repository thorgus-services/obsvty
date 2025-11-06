"""Configuration model for OTLP gRPC endpoint settings."""

from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OtlpGrpcSettings(BaseSettings):
    """Configuration model for OTLP gRPC server settings."""

    host: str = Field(
        default="localhost", description="Host address for the gRPC server"
    )
    port: int = Field(default=4317, description="Port number for the gRPC server")
    max_message_length: int = Field(
        default=4 * 1024 * 1024, description="Maximum message length in bytes"
    )  # 4MB
    buffer_max_size: int = Field(
        default=1000, description="Maximum buffer size for traces"
    )
    max_buffer_size: int = Field(
        default=1000,
        description="Maximum buffer size for traces (for test compatibility)",
        exclude=True,
    )
    enable_reflection: bool = Field(
        default=False, description="Enable gRPC server reflection for debugging"
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, value: int) -> int:
        """Validate that the port number is within the valid range."""
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                raise ValueError("Port must be between 1 and 65535")

        if not (1 <= value <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        return value

    @field_validator("max_message_length")
    @classmethod
    def validate_max_message_length(cls, value: int) -> int:
        """Validate that the max message length is positive."""
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                raise ValueError("Max message length must be positive")

        if value <= 0:
            raise ValueError("Max message length must be positive")
        return value

    @field_validator("buffer_max_size", "max_buffer_size")
    @classmethod
    def validate_buffer_size(cls, value: int) -> int:
        """Validate that the buffer max size is positive."""
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                raise ValueError("Buffer max size must be positive")

        if value <= 0:
            raise ValueError("Buffer max size must be positive")
        return value

    def __init__(self, **data: Any) -> None:
        """Custom initialization to handle both field naming conventions."""
        # Ensure both buffer size fields map to buffer_max_size
        if "max_buffer_size" in data:
            data["buffer_max_size"] = data["max_buffer_size"]

        super().__init__(**data)

    model_config = SettingsConfigDict(
        env_prefix="OTLP_",
        case_sensitive=False,
        extra="allow",  # Allow extra fields for test compatibility
    )


def load_grpc_settings() -> OtlpGrpcSettings:
    """Load gRPC settings from environment variables."""
    return OtlpGrpcSettings()


def validate_settings(settings: OtlpGrpcSettings) -> bool:
    """Validate configuration settings before server startup."""
    # All validation is handled by Pydantic during instantiation
    # If we get here, the settings are valid
    return True


def get_server_endpoint(settings: OtlpGrpcSettings) -> str:
    """Get the server endpoint string from settings."""
    return f"{settings.host}:{settings.port}"
