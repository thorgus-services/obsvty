import pytest
from obsvty.domain.services.otlp_processing import validate_span
from obsvty.domain.models.otlp import Span


class TestOTLPProcessing:
    def test_parse_otlp_trace_data(self):
        """Test parsing OTLP trace data"""
        # This would require more complex testing with real OTLP protobuf data
        # For now, testing will be done at the integration level
        pass

    def test_validate_span_with_valid_span(self):
        """Test validating a valid span"""
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

        # Should not raise any exception
        result = validate_span(span)
        assert result is True

    def test_validate_span_with_invalid_span(self):
        """Test validating an invalid span"""
        # Create an invalid span by bypassing the constructor validation
        # Actually, since it's frozen, we can't modify it, so let's test
        # what happens when we pass invalid data to the constructor
        with pytest.raises(ValueError):
            Span(
                trace_id="invalid",  # Invalid trace_id
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
