"""Domain module initialization.

Exports core domain entities, value objects, and events following the
Hexagonal Architecture pattern. This module provides the stable core
that adapters depend on, but never depend on any infrastructure details.
"""

from .observability import (
    SpanEvent,
    SpanId,
    SpanStatus,
    TraceId,
    TraceSpan,
    ProcessedSpan,
    validate_attributes_format,
    validate_scope_spans_structure,
    validate_span_structure,
    validate_span_id_format,
)

__all__ = [
    "SpanEvent",
    "SpanId",
    "SpanStatus",
    "TraceId",
    "TraceSpan",
    "ProcessedSpan",
    "validate_attributes_format",
    "validate_scope_spans_structure",
    "validate_span_structure",
    "validate_span_id_format",
]
