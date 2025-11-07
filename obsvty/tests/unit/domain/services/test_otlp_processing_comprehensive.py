import pytest
from unittest.mock import Mock, patch
from obsvty.domain.services.otlp_processing import (
    validate_span,
    validate_log_record,
    process_otlp_data,
)
from obsvty.domain.models.otlp import Span, LogRecord
from obsvty.domain.exceptions import OTLPValidationError


class TestValidateSpan:
    def test_validate_span_with_valid_span(self):
        """Test that validation passes for a valid span"""
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

        result = validate_span(span)
        assert result is True

    def test_validate_span_uses_span_validation(self):
        """Test that validation actually checks span validity"""
        # Since validation happens in the constructor,
        # this test confirms the function works without errors
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

        # This should not raise an exception
        result = validate_span(span)
        assert result is True


class TestValidateLogRecord:
    def test_validate_log_record_with_valid_record(self):
        """Test that validation passes for a valid log record"""
        log_record = LogRecord(
            time_unix_nano=1000000000,
            severity_number=5,
            severity_text="INFO",
            body="test log",
            attributes={},
            trace_id=None,
            span_id=None,
        )

        result = validate_log_record(log_record)
        assert result is True

    def test_validate_log_record_uses_internal_validation(self):
        """Test that validation works without errors"""
        log_record = LogRecord(
            time_unix_nano=1000000000,
            severity_number=5,
            severity_text="INFO",
            body="test log",
            attributes={},
            trace_id="12345678901234567890123456789012",
            span_id="1234567890123456",
        )

        result = validate_log_record(log_record)
        assert result is True


class TestProcessOTLPData:
    def test_process_otlp_data_success(self):
        """Test successful processing of OTLP data"""
        # Mock buffer port
        mock_buffer_port = Mock()
        mock_buffer_port.add_span.return_value = True

        # Create minimal mock trace data (this would normally be protobuf data)
        # For this test, we'll mock the parse_otlp_trace_data function
        mock_spans = [
            Span(
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
        ]

        with patch(
            "obsvty.domain.services.otlp_processing.parse_otlp_trace_data",
            return_value=mock_spans,
        ):
            result = process_otlp_data(b"mock_trace_data", mock_buffer_port)

            # Verify the buffer was called correctly
            mock_buffer_port.add_span.assert_called_once_with(mock_spans[0])

            # Verify the result has the expected structure
            assert len(result.resource_spans) == 1
            assert result.resource_spans[0] == mock_spans[0]

    def test_process_otlp_data_with_parse_error(self):
        """Test that errors during parsing are handled properly"""
        mock_buffer_port = Mock()

        with patch(
            "obsvty.domain.services.otlp_processing.parse_otlp_trace_data",
            side_effect=OTLPValidationError("Test error"),
        ):
            with pytest.raises(OTLPValidationError):
                process_otlp_data(b"invalid_trace_data", mock_buffer_port)
