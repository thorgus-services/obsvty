"""Thread-safe buffer management for OTLP trace data."""

import threading
from collections import deque
from typing import List, Deque
from ..domain.observability import TraceSpan
from ..ports.buffer import TraceBufferPort


class ObservabilityBuffer(TraceBufferPort):
    def __init__(self, max_size: int = 1000) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._buffer: Deque[TraceSpan] = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self._max_size = max_size

    def add_span(self, trace_span: TraceSpan) -> bool:
        with self._lock:
            self._buffer.append(trace_span)
            return True

    def get_spans(self, count: int) -> List[TraceSpan]:
        with self._lock:
            span_list = list(self._buffer)
            result = []
            for i in range(min(count, len(span_list))):
                result.append(span_list[i])
            return result

    def size(self) -> int:
        with self._lock:
            return len(self._buffer)

    def is_full(self) -> bool:
        with self._lock:
            return len(self._buffer) >= self._max_size

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def current_size(self) -> int:
        with self._lock:
            return len(self._buffer)

    @property
    def buffer(self) -> Deque[TraceSpan]:
        with self._lock:
            return deque(self._buffer)

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._buffer) == 0

    def clear(self) -> None:
        with self._lock:
            self._buffer.clear()


class ObservabilityBufferWithConsume(TraceBufferPort):
    def __init__(self, max_size: int = 1000) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._buffer: Deque[TraceSpan] = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self._max_size = max_size

    def add_span(self, trace_span: TraceSpan) -> bool:
        with self._lock:
            self._buffer.append(trace_span)
            return True

    def get_spans(self, count: int) -> List[TraceSpan]:
        with self._lock:
            result = []
            for _ in range(min(count, len(self._buffer))):
                result.append(self._buffer.popleft())
            return result

    def size(self) -> int:
        with self._lock:
            return len(self._buffer)

    def is_full(self) -> bool:
        with self._lock:
            return len(self._buffer) >= self._max_size

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def current_size(self) -> int:
        with self._lock:
            return len(self._buffer)

    @property
    def buffer(self) -> Deque[TraceSpan]:
        with self._lock:
            return deque(self._buffer)

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._buffer) == 0

    def clear(self) -> None:
        with self._lock:
            self._buffer.clear()


class TraceBufferPortReadOnly(TraceBufferPort):
    def __init__(self, max_size: int = 1000) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._buffer: Deque[TraceSpan] = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self._max_size = max_size

    def add_span(self, trace_span: TraceSpan) -> bool:
        with self._lock:
            self._buffer.append(trace_span)
            return True

    def get_spans(self, count: int) -> List[TraceSpan]:
        with self._lock:
            span_list = list(self._buffer)
            result = []
            for i in range(min(count, len(span_list))):
                result.append(span_list[i])
            return result

    def size(self) -> int:
        with self._lock:
            return len(self._buffer)

    def is_full(self) -> bool:
        with self._lock:
            return len(self._buffer) >= self._max_size

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def current_size(self) -> int:
        with self._lock:
            return len(self._buffer)

    @property
    def buffer(self) -> Deque[TraceSpan]:
        with self._lock:
            return deque(self._buffer)

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._buffer) == 0

    def clear(self) -> None:
        with self._lock:
            self._buffer.clear()


class RejectWhenFullBuffer(TraceBufferPort):
    def __init__(self, max_size: int = 1000) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")

        self._buffer: Deque[TraceSpan] = deque(maxlen=None)
        self._lock = threading.Lock()
        self._max_size = max_size

    def add_span(self, trace_span: TraceSpan) -> bool:
        with self._lock:
            if len(self._buffer) >= self._max_size:
                return False
            self._buffer.append(trace_span)
            return True

    def get_spans(self, count: int) -> List[TraceSpan]:
        with self._lock:
            span_list = list(self._buffer)
            result = []
            for i in range(min(count, len(span_list))):
                result.append(span_list[i])
            return result

    def size(self) -> int:
        with self._lock:
            return len(self._buffer)

    def is_full(self) -> bool:
        with self._lock:
            return len(self._buffer) >= self._max_size

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def current_size(self) -> int:
        with self._lock:
            return len(self._buffer)

    @property
    def buffer(self) -> Deque[TraceSpan]:
        with self._lock:
            return deque(self._buffer)

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._buffer) == 0

    def clear(self) -> None:
        with self._lock:
            self._buffer.clear()
