"""Unit tests for domain entities and value objects in the observability module.

This module contains comprehensive unit tests for the core domain entities
(TraceSpan, TraceId, SpanId, SpanEvent, SpanStatus, ObservabilityBuffer)
and validation functions following TDD principles.
"""

import pytest
from datetime import datetime

from src.obsvty.domain.observability import (
    ObservabilityBuffer,
    SpanEvent,
    SpanId,
    SpanStatus,
    TraceId,
    TraceSpan,
    validate_attributes_format,
    validate_resource_spans_structure,
    validate_scope_spans_structure,
    validate_span_structure,
    validate_span_id_format,
    validate_trace_id_format,
    validate_trace_span_structure,
)


class TestTraceId:
    """Test suite for TraceId value object."""

    def test_trace_id_creation_with_valid_hex_string(self) -> None:
        """Test creating a TraceId with a valid hex-encoded 32-character string."""
        trace_id = TraceId(value="12345678901234567890123456789012")
        assert trace_id.value == "12345678901234567890123456789012"

    def test_trace_id_creation_with_invalid_format_raises_error(self) -> None:
        """Test that creating a TraceId with invalid format raises ValueError."""
        with pytest.raises(ValueError):
            TraceId(value="invalid_trace_id")

        with pytest.raises(ValueError):
            TraceId(value="123")  # Too short

        with pytest.raises(ValueError):
            TraceId(value="123456789012345678901234567890123")  # Too long

    def test_trace_id_creation_with_empty_string_raises_error(self) -> None:
        """Test that creating a TraceId with empty string raises ValueError."""
        with pytest.raises(ValueError):
            TraceId(value="")

    def test_trace_id_format_validation(self) -> None:
        """Test trace ID format validation function."""
        assert validate_trace_id_format("12345678901234567890123456789012") is True
        assert (
            validate_trace_id_format("1234567890123456789012345678901g") is False
        )  # Contains 'g'
        assert validate_trace_id_format("123") is False  # Too short
        assert validate_trace_id_format("") is False  # Empty


class TestSpanId:
    """Test suite for SpanId value object."""

    def test_span_id_creation_with_valid_hex_string(self) -> None:
        """Test creating a SpanId with a valid hex-encoded 16-character string."""
        span_id = SpanId(value="1234567890123456")
        assert span_id.value == "1234567890123456"

    def test_span_id_creation_with_invalid_format_raises_error(self) -> None:
        """Test that creating a SpanId with invalid format raises ValueError."""
        with pytest.raises(ValueError):
            SpanId(value="invalid_span_id")

        with pytest.raises(ValueError):
            SpanId(value="123")  # Too short

        with pytest.raises(ValueError):
            SpanId(value="12345678901234567")  # Too long

    def test_span_id_creation_with_empty_string_raises_error(self) -> None:
        """Test that creating a SpanId with empty string raises ValueError."""
        with pytest.raises(ValueError):
            SpanId(value="")

    def test_span_id_format_validation(self) -> None:
        """Test span ID format validation function."""
        assert validate_span_id_format("1234567890123456") is True
        assert validate_span_id_format("123456789012345g") is False  # Contains 'g'
        assert validate_span_id_format("123") is False  # Too short
        assert validate_span_id_format("") is False  # Empty


class TestSpanEvent:
    """Test suite for SpanEvent value object."""

    def test_span_event_creation_with_valid_data(self) -> None:
        """Test creating a SpanEvent with valid data."""
        event = SpanEvent(
            name="test_event", timestamp=datetime.now(), attributes={"key": "value"}
        )
        assert event.name == "test_event"
        assert event.attributes == {"key": "value"}

    def test_span_event_creation_with_empty_name_raises_error(self) -> None:
        """Test that creating a SpanEvent with empty name raises ValueError."""
        with pytest.raises(ValueError):
            SpanEvent(name="", timestamp=datetime.now(), attributes={"key": "value"})


