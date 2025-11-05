"""Unit tests for the OTLP parsing service.

This module contains comprehensive unit tests for the OTLP parsing service,
verifying the conversion of OTLP protocol buffer objects to internal domain
structures following TDD principles.
"""

import pytest

from src.obsvty.application.services.otlp_parsing_service import (
    OTLPParsingService,
    parse_resource_spans,
)


class TestOTLPParsingService:
    """Test suite for the OTLP parsing service."""

    def test_parse_resource_spans_with_valid_data(self) -> None:
        """Test parsing ResourceSpans with valid data structure."""
        resource_spans_data = {
            "scope_spans": [
                {
                    "spans": [
                        {
                            "trace_id": "12345678901234567890123456789012",
                            "span_id": "1234567890123456",
                            "parent_span_id": "abcdefabcdefabcd",
                            "name": "test_span",
                            "start_time_unix_nano": 1000000000,
                            "end_time_unix_nano": 2000000000,
                            "attributes": [
                                {"key": "key1", "value": {"stringValue": "value1"}},
                                {"key": "key2", "value": {"intValue": 123}},
                            ],
                            "events": [
                                {
                                    "name": "test_event",
                                    "time_unix_nano": 1500000000,
                                    "attributes": [
                                        {
                                            "key": "event_key",
                                            "value": {"stringValue": "event_value"},
                                        }
                                    ],
                                }
                            ],
                            "status": {"code": 1, "message": "OK"},
                            "kind": 1,
                        }
                    ]
                }
            ]
        }

        service = OTLPParsingService()
        trace_spans = service.parse_resource_spans(resource_spans_data)

        assert len(trace_spans) == 1
        span = trace_spans[0]

        assert span.trace_id.value == "12345678901234567890123456789012"
        assert span.span_id.value == "1234567890123456"
        assert span.parent_span_id is not None
        assert span.parent_span_id.value == "abcdefabcdefabcd"
        assert span.name == "test_span"
        assert span.start_time_unix_nano == 1000000000
        assert span.end_time_unix_nano == 2000000000
        assert span.attributes == {"key1": "value1", "key2": 123}
        assert len(span.events) == 1
        assert span.events[0].name == "test_event"
        assert span.events[0].attributes == {"event_key": "event_value"}
        assert span.status.code == 1
        assert span.status.message == "OK"
        assert span.kind == 1

    def test_parse_resource_spans_with_instrumentation_library_spans(self) -> None:
        """Test parsing ResourceSpans with instrumentation_library_spans (backward compatibility)."""
        resource_spans_data = {
            "instrumentation_library_spans": [
                {
                    "spans": [
                        {
                            "trace_id": "12345678901234567890123456789012",
                            "span_id": "1234567890123456",
                            "name": "test_span",
                            "start_time_unix_nano": 1000000000,
                            "end_time_unix_nano": 2000000000,
                            "attributes": [],
                            "events": [],
                            "status": {"code": 0},
                        }
                    ]
                }
            ]
        }

        service = OTLPParsingService()
        trace_spans = service.parse_resource_spans(resource_spans_data)

        assert len(trace_spans) == 1
        span = trace_spans[0]
        assert span.trace_id.value == "12345678901234567890123456789012"

    def test_parse_resource_spans_with_invalid_data_raises_error(self) -> None:
        """Test that parsing invalid ResourceSpans raises ValueError."""
        resource_spans_data = {
            # Missing both scope_spans and instrumentation_library_spans
        }

        service = OTLPParsingService()
        with pytest.raises(ValueError):
            service.parse_resource_spans(resource_spans_data)

    def test_parse_resource_spans_with_invalid_span_data_continues_processing(
        self,
    ) -> None:
        """Test that parsing continues when some spans are invalid."""
        resource_spans_data = {
            "scope_spans": [
                {
                    "spans": [
                        {
                            # Invalid span (missing required fields)
                        },
                        {
                            "trace_id": "12345678901234567890123456789012",
                            "span_id": "1234567890123456",
                            "name": "valid_span",
                            "start_time_unix_nano": 1000000000,
                            "end_time_unix_nano": 2000000000,
                            "attributes": [],
                            "events": [],
                            "status": {"code": 0},
                        },
                    ]
                }
            ]
        }

        service = OTLPParsingService()
        trace_spans = service.parse_resource_spans(resource_spans_data)

        # Should only return the valid span
        assert len(trace_spans) == 1
        assert trace_spans[0].name == "valid_span"

    def test_parse_span_with_all_fields(self) -> None:
        """Test parsing a single span with all possible fields."""
        service = OTLPParsingService()

        span_data = {
            "trace_id": "12345678901234567890123456789012",
            "span_id": "1234567890123456",
            "parent_span_id": "abcdefabcdefabcd",
            "name": "test_span",
            "start_time_unix_nano": 1000000000,
            "end_time_unix_nano": 2000000000,
            "attributes": [
                {"key": "string_attr", "value": {"stringValue": "test_value"}},
                {"key": "int_attr", "value": {"intValue": 42}},
                {"key": "bool_attr", "value": {"boolValue": True}},
                {"key": "double_attr", "value": {"doubleValue": 3.14}},
                {
                    "key": "array_attr",
                    "value": {
                        "arrayValue": {
                            "values": [
                                {"stringValue": "item1"},
                                {"intValue": 2},
                                {"boolValue": False},
                            ]
                        }
                    },
                },
            ],
            "events": [
                {
                    "name": "event1",
                    "time_unix_nano": 1500000000,
                    "attributes": [
                        {"key": "event_attr", "value": {"stringValue": "event_value"}}
                    ],
                }
            ],
            "status": {"code": 2, "message": "Error occurred"},
            "kind": 3,
        }

        trace_span = service._parse_span(span_data)

        assert trace_span.trace_id.value == "12345678901234567890123456789012"
        assert trace_span.span_id.value == "1234567890123456"
        assert trace_span.parent_span_id is not None
        assert trace_span.parent_span_id.value == "abcdefabcdefabcd"
        assert trace_span.name == "test_span"
        assert trace_span.start_time_unix_nano == 1000000000
        assert trace_span.end_time_unix_nano == 2000000000
        assert trace_span.attributes == {
            "string_attr": "test_value",
            "int_attr": 42,
            "bool_attr": True,
            "double_attr": 3.14,
            "array_attr": ["item1", 2, False],
        }
        assert len(trace_span.events) == 1
        assert trace_span.events[0].name == "event1"
        assert trace_span.events[0].attributes == {"event_attr": "event_value"}
        assert trace_span.status.code == 2
        assert trace_span.status.message == "Error occurred"
        assert trace_span.kind == 3

    def test_parse_span_with_no_parent_span_id(self) -> None:
        """Test parsing a span without parent_span_id."""
        service = OTLPParsingService()

        span_data = {
            "trace_id": "12345678901234567890123456789012",
            "span_id": "1234567890123456",
            "name": "test_span",
            "start_time_unix_nano": 1000000000,
            "end_time_unix_nano": 2000000000,
            "attributes": [],
            "events": [],
            "status": {"code": 0},
            "kind": 0,
        }

        trace_span = service._parse_span(span_data)

        assert trace_span.trace_id.value == "12345678901234567890123456789012"
        assert trace_span.span_id.value == "1234567890123456"
        assert trace_span.parent_span_id is None
        assert trace_span.name == "test_span"

    def test_parse_span_with_invalid_format_raises_error(self) -> None:
        """Test that parsing a span with invalid format raises ValueError."""
        service = OTLPParsingService()

        span_data = {
            "trace_id": "invalid_trace_id",  # Invalid format
            "span_id": "1234567890123456",
            "name": "test_span",
            "start_time_unix_nano": 1000000000,
            "end_time_unix_nano": 2000000000,
            "attributes": [],
            "events": [],
            "status": {"code": 0},
        }

        with pytest.raises(ValueError):
            service._parse_span(span_data)

    def test_extract_value_from_otlp_value(self) -> None:
        """Test extracting values from OTLP value objects."""
        service = OTLPParsingService()

        # String value
        assert service._extract_value_from_otlp_value({"stringValue": "test"}) == "test"

        # Int value
        assert service._extract_value_from_otlp_value({"intValue": 42}) == 42

        # Bool value
        assert service._extract_value_from_otlp_value({"boolValue": True}) is True

        # Double value
        assert service._extract_value_from_otlp_value({"doubleValue": 3.14}) == 3.14

        # Array value
        array_result = service._extract_value_from_otlp_value(
            {
                "arrayValue": {
                    "values": [
                        {"stringValue": "item1"},
                        {"intValue": 2},
                        {"boolValue": False},
                    ]
                }
            }
        )
        assert array_result == ["item1", 2, False]

        # KV list value (nested attributes)
        kvlist_result = service._extract_value_from_otlp_value(
            {
                "kvlistValue": {
                    "values": [
                        {"key": "nested_key", "value": {"stringValue": "nested_value"}}
                    ]
                }
            }
        )
        assert kvlist_result == {"nested_key": "nested_value"}

        # Unknown format returns as-is
        unknown_result = service._extract_value_from_otlp_value(
            {"unknownField": "value"}
        )
        assert unknown_result == {"unknownField": "value"}


class TestConvenienceFunction:
    """Test suite for the convenience parsing function."""

    def test_parse_resource_spans_convenience_function(self) -> None:
        """Test the convenience function for parsing ResourceSpans."""
        resource_spans_data = {
            "scope_spans": [
                {
                    "spans": [
                        {
                            "trace_id": "12345678901234567890123456789012",
                            "span_id": "1234567890123456",
                            "name": "test_span",
                            "start_time_unix_nano": 1000000000,
                            "end_time_unix_nano": 2000000000,
                            "attributes": [],
                            "events": [],
                            "status": {"code": 0},
                        }
                    ]
                }
            ]
        }

        trace_spans = parse_resource_spans(resource_spans_data)

        assert len(trace_spans) == 1
        assert trace_spans[0].trace_id.value == "12345678901234567890123456789012"
        assert trace_spans[0].span_id.value == "1234567890123456"
        assert trace_spans[0].name == "test_span"
