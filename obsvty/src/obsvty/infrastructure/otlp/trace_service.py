"""Trace service implementation for OTLP gRPC ingestion."""

import logging
import grpc
from concurrent import futures

from opentelemetry.proto.collector.trace.v1 import (
    trace_service_pb2,
    trace_service_pb2_grpc,
)
from opentelemetry.proto.collector.metrics.v1 import (
    metrics_service_pb2,
    metrics_service_pb2_grpc,
)
from opentelemetry.proto.collector.logs.v1 import (
    logs_service_pb2,
    logs_service_pb2_grpc,
)

from obsvty.application.ports.otlp_ports import OTLPIngestionPort


logger = logging.getLogger(__name__)


class TraceService(trace_service_pb2_grpc.TraceServiceServicer):  # type: ignore
    """gRPC service implementation for trace ingestion."""

    def __init__(self, ingestion_port: OTLPIngestionPort):
        self.ingestion_port = ingestion_port

    def Export(
        self,
        request: trace_service_pb2.ExportTraceServiceRequest,
        context: grpc.ServicerContext,
    ) -> trace_service_pb2.ExportTraceServiceResponse:
        """
        Handle the Export request for traces.

        Args:
            request: The OTLP trace export request
            context: gRPC context

        Returns:
            The OTLP trace export response with success status
        """
        try:
            # Convert the request to bytes for ingestion
            request_bytes = request.SerializeToString()

            # Process the trace data through the port
            self.ingestion_port.ingest_traces(request_bytes)

            logger.info(
                f"Successfully processed trace export request with {len(request.resource_spans)} resource spans"
            )

            # Return success response
            return trace_service_pb2.ExportTraceServiceResponse(
                partial_success=trace_service_pb2.ExportTracePartialSuccess()
            )
        except Exception as e:
            logger.error(f"Error processing trace export request: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return trace_service_pb2.ExportTraceServiceResponse()


class MetricsService(metrics_service_pb2_grpc.MetricsServiceServicer):  # type: ignore
    """gRPC service implementation for metrics ingestion."""

    def __init__(self, ingestion_port: OTLPIngestionPort):
        self.ingestion_port = ingestion_port

    def Export(
        self,
        request: metrics_service_pb2.ExportMetricsServiceRequest,
        context: grpc.ServicerContext,
    ) -> metrics_service_pb2.ExportMetricsServiceResponse:
        """
        Handle the Export request for metrics.

        Args:
            request: The OTLP metrics export request
            context: gRPC context

        Returns:
            The OTLP metrics export response with success status
        """
        try:
            # Convert the request to bytes for ingestion
            request_bytes = request.SerializeToString()

            # Process the metric data through the port
            self.ingestion_port.ingest_metrics(request_bytes)

            logger.info(
                f"Successfully processed metrics export request with {len(request.resource_metrics)} resource metrics"
            )

            # Return success response
            return metrics_service_pb2.ExportMetricsServiceResponse(
                partial_success=metrics_service_pb2.ExportMetricsPartialSuccess()
            )
        except Exception as e:
            logger.error(f"Error processing metrics export request: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return metrics_service_pb2.ExportMetricsServiceResponse()


class LogsService(logs_service_pb2_grpc.LogsServiceServicer):  # type: ignore
    """gRPC service implementation for logs ingestion."""

    def __init__(self, ingestion_port: OTLPIngestionPort):
        self.ingestion_port = ingestion_port

    def Export(
        self,
        request: logs_service_pb2.ExportLogsServiceRequest,
        context: grpc.ServicerContext,
    ) -> logs_service_pb2.ExportLogsServiceResponse:
        """
        Handle the Export request for logs.

        Args:
            request: The OTLP logs export request
            context: gRPC context

        Returns:
            The OTLP logs export response with success status
        """
        try:
            # Convert the request to bytes for ingestion
            request_bytes = request.SerializeToString()

            # Process the log data through the port
            self.ingestion_port.ingest_logs(request_bytes)

            logger.info(
                f"Successfully processed logs export request with {len(request.resource_logs)} resource logs"
            )

            # Return success response
            return logs_service_pb2.ExportLogsServiceResponse(
                partial_success=logs_service_pb2.ExportLogsPartialSuccess()
            )
        except Exception as e:
            logger.error(f"Error processing logs export request: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return logs_service_pb2.ExportLogsServiceResponse()


def create_grpc_server(
    ingestion_port: OTLPIngestionPort, port: int = 4317
) -> grpc.Server:
    """
    Create and configure a gRPC server with OTLP services.

    Args:
        ingestion_port: The port for OTLP ingestion
        port: The port number to bind the server to (default 4317 for OTLP)

    Returns:
        Configured gRPC server instance
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register the OTLP services
    trace_service_pb2_grpc.add_TraceServiceServicer_to_server(
        TraceService(ingestion_port), server
    )
    metrics_service_pb2_grpc.add_MetricsServiceServicer_to_server(
        MetricsService(ingestion_port), server
    )
    logs_service_pb2_grpc.add_LogsServiceServicer_to_server(
        LogsService(ingestion_port), server
    )

    # Add gRPC reflection for debugging tools
    try:
        from grpc_reflection.v1alpha import reflection

        reflection.enable_server_reflection(
            (
                trace_service_pb2.DESCRIPTOR.services_by_name["TraceService"].full_name,
                metrics_service_pb2.DESCRIPTOR.services_by_name[
                    "MetricsService"
                ].full_name,
                logs_service_pb2.DESCRIPTOR.services_by_name["LogsService"].full_name,
                reflection.SERVICE_NAME,
            ),
            server,
        )
    except ImportError:
        logger.warning("grpc_reflection not available, skipping server reflection")

    server.add_insecure_port(f"[::]:{port}")

    return server
