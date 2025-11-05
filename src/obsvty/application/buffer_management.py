"""Thread-safe buffer management for OTLP trace data."""

import threading
from collections import deque
from typing import List, Deque
from ..domain.observability import TraceSpan
from ..ports.buffer import TraceBufferPort


class ObservabilityBuffer(TraceBufferPort):
    """Thread-safe buffer implementation for storing OTLP trace spans with FIFO discard policy."""

    def __init__(self, max_size: int = 1000) -> None:
        """
        Initialize the buffer with a maximum size.

        Args:
            max_size: Maximum number of spans the buffer can hold
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._buffer: Deque[TraceSpan] = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self._max_size = max_size

    def add_span(self, trace_span: TraceSpan) -> bool:
        """
        Add a span to the buffer, applying FIFO discard policy if needed.

        Args:
            trace_span: The trace span to add to the buffer

        Returns:
            True if the span was added successfully, with FIFO discard when at capacity
        """
        with self._lock:
            self._buffer.append(trace_span)  # This automatically applies FIFO

            # In FIFO with maxlen, the item is always added successfully
            return True

    def get_spans(self, count: int) -> List[TraceSpan]:
        """
        Get up to 'count' spans from the buffer (read-only, doesn't consume).

        Args:
            count: Maximum number of spans to retrieve

        Returns:
            List of spans (up to 'count' in number)
        """
        with self._lock:
            span_list = list(self._buffer)
            result = []
            for i in range(min(count, len(span_list))):
                result.append(span_list[i])
            return result

    def size(self) -> int:
        """Get current buffer size."""
        with self._lock:
            return len(self._buffer)

    def is_full(self) -> bool:
        """Check if buffer is at maximum capacity."""
        with self._lock:
            return len(self._buffer) >= self._max_size

    @property
    def max_size(self) -> int:
        """Get maximum buffer size."""
        return self._max_size

    @property
    def current_size(self) -> int:
        """Get current buffer size (for compatibility with existing tests)."""
        with self._lock:
            return len(self._buffer)

    @property
    def buffer(self) -> Deque[TraceSpan]:
        """Get the internal buffer (for testing compatibility)."""
        with self._lock:
            # Return a copy to prevent external modification
            return deque(self._buffer)

    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        with self._lock:
            return len(self._buffer) == 0

    def clear(self) -> None:
        """Clear the buffer (for testing compatibility)."""
        with self._lock:
            self._buffer.clear()


class ObservabilityBufferWithConsume(TraceBufferPort):
    """
    Alternative implementation that provides consume functionality (removes spans when retrieved).
    This follows a more traditional queue pattern where getting spans also removes them.
    """

    def __init__(self, max_size: int = 1000) -> None:
        """
        Initialize the buffer with a maximum size.

        Args:
            max_size: Maximum number of spans the buffer can hold
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._buffer: Deque[TraceSpan] = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self._max_size = max_size

    def add_span(self, trace_span: TraceSpan) -> bool:
        """
        Add a span to the buffer, applying FIFO discard policy if needed.

        Args:
            trace_span: The trace span to add to the buffer

        Returns:
            True if the span was added successfully, with FIFO discard when at capacity
        """
        with self._lock:
            self._buffer.append(trace_span)  # This automatically applies FIFO
            return True  # Always returns True for FIFO implementation

    def get_spans(self, count: int) -> List[TraceSpan]:
        """
        Get and remove up to 'count' spans from the buffer.

        Args:
            count: Maximum number of spans to retrieve and remove

        Returns:
            List of spans (up to 'count' in number)
        """
        with self._lock:
            result = []
            for _ in range(min(count, len(self._buffer))):
                result.append(self._buffer.popleft())
            return result

    def size(self) -> int:
        """Get current buffer size."""
        with self._lock:
            return len(self._buffer)

    def is_full(self) -> bool:
        """Check if buffer is at maximum capacity."""
        with self._lock:
            return len(self._buffer) >= self._max_size

    @property
    def max_size(self) -> int:
        """Get maximum buffer size."""
        return self._max_size

    @property
    def current_size(self) -> int:
        """Get current buffer size (for compatibility with existing tests)."""
        with self._lock:
            return len(self._buffer)

    @property
    def buffer(self) -> Deque[TraceSpan]:
        """Get the internal buffer (for testing compatibility)."""
        with self._lock:
            # Return a copy to prevent external modification
            return deque(self._buffer)

    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        with self._lock:
            return len(self._buffer) == 0

    def clear(self) -> None:
        """Clear the buffer (for testing compatibility)."""
        with self._lock:
            self._buffer.clear()


class TraceBufferPortReadOnly(TraceBufferPort):
    """
    A read-only buffer interface implementation that doesn't consume spans when retrieved.
    """

    def __init__(self, max_size: int = 1000) -> None:
        """
        Initialize the buffer with a maximum size.

        Args:
            max_size: Maximum number of spans the buffer can hold
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._buffer: Deque[TraceSpan] = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self._max_size = max_size

    def add_span(self, trace_span: TraceSpan) -> bool:
        """
        Add a span to the buffer, applying FIFO discard policy if needed.

        Args:
            trace_span: The trace span to add to the buffer

        Returns:
            True if the span was added successfully, with FIFO discard when at capacity
        """
        with self._lock:
            self._buffer.append(trace_span)  # This automatically applies FIFO
            return True  # Always returns True for FIFO implementation

    def get_spans(self, count: int) -> List[TraceSpan]:
        """
        Get up to 'count' spans from the buffer (read-only, doesn't consume).

        Args:
            count: Maximum number of spans to retrieve

        Returns:
            List of spans (up to 'count' in number)
        """
        with self._lock:
            span_list = list(self._buffer)
            result = []
            for i in range(min(count, len(span_list))):
                result.append(span_list[i])
            return result

    def size(self) -> int:
        """Get current buffer size."""
        with self._lock:
            return len(self._buffer)

    def is_full(self) -> bool:
        """Check if buffer is at maximum capacity."""
        with self._lock:
            return len(self._buffer) >= self._max_size

    @property
    def max_size(self) -> int:
        """Get maximum buffer size."""
        return self._max_size

    @property
    def current_size(self) -> int:
        """Get current buffer size (for compatibility with existing tests)."""
        with self._lock:
            return len(self._buffer)

    @property
    def buffer(self) -> Deque[TraceSpan]:
        """Get the internal buffer (for testing compatibility)."""
        with self._lock:
            # Return a copy to prevent external modification
            return deque(self._buffer)

    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        with self._lock:
            return len(self._buffer) == 0

    def clear(self) -> None:
        """Clear the buffer (for testing compatibility)."""
        with self._lock:
            self._buffer.clear()


class RejectWhenFullBuffer(TraceBufferPort):
    """
    A buffer implementation that rejects new items when at full capacity.
    """

    def __init__(self, max_size: int = 1000) -> None:
        """
        Initialize the buffer with a maximum size.

        Args:
            max_size: Maximum number of spans the buffer can hold
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._buffer: Deque[TraceSpan] = deque(maxlen=None)  # No automatic discard
        self._lock = threading.Lock()
        self._max_size = max_size

    def add_span(self, trace_span: TraceSpan) -> bool:
        """
        Add a span to the buffer, returning True if successful, False if rejected due to capacity.

        Args:
            trace_span: The trace span to add to the buffer

        Returns:
            True if the span was added successfully, False if rejected due to capacity.
        """
        with self._lock:
            if len(self._buffer) >= self._max_size:
                # Buffer is full, reject the new span
                return False
            else:
                # Buffer has space, add the span
                self._buffer.append(trace_span)
                return True

    def get_spans(self, count: int) -> List[TraceSpan]:
        """
        Get up to 'count' spans from the buffer (read-only, doesn't consume).

        Args:
            count: Maximum number of spans to retrieve

        Returns:
            List of spans (up to 'count' in number)
        """
        with self._lock:
            span_list = list(self._buffer)
            result = []
            for i in range(min(count, len(span_list))):
                result.append(span_list[i])
            return result

    def size(self) -> int:
        """Get current buffer size."""
        with self._lock:
            return len(self._buffer)

    def is_full(self) -> bool:
        """Check if buffer is at maximum capacity."""
        with self._lock:
            return len(self._buffer) >= self._max_size

    @property
    def max_size(self) -> int:
        """Get maximum buffer size."""
        return self._max_size

    @property
    def current_size(self) -> int:
        """Get current buffer size (for compatibility with existing tests)."""
        with self._lock:
            return len(self._buffer)

    @property
    def buffer(self) -> Deque[TraceSpan]:
        """Get the internal buffer (for testing compatibility)."""
        with self._lock:
            # Return a copy to prevent external modification
            return deque(self._buffer)

    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        with self._lock:
            return len(self._buffer) == 0

    def clear(self) -> None:
        """Clear the buffer (for testing compatibility)."""
        with self._lock:
            self._buffer.clear()
