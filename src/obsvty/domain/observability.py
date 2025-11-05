"""Observability domain entities and value objects."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import re


@dataclass(frozen=True)
class TraceId:
    """Value object representing a trace ID."""

    value: str

    def __post_init__(self) -> None:
        """Validate trace ID format."""
        if not isinstance(self.value, str):
            raise ValueError("TraceId value must be a string")
        # Basic validation for hex-encoded trace ID (32 hex characters)
        if not re.match(r"^[a-fA-F0-9]{32}$", self.value):
            raise ValueError("TraceId must be a 32-character hex string")


@dataclass(frozen=True)
class SpanId:
    """Value object representing a span ID."""

    value: str

    def __post_init__(self) -> None:
        """Validate span ID format."""
        if not isinstance(self.value, str):
            raise ValueError("SpanId value must be a string")
        # Basic validation for hex-encoded span ID (16 hex characters)
        if not re.match(r"^[a-fA-F0-9]{16}$", self.value):
            raise ValueError("SpanId must be a 16-character hex string")


@dataclass
class TraceSpan:
    """Individual unit of work within a distributed trace."""

    trace_id: TraceId  # hex-encoded value object
    span_id: SpanId  # hex-encoded value object
    parent_span_id: Optional[SpanId]
    name: str
    start_time_unix_nano: int
    end_time_unix_nano: int
    attributes: Dict[str, Any]
    events: List["SpanEvent"]
    status: "SpanStatus"
    kind: Optional[int] = 0  # Add kind field as used in the gRPC adapter

    def __post_init__(self) -> None:
        """Validate TraceSpan fields."""
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("TraceSpan name must be a non-empty string")

        if self.start_time_unix_nano < 0:
            raise ValueError("start_time_unix_nano must be non-negative")

        if self.end_time_unix_nano < 0:
            raise ValueError("end_time_unix_nano must be non-negative")

        if self.end_time_unix_nano < self.start_time_unix_nano:
            raise ValueError("end_time_unix_nano cannot be before start_time_unix_nano")

        if self.kind is not None and self.kind not in range(
            5
        ):  # 0-4 are valid according to OTLP spec
            raise ValueError(f"Invalid span kind: {self.kind}")


@dataclass
class SpanEvent:
    """An event that occurred during a span."""

    name: str
    attributes: Dict[str, Any]
    timestamp: Any = None  # Set by parsing service
    timestamp_unix_nano: int = 0  # Alternative timestamp representation

    def __post_init__(self) -> None:
        """Validate SpanEvent fields."""
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("SpanEvent name must be a non-empty string")


@dataclass
class SpanStatus:
    """The status of a span."""

    code: int
    message: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate SpanStatus fields."""
        # Validate code: 0 (UNSET), 1 (OK), 2 (ERROR) are valid according to OTLP spec
        if self.code not in [0, 1, 2]:
            raise ValueError(f"Invalid status code: {self.code}. Must be 0, 1, or 2.")

        if self.message is not None and not isinstance(self.message, str):
            raise ValueError("SpanStatus message must be a string")


@dataclass
class ProcessedSpan:
    """A processed span ready for further action."""

    original_span: TraceSpan
    processed_at: int
    additional_metadata: Dict[str, Any]


def validate_attributes_format(attributes_data: Any) -> bool:
    """Validate attributes format."""
    if attributes_data is None:
        return True  # None is valid

    if isinstance(attributes_data, dict):
        return True  # Direct dictionary format is valid

    if not isinstance(attributes_data, list):
        return False

    for attr in attributes_data:
        if not isinstance(attr, dict) or "key" not in attr or "value" not in attr:
            return False
    return True


def validate_scope_spans_structure(scope_spans_data: Any) -> bool:
    """Validate scope spans structure."""
    if not isinstance(scope_spans_data, dict):
        return False

    return "spans" in scope_spans_data


def validate_span_structure(span_data: Any) -> bool:
    """Validate span structure."""
    if not isinstance(span_data, dict):
        return False

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

    # Check for valid trace_id format if it's a string
    trace_id = span_data.get("trace_id")
    if isinstance(trace_id, str):
        if not re.match(r"^[a-fA-F0-9]{32}$", trace_id):
            return False

    # Check for valid span_id format if it's a string
    span_id = span_data.get("span_id")
    if isinstance(span_id, str):
        if not re.match(r"^[a-fA-F0-9]{16}$", span_id):
            return False

    # Check that end time is not before start time
    start_time = span_data.get("start_time_unix_nano", 0)
    end_time = span_data.get("end_time_unix_nano", 0)
    if end_time < start_time:
        return False

    return True


def validate_span_id_format(span_id_value: Any) -> bool:
    """Validate span ID format."""
    if not isinstance(span_id_value, str):
        return False
    # Should be 16 hex characters
    return re.match(r"^[a-fA-F0-9]{16}$", span_id_value) is not None


def validate_trace_id_format(trace_id_value: Any) -> bool:
    """Validate trace ID format."""
    if not isinstance(trace_id_value, str):
        return False
    # Should be 32 hex characters
    return re.match(r"^[a-fA-F0-9]{32}$", trace_id_value) is not None


def validate_resource_spans_structure(resource_spans_data: Any) -> bool:
    """Validate resource spans structure."""
    if not isinstance(resource_spans_data, dict):
        return False

    # Check if either scope_spans or instrumentation_library_spans exists
    has_scope_spans = "scope_spans" in resource_spans_data and isinstance(
        resource_spans_data["scope_spans"], list
    )
    has_instrumentation_spans = (
        "instrumentation_library_spans" in resource_spans_data
        and isinstance(resource_spans_data["instrumentation_library_spans"], list)
    )

    return has_scope_spans or has_instrumentation_spans


def validate_trace_span_structure(trace_span_data: Any) -> bool:
    """Validate trace span structure."""
    if not isinstance(trace_span_data, dict):
        return False

    required_fields = [
        "trace_id",
        "span_id",
        "name",
        "start_time_unix_nano",
        "end_time_unix_nano",
    ]

    for field in required_fields:
        if field not in trace_span_data:
            return False

    # Additional validation for field types/values
    trace_id = trace_span_data.get("trace_id")
    if isinstance(trace_id, str):
        if not re.match(r"^[a-fA-F0-9]{32}$", trace_id):
            return False

    span_id = trace_span_data.get("span_id")
    if isinstance(span_id, str):
        if not re.match(r"^[a-fA-F0-9]{16}$", span_id):
            return False

    # Validate time fields are non-negative
    start_time = trace_span_data.get("start_time_unix_nano", 0)
    end_time = trace_span_data.get("end_time_unix_nano", 0)
    if start_time < 0 or end_time < 0 or end_time < start_time:
        return False

    return True