class TestSpanStatus:
    """Test suite for SpanStatus value object."""

    def test_span_status_creation_with_valid_codes(self) -> None:
        """Test creating a SpanStatus with valid codes."""
        # UNSET
        status = SpanStatus(code=0)
        assert status.code == 0
        assert status.message is None

        # OK
        status = SpanStatus(code=1, message="Success")
        assert status.code == 1
        assert status.message == "Success"

        # ERROR
        status = SpanStatus(code=2)
        assert status.code == 2

    def test_span_status_creation_with_invalid_code_raises_error(self) -> None:
        """Test that creating a SpanStatus with invalid code raises ValueError."""
        with pytest.raises(ValueError):
            SpanStatus(code=3)  # Invalid code

        with pytest.raises(ValueError):
            SpanStatus(code=-1)  # Invalid code

    def test_span_status_creation_with_invalid_message_type_raises_error(self) -> None:
        """Test that creating a SpanStatus with invalid message type raises ValueError."""
        with pytest.raises(ValueError):
            SpanStatus(code=1, message=123)  # Message should be string


class TestTraceSpan:
    """Test suite for TraceSpan entity."""

    def test_trace_span_creation_with_valid_data(self) -> None:
        """Test creating a TraceSpan with valid data."""
        trace_id = TraceId(value="12345678901234567890123456789012")
        span_id = SpanId(value="1234567890123456")
        parent_span_id = SpanId(value="abcdefabcdefabcd")

        status = SpanStatus(code=1, message="OK")
        event = SpanEvent(
            name="test_event", timestamp=datetime.now(), attributes={"key": "value"}
        )

        span = TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name="test_span",
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={"attr_key": "attr_value"},
            events=[event],
            status=status,
        )

        assert span.trace_id == trace_id
        assert span.span_id == span_id
        assert span.parent_span_id == parent_span_id
        assert span.name == "test_span"
        assert span.start_time_unix_nano == 1000000000
        assert span.end_time_unix_nano == 2000000000
        assert span.attributes == {"attr_key": "attr_value"}
        assert len(span.events) == 1
        assert span.status == status
        assert span.kind == 0

    def test_trace_span_creation_with_empty_name_raises_error(self) -> None:
        """Test that creating a TraceSpan with empty name raises ValueError."""
        trace_id = TraceId(value="12345678901234567890123456789012")
        span_id = SpanId(value="1234567890123456")
        status = SpanStatus(code=0)

        with pytest.raises(ValueError):
            TraceSpan(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=None,
                name="",
                start_time_unix_nano=1000000000,
                end_time_unix_nano=2000000000,
                attributes={},
                events=[],
                status=status,
            )

    def test_trace_span_creation_with_negative_start_time_raises_error(self) -> None:
        """Test that creating a TraceSpan with negative start time raises ValueError."""
        trace_id = TraceId(value="12345678901234567890123456789012")
        span_id = SpanId(value="1234567890123456")
        status = SpanStatus(code=0)

        with pytest.raises(ValueError):
            TraceSpan(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=None,
                name="test_span",
                start_time_unix_nano=-1,
                end_time_unix_nano=2000000000,
                attributes={},
                events=[],
                status=status,
            )

    def test_trace_span_creation_with_end_time_before_start_time_raises_error(
        self,
    ) -> None:
        """Test that creating a TraceSpan with end time before start time raises ValueError."""
        trace_id = TraceId(value="12345678901234567890123456789012")
        span_id = SpanId(value="1234567890123456")
        status = SpanStatus(code=0)

        with pytest.raises(ValueError):
            TraceSpan(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=None,
                name="test_span",
                start_time_unix_nano=2000000000,
                end_time_unix_nano=1000000000,  # Before start time
                attributes={},
                events=[],
                status=status,
            )

    def test_trace_span_creation_with_invalid_kind_raises_error(self) -> None:
        """Test that creating a TraceSpan with invalid kind raises ValueError."""
        trace_id = TraceId(value="12345678901234567890123456789012")
        span_id = SpanId(value="1234567890123456")
        status = SpanStatus(code=0)

        with pytest.raises(ValueError):
            TraceSpan(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=None,
                name="test_span",
                start_time_unix_nano=1000000000,
                end_time_unix_nano=2000000000,
                attributes={},
                events=[],
                status=status,
                kind=5,  # Invalid kind
            )


