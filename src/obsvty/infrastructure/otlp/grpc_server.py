"""gRPC server configuration and startup."""

import logging
from typing import Optional
import grpc

from obsvty.infrastructure.otlp.trace_service import create_grpc_server
from obsvty.application.ports.otlp_ports import OTLPIngestionPort


logger = logging.getLogger(__name__)


class GRPCServerConfig:
    """Configuration for the OTLP gRPC server."""

    def __init__(
        self,
        port: int = 4317,
        max_workers: int = 10,
        max_message_length: int = 4 * 1024 * 1024,  # 4MB
    ):
        self.port = port
        self.max_workers = max_workers
        self.max_message_length = max_message_length


def start_grpc_server(
    ingestion_port: OTLPIngestionPort, config: Optional[GRPCServerConfig] = None
) -> grpc.Server:
    """
    Start the OTLP gRPC server.

    Args:
        ingestion_port: The port for OTLP ingestion
        config: Optional server configuration

    Returns:
        The started gRPC server instance
    """
    if config is None:
        config = GRPCServerConfig()

    logger.info(f"Starting OTLP gRPC server on port {config.port}")

    # Create the gRPC server with the specified configuration
    server = create_grpc_server(ingestion_port, config.port)

    # Start the server
    server.start()

    logger.info(f"OTLP gRPC server started successfully on port {config.port}")

    return server
