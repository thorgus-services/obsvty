"""Unit tests for trace parsing and buffer storage functionality."""

import time

from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.trace.v1 import trace_pb2

from src.obsvty.application.buffer_management import RejectWhenFullBuffer
from src.obsvty.domain.observability import TraceSpan, TraceId, SpanId, SpanStatus


def test_trace_parsing_from_otlp_to_domain():
    """Test parsing of OTLP span to domain TraceSpan object."""
    # Create an OTLP span
    otlp_span = trace_pb2.Span(
        trace_id=b"\x00" * 16,  # 16-byte trace ID
        span_id=b"\x00" * 8,  # 8-byte span ID
        name="test-span",
        kind=trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL,
        start_time_unix_nano=int(time.time() * 1_000_000_000),
        end_time_unix_nano=int(time.time() * 1_000_000_000) + 1000000,
        attributes=[
            common_pb2.KeyValue(
                key="key", value=common_pb2.AnyValue(string_value="value")
            )
        ],
    )

    # Simulate the parsing that would happen in OTLPgRPCAdapter
    trace_id = TraceId(value=otlp_span.trace_id.hex())
    span_id = SpanId(value=otlp_span.span_id.hex())
    parent_span_id = (
        SpanId(value=otlp_span.parent_span_id.hex())
        if otlp_span.parent_span_id
        else None
    )

    attributes = {}
    for attr in otlp_span.attributes:
        if attr.value.HasField("string_value"):
            attributes[attr.key] = attr.value.string_value

    status = SpanStatus(
        code=0,  # Using a valid default code
        message=None,
    )

    parsed_trace_span = TraceSpan(
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=parent_span_id,
        name=otlp_span.name,
        start_time_unix_nano=otlp_span.start_time_unix_nano,
        end_time_unix_nano=otlp_span.end_time_unix_nano,
        attributes=attributes,
        events=[],
        status=status,
        kind=otlp_span.kind,
    )

    assert parsed_trace_span.trace_id.value is not None
    assert len(parsed_trace_span.trace_id.value) == 32
    assert parsed_trace_span.span_id.value is not None
    assert len(parsed_trace_span.span_id.value) == 16
    assert parsed_trace_span.name is not None and parsed_trace_span.name != ""
    assert parsed_trace_span.start_time_unix_nano > 0
    assert (
        parsed_trace_span.end_time_unix_nano >= parsed_trace_span.start_time_unix_nano
    )
    assert "key" in parsed_trace_span.attributes
    assert parsed_trace_span.attributes["key"] == "value"


def test_trace_storage_in_buffer():
    """Test storing parsed traces in buffer."""
    buffer_manager = RejectWhenFullBuffer(max_size=100)

    trace_span = TraceSpan(
        trace_id=TraceId(value="a1b2c3d4e5f678901234567890abcdef"),  # 32 hex chars
        span_id=SpanId(value="a1b2c3d4e5f67890"),  # 16 hex chars
        parent_span_id=None,
        name="test-span",
        start_time_unix_nano=int(time.time() * 1_000_000_000),
        end_time_unix_nano=int(time.time() * 1_000_000_000) + 1000000,
        attributes={"key": "value"},
        events=[],
        status=SpanStatus(code=0, message=None),
        kind=1,
    )

    success = buffer_manager.add_span(trace_span)

    stored_spans = buffer_manager.get_spans(10)
    assert success
    assert len(stored_spans) == 1
    assert stored_spans[0].trace_id.value == trace_span.trace_id.value
    assert stored_spans[0].name == trace_span.name


def test_trace_storage_capacity_limit():
    """Test buffer capacity limits."""
    small_buffer = RejectWhenFullBuffer(max_size=3)

    add_results = []
    for i in range(5):
        # Generate unique trace IDs and span IDs as valid hex strings
        trace_id_base = "a1b2c3d4e5f678901234567890abcdef"
        span_id_base = "a1b2c3d4e5f67890"
        # Create unique IDs by modifying a few characters based on index i
        trace_id_value = (
            f"{trace_id_base[:31]}{i:x}" if i < 10 else f"{trace_id_base[:30]}{i:x}"
        )
        span_id_value = (
            f"{span_id_base[:15]}{i:x}" if i < 10 else f"{span_id_base[:14]}{i:x}"
        )
        # Ensure they are exactly 32 and 16 characters respectively
        trace_id_value = trace_id_value.ljust(32, "a")[:32]
        span_id_value = span_id_value.ljust(16, "a")[:16]

        trace_span = TraceSpan(
            trace_id=TraceId(value=trace_id_value),
            span_id=SpanId(value=span_id_value),
            parent_span_id=None,
            name=f"span-{i}",
            start_time_unix_nano=int(time.time() * 1_000_000_000) + i,
            end_time_unix_nano=int(time.time() * 1_000_000_000) + i + 1000000,
            attributes={"index": i},
            events=[],
            status=SpanStatus(code=0, message=None),
            kind=1,
        )
        result = small_buffer.add_span(trace_span)
        add_results.append(result)

    assert add_results[0]
    assert add_results[1]
    assert add_results[2]
    assert not add_results[3]
    assert not add_results[4]

    stored_spans = small_buffer.get_spans(10)
    assert len(stored_spans) == 3


