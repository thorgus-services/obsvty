"""Integration tests for OTLP gRPC endpoint functionality."""

import grpc
from unittest.mock import Mock, patch
import pytest

from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.resource.v1 import resource_pb2
from opentelemetry.proto.trace.v1 import trace_pb2

from src.obsvty.adapters.messaging.otlp_grpc import OTLPgRPCAdapter
from src.obsvty.config import OtlpGrpcSettings


@pytest.fixture
def otlp_adapter(process_trace_use_case, otlp_config):
    return OTLPgRPCAdapter(process_trace_use_case, otlp_config)


def test_otlp_endpoint_accepts_valid_requests(
    otlp_adapter: OTLPgRPCAdapter,
    otlp_config: OtlpGrpcSettings,
) -> None:
    """Test if OTLP gRPC endpoint accepts valid requests."""
    # Create a valid trace request following OTLP v1.9 specification
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
                                trace_id=b"\x00" * 16,  # 16-byte trace ID
                                span_id=b"\x00" * 8,  # 8-byte span ID
                                name="test-span",
                                kind=trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL,
                                start_time_unix_nano=1000000000,
                                end_time_unix_nano=2000000000,
                            )
                        ],
                    )
                ],
            )
        ]
    )

    context = Mock(spec=grpc.ServicerContext)

    response = otlp_adapter.Export(trace_request, context)

    assert response is not None
    assert hasattr(response, "partial_success")


def test_otlp_endpoint_rejects_invalid_requests(
    otlp_adapter: OTLPgRPCAdapter,
) -> None:
    """Test if OTLP gRPC endpoint properly handles invalid requests."""
    # Create an invalid/empty trace request
    invalid_request = trace_service_pb2.ExportTraceServiceRequest()

    with patch("src.obsvty.adapters.messaging.otlp_grpc.logger"):
        context = Mock(spec=grpc.ServicerContext)
        response = otlp_adapter.Export(invalid_request, context)

        # Should still return a response but may log errors
        assert response is not None


def test_otlp_endpoint_connectivity(
    otlp_adapter: OTLPgRPCAdapter,
) -> None:
    """Test if OTLP gRPC endpoint responds to minimal requests."""
    minimal_request = trace_service_pb2.ExportTraceServiceRequest(resource_spans=[])

    context = Mock(spec=grpc.ServicerContext)
    response = otlp_adapter.Export(minimal_request, context)

    assert response is not None


def test_otlp_endpoint_multiple_requests(
    otlp_adapter: OTLPgRPCAdapter,
) -> None:
    """Test if OTLP gRPC endpoint can handle multiple requests sequentially."""
    # Create a base valid trace request
    base_request = trace_service_pb2.ExportTraceServiceRequest(
        resource_spans=[
            trace_pb2.ResourceSpans(
                scope_spans=[
                    trace_pb2.ScopeSpans(
                        spans=[
                            trace_pb2.Span(
                                trace_id=b"\x00" * 16,
                                span_id=b"\x00" * 8,
                                name="test-span",
                                kind=trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL,
                                start_time_unix_nano=1000000000,
                                end_time_unix_nano=2000000000,
                            )
                        ],
                    )
                ],
            )
        ]
    )

    context = Mock(spec=grpc.ServicerContext)

    for i in range(3):
        modified_request = trace_service_pb2.ExportTraceServiceRequest()
        modified_request.CopyFrom(base_request)

        trace_id_bytes = i.to_bytes(16, byteorder="big")
        modified_request.resource_spans[0].scope_spans[0].spans[
            0
        ].trace_id = trace_id_bytes

        response = otlp_adapter.Export(modified_request, context)
        assert response is not None
        assert hasattr(response, "partial_success")


def test_otlp_protocol_endpoint_conformance_with_valid_request(
    otlp_adapter: OTLPgRPCAdapter,
    otlp_config: OtlpGrpcSettings,
) -> None:
    """Test if OTLP gRPC endpoint follows protocol specification."""
    # Create a valid trace request following OTLP v1.9 specification
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
                                trace_id=b"\x00" * 16,  # 16-byte trace ID
                                span_id=b"\x00" * 8,  # 8-byte span ID
                                name="test-span",
                                kind=trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL,
                                start_time_unix_nano=1000000000,
                                end_time_unix_nano=2000000000,
                            )
                        ],
                    )
                ],
            )
        ]
    )

    context = Mock(spec=grpc.ServicerContext)
    response = otlp_adapter.Export(trace_request, context)

    assert response is not None
