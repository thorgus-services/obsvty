"""Composition root and server entrypoint (Dependency Injection bootstrap).

This module wires application use cases to concrete implementations of ports.
It provides both the composition root for dependency injection and the main
server entrypoint that loads configuration and starts the OTLP gRPC server
following the principles of Hexagonal Architecture and configuration as code.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

import grpc
from dotenv import load_dotenv

from .adapters.messaging.otlp_grpc import OTLPgRPCAdapter
from .config.settings import (
    OtlpGrpcSettings,
    load_grpc_settings,
    validate_settings,
    get_server_endpoint,
)
from .ports.storage import TraceStoragePort
from .use_cases import ProcessTraceUseCase


def build_use_cases(storage: TraceStoragePort) -> Dict[str, Any]:
    """Build and return the application use cases.

    Args:
        storage: Concrete implementation of TraceStoragePort.

    Returns:
        A dictionary with instantiated use cases.
    """
    return {
        "process_trace": ProcessTraceUseCase(storage=storage),
    }


def build_otlp_grpc_adapter(
    storage: TraceStoragePort, config: OtlpGrpcSettings
) -> OTLPgRPCAdapter:
    """Build and return the OTLP gRPC adapter with provided configuration.

    This function creates an instance of the OTLP gRPC adapter, configuring it
    with the appropriate use cases and server settings following the principles
    of dependency injection and hexagonal architecture.

    Args:
        storage: Concrete implementation of TraceStoragePort to be used by the adapter
        config: Configuration settings for the adapter

    Returns:
        OTLPgRPCAdapter: Configured and ready-to-use OTLP gRPC adapter
    """
    # Build the use case first (dependency inversion principle)
    use_cases = build_use_cases(storage)
    process_trace_use_case = use_cases["process_trace"]

    # Import the backward compatibility config model and convert to it
    # This maintains compatibility with the existing adapter implementation
    from .config.settings import OTLPGRPCServerConfig

    # Create a compatibility config object with values from new settings
    compat_config = OTLPGRPCServerConfig(
        host=config.host,
        port=config.port,
        max_buffer_size=config.buffer_max_size,
        max_message_length=config.max_message_length,
        # Use default values for the additional fields that don't exist in new settings
    )

    # Create and return the adapter with the compatibility config
    adapter = OTLPgRPCAdapter(
        process_trace_use_case=process_trace_use_case, config=compat_config
    )

    return adapter


def configure_grpc_server(settings: OtlpGrpcSettings) -> grpc.Server:
    """Configure gRPC server with provided settings.

    This function configures a gRPC server instance with the specified settings
    following the principles of dependency injection and configuration validation.

    Args:
        settings: The configuration settings to use for server configuration

    Returns:
        grpc.Server: A configured gRPC server instance
    """
    import concurrent.futures

    # Validate settings before creating the server
    if not validate_settings(settings):
        raise ValueError("Invalid configuration settings provided")

    # Create gRPC server with thread pool and configuration
    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_receive_message_length", settings.max_message_length),
            ("grpc.max_send_message_length", settings.max_message_length),
        ],
    )

    return server


def load_grpc_settings_with_fallback() -> OtlpGrpcSettings:
    """Load gRPC settings from environment variables with validation.

    This function loads the OTLP gRPC server configuration from environment
    variables following the Hexagonal Architecture principles, with proper
    validation and error handling for server startup.

    Returns:
        OtlpGrpcSettings: Validated configuration instance loaded from environment
    """
    # Load settings using the standard function
    settings = load_grpc_settings()

    # Validate settings
    if not validate_settings(settings):
        raise ValueError("Loaded configuration settings failed validation")

    return settings


def start_server_with_config(
    storage: TraceStoragePort, settings: OtlpGrpcSettings
) -> OTLPgRPCAdapter:
    """Start the OTLP gRPC server with the provided configuration and storage.

    Args:
        storage: Concrete implementation of TraceStoragePort for trace persistence
        settings: Configuration settings for the server

    Returns:
        OTLPgRPCAdapter: The started adapter instance
    """
    # Build the adapter with configuration
    adapter = build_otlp_grpc_adapter(storage, settings)

    # Start the server
    adapter.start_server()

    return adapter


def setup_signal_handlers(adapter: OTLPgRPCAdapter) -> None:
    """Set up signal handlers for graceful server shutdown.

    Args:
        adapter: The OTLP gRPC adapter to shut down gracefully
    """
    import signal
    import sys
    from types import FrameType
    from typing import Optional

    def signal_handler(signum: int, frame: Optional[FrameType]) -> None:
        print(f"\nReceived signal {signum}. Shutting down server gracefully...")
        adapter.stop_server()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def main() -> int:
    """Entrypoint for ``python -m obsvty``.

    Loads configuration from environment variables and starts the OTLP gRPC server
    following the principles of configuration as code and environment-based setup.
    The server is configured with the loaded settings and made ready to accept
    OTLP client connections.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Load environment variables first
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info(f"Loaded environment variables from {env_path}")
    else:
        # Attempt project-root .env if running from inside src
        project_env = Path(__file__).resolve().parents[2] / ".env"
        if project_env.exists():
            load_dotenv(dotenv_path=project_env)
        logger.info("No .env file found, using system environment variables")

    try:
        # Load configuration from environment variables
        settings = load_grpc_settings_with_fallback()

        logger.info(
            f"Starting OTLP gRPC server with configuration: host={settings.host}, port={settings.port}"
        )

        # Get the server endpoint for display
        endpoint = get_server_endpoint(settings)
        logger.info(f"Server endpoint: {endpoint}")
        print(f"OTLP gRPC server configured to start on {endpoint}")

        print("Note: Actual server startup requires concrete storage implementation.")
        print(
            "For full server functionality, provide a concrete TraceStoragePort implementation."
        )
        print(f"Configuration loaded successfully. Server would start on {endpoint}")

        # For a complete server startup, we would need a concrete storage implementation
        # This is where you would typically integrate with a real storage solution
        # such as a database adapter or file system adapter

        return 0

    except Exception as e:
        logger.error(f"Failed to start OTLP gRPC server: {e}", exc_info=True)
        print(f"Error starting server: {e}")
        return 1
