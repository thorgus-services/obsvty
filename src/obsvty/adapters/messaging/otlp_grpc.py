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

from ...config import OtlpGrpcSettings
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
    def __init__(
        self,
        process_trace_use_case: ProcessTraceUseCase,
        config: OtlpGrpcSettings,
    ):
        self._process_trace_use_case = process_trace_use_case
        self._config = config

        buffer_size = getattr(config, "max_buffer_size", 1000)

        self._buffer = RejectWhenFullBuffer(max_size=buffer_size)

        self._server: grpc.Server | None = None
        self._lock = threading.RLock()
        logger.info("OTLP gRPC Adapter initialized")

    def Export(
        self, request: ExportTraceServiceRequest, context: grpc.ServicerContext
    ) -> ExportTraceServiceResponse:
        logger.debug(
            f"Received OTLP trace export request with {len(request.resource_spans)} resource spans"
        )

        try:
            self._process_trace_request(request)
            response = ExportTraceServiceResponse()
            logger.info(
                f"Successfully processed OTLP trace export request with {len(request.resource_spans)} resource spans"
            )
            return response

        except Exception as e:
            logger.error(
                f"Error processing OTLP trace export request: {str(e)}", exc_info=True
            )
            return ExportTraceServiceResponse()

    def export_traces(
        self, request: ExportTraceServiceRequest
    ) -> ExportTraceServiceResponse:
        mock_context = Mock(spec=grpc.ServicerContext)
        return self.Export(request, mock_context)

    def _process_trace_request(self, request: ExportTraceServiceRequest) -> None:
        self._process_resource_spans(request.resource_spans)
        trace_bytes = request.SerializeToString()
        self._process_trace_use_case.run(trace_bytes)

    def _process_resource_spans(self, resource_spans: Any) -> None:
        for resource_span in resource_spans:
            self._process_scope_spans(resource_span.scope_spans)

    def _process_scope_spans(self, scope_spans: Any) -> None:
        for scope_span in scope_spans:
            self._process_spans(scope_span.spans)

    def _process_spans(self, spans: Any) -> None:
        for span in spans:
            trace_span = self._create_trace_span_from_otlp(span)
            self._handle_span_buffering(trace_span)

    def _handle_span_buffering(self, trace_span: TraceSpan) -> None:
        with self._lock:
            if not self._buffer.add_span(trace_span):
                logger.warning("Trace buffer is full, processing immediately")
                self._process_buffer_contents()

    def _create_trace_span_from_otlp(self, otlp_span: Any) -> TraceSpan:
        trace_id = TraceId(value=otlp_span.trace_id.hex())
        span_id = SpanId(value=otlp_span.span_id.hex())
        parent_span_id = (
            SpanId(value=otlp_span.parent_span_id.hex())
            if otlp_span.parent_span_id
            else None
        )

        attributes = self._extract_attributes(otlp_span.attributes)
        events = self._extract_events(otlp_span.events)
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

    def _extract_attributes(self, attributes: Any) -> dict[str, Any]:
        result = {}
        for attr in attributes:
            result[attr.key] = self._extract_attribute_value(attr.value)
        return result

    def _extract_events(self, events: Any) -> list[SpanEvent]:
        result = []
        for event in events:
            event_attrs = {}
            for attr in event.attributes:
                event_attrs[attr.key] = self._extract_attribute_value(attr.value)

            span_event = SpanEvent(
                name=event.name,
                timestamp=self._nanos_to_datetime(event.time_unix_nano),
                attributes=event_attrs,
            )
            result.append(span_event)
        return result

    def _extract_attribute_value(self, any_value: Any) -> Any:
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
        seconds = nanos // 1_000_000_000
        micros = (nanos % 1_000_000_000) // 1000
        return datetime.fromtimestamp(seconds).replace(microsecond=micros)

    def _process_buffer_contents(self) -> None:
        logger.info(f"Processing {self._buffer.size()} spans from buffer")

    def start_server(self) -> None:
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

        server_address = f"{self._config.host}:{self._config.port}"
        self._server.add_insecure_port(server_address)

        self._server.start()
        logger.info(f"OTLP gRPC server started on {server_address}")

    def stop_server(self) -> None:
        if self._server:
            logger.info("Stopping OTLP gRPC server gracefully...")
            self._health_servicer.set("", health_pb2.HealthCheckResponse.NOT_SERVING)
            self._server.stop(grace=5.0)
            logger.info("OTLP gRPC server stopped")

    def serve_forever(self) -> None:
        if self._server:
            logger.info("Server running indefinitely...")
            self._server.wait_for_termination()

    def get_buffer_status(self) -> dict[str, Any]:
        with self._lock:
            return {
                "current_size": self._buffer.size(),
                "max_size": self._buffer.max_size,
                "is_full": self._buffer.is_full(),
                "is_empty": self._buffer.is_empty(),
            }
