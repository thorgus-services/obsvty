"""Unit tests for OTLP protocol validation logic."""

from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from opentelemetry.proto.trace.v1 import trace_pb2
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.resource.v1 import resource_pb2
import time

from src.obsvty.domain.observability import (
    validate_trace_id_format,
    validate_span_id_format,
    validate_span_structure,
    validate_resource_spans_structure,
    validate_trace_span_structure,
)


def test_validate_trace_id_format():
    assert validate_trace_id_format("a1b2c3d4e5f678901234567890abcdef") is True
    assert validate_trace_id_format("invalid_format") is False
    assert validate_trace_id_format(123) is False


def test_validate_span_id_format():
    assert validate_span_id_format("a1b2c3d4e5f67890") is True
    assert validate_span_id_format("invalid") is False
    assert validate_span_id_format(123) is False


def test_validate_span_structure():
    span_data = {
        "trace_id": "a1b2c3d4e5f678901234567890abcdef",
        "span_id": "a1b2c3d4e5f67890",
        "name": "test-span",
        "start_time_unix_nano": 100,
        "end_time_unix_nano": 200,
    }
    assert validate_span_structure(span_data) is True

    # Test invalid trace_id format
    span_data_invalid = span_data.copy()
    span_data_invalid["trace_id"] = "invalid"
    assert validate_span_structure(span_data_invalid) is False

    # Test end time before start time
    span_data_invalid = span_data.copy()
    span_data_invalid["start_time_unix_nano"] = 200
    span_data_invalid["end_time_unix_nano"] = 100
    assert validate_span_structure(span_data_invalid) is False


def test_validate_resource_spans_structure():
    resource_spans_data = {"scope_spans": []}
    assert validate_resource_spans_structure(resource_spans_data) is True

    resource_spans_data = {"instrumentation_library_spans": []}
    assert validate_resource_spans_structure(resource_spans_data) is True

    resource_spans_data = {"other_field": []}
    assert validate_resource_spans_structure(resource_spans_data) is False


def test_validate_trace_span_structure():
    trace_span_data = {
        "trace_id": "a1b2c3d4e5f678901234567890abcdef",
        "span_id": "a1b2c3d4e5f67890",
        "name": "test-span",
        "start_time_unix_nano": 100,
        "end_time_unix_nano": 200,
    }
    assert validate_trace_span_structure(trace_span_data) is True

    # Test invalid data
    assert validate_trace_span_structure("invalid") is False


class OtlpProtocolValidator:
    """OTLP protocol validation logic extracted from validation tests."""

    def validate_trace_format(
        self, trace_request: trace_service_pb2.ExportTraceServiceRequest
    ) -> bool:
        if not hasattr(trace_request, "resource_spans"):
            return False

        return all(
            self.validate_resource_span(rs) for rs in trace_request.resource_spans
        )

    def validate_resource_span(self, resource_span) -> bool:
        has_resource = hasattr(resource_span, "resource")
        has_scope_spans = hasattr(resource_span, "scope_spans")

        if has_resource and resource_span.resource:
            pass

        if has_scope_spans and resource_span.scope_spans:
            for scope_span in resource_span.scope_spans:
                if not self.validate_scope_span(scope_span):
                    return False

        return True

    def validate_scope_span(self, scope_span) -> bool:
        has_spans = hasattr(scope_span, "spans")

        if has_spans and scope_span.spans:
            for span in scope_span.spans:
                if not self.validate_span(span):
                    return False

        return True

    def validate_span(self, span) -> bool:
        if not span.name:
            return False

        if len(span.trace_id) != 16:
            return False

        if len(span.span_id) != 8:
            return False

        valid_kinds = [
            trace_pb2.Span.SpanKind.SPAN_KIND_UNSPECIFIED,
            trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL,
            trace_pb2.Span.SpanKind.SPAN_KIND_SERVER,
            trace_pb2.Span.SpanKind.SPAN_KIND_CLIENT,
            trace_pb2.Span.SpanKind.SPAN_KIND_PRODUCER,
            trace_pb2.Span.SpanKind.SPAN_KIND_CONSUMER,
        ]

        if span.kind not in valid_kinds:
            return False

        if span.start_time_unix_nano == 0:
            return False

        if span.end_time_unix_nano < span.start_time_unix_nano:
            return False

        return True


def test_otlp_protocol_trace_format_compliance():
    """Create a valid trace request following OTLP v1.9 specification"""
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
                                start_time_unix_nano=int(time.time() * 1_000_000_000),
                                end_time_unix_nano=int(time.time() * 1_000_000_000)
                                + 1000000,
                            )
                        ],
                    )
                ],
            )
        ]
    )

    validator = OtlpProtocolValidator()

    is_compliant = validator.validate_trace_format(trace_request)

    assert is_compliant, "Trace request should follow OTLP v1.9 specification"


def test_otlp_protocol_span_structure_compliance():
    """Create a valid trace request following OTLP v1.9 specification"""
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
                                start_time_unix_nano=int(time.time() * 1_000_000_000),
                                end_time_unix_nano=int(time.time() * 1_000_000_000)
                                + 1000000,
                            )
                        ],
                    )
                ],
            )
        ]
    )

    validator = OtlpProtocolValidator()

    for resource_span in trace_request.resource_spans:
        for scope_span in resource_span.scope_spans:
            for span in scope_span.spans:
                is_span_compliant = validator.validate_span(span)
                assert (
                    is_span_compliant
                ), f"Span {span.name} should follow OTLP v1.9 specification"


def test_otlp_protocol_fields_validation():
    """Create a valid trace request following OTLP v1.9 specification"""
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
                                start_time_unix_nano=int(time.time() * 1_000_000_000),
                                end_time_unix_nano=int(time.time() * 1_000_000_000)
                                + 1000000,
                            )
                        ],
                    )
                ],
            )
        ]
    )

    resource_spans = trace_request.resource_spans
    assert len(resource_spans) > 0

    scope_spans = resource_spans[0].scope_spans
    assert len(scope_spans) > 0

    spans = scope_spans[0].spans
    assert len(spans) > 0

    span = spans[0]

    assert span.name != ""
    assert len(span.trace_id) == 16
    assert len(span.span_id) == 8
    assert span.start_time_unix_nano > 0
    assert span.end_time_unix_nano >= span.start_time_unix_nano


def test_otlp_protocol_valid_span_kinds():
    """Create a valid trace request following OTLP v1.9 specification"""
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
                                start_time_unix_nano=int(time.time() * 1_000_000_000),
                                end_time_unix_nano=int(time.time() * 1_000_000_000)
                                + 1000000,
                            )
                        ],
                    )
                ],
            )
        ]
    )

    span = trace_request.resource_spans[0].scope_spans[0].spans[0]

    valid_kinds = [
        trace_pb2.Span.SpanKind.SPAN_KIND_UNSPECIFIED,
        trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL,
        trace_pb2.Span.SpanKind.SPAN_KIND_SERVER,
        trace_pb2.Span.SpanKind.SPAN_KIND_CLIENT,
        trace_pb2.Span.SpanKind.SPAN_KIND_PRODUCER,
        trace_pb2.Span.SpanKind.SPAN_KIND_CONSUMER,
    ]

    assert span.kind in valid_kinds
