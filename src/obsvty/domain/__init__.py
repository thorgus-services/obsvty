"""Domain module initialization.

Exports core domain entities, value objects, and events following the
Hexagonal Architecture pattern. This module provides the stable core
that adapters depend on, but never depend on any infrastructure details.
"""

from .observability import (
    ObservabilityBuffer,
    SpanEvent,
    SpanId,
    SpanStatus,
    TraceId,
    TraceSpan,
)

__all__ = [
    "ObservabilityBuffer",
    "SpanEvent",
    "SpanId",
    "SpanStatus",
    "TraceId",
    "TraceSpan",
]
