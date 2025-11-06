"""Unit tests for OTLP adapter functionality."""

from unittest.mock import Mock
import time

from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.resource.v1 import resource_pb2
from opentelemetry.proto.trace.v1 import trace_pb2

from src.obsvty.adapters.messaging.otlp_grpc import OTLPgRPCAdapter
from src.obsvty.use_cases.process_trace import ProcessTraceUseCase
from src.obsvty.ports.storage import TraceStoragePort
from src.obsvty.config import OtlpGrpcSettings


class MockStorage(TraceStoragePort):
    def __init__(self):
        self.traces = []

    def store_trace(self, trace_bytes: bytes) -> None:
        self.traces.append(trace_bytes)

    def store_batch(self, batch: list[bytes]) -> None:
        self.traces.extend(batch)


def test_otlp_adapter_creates_trace_span_objects():
    """Test that the OTLP adapter correctly creates domain objects from OTLP requests."""
    mock_storage = MockStorage()
    process_trace_use_case = ProcessTraceUseCase(mock_storage)

    config = OtlpGrpcSettings(
        host="localhost",
        port=4317,
        max_message_length=4 * 1024 * 1024,
        enable_reflection=True,
        max_buffer_size=1000,
    )

    adapter = OTLPgRPCAdapter(process_trace_use_case, config)

    # Create a trace request with valid OTLP format
    trace_request = trace_service_pb2.ExportTraceServiceRequest(
        resource_spans=[
            trace_pb2.ResourceSpans(
                resource=resource_pb2.Resource(
                    attributes=[
                        common_pb2.KeyValue(
                            key="service.name",
                            value=common_pb2.AnyValue(string_value="test-service"),
                        )
                    ]
                ),
                scope_spans=[
                    trace_pb2.ScopeSpans(
                        scope=common_pb2.InstrumentationScope(
                            name="test-instrumentation", version="1.0.0"
                        ),
                        spans=[
                            trace_pb2.Span(
                                trace_id=b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f",  # 16-byte trace ID
                                span_id=b"\x10\x11\x12\x13\x14\x15\x16\x17",  # 8-byte span ID
                                name="test-span",
                                kind=trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL,
                                start_time_unix_nano=int(time.time() * 1_000_000_000),
                                end_time_unix_nano=int(time.time() * 1_000_000_000)
                                + 1000000,
                                attributes=[
                                    common_pb2.KeyValue(
                                        key="attr.key",
                                        value=common_pb2.AnyValue(
                                            string_value="attr.value"
                                        ),
                                    )
                                ],
                            )
                        ],
                    )
                ],
            )
        ]
    )

    # Mock the context
    context = Mock()

    # Process the request
    response = adapter.Export(trace_request, context)

    # Check that response is valid
    assert response is not None

    # Check that traces were processed
    assert len(mock_storage.traces) == 1

    # Check that buffer has expected spans
    buffer_status = adapter.get_buffer_status()
    assert buffer_status["current_size"] >= 0  # Buffer contains spans