class TestObservabilityBuffer:
    """Test suite for ObservabilityBuffer value object."""

    def test_buffer_creation_with_valid_max_size(self) -> None:
        """Test creating an ObservabilityBuffer with valid max size."""
        buffer = ObservabilityBuffer(max_size=100)
        assert buffer.max_size == 100
        assert buffer.current_size == 0
        assert len(buffer.buffer) == 0

    def test_buffer_creation_with_invalid_max_size_raises_error(self) -> None:
        """Test that creating a buffer with invalid max size raises ValueError."""
        with pytest.raises(ValueError):
            ObservabilityBuffer(max_size=0)

        with pytest.raises(ValueError):
            ObservabilityBuffer(max_size=-1)

    def test_buffer_add_span_successfully(self) -> None:
        """Test adding a span to the buffer successfully."""
        buffer = ObservabilityBuffer(max_size=2)
        assert buffer.is_empty() is True
        assert buffer.is_full() is False

        # Create a test span
        trace_id = TraceId(value="12345678901234567890123456789012")
        span_id = SpanId(value="1234567890123456")
        status = SpanStatus(code=0)
        span = TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=None,
            name="test_span",
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status=status,
        )

        # Add span to buffer
        result = buffer.add_span(span)
        assert result is True
        assert buffer.current_size == 1
        assert len(buffer.buffer) == 1
        assert buffer.is_empty() is False

    def test_buffer_add_span_when_full_returns_false(self) -> None:
        """Test that adding a span to a full buffer returns False."""
        buffer = ObservabilityBuffer(max_size=1)
        assert buffer.is_full() is False

        # Create a test span
        trace_id = TraceId(value="12345678901234567890123456789012")
        span_id = SpanId(value="1234567890123456")
        status = SpanStatus(code=0)
        span = TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=None,
            name="test_span",
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status=status,
        )

        # Add first span
        result1 = buffer.add_span(span)
        assert result1 is True
        assert buffer.is_full() is True

        # Try to add another span - should fail
        result2 = buffer.add_span(span)
        assert result2 is False
        assert buffer.current_size == 1
        assert len(buffer.buffer) == 1

    def test_buffer_clear(self) -> None:
        """Test clearing the buffer."""
        buffer = ObservabilityBuffer(max_size=10)

        # Add a span
        trace_id = TraceId(value="12345678901234567890123456789012")
        span_id = SpanId(value="1234567890123456")
        status = SpanStatus(code=0)
        span = TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=None,
            name="test_span",
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status=status,
        )

        buffer.add_span(span)
        assert buffer.current_size == 1
        assert buffer.is_empty() is False

        # Clear the buffer
        buffer.clear()
        assert buffer.current_size == 0
        assert len(buffer.buffer) == 0
        assert buffer.is_empty() is True


