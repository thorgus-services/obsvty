"""Comprehensive tests for buffer management to achieve >90% coverage."""

import pytest
from src.obsvty.domain.observability import TraceSpan, SpanEvent, SpanStatus
from src.obsvty.application.buffer_management import (
    ObservabilityBuffer,
    ObservabilityBufferWithConsume,
    TraceBufferPortReadOnly,
    RejectWhenFullBuffer,
)


def create_test_trace_span(span_id: str = "test_span_01234567") -> TraceSpan:
    """Helper function to create a test trace span."""
    return TraceSpan(
        trace_id="0211a9f06dc228362a23942e479043d3",
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


class TestTraceBufferPortReadOnly:
    """Test cases for TraceBufferPortReadOnly implementation."""

    def test_readonly_buffer_initialization(self):
        """Test that readonly buffer initializes correctly."""
        # Arrange & Act
        buffer = TraceBufferPortReadOnly(max_size=5)

        # Assert
        assert buffer.size() == 0
        assert buffer.max_size == 5
        assert buffer.current_size == 0
        assert buffer.is_empty()
        assert not buffer.is_full()

    def test_readonly_buffer_initialization_default_size(self):
        """Test that readonly buffer initializes with default size."""
        # Arrange & Act
        buffer = TraceBufferPortReadOnly()

        # Assert
        assert buffer.size() == 0
        assert buffer.max_size == 1000  # default

    def test_readonly_buffer_invalid_size_raises_error(self):
        """Test that readonly buffer raises error for non-positive size."""
        # Act & Assert
        with pytest.raises(ValueError, match="max_size must be positive"):
            TraceBufferPortReadOnly(max_size=0)

        with pytest.raises(ValueError, match="max_size must be positive"):
            TraceBufferPortReadOnly(max_size=-1)

    def test_readonly_add_span(self):
        """Test that readonly buffer adds spans correctly."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=5)
        trace_span = create_test_trace_span()

        # Act
        result = buffer.add_span(trace_span)

        # Assert
        assert result is True
        assert buffer.size() == 1

    def test_readonly_get_spans_does_not_consume(self):
        """Test that getting spans does not consume them in readonly buffer."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=10)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")
        buffer.add_span(span1)
        buffer.add_span(span2)

        # Act
        spans = buffer.get_spans(5)

        # Assert
        assert len(spans) == 2
        assert buffer.size() == 2  # Size unchanged since it's readonly

    def test_readonly_get_spans_partial(self):
        """Test getting partial spans from readonly buffer."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=10)
        spans_to_add = [create_test_trace_span(f"span_{i:02d}") for i in range(5)]
        for span in spans_to_add:
            buffer.add_span(span)

        # Act
        retrieved_spans = buffer.get_spans(3)

        # Assert
        assert len(retrieved_spans) == 3
        assert buffer.size() == 5  # Size unchanged since it's readonly

    def test_readonly_buffer_max_size_property(self):
        """Test the max_size property."""
        # Arrange & Act
        buffer = TraceBufferPortReadOnly(max_size=7)

        # Assert
        assert buffer.max_size == 7

    def test_readonly_buffer_current_size_property(self):
        """Test the current_size property."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=10)
        span = create_test_trace_span("span_1")

        # Act
        buffer.add_span(span)

        # Assert
        assert buffer.current_size == 1

    def test_readonly_buffer_is_empty_method(self):
        """Test the is_empty method."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=5)

        # Assert
        assert buffer.is_empty()

        # Act
        buffer.add_span(create_test_trace_span())

        # Assert
        assert not buffer.is_empty()

    def test_readonly_buffer_is_full_method(self):
        """Test the is_full method."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=2)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")

        # Assert
        assert not buffer.is_full()

        # Act
        buffer.add_span(span1)
        buffer.add_span(span2)

        # Assert
        assert buffer.is_full()

    def test_readonly_buffer_clear_method(self):
        """Test the clear method."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=10)
        buffer.add_span(create_test_trace_span("span_1"))
        buffer.add_span(create_test_trace_span("span_2"))

        # Assert
        assert buffer.size() == 2

        # Act
        buffer.clear()

        # Assert
        assert buffer.size() == 0
        assert buffer.is_empty()

    def test_readonly_buffer_buffer_property(self):
        """Test the buffer property."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=10)
        span = create_test_trace_span("span_1")
        buffer.add_span(span)

        # Act
        internal_buffer = buffer.buffer

        # Assert
        assert len(internal_buffer) == 1
        assert list(internal_buffer)[0].span_id == "span_1"

    def test_readonly_buffer_fifo_behavior(self):
        """Test that readonly buffer still has FIFO behavior when at capacity."""
        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=2)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")
        span3 = create_test_trace_span("span_3")  # This should cause discard

        # Act
        buffer.add_span(span1)
        buffer.add_span(span2)
        buffer.add_span(span3)

        # Assert
        assert buffer.size() == 2
        spans = buffer.get_spans(10)
        # Should contain span_2 and span_3 (oldest span_1 discarded)
        span_ids = [span.span_id for span in spans]
        assert "span_1" not in span_ids
        assert "span_2" in span_ids
        assert "span_3" in span_ids


