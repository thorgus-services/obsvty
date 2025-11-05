"""Domain entities and value objects for observability data.

This module defines the core domain model for handling trace spans and
observability data, following domain-driven design principles.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


@dataclass(frozen=True)
class TraceId:
    """Value object representing a trace identifier."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or len(self.value) == 0:
            raise ValueError("TraceId value must be a non-empty string")
        # Validate hex-encoded 16 bytes (32 hex characters)
        if not re.match(r"^[0-9a-fA-F]{32}$", self.value):
            raise ValueError(
                "TraceId value must be a hex-encoded 32-character string (16 bytes)"
            )


@dataclass(frozen=True)
class SpanId:
    """Value object representing a span identifier."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or len(self.value) == 0:
            raise ValueError("SpanId value must be a non-empty string")
        # Validate hex-encoded 8 bytes (16 hex characters)
        if not re.match(r"^[0-9a-fA-F]{16}$", self.value):
            raise ValueError(
                "SpanId value must be a hex-encoded 16-character string (8 bytes)"
            )


@dataclass(frozen=True)
class SpanEvent:
    """Value object representing an event within a span."""

    name: str
    timestamp: datetime
    attributes: Dict[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or len(self.name) == 0:
            raise ValueError("SpanEvent name must be a non-empty string")


@dataclass(frozen=True)
class SpanStatus:
    """Value object representing the status of a span."""

    code: int  # 0 = UNSET, 1 = OK, 2 = ERROR
    message: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.code, int) or self.code not in (0, 1, 2):
            raise ValueError("SpanStatus code must be 0 (UNSET), 1 (OK), or 2 (ERROR)")
        if self.message is not None and not isinstance(self.message, str):
            raise ValueError("SpanStatus message must be a string if provided")


@dataclass
class TraceSpan:
    """Entity representing a single trace span."""

    trace_id: TraceId
    span_id: SpanId
    parent_span_id: Optional[SpanId]
    name: str
    start_time_unix_nano: int
    end_time_unix_nano: int
    attributes: Dict[str, Any]
    events: List[SpanEvent]
    status: SpanStatus
    kind: int = 0  # 0 = INTERNAL, 1 = SERVER, 2 = CLIENT, 3 = PRODUCER, 4 = CONSUMER

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or len(self.name) == 0:
            raise ValueError("TraceSpan name must be a non-empty string")
        if self.start_time_unix_nano < 0:
            raise ValueError("start_time_unix_nano must be a non-negative integer")
        if self.end_time_unix_nano < self.start_time_unix_nano:
            raise ValueError("end_time_unix_nano must be >= start_time_unix_nano")
        if not isinstance(self.attributes, dict):
            raise ValueError("attributes must be a dictionary")
        if not isinstance(self.events, list):
            raise ValueError("events must be a list")
        if not isinstance(self.kind, int) or self.kind not in range(5):
            raise ValueError("kind must be an integer between 0 and 4")


@dataclass
class ObservabilityBuffer:
    """Value object representing a buffer for collecting observability data."""

    max_size: int
    current_size: int = 0
    buffer: List[TraceSpan] = None  # type: ignore

    def __post_init__(self) -> None:
        if self.buffer is None:
            object.__setattr__(self, "buffer", [])
        if self.max_size <= 0:
            raise ValueError("max_size must be a positive integer")
        if self.current_size < 0:
            raise ValueError("current_size must be non-negative")
        if self.current_size != len(self.buffer):
            raise ValueError("current_size must match actual buffer length")

    def add_span(self, span: TraceSpan) -> bool:
        """Add a span to the buffer, returning True if successful."""
        if self.current_size >= self.max_size:
            return False  # Buffer is full

        self.buffer.append(span)
        object.__setattr__(self, "current_size", self.current_size + 1)
        return True

    def is_full(self) -> bool:
        """Check if the buffer is at maximum capacity."""
        return self.current_size >= self.max_size

    def is_empty(self) -> bool:
        """Check if the buffer is empty."""
        return self.current_size == 0

    def clear(self) -> None:
        """Clear all spans from the buffer."""
        object.__setattr__(self, "buffer", [])
        object.__setattr__(self, "current_size", 0)


def validate_trace_id_format(trace_id_value: str) -> bool:
    """Validate if the trace ID format is compliant with OTLP v1.9 specification.

    Args:
        trace_id_value: The trace ID string to validate.

    Returns:
        True if the format is valid, False otherwise.
    """
    if not isinstance(trace_id_value, str) or len(trace_id_value) != 32:
        return False
    return bool(re.match(r"^[0-9a-fA-F]{32}$", trace_id_value))


def validate_span_id_format(span_id_value: str) -> bool:
    """Validate if the span ID format is compliant with OTLP v1.9 specification.

    Args:
        span_id_value: The span ID string to validate.

    Returns:
        True if the format is valid, False otherwise.
    """
    if not isinstance(span_id_value, str) or len(span_id_value) != 16:
        return False
    return bool(re.match(r"^[0-9a-fA-F]{16}$", span_id_value))


def validate_trace_span_structure(span_data: Dict[str, Any]) -> bool:
    """Validate minimal structural requirements for a TraceSpan according to OTLP v1.9.

    Args:
        span_data: The span data dictionary to validate.

    Returns:
        True if the structure is valid, False otherwise.
    """
    if not isinstance(span_data, dict):
        return False

    required_fields = [
        "trace_id",
        "span_id",
        "name",
        "start_time_unix_nano",
        "end_time_unix_nano",
    ]
    return all(field in span_data for field in required_fields)


def validate_resource_spans_structure(resource_spans_data: Dict[str, Any]) -> bool:
    """Validate minimal structural requirements for ResourceSpans according to OTLP v1.9.

    Args:
        resource_spans_data: The ResourceSpans data dictionary to validate.

    Returns:
        True if the structure is valid, False otherwise.
    """
    if not isinstance(resource_spans_data, dict):
        return False

    # Check if scope_spans or instrumentation_library_spans exists
    has_scope_spans = "scope_spans" in resource_spans_data
    has_instrumentation_spans = "instrumentation_library_spans" in resource_spans_data

    # ResourceSpans must have either scope_spans or instrumentation_library_spans (for backward compatibility)
    if not (has_scope_spans or has_instrumentation_spans):
        return False

    # Validate resource if present
    if "resource" in resource_spans_data:
        resource = resource_spans_data["resource"]
        if not isinstance(resource, dict):
            return False

    # Validate schema_url if present
    if "schema_url" in resource_spans_data:
        schema_url = resource_spans_data["schema_url"]
        if not isinstance(schema_url, str):
            return False

    return True


def validate_scope_spans_structure(scope_spans_data: Dict[str, Any]) -> bool:
    """Validate minimal structural requirements for ScopeSpans according to OTLP v1.9.

    Args:
        scope_spans_data: The ScopeSpans data dictionary to validate.

    Returns:
        True if the structure is valid, False otherwise.
    """
    if not isinstance(scope_spans_data, dict):
        return False

    # Check if spans exists and is a list
    if "spans" not in scope_spans_data or not isinstance(
        scope_spans_data["spans"], list
    ):
        return False

    # Validate instrumentation_scope if present
    if "instrumentation_scope" in scope_spans_data:
        instrumentation_scope = scope_spans_data["instrumentation_scope"]
        if not isinstance(instrumentation_scope, dict):
            return False

    # Validate schema_url if present
    if "schema_url" in scope_spans_data:
        schema_url = scope_spans_data["schema_url"]
        if not isinstance(schema_url, str):
            return False

    return True


def validate_span_structure(span_data: Dict[str, Any]) -> bool:
    """Validate minimal structural requirements for an OTLP Span according to OTLP v1.9.

    Args:
        span_data: The Span data dictionary to validate.

    Returns:
        True if the structure is valid, False otherwise.
    """
    if not isinstance(span_data, dict):
        return False

    # Required fields for OTLP Span
    required_fields = [
        "trace_id",
        "span_id",
        "name",
        "start_time_unix_nano",
        "end_time_unix_nano",
    ]

    for field in required_fields:
        if field not in span_data:
            return False
        # Trace ID and Span ID must be non-empty strings
        if field in ["trace_id", "span_id"] and not isinstance(span_data[field], str):
            return False
        if field in ["trace_id", "span_id"] and len(span_data[field]) == 0:
            return False
        # Time fields must be integers
        if field in ["start_time_unix_nano", "end_time_unix_nano"] and not isinstance(
            span_data[field], int
        ):
            return False

    # Validate trace_id and span_id formats if they exist
    if "trace_id" in span_data and not validate_trace_id_format(span_data["trace_id"]):
        return False
    if "span_id" in span_data and not validate_span_id_format(span_data["span_id"]):
        return False

    # End time must be >= start time
    if span_data["end_time_unix_nano"] < span_data["start_time_unix_nano"]:
        return False

    return True


def validate_attributes_format(
    attributes: Union[List[Dict[str, Any]], Dict[str, Any], None],
) -> bool:
    """Validate attributes format according to OTLP v1.9 specification.

    Args:
        attributes: The attributes to validate.

    Returns:
        True if the attributes format is valid, False otherwise.
    """
    if attributes is None:
        return True

    if isinstance(attributes, dict):
        # Direct dictionary format
        return all(isinstance(k, str) for k in attributes.keys())

    if isinstance(attributes, list):
        # List of key-value pairs format (OTLP protocol buffer format)
        for attr in attributes:
            if not isinstance(attr, dict):
                return False
            if "key" not in attr or "value" not in attr:
                return False
            if not isinstance(attr["key"], str):
                return False
        return True

    return False
