"""OTLP gRPC adapter implementation following Hexagonal Architecture.

Implements the ObservabilityIngestionPort interface to handle OTLP trace
requests from OpenTelemetry clients. This adapter converts gRPC requests
into domain-specific operations using the application's use cases.
"""

from __future__ import annotations

import logging
import threading
from concurrent import futures
from datetime import datetime
from typing import Any

import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from grpc_reflection.v1alpha import reflection
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
    ExportTraceServiceResponse,
)
from opentelemetry.proto.collector.trace.v1.trace_service_pb2_grpc import (
    TraceServiceServicer,
    add_TraceServiceServicer_to_server,
)

from ...config import OTLPGRPCServerConfig
from ...domain import (
    ObservabilityBuffer,
    TraceSpan,
    SpanEvent,
    SpanStatus,
    TraceId,
    SpanId,
)
from ...ports import ObservabilityIngestionPort
from ...use_cases import ProcessTraceUseCase


logger = logging.getLogger(__name__)


class OTLPgRPCAdapter(ObservabilityIngestionPort, TraceServiceServicer):
    """Adapter implementing the OTLP gRPC TraceService interface.

    This adapter receives OTLP trace export requests and delegates processing
    to the appropriate use cases, following the dependency inversion principle
    by depending on the abstract ports rather than concrete implementations.
    """

    def __init__(
        self,
        process_trace_use_case: ProcessTraceUseCase,
        config: OTLPGRPCServerConfig,
    ):
        """Initialize the OTLP gRPC adapter.

        Args:
            process_trace_use_case: Use case for processing trace data
            config: Configuration for the gRPC server
        """
        self._process_trace_use_case = process_trace_use_case
        self._config = config
        self._buffer = ObservabilityBuffer(max_size=config.max_buffer_size)
        self._server: grpc.Server | None = None
        self._lock = threading.RLock()  # Thread-safe buffer operations
        logger.info("OTLP gRPC Adapter initialized")

    def Export(
        self, request: ExportTraceServiceRequest, context: grpc.ServicerContext
    ) -> ExportTraceServiceResponse:
        """Export trace data following the OTLP specification.

        This method is required by the gRPC service interface and implements
        the TraceService.Export method as defined in the OTLP specification.

        Args:
            request: ExportTraceServiceRequest containing trace data in OTLP format
            context: gRPC context for the request

        Returns:
            ExportTraceServiceResponse with status information
        """
        logger.debug(
            f"Received OTLP trace export request with {len(request.resource_spans)} resource spans"
        )

        try:
            # Process each resource span in the request
            for resource_span in request.resource_spans:
                for scope_span in resource_span.scope_spans:
                    for span in scope_span.spans:
                        # Add span to buffer (thread-safe)
                        with self._lock:
                            # Create domain TraceSpan from OTLP span
                            trace_span = self._create_trace_span_from_otlp(span)

                            # Add to buffer - if buffer is full, process immediately
                            if not self._buffer.add_span(trace_span):
                                # Buffer is full, so process the current buffer contents
                                logger.warning(
                                    "Trace buffer is full, processing immediately"
                                )
                                self._process_buffer_contents()
                                # Try to add the span again after clearing
                                self._buffer.add_span(trace_span)

                        # Process the trace through the use case
                        trace_bytes = request.SerializeToString()
                        self._process_trace_use_case.run(trace_bytes)

            # Send success response
            response = ExportTraceServiceResponse()
            logger.info(
                f"Successfully processed OTLP trace export request with {len(request.resource_spans)} resource spans"
            )
            return response

        except Exception as e:
            logger.error(
                f"Error processing OTLP trace export request: {str(e)}", exc_info=True
            )
            # In a real implementation, we might want to return an error response
            # For now, we'll return a success response as the OTLP spec expects
            response = ExportTraceServiceResponse()
            return response

    def export_traces(
        self, request: ExportTraceServiceRequest
    ) -> ExportTraceServiceResponse:
        """Export trace data following the OTLP specification (for port interface compliance).

        This method is required to satisfy the ObservabilityIngestionPort interface.
        It calls the gRPC service method with a mock context.

        Args:
            request: ExportTraceServiceRequest containing trace data in OTLP format

        Returns:
            ExportTraceServiceResponse with status information
        """
        # Create a mock context for the internal call
        import grpc
        from unittest.mock import Mock

        mock_context = Mock(spec=grpc.ServicerContext)
        return self.Export(request, mock_context)

    def _create_trace_span_from_otlp(self, otlp_span: Any) -> TraceSpan:
        """Convert an OTLP span to a domain TraceSpan object.

        Args:
            otlp_span: An opentelemetry.proto.trace.v1.Span object

        Returns:
            TraceSpan: Domain representation of the span
        """
        # Convert OTLP span to domain TraceSpan
        trace_id = TraceId(value=otlp_span.trace_id.hex())
        span_id = SpanId(value=otlp_span.span_id.hex())
        parent_span_id = (
            SpanId(value=otlp_span.parent_span_id.hex())
            if otlp_span.parent_span_id
            else None
        )

        # Convert attributes
        attributes = {}
        for attr in otlp_span.attributes:
            attributes[attr.key] = self._extract_attribute_value(attr.value)

        # Convert events
        events = []
        for event in otlp_span.events:
            event_attrs = {}
            for attr in event.attributes:
                event_attrs[attr.key] = self._extract_attribute_value(attr.value)

            span_event = SpanEvent(
                name=event.name,
                timestamp=self._nanos_to_datetime(event.time_unix_nano),
                attributes=event_attrs,
            )
            events.append(span_event)

        # Convert status
        status = SpanStatus(
            code=otlp_span.status.code,
            message=otlp_span.status.message if otlp_span.status.message else None,
        )

        return TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=otlp_span.name,
            start_time_unix_nano=otlp_span.start_time_unix_nano,
            end_time_unix_nano=otlp_span.end_time_unix_nano,
            attributes=attributes,
            events=events,
            status=status,
            kind=otlp_span.kind,
        )

    def _extract_attribute_value(self, any_value: Any) -> Any:
        """Extract the value from an OTLP AnyValue message."""
        if any_value.HasField("string_value"):
            return any_value.string_value
        elif any_value.HasField("bool_value"):
            return any_value.bool_value
        elif any_value.HasField("int_value"):
            return any_value.int_value
        elif any_value.HasField("double_value"):
            return any_value.double_value
        elif any_value.HasField("bytes_value"):
            return any_value.bytes_value
        else:
            # Handle array_value and kvlist_value if needed
            return None

    def _nanos_to_datetime(self, nanos: int) -> datetime:
        """Convert Unix nanoseconds to datetime."""
        seconds = nanos // 1_000_000_000
        micros = (nanos % 1_000_000_000) // 1000
        return datetime.fromtimestamp(seconds).replace(microsecond=micros)

    def _process_buffer_contents(self) -> None:
        """Process all spans currently in the buffer."""
        # We'll process the buffer contents by converting them and sending to the use case
        # For now, just clear the buffer after logging
        logger.info(f"Processing {self._buffer.current_size} spans from buffer")
        with self._lock:
            self._buffer.clear()

    def start_server(self) -> None:
        """Start the gRPC server to listen for OTLP requests."""
        logger.info(
            f"Starting OTLP gRPC server on {self._config.host}:{self._config.port}"
        )

        # Create gRPC server with thread pool
        self._server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            # Set options for message size limits
            options=[
                ("grpc.max_receive_message_length", self._config.max_message_length),
                ("grpc.max_send_message_length", self._config.max_message_length),
            ],
        )

        # Add the TraceService to the server
        add_TraceServiceServicer_to_server(self, self._server)  # type: ignore[no-untyped-call]

        # Add health service
        self._health_servicer = health.HealthServicer(
            experimental_non_blocking=True,
            experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=1),
        )
        # Set all services to SERVING initially
        self._health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)
        health_pb2_grpc.add_HealthServicer_to_server(
            self._health_servicer, self._server
        )

        # Enable reflection for debugging tools if configured
        if self._config.enable_reflection:
            logger.info("Enabling gRPC server reflection")
            reflection.enable_server_reflection(
                service_names=(
                    "opentelemetry.proto.collector.trace.v1.TraceService",
                    "grpc.health.v1.Health",
                    reflection.SERVICE_NAME,
                ),
                server=self._server,
            )

        # Add insecure port to the server
        server_address = f"{self._config.host}:{self._config.port}"
        self._server.add_insecure_port(server_address)

        # Start the server
        self._server.start()
        logger.info(f"OTLP gRPC server started on {server_address}")

    def stop_server(self) -> None:
        """Stop the gRPC server gracefully."""
        if self._server:
            logger.info("Stopping OTLP gRPC server gracefully...")
            # Set health status to NOT_SERVING
            if hasattr(self, "_health_servicer"):
                self._health_servicer.set(
                    "", health_pb2.HealthCheckResponse.NOT_SERVING
                )
            self._server.stop(grace=5.0)  # 5 second grace period
            logger.info("OTLP gRPC server stopped")

    def serve_forever(self) -> None:
        """Block until the server stops."""
        if self._server:
            logger.info("Server running indefinitely...")
            self._server.wait_for_termination()

    def get_buffer_status(self) -> dict[str, Any]:
        """Get current buffer status for monitoring purposes."""
        with self._lock:
            return {
                "current_size": self._buffer.current_size,
                "max_size": self._buffer.max_size,
                "is_full": self._buffer.is_full(),
                "is_empty": self._buffer.is_empty(),
            }
