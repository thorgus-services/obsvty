"""In-memory buffer implementation for temporary data storage."""

import threading
from typing import List, Any
from obsvty.application.ports.otlp_ports import TraceBufferPort
from obsvty.domain.models.otlp import Span, LogRecord


class MemoryBuffer(TraceBufferPort):
    """Thread-safe in-memory buffer implementation for temporary data storage."""

    def __init__(self, max_size: int = 1000):
        self._max_size = max_size
        self._spans: List[Span] = []
        self._logs: List[LogRecord] = []
        self._metrics: List[Any] = []
        self._lock = threading.RLock()  # Reentrant lock for thread safety

    def add_span(self, trace_span: Span) -> bool:
        """Add a span to the buffer."""
        with self._lock:
            if self.is_full():
                return False

            self._spans.append(trace_span)
            return True

    def add_log(self, log_record: LogRecord) -> bool:
        """Add a log record to the buffer."""
        with self._lock:
            if self.is_full():
                return False

            self._logs.append(log_record)
            return True

    def add_metric(self, metric_data: Any) -> bool:
        """Add metric data to the buffer."""
        with self._lock:
            if self.is_full():
                return False

            self._metrics.append(metric_data)
            return True

    def get_spans(self, count: int) -> List[Span]:
        """Get a specified number of spans from the buffer."""
        with self._lock:
            result = self._spans[:count]
            # Optionally remove the retrieved spans from the buffer
            # For now, we'll just return them without removal
            return result.copy()  # Return a copy to maintain immutability

    def get_logs(self, count: int) -> List[LogRecord]:
        """Get a specified number of log records from the buffer."""
        with self._lock:
            result = self._logs[:count]
            return result.copy()  # Return a copy to maintain immutability

    def size(self) -> int:
        """Get the current size of the buffer."""
        with self._lock:
            return len(self._spans) + len(self._logs) + len(self._metrics)

    def is_full(self) -> bool:
        """Check if the buffer is full."""
        with self._lock:
            return self.size() >= self._max_size

    def clear(self) -> None:
        """Clear all data from the buffer."""
        with self._lock:
            self._spans.clear()
            self._logs.clear()
            self._metrics.clear()

    def get_all_spans(self) -> List[Span]:
        """Get all spans from the buffer."""
        with self._lock:
            return self._spans.copy()

    def get_all_logs(self) -> List[LogRecord]:
        """Get all log records from the buffer."""
        with self._lock:
            return self._logs.copy()

    def get_all_metrics(self) -> List[Any]:
        """Get all metric data from the buffer."""
        with self._lock:
            return self._metrics.copy()
