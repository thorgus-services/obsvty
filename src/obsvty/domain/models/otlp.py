from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import re


@dataclass(frozen=True)
class Span:
    """
    Immutable value object representing an OTLP Span with validation.
    """

    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    kind: int
    start_time_unix_nano: int
    end_time_unix_nano: int
    attributes: Dict[str, Any]
    events: List[Dict[str, Any]]
    status: Dict[str, Any]

    def __post_init__(self) -> None:
        # Validate trace_id: must be 32-character hex string
        if not re.match(r"^[a-fA-F0-9]{32}$", self.trace_id):
            raise ValueError("trace_id must be a 32-character hex string")

        # Validate span_id: must be 16-character hex string
        if not re.match(r"^[a-fA-F0-9]{16}$", self.span_id):
            raise ValueError("span_id must be a 16-character hex string")

        # Validate parent_span_id if provided: must be 16-character hex string
        if self.parent_span_id is not None:
            if not re.match(r"^[a-fA-F0-9]{16}$", self.parent_span_id):
                raise ValueError("parent_span_id must be a 16-character hex string")

        # Validate time values are non-negative
        if self.start_time_unix_nano < 0:
            raise ValueError("start_time_unix_nano must be non-negative")
        if self.end_time_unix_nano < 0:
            raise ValueError("end_time_unix_nano must be non-negative")
        if self.end_time_unix_nano < self.start_time_unix_nano:
            raise ValueError("end_time_unix_nano must be >= start_time_unix_nano")


@dataclass(frozen=True)
class LogRecord:
    """
    Immutable value object representing an OTLP LogRecord.
    """

    time_unix_nano: int
    severity_number: int
    severity_text: str
    body: str
    attributes: Dict[str, Any]
    trace_id: Optional[str]
    span_id: Optional[str]

    def __post_init__(self) -> None:
        # Validate time_unix_nano: must be non-negative
        if self.time_unix_nano < 0:
            raise ValueError("time_unix_nano must be non-negative")

        # Validate severity_number: must be non-negative
        if self.severity_number < 0:
            raise ValueError("severity_number must be non-negative")

        # Validate trace_id if provided: must be 32-character hex string
        if self.trace_id is not None:
            if not re.match(r"^[a-fA-F0-9]{32}$", self.trace_id):
                raise ValueError("trace_id must be a 32-character hex string")

        # Validate span_id if provided: must be 16-character hex string
        if self.span_id is not None:
            if not re.match(r"^[a-fA-F0-9]{16}$", self.span_id):
                raise ValueError("span_id must be a 16-character hex string")


@dataclass(frozen=True)
class OTLPData:
    """
    Immutable value object representing OTLP data container.
    """

    resource_spans: Tuple[Span, ...] = field(default_factory=tuple)
    resource_metrics: Tuple[Any, ...] = field(
        default_factory=tuple
    )  # Using Any for now, will be refined later
    resource_logs: Tuple[LogRecord, ...] = field(default_factory=tuple)
    received_at: datetime = field(default_factory=datetime.now)
    source_endpoint: str = ""