class TestRejectWhenFullBuffer:
    """Test cases for RejectWhenFullBuffer implementation."""

    def test_reject_when_full_initialization(self):
        """Test that reject when full buffer initializes correctly."""
        # Arrange & Act
        buffer = RejectWhenFullBuffer(max_size=5)

        # Assert
        assert buffer.size() == 0
        assert buffer.max_size == 5
        assert buffer.current_size == 0
        assert buffer.is_empty()
        assert not buffer.is_full()

    def test_reject_when_full_invalid_size_raises_error(self):
        """Test that reject when full buffer raises error for non-positive size."""
        # Act & Assert
        with pytest.raises(ValueError, match="max_size must be positive"):
            RejectWhenFullBuffer(max_size=0)

        with pytest.raises(ValueError, match="max_size must be positive"):
            RejectWhenFullBuffer(max_size=-1)

    def test_reject_when_full_add_success_when_space(self):
        """Test that buffer accepts spans when there is space."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=5)
        trace_span = create_test_trace_span()

        # Act
        result = buffer.add_span(trace_span)

        # Assert
        assert result is True
        assert buffer.size() == 1

    def test_reject_when_full_add_rejects_when_full(self):
        """Test that buffer rejects spans when at capacity."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=2)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")
        span3 = create_test_trace_span("span_3")  # This should be rejected

        # Act
        result1 = buffer.add_span(span1)
        result2 = buffer.add_span(span2)
        result3 = buffer.add_span(span3)  # Should be rejected

        # Assert
        assert result1 is True
        assert result2 is True
        assert result3 is False  # Rejected because buffer is full
        assert buffer.size() == 2  # Still at max capacity

    def test_reject_when_full_get_spans_readonly(self):
        """Test getting spans doesn't consume them in reject when full buffer."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=10)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")
        buffer.add_span(span1)
        buffer.add_span(span2)

        # Act
        spans = buffer.get_spans(5)

        # Assert
        assert len(spans) == 2
        assert buffer.size() == 2  # Size unchanged since get_spans is readonly

    def test_reject_when_full_buffer_methods(self):
        """Test all buffer methods work correctly with reject when full buffer."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=3)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")
        span3 = create_test_trace_span("span_3")
        span4 = create_test_trace_span("span_4")  # This should be rejected

        # Act
        result1 = buffer.add_span(span1)
        result2 = buffer.add_span(span2)
        result3 = buffer.add_span(span3)
        result4 = buffer.add_span(span4)  # This should be rejected

        # Assert
        assert all([result1, result2, result3])  # First 3 should succeed
        assert result4 is False  # 4th should fail
        assert buffer.size() == 3  # At max capacity
        assert buffer.is_full()
        assert not buffer.is_empty()
        assert buffer.current_size == 3

    def test_reject_when_full_max_size_property(self):
        """Test the max_size property."""
        # Arrange & Act
        buffer = RejectWhenFullBuffer(max_size=7)

        # Assert
        assert buffer.max_size == 7

    def test_reject_when_full_current_size_property(self):
        """Test the current_size property."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=10)
        span = create_test_trace_span("span_1")

        # Act
        buffer.add_span(span)

        # Assert
        assert buffer.current_size == 1

    def test_reject_when_full_is_empty_method(self):
        """Test the is_empty method."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=5)

        # Assert
        assert buffer.is_empty()

        # Act
        buffer.add_span(create_test_trace_span())

        # Assert
        assert not buffer.is_empty()

    def test_reject_when_full_is_full_method(self):
        """Test the is_full method."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=2)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")

        # Assert
        assert not buffer.is_full()

        # Act
        buffer.add_span(span1)
        buffer.add_span(span2)

        # Assert
        assert buffer.is_full()

    def test_reject_when_full_clear_method(self):
        """Test the clear method."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=10)
        buffer.add_span(create_test_trace_span("span_1"))
        buffer.add_span(create_test_trace_span("span_2"))

        # Assert
        assert buffer.size() == 2

        # Act
        buffer.clear()

        # Assert
        assert buffer.size() == 0
        assert buffer.is_empty()

    def test_reject_when_full_buffer_property(self):
        """Test the buffer property."""
        # Arrange
        buffer = RejectWhenFullBuffer(max_size=10)
        span = create_test_trace_span("span_1")
        buffer.add_span(span)

        # Act
        internal_buffer = buffer.buffer

        # Assert
        assert len(internal_buffer) == 1
        assert list(internal_buffer)[0].span_id == "span_1"


