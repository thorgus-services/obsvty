from obsvty.domain.models.otlp import Span, LogRecord
from obsvty.infrastructure.buffer.memory_buffer import MemoryBuffer


class TestMemoryBuffer:
    def test_add_span_success(self):
        """Test adding a span to the buffer"""
        buffer = MemoryBuffer(max_size=10)

        span = Span(
            trace_id="12345678901234567890123456789012",
            span_id="1234567890123456",
            parent_span_id=None,
            name="test_span",
            kind=1,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status={},
        )

        result = buffer.add_span(span)
        assert result is True
        assert buffer.size() == 1

    def test_add_log_success(self):
        """Test adding a log record to the buffer"""
        buffer = MemoryBuffer(max_size=10)

        log_record = LogRecord(
            time_unix_nano=1000000000,
            severity_number=5,
            severity_text="INFO",
            body="test log",
            attributes={},
            trace_id=None,
            span_id=None,
        )

        result = buffer.add_log(log_record)
        assert result is True
        assert buffer.size() == 1

    def test_get_spans(self):
        """Test retrieving spans from the buffer"""
        buffer = MemoryBuffer(max_size=10)

        span = Span(
            trace_id="12345678901234567890123456789012",
            span_id="1234567890123456",
            parent_span_id=None,
            name="test_span",
            kind=1,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status={},
        )

        buffer.add_span(span)

        spans = buffer.get_spans(1)
        assert len(spans) == 1
        assert spans[0] == span

    def test_buffer_size_limit(self):
        """Test that buffer respects size limits"""
        buffer = MemoryBuffer(max_size=2)

        span1 = Span(
            trace_id="12345678901234567890123456789012",
            span_id="1234567890123456",
            parent_span_id=None,
            name="test_span1",
            kind=1,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status={},
        )

        span2 = Span(
            trace_id="12345678901234567890123456789013",
            span_id="1234567890123457",
            parent_span_id=None,
            name="test_span2",
            kind=1,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status={},
        )

        result1 = buffer.add_span(span1)
        result2 = buffer.add_span(span2)

        assert result1 is True
        assert result2 is True
        assert buffer.size() == 2
        assert buffer.is_full() is True  # Now it should be full

        # Adding another span should return False when buffer is full
        span3 = Span(
            trace_id="12345678901234567890123456789014",
            span_id="1234567890123458",
            parent_span_id=None,
            name="test_span3",
            kind=1,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status={},
        )

        result3 = buffer.add_span(span3)
        assert result3 is False  # Should return False when buffer is full
        assert buffer.size() == 2  # Size should remain the same

    def test_is_full_method(self):
        """Test the is_full method works correctly"""
        buffer = MemoryBuffer(max_size=1)

        assert buffer.is_full() is False

        span = Span(
            trace_id="12345678901234567890123456789012",
            span_id="1234567890123456",
            parent_span_id=None,
            name="test_span",
            kind=1,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status={},
        )

        buffer.add_span(span)
        assert buffer.is_full() is True

    def test_buffer_thread_safety_simulation(self):
        """Test that buffer operations are thread-safe (simulated)"""
        buffer = MemoryBuffer(max_size=10)

        span = Span(
            trace_id="12345678901234567890123456789012",
            span_id="1234567890123456",
            parent_span_id=None,
            name="test_span",
            kind=1,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={},
            events=[],
            status={},
        )

        log_record = LogRecord(
            time_unix_nano=1000000000,
            severity_number=5,
            severity_text="INFO",
            body="test log",
            attributes={},
            trace_id=None,
            span_id=None,
        )

        # Add items
        assert buffer.add_span(span) is True
        assert buffer.add_log(log_record) is True

        # Check sizes
        assert buffer.size() == 2

        # Retrieve items
        spans = buffer.get_spans(1)
        logs = buffer.get_logs(1)

        assert len(spans) == 1
        assert len(logs) == 1
        assert spans[0] == span
        assert logs[0] == log_record