class TestValidationFunctions:
    """Test suite for validation functions."""

    def test_validate_trace_span_structure_with_valid_data(self) -> None:
        """Test that validate_trace_span_structure returns True for valid data."""
        valid_span_data = {
            "trace_id": "12345678901234567890123456789012",
            "span_id": "1234567890123456",
            "name": "test_span",
            "start_time_unix_nano": 1000000000,
            "end_time_unix_nano": 2000000000,
        }
        assert validate_trace_span_structure(valid_span_data) is True

    def test_validate_trace_span_structure_with_missing_required_fields(self) -> None:
        """Test that validate_trace_span_structure returns False for missing required fields."""
        invalid_span_data = {
            "trace_id": "12345678901234567890123456789012",
            "span_id": "1234567890123456",
            # Missing 'name', 'start_time_unix_nano', 'end_time_unix_nano'
        }
        assert validate_trace_span_structure(invalid_span_data) is False

    def test_validate_resource_spans_structure_with_valid_data(self) -> None:
        """Test that validate_resource_spans_structure returns True for valid data."""
        valid_resource_spans_data = {"scope_spans": [{"spans": []}]}
        assert validate_resource_spans_structure(valid_resource_spans_data) is True

    def test_validate_resource_spans_structure_without_scope_spans(self) -> None:
        """Test that validate_resource_spans_structure returns True for data with instrumentation_library_spans."""
        valid_resource_spans_data = {"instrumentation_library_spans": [{"spans": []}]}
        assert validate_resource_spans_structure(valid_resource_spans_data) is True

    def test_validate_resource_spans_structure_with_invalid_data(self) -> None:
        """Test that validate_resource_spans_structure returns False for invalid data."""
        invalid_resource_spans_data = {
            # Missing both 'scope_spans' and 'instrumentation_library_spans'
        }
        assert validate_resource_spans_structure(invalid_resource_spans_data) is False

    def test_validate_scope_spans_structure_with_valid_data(self) -> None:
        """Test that validate_scope_spans_structure returns True for valid data."""
        valid_scope_spans_data = {"spans": []}
        assert validate_scope_spans_structure(valid_scope_spans_data) is True

    def test_validate_scope_spans_structure_without_spans(self) -> None:
        """Test that validate_scope_spans_structure returns False for data without spans."""
        invalid_scope_spans_data = {
            # Missing 'spans'
        }
        assert validate_scope_spans_structure(invalid_scope_spans_data) is False

    def test_validate_span_structure_with_valid_data(self) -> None:
        """Test that validate_span_structure returns True for valid data."""
        valid_span_data = {
            "trace_id": "12345678901234567890123456789012",
            "span_id": "1234567890123456",
            "name": "test_span",
            "start_time_unix_nano": 1000000000,
            "end_time_unix_nano": 2000000000,
        }
        assert validate_span_structure(valid_span_data) is True

    def test_validate_span_structure_with_invalid_data(self) -> None:
        """Test that validate_span_structure returns False for invalid data."""
        # Missing required fields
        invalid_span_data = {
            "trace_id": "12345678901234567890123456789012",
            "span_id": "1234567890123456",
            # Missing 'name', 'start_time_unix_nano', 'end_time_unix_nano'
        }
        assert validate_span_structure(invalid_span_data) is False

        # Invalid trace_id format
        invalid_span_data = {
            "trace_id": "invalid_trace_id",  # Invalid format
            "span_id": "1234567890123456",
            "name": "test_span",
            "start_time_unix_nano": 1000000000,
            "end_time_unix_nano": 2000000000,
        }
        assert validate_span_structure(invalid_span_data) is False

        # Invalid span_id format
        invalid_span_data = {
            "trace_id": "12345678901234567890123456789012",
            "span_id": "invalid_span_id",  # Invalid format
            "name": "test_span",
            "start_time_unix_nano": 1000000000,
            "end_time_unix_nano": 2000000000,
        }
        assert validate_span_structure(invalid_span_data) is False

        # End time before start time
        invalid_span_data = {
            "trace_id": "12345678901234567890123456789012",
            "span_id": "1234567890123456",
            "name": "test_span",
            "start_time_unix_nano": 2000000000,
            "end_time_unix_nano": 1000000000,  # Before start time
        }
        assert validate_span_structure(invalid_span_data) is False

    def test_validate_attributes_format(self) -> None:
        """Test the validate_attributes_format function."""
        # Valid dictionary format
        assert validate_attributes_format({"key": "value"}) is True

        # Valid list format
        assert (
            validate_attributes_format(
                [
                    {"key": "name", "value": {"stringValue": "test"}},
                    {"key": "count", "value": {"intValue": 5}},
                ]
            )
            is True
        )

        # None is valid
        assert validate_attributes_format(None) is True

        # Invalid format
        assert validate_attributes_format("invalid") is False
        assert validate_attributes_format(123) is False
        assert (
            validate_attributes_format(
                [
                    {"value": {"stringValue": "test"}}  # Missing 'key'
                ]
            )
            is False
        )