class TestBufferPropertiesAndEdgeCases:
    """Test additional properties and edge cases for all buffer implementations."""

    @pytest.mark.parametrize(
        "buffer_class",
        [
            ObservabilityBuffer,
            ObservabilityBufferWithConsume,
            TraceBufferPortReadOnly,
            RejectWhenFullBuffer,
        ],
    )
    def test_buffer_properties_consistency(self, buffer_class):
        """Test that all buffer classes have consistent property behavior."""
        # Arrange
        buffer = buffer_class(max_size=5)
        span = create_test_trace_span("test_span")

        # Act
        buffer.add_span(span)

        # Assert
        if hasattr(buffer, "current_size"):
            assert buffer.current_size == 1
        assert buffer.size() == 1
        assert buffer.max_size == 5
        assert not buffer.is_empty()
        assert not buffer.is_full()

    def test_observability_buffer_properties(self):
        """Test all properties for ObservabilityBuffer."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=3)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")

        # Act
        buffer.add_span(span1)
        buffer.add_span(span2)

        # Assert
        assert buffer.current_size == 2
        assert buffer.size() == 2
        assert buffer.max_size == 3
        assert not buffer.is_empty()
        assert not buffer.is_full()

    def test_observability_buffer_with_consume_properties(self):
        """Test all properties for ObservabilityBufferWithConsume."""
        # Arrange
        buffer = ObservabilityBufferWithConsume(max_size=3)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")

        # Act
        buffer.add_span(span1)
        buffer.add_span(span2)

        # Assert
        assert buffer.current_size == 2
        assert buffer.size() == 2
        assert buffer.max_size == 3
        assert not buffer.is_empty()
        assert not buffer.is_full()

    def test_buffer_clear_method_for_all_implementations(self):
        """Test clear method for all implementations."""
        for buffer_class in [
            ObservabilityBuffer,
            ObservabilityBufferWithConsume,
            TraceBufferPortReadOnly,
            RejectWhenFullBuffer,
        ]:
            # Arrange
            buffer = buffer_class(max_size=5)
            buffer.add_span(create_test_trace_span("span_1"))
            buffer.add_span(create_test_trace_span("span_2"))

            # Assert initial state
            assert buffer.size() > 0
            assert not buffer.is_empty()

            # Act
            buffer.clear()

            # Assert final state
            assert buffer.size() == 0
            assert buffer.is_empty()

    def test_buffer_is_empty_method_for_all_implementations(self):
        """Test is_empty method for all implementations."""
        for buffer_class in [
            ObservabilityBuffer,
            ObservabilityBufferWithConsume,
            TraceBufferPortReadOnly,
            RejectWhenFullBuffer,
        ]:
            # Arrange
            buffer = buffer_class(max_size=5)

            # Assert initially empty
            assert buffer.is_empty()

            # Act
            buffer.add_span(create_test_trace_span())

            # Assert no longer empty
            assert not buffer.is_empty()

    def test_buffer_fifo_discard_with_actual_span_discard(self):
        """Test that FIFO buffer actually discards old spans."""
        # Arrange
        buffer = ObservabilityBuffer(max_size=3)
        span1 = create_test_trace_span("span_1")
        span2 = create_test_trace_span("span_2")
        span3 = create_test_trace_span("span_3")
        span4 = create_test_trace_span("span_4")
        span5 = create_test_trace_span("span_5")

        # Act - Add spans to cause discards
        buffer.add_span(span1)  # Will be discarded
        buffer.add_span(span2)  # Will be discarded
        buffer.add_span(span3)  # Will remain
        buffer.add_span(span4)  # Will remain
        buffer.add_span(span5)  # Will remain

        # Assert
        assert buffer.size() == 3
        spans = buffer.get_spans(10)
        span_ids = [span.span_id for span in spans]

        # The oldest spans (span_1 and span_2) should be discarded
        # The newest spans (span_3, span_4, span_5) should remain
        assert "span_1" not in span_ids
        assert "span_2" not in span_ids
        assert "span_3" in span_ids
        assert "span_4" in span_ids
        assert "span_5" in span_ids

    def test_edge_case_zero_size_buffer(self):
        """Test that zero size buffer raises appropriate error."""
        for buffer_class in [
            ObservabilityBuffer,
            ObservabilityBufferWithConsume,
            TraceBufferPortReadOnly,
            RejectWhenFullBuffer,
        ]:
            with pytest.raises(ValueError, match="max_size must be positive"):
                buffer_class(max_size=0)

    def test_edge_case_negative_size_buffer(self):
        """Test that negative size buffer raises appropriate error."""
        for buffer_class in [
            ObservabilityBuffer,
            ObservabilityBufferWithConsume,
            TraceBufferPortReadOnly,
            RejectWhenFullBuffer,
        ]:
            with pytest.raises(ValueError, match="max_size must be positive"):
                buffer_class(max_size=-5)

    def test_large_count_get_spans(self):
        """Test getting more spans than available."""
        for buffer_class in [
            ObservabilityBuffer,
            ObservabilityBufferWithConsume,  # For this one, gets will also remove
            TraceBufferPortReadOnly,
            RejectWhenFullBuffer,
        ]:
            # Arrange
            buffer = buffer_class(max_size=10)
            spans_to_add = [create_test_trace_span(f"span_{i:02d}") for i in range(3)]
            for span in spans_to_add:
                buffer.add_span(span)

            # Act
            retrieved_spans = buffer.get_spans(100)  # Request more than available

            # Assert
            if buffer_class == ObservabilityBufferWithConsume:
                # For consume buffer, this will remove the spans
                assert len(retrieved_spans) == 3
                assert buffer.size() == 0  # All consumed
            else:
                # For non-consume buffers, this should return available spans
                assert len(retrieved_spans) == 3
                assert buffer.size() == 3  # Size unchanged


class TestBufferThreadSafetyAdditional:
    """Additional thread-safety tests for the missing buffer implementations."""

    def test_readonly_buffer_thread_safety(self):
        """Test thread safety for readonly buffer implementation."""
        import threading
        import time

        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=100)
        results = []

        def worker(worker_id: int):
            """Worker function to add spans from multiple threads."""
            for i in range(5):
                span = create_test_trace_span(f"thread_{worker_id}_span_{i:02d}")
                result = buffer.add_span(span)
                results.append(result)
                time.sleep(0.001)  # Small delay to allow other threads

        # Act - Run multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Assert
        assert len(results) == 15  # 3 threads * 5 spans each
        assert all(results)  # All should succeed
        assert buffer.size() == 15  # All spans added

    def test_reject_when_full_buffer_thread_safety(self):
        """Test thread safety for reject when full buffer implementation."""
        import threading
        import time

        # Arrange
        buffer = RejectWhenFullBuffer(max_size=10)
        results = []

        def worker(worker_id: int):
            """Worker function to add spans from multiple threads."""
            for i in range(4):  # More than capacity to test rejections
                span = create_test_trace_span(f"thread_{worker_id}_span_{i:02d}")
                result = buffer.add_span(span)
                results.append(result)
                time.sleep(0.001)  # Small delay to allow other threads

        # Act - Run multiple threads
        threads = []
        for i in range(3):  # 3 threads * 4 spans each = 12 total, but max is 10
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Assert
        assert len(results) == 12  # 3 threads * 4 spans each
        # Should have at least 10 successes and at most 2 rejections
        success_count = sum(results)
        assert 10 <= success_count <= 12  # Some additions may be rejected
        assert buffer.size() == buffer.max_size  # Buffer full at max capacity

    def test_concurrent_get_operations_readonly_buffer(self):
        """Test concurrent get operations on readonly buffer."""
        import threading
        import time

        # Arrange
        buffer = TraceBufferPortReadOnly(max_size=20)
        # Add some initial spans
        for i in range(10):
            buffer.add_span(create_test_trace_span(f"init_span_{i:02d}"))

        results = []

        def get_worker(worker_id: int):
            """Worker function to get spans from multiple threads."""
            for _ in range(3):
                spans = buffer.get_spans(5)
                results.append(len(spans))
                time.sleep(0.001)  # Small delay

        # Act - Run multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=get_worker, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Assert - All gets should return up to 5 spans (since we requested 5 and there were 10 available)
        assert len(results) == 9  # 3 threads * 3 iterations each
        assert all(count <= 5 for count in results)  # All should get up to 5 spans
        assert all(count > 0 for count in results)  # All should get at least some spans
        assert buffer.size() == 10  # Size unchanged since readonly
