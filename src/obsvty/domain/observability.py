"""Domain entities and value objects for observability data.

This module defines the core domain model for handling trace spans and
observability data, following domain-driven design principles.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class TraceId:
    """Value object representing a trace identifier."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or len(self.value) == 0:
            raise ValueError("TraceId value must be a non-empty string")


@dataclass(frozen=True)
class SpanId:
    """Value object representing a span identifier."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or len(self.value) == 0:
            raise ValueError("SpanId value must be a non-empty string")


@dataclass(frozen=True)
class SpanEvent:
    """Value object representing an event within a span."""

    name: str
    timestamp: datetime
    attributes: Dict[str, Any]


@dataclass(frozen=True)
class SpanStatus:
    """Value object representing the status of a span."""

    code: int  # 0 = UNSET, 1 = OK, 2 = ERROR
    message: Optional[str] = None


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
