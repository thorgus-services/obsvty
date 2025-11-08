"""Main application entry point for the OTLP gRPC ingestion service."""

from typing import Tuple, Any
from obsvty.infrastructure.otlp.grpc_server import start_grpc_server, GRPCServerConfig
from obsvty.infrastructure.buffer.memory_buffer import MemoryBuffer
from obsvty.application.ports.otlp_ports import OTLPIngestionPort
from obsvty.domain.services.otlp_processing import process_otlp_data
import logging


logger = logging.getLogger(__name__)


class OTLPIngestionService(OTLPIngestionPort):
    """Concrete implementation of OTLPIngestionPort that processes and stores data."""

    def __init__(self, buffer_port: Any) -> None:
        self.buffer = buffer_port

    def ingest_traces(self, trace_data: bytes) -> None:
        """Process and store trace data."""
        try:
            # Process the trace data using domain services
            otlp_data = process_otlp_data(trace_data, self.buffer)
            logger.info(f"Ingested {len(otlp_data.resource_spans)} spans")
        except Exception as e:
            logger.error(f"Error ingesting traces: {e}")
            raise

    def ingest_metrics(self, metric_data: bytes) -> None:
        """Process and store metric data."""
        try:
            # Add implementation for metrics
            # For now, just store in buffer
            logger.info(f"Ingested metrics data of size {len(metric_data)} bytes")
        except Exception as e:
            logger.error(f"Error ingesting metrics: {e}")
            raise

    def ingest_logs(self, log_data: bytes) -> None:
        """Process and store log data."""
        try:
            # Add implementation for logs
            # For now, just store in buffer
            logger.info(f"Ingested logs data of size {len(log_data)} bytes")
        except Exception as e:
            logger.error(f"Error ingesting logs: {e}")
            raise


def create_application(
    buffer_size: int = 1000,
) -> Tuple["OTLPIngestionService", "MemoryBuffer"]:
    """Create the OTLP ingestion application with default configuration."""
    # Create buffer
    buffer = MemoryBuffer(max_size=buffer_size)

    # Create ingestion service
    ingestion_service = OTLPIngestionService(buffer)

    return ingestion_service, buffer


def main(port: int = 4317, buffer_size: int = 1000) -> None:
    """Main entry point to start the OTLP gRPC server."""
    logger.info("Starting OTLP gRPC Ingestion Service...")

    # Create the application
    ingestion_service, buffer = create_application(buffer_size)

    # Create server configuration
    config = GRPCServerConfig(port=port, max_workers=10)

    # Start the gRPC server
    server = start_grpc_server(ingestion_service, config)

    logger.info(f"OTLP gRPC server listening on port {port}")

    try:
        # Keep the server running
        import time

        while True:
            time.sleep(86400)  # Sleep for a day, then repeat
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)
        logger.info("Server stopped")


if __name__ == "__main__":
    main()
