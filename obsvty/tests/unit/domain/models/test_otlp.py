import pytest
import dataclasses
from obsvty.domain.models.otlp import Span, LogRecord, OTLPData


class TestSpan:
    def test_span_creation_with_valid_data(self):
        """Test creating a Span with valid data"""
        span = Span(
            trace_id="12345678901234567890123456789012",
            span_id="1234567890123456",
            parent_span_id="abcdef1234567890",
            name="test_span",
            kind=1,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes={"key": "value"},
            events=[{"time": 1500000000, "name": "test_event"}],
            status={"code": 1, "message": "OK"},
        )

        assert span.trace_id == "12345678901234567890123456789012"
        assert span.span_id == "1234567890123456"
        assert span.parent_span_id == "abcdef1234567890"
        assert span.name == "test_span"
        assert span.kind == 1
        assert span.start_time_unix_nano == 1000000000
        assert span.end_time_unix_nano == 2000000000
        assert span.attributes == {"key": "value"}
        assert span.events == [{"time": 1500000000, "name": "test_event"}]
        assert span.status == {"code": 1, "message": "OK"}

    def test_span_creation_fails_with_invalid_trace_id(self):
        """Test that creating a Span with invalid trace_id fails"""
        with pytest.raises(
            ValueError, match="trace_id must be a 32-character hex string"
        ):
            Span(
                trace_id="invalid_trace_id",  # Too short
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

    def test_span_creation_fails_with_invalid_span_id(self):
        """Test that creating a Span with invalid span_id fails"""
        with pytest.raises(
            ValueError, match="span_id must be a 16-character hex string"
        ):
            Span(
                trace_id="12345678901234567890123456789012",
                span_id="invalid_span_id",  # Too short
                parent_span_id=None,
                name="test_span",
                kind=1,
                start_time_unix_nano=1000000000,
                end_time_unix_nano=2000000000,
                attributes={},
                events=[],
                status={},
            )

    def test_span_is_immutable(self):
        """Test that Span is immutable after creation"""
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

        with pytest.raises(dataclasses.FrozenInstanceError):
            span.name = "new_name"


class TestLogRecord:
    def test_log_record_creation_with_valid_data(self):
        """Test creating a LogRecord with valid data"""
        log_record = LogRecord(
            time_unix_nano=1000000000,
            severity_number=5,
            severity_text="INFO",
            body="This is a log message",
            attributes={"service": "test"},
            trace_id="12345678901234567890123456789012",
            span_id="1234567890123456",
        )

        assert log_record.time_unix_nano == 1000000000
        assert log_record.severity_number == 5
        assert log_record.severity_text == "INFO"
        assert log_record.body == "This is a log message"
        assert log_record.attributes == {"service": "test"}
        assert log_record.trace_id == "12345678901234567890123456789012"
        assert log_record.span_id == "1234567890123456"

    def test_log_record_creation_with_optional_fields(self):
        """Test creating a LogRecord with optional fields as None"""
        log_record = LogRecord(
            time_unix_nano=1000000000,
            severity_number=5,
            severity_text="INFO",
            body="This is a log message",
            attributes={},
            trace_id=None,
            span_id=None,
        )

        assert log_record.trace_id is None
        assert log_record.span_id is None


class TestOTLPData:
    def test_otlp_data_creation_with_valid_data(self):
        """Test creating an OTLPData with valid data"""
        from datetime import datetime

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
            body="This is a log message",
            attributes={},
            trace_id=None,
            span_id=None,
        )

        otlp_data = OTLPData(
            resource_spans=[span],
            resource_metrics=[],
            resource_logs=[log_record],
            received_at=datetime.now(),
            source_endpoint="test_endpoint",
        )

        assert len(otlp_data.resource_spans) == 1
        assert len(otlp_data.resource_metrics) == 0
        assert len(otlp_data.resource_logs) == 1
        assert otlp_data.source_endpoint == "test_endpoint"
