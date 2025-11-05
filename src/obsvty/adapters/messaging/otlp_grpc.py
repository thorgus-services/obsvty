"""OTLP gRPC adapter implementing ObservabilityIngestionPort."""

import logging
import threading
from concurrent import futures
from datetime import datetime
from typing import Any
from unittest.mock import Mock

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

from ...config import OTLPGRPCServerConfig, OtlpGrpcSettings
from ...domain.observability import (
    TraceId,
    TraceSpan,
    SpanEvent,
    SpanStatus,
    SpanId,
)
from ...application.buffer_management import RejectWhenFullBuffer
from ...ports import ObservabilityIngestionPort
from ...use_cases import ProcessTraceUseCase


logger = logging.getLogger(__name__)


class OTLPgRPCAdapter(ObservabilityIngestionPort, TraceServiceServicer):
    """Adapter implementing the OTLP gRPC TraceService interface."""

    def __init__(
        self,
        process_trace_use_case: ProcessTraceUseCase,
        config: OTLPGRPCServerConfig | OtlpGrpcSettings,  # Support both config types
    ):
        self._process_trace_use_case = process_trace_use_case
        self._config = config

        # Handle both config types: new config uses buffer_max_size, old uses max_buffer_size
        if hasattr(config, "buffer_max_size"):
            buffer_size = config.buffer_max_size
        elif hasattr(config, "max_buffer_size"):
            buffer_size = config.max_buffer_size
        else:
            # Default value if neither attribute exists
            buffer_size = 1000

        self._buffer = RejectWhenFullBuffer(max_size=buffer_size)

        self._server: grpc.Server | None = None
        self._lock = threading.RLock()
        logger.info("OTLP gRPC Adapter initialized")

    def Export(
        self, request: ExportTraceServiceRequest, context: grpc.ServicerContext
    ) -> ExportTraceServiceResponse:
        """Export trace data following the OTLP specification."""
        logger.debug(
            f"Received OTLP trace export request with {len(request.resource_spans)} resource spans"
        )

        try:
            for resource_span in request.resource_spans:
                for scope_span in resource_span.scope_spans:
                    for span in scope_span.spans:
                        with self._lock:
                            trace_span = self._create_trace_span_from_otlp(span)

                            if not self._buffer.add_span(trace_span):
                                logger.warning(
                                    "Trace buffer is full, processing immediately"
                                )
                                self._process_buffer_contents()
                                self._buffer.add_span(trace_span)

                        trace_bytes = request.SerializeToString()
                        self._process_trace_use_case.run(trace_bytes)

            response = ExportTraceServiceResponse()
            logger.info(
                f"Successfully processed OTLP trace export request with {len(request.resource_spans)} resource spans"
            )
            return response

        except Exception as e:
            logger.error(
                f"Error processing OTLP trace export request: {str(e)}", exc_info=True
            )
            response = ExportTraceServiceResponse()
            return response

    def export_traces(
        self, request: ExportTraceServiceRequest
    ) -> ExportTraceServiceResponse:
        """Export trace data for port interface compliance."""
        mock_context = Mock(spec=grpc.ServicerContext)
        return self.Export(request, mock_context)

    def _create_trace_span_from_otlp(self, otlp_span: Any) -> TraceSpan:
        """Convert an OTLP span to a domain TraceSpan object."""
        trace_id = TraceId(value=otlp_span.trace_id.hex())
        span_id = SpanId(value=otlp_span.span_id.hex())
        parent_span_id = (
            SpanId(value=otlp_span.parent_span_id.hex())
            if otlp_span.parent_span_id
            else None
        )

        attributes = {}
        for attr in otlp_span.attributes:
            attributes[attr.key] = self._extract_attribute_value(attr.value)

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
            return None

    def _nanos_to_datetime(self, nanos: int) -> datetime:
        """Convert Unix nanoseconds to datetime."""
        seconds = nanos // 1_000_000_000
        micros = (nanos % 1_000_000_000) // 1000
        return datetime.fromtimestamp(seconds).replace(microsecond=micros)

    def _process_buffer_contents(self) -> None:
        """Process all spans currently in the buffer."""
        logger.info(f"Processing {self._buffer.size()} spans from buffer")

    def start_server(self) -> None:
        """Start the gRPC server to listen for OTLP requests."""
        logger.info(
            f"Starting OTLP gRPC server on {self._config.host}:{self._config.port}"
        )

        self._server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            options=[
                ("grpc.max_receive_message_length", self._config.max_message_length),
                ("grpc.max_send_message_length", self._config.max_message_length),
            ],
        )

        add_TraceServiceServicer_to_server(self, self._server)  # type: ignore[no-untyped-call]

        self._health_servicer = health.HealthServicer(
            experimental_non_blocking=True,
            experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=1),
        )
        self._health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)
        health_pb2_grpc.add_HealthServicer_to_server(
            self._health_servicer, self._server
        )

        # Enable reflection for debugging tools if configured (only available in old config)
        if (
            hasattr(self._config, "enable_reflection")
            and self._config.enable_reflection
        ):
            logger.info("Enabling gRPC server reflection")
            reflection.enable_server_reflection(
                service_names=(
                    "opentelemetry.proto.collector.trace.v1.TraceService",
                    "grpc.health.v1.Health",
                    reflection.SERVICE_NAME,
                ),
                server=self._server,
            )

        server_address = f"{self._config.host}:{self._config.port}"
        self._server.add_insecure_port(server_address)

        self._server.start()
        logger.info(f"OTLP gRPC server started on {server_address}")

    def stop_server(self) -> None:
        """Stop the gRPC server gracefully."""
        if self._server:
            logger.info("Stopping OTLP gRPC server gracefully...")
            if hasattr(self, "_health_servicer"):
                self._health_servicer.set(
                    "", health_pb2.HealthCheckResponse.NOT_SERVING
                )
            self._server.stop(grace=5.0)
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
                "current_size": self._buffer.size(),
                "max_size": self._buffer.max_size,
                "is_full": self._buffer.is_full(),
                "is_empty": self._buffer.is_empty(),
            }
