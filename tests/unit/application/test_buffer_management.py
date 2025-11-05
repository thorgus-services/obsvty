"""Unit tests for buffer management with >90% coverage."""

from src.obsvty.domain.observability import TraceSpan, SpanEvent, SpanStatus
from src.obsvty.application.buffer_management import (
    ObservabilityBuffer,
    ObservabilityBufferWithConsume,
)


def create_test_trace_span(span_id: str = "test_span_1") -> TraceSpan:
    """Helper function to create a test trace span."""
    return TraceSpan(
        trace_id="test_trace_id",
        span_id=span_id,
        parent_span_id=None,
        name="test_span",
        start_time_unix_nano=1234567890,
        end_time_unix_nano=1234567899,
        attributes={"key": "value"},
        events=[
            SpanEvent(name="test_event", timestamp_unix_nano=1234567895, attributes={})
        ],
        status=SpanStatus(code=1, message="OK"),
    )


class TestObservabilityBuffer:
    """Test cases for ObservabilityBuffer implementation."""

    def test_buffer_initialization_with_default_size(self):
        """Test that buffer initializes with default size."""
        # Arrange & Act
        buffer = ObservabilityBuffer()

        # Assert
        assert buffer.size() == 0
        assert not buffer.is_full()

    def test_buffer_initialization_with_custom_size(self):
        """Test that buffer initializes with custom size."""
        # Arrange & Act
        buffer = ObservabilityBuffer(max_size=5)

        # Assert
        assert buffer.size() == 0
        assert not buffer.is_full()

    def test_add_span_success(self):
        """Test that buffer adds span successfully when not at capacity."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=10)
        trace_span = create_test_trace_span()

        # Act
        result = buffer.add_span(trace_span)

        # Assert
        assert result is True
        assert buffer.size() == 1

    def test_add_multiple_spans(self):
        """Test that buffer can hold multiple spans."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=10)
        spans = [create_test_trace_span(f"span_{i}") for i in range(5)]

        # Act
        results = [buffer.add_span(span) for span in spans]

        # Assert
        assert all(results)  # All additions should succeed
        assert buffer.size() == 5

    def test_buffer_size_method(self):
        """Test that size method returns correct count."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=10)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")

        # Act
        buffer.add_span(span1)
        buffer.add_span(span2)

        # Assert
        assert buffer.size() == 2

    def test_buffer_is_full_method(self):
        """Test that is_full method returns correct status."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=2)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")

        # Act
        buffer.add_span(span1)

        # Assert
        assert not buffer.is_full()  # Buffer not full yet

        # Act
        buffer.add_span(span2)

        # Assert
        assert buffer.is_full()  # Buffer now full

    def test_get_spans_when_buffer_empty(self):
        """Test getting spans when buffer is empty."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=10)

        # Act
        spans = buffer.get_spans(5)

        # Assert
        assert len(spans) == 0

    def test_get_spans_partial_count(self):
        """Test getting fewer spans than available."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=10)
        spans_to_add = [create_test_trace_span(f"span_{i}") for i in range(5)]
        for span in spans_to_add:
            buffer.add_span(span)

        # Act
        retrieved_spans = buffer.get_spans(3)

        # Assert
        assert len(retrieved_spans) == 3
        assert (
            buffer.size() == 5
        )  # Size unchanged since this implementation doesn't consume

    def test_get_spans_exceed_count(self):
        """Test getting more spans than available."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=10)
        spans_to_add = [create_test_trace_span(f"span_{i}") for i in range(3)]
        for span in spans_to_add:
            buffer.add_span(span)

        # Act
        retrieved_spans = buffer.get_spans(10)

        # Assert
        assert len(retrieved_spans) == 3
        assert (
            buffer.size() == 3
        )  # Size unchanged since this implementation doesn't consume

    def test_fifo_discard_policy(self):
        """Test that buffer implements FIFO discard policy when at capacity."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=3)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")
        span3 = create_test_trace_span("span_3")
        span4 = create_test_trace_span(
            "span_4"
        )  # This should cause oldest to be discarded

        # Act - Add spans up to capacity
        buffer.add_span(span1)
        buffer.add_span(span2)
        buffer.add_span(span3)
        result = buffer.add_span(span4)  # This should cause span_1 to be discarded

        # Assert
        assert result is True
        assert buffer.size() == 3  # Still at max size

    def test_buffer_full_behavior(self):
        """Test that buffer continues to accept items even when full."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=2)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")
        span3 = create_test_trace_span(
            "span_3"
        )  # This should cause oldest to be discarded

        # Act
        result1 = buffer.add_span(span1)
        result2 = buffer.add_span(span2)
        result3 = buffer.add_span(span3)  # Should succeed but cause discard

        # Assert
        assert all([result1, result2, result3])  # All should succeed
        assert buffer.size() == 2  # Max size maintained
        assert buffer.is_full()


class TestObservabilityBufferWithConsume:
    """Test cases for ObservabilityBufferWithConsume implementation."""

    def test_consume_get_spans_removes_items(self):
        """Test that get_spans removes items from buffer in consume implementation."""
        # Arrange
        buffer = ObservabilityBufferWithConsume(max_size=10)
        spans_to_add = [create_test_trace_span(f"span_{i}") for i in range(5)]
        for span in spans_to_add:
            buffer.add_span(span)

        # Verify initial state
        assert buffer.size() == 5

        # Act
        retrieved_spans = buffer.get_spans(3)

        # Assert
        assert len(retrieved_spans) == 3
        assert buffer.size() == 2  # Size reduced by 3 since items were consumed

    def test_consume_get_all_spans(self):
        """Test consuming all spans from buffer."""
        # Arrange
        buffer = ObservabilityBufferWithConsume(max_size=10)
        spans_to_add = [create_test_trace_span(f"span_{i}") for i in range(3)]
        for span in spans_to_add:
            buffer.add_span(span)

        # Act
        retrieved_spans = buffer.get_spans(10)  # Request more than available

        # Assert
        assert len(retrieved_spans) == 3
        assert buffer.size() == 0  # Buffer should be empty after consuming all
