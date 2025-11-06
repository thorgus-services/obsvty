"""Buffer interface for OTLP data storage."""

from typing import List, Protocol
from ..domain.observability import TraceSpan


class TraceBufferPort(Protocol):
    """Interface for trace buffer operations."""

    def add_span(self, trace_span: TraceSpan) -> bool:
        """Add a span to the buffer, returning True if successful, False if discarded."""
        ...

    def get_spans(self, count: int) -> List[TraceSpan]:
        """Get up to 'count' spans from the buffer."""
        ...

    def size(self) -> int:
        """Get current buffer size."""
        ...

    def is_full(self) -> bool:
        """Check if buffer is at maximum capacity."""
        ...