def test_trace_retrieval_from_buffer():
    """Test retrieving stored traces from buffer."""
    buffer_manager = RejectWhenFullBuffer(max_size=100)

    span1 = TraceSpan(
        trace_id=TraceId(value="a1b2c3d4e5f678901234567890abcdef"),  # 32 hex chars
        span_id=SpanId(value="a1b2c3d4e5f67890"),  # 16 hex chars
        parent_span_id=None,
        name="retrieve-span-1",
        start_time_unix_nano=int(time.time() * 1_000_000_000),
        end_time_unix_nano=int(time.time() * 1_000_000_000) + 1000000,
        attributes={"test": "value1"},
        events=[],
        status=SpanStatus(code=0, message=None),
        kind=1,
    )

    span2 = TraceSpan(
        trace_id=TraceId(value="b1c2d3e4f5a678901234567890abcdef"),  # 32 hex chars
        span_id=SpanId(value="b1c2d3e4f5a67890"),  # 16 hex chars
        parent_span_id=None,
        name="retrieve-span-2",
        start_time_unix_nano=int(time.time() * 1_000_000_000) + 1,
        end_time_unix_nano=int(time.time() * 1_000_000_000) + 1 + 1000000,
        attributes={"test": "value2"},
        events=[],
        status=SpanStatus(code=0, message=None),
        kind=1,
    )

    buffer_manager.add_span(span1)
    buffer_manager.add_span(span2)

    retrieved_spans = buffer_manager.get_spans(10)

    assert len(retrieved_spans) == 2
    assert retrieved_spans[0].trace_id.value == span1.trace_id.value
    assert retrieved_spans[1].trace_id.value == span2.trace_id.value
    assert retrieved_spans[0].name == span1.name
    assert retrieved_spans[1].name == span2.name


def test_buffer_persistence_across_operations():
    """Test buffer maintains state across multiple operations."""
    buffer_manager = RejectWhenFullBuffer(max_size=100)

    initial_count = len(buffer_manager.get_spans(10))
    assert initial_count == 0

    span_a = TraceSpan(
        trace_id=TraceId(value="a1b2c3d4e5f678901234567890abcdef"),  # 32 hex chars
        span_id=SpanId(value="a1b2c3d4e5f67890"),  # 16 hex chars
        parent_span_id=None,
        name="span-a",
        start_time_unix_nano=100,
        end_time_unix_nano=200,
        attributes={"test": "a"},
        events=[],
        status=SpanStatus(code=0, message=None),
        kind=1,
    )

    span_b = TraceSpan(
        trace_id=TraceId(value="b1c2d3e4f5a678901234567890abcdef"),  # 32 hex chars
        span_id=SpanId(value="b1c2d3e4f5a67890"),  # 16 hex chars
        parent_span_id=None,
        name="span-b",
        start_time_unix_nano=100,
        end_time_unix_nano=200,
        attributes={"test": "b"},
        events=[],
        status=SpanStatus(code=0, message=None),
        kind=1,
    )

    buffer_manager.add_span(span_a)
    first_retrieval = buffer_manager.get_spans(10)

    buffer_manager.add_span(span_b)
    second_retrieval = buffer_manager.get_spans(10)

    assert len(first_retrieval) == 1
    assert first_retrieval[0].trace_id.value == "a1b2c3d4e5f678901234567890abcdef"

    assert len(second_retrieval) == 2
    assert second_retrieval[0].trace_id.value == "a1b2c3d4e5f678901234567890abcdef"
    assert second_retrieval[1].trace_id.value == "b1c2d3e4f5a678901234567890abcdef"


def test_buffer_clear_functionality():
    """Test buffer clear functionality."""
    buffer_manager = RejectWhenFullBuffer(max_size=100)

    span1 = TraceSpan(
        trace_id=TraceId(value="a1b2c3d4e5f678901234567890abcdef"),  # 32 hex chars
        span_id=SpanId(value="a1b2c3d4e5f67890"),  # 16 hex chars
        parent_span_id=None,
        name="span-1",
        start_time_unix_nano=100,
        end_time_unix_nano=200,
        attributes={"test": "clear1"},
        events=[],
        status=SpanStatus(code=0, message=None),
        kind=1,
    )

    span2 = TraceSpan(
        trace_id=TraceId(value="b1c2d3e4f5a678901234567890abcdef"),  # 32 hex chars
        span_id=SpanId(value="b1c2d3e4f5a67890"),  # 16 hex chars
        parent_span_id=None,
        name="span-2",
        start_time_unix_nano=100,
        end_time_unix_nano=200,
        attributes={"test": "clear2"},
        events=[],
        status=SpanStatus(code=0, message=None),
        kind=1,
    )

    buffer_manager.add_span(span1)
    buffer_manager.add_span(span2)

    assert len(buffer_manager.get_spans(10)) == 2

    buffer_manager.clear()

    assert len(buffer_manager.get_spans(10)) == 0
