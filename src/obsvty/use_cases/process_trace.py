"""Minimal OTLP trace processing use case.

Implements the orchestration logic for handling incoming trace payloads and
delegating persistence to the storage port. This is intentionally lean to
enable iterative development guided by tests.
"""

from __future__ import annotations

from typing import Sequence

from ..ports.storage import TraceStoragePort


class ProcessTraceUseCase:
    """Application use case to process trace payloads."""

    def __init__(self, storage: TraceStoragePort) -> None:
        self._storage = storage

    def run(self, trace_bytes: bytes) -> None:
        """Process a single trace and persist it via the storage port."""
        self._storage.store_trace(trace_bytes)

    def run_batch(self, batch: Sequence[bytes]) -> None:
        """Process a batch of traces and persist them via the storage port."""
        self._storage.store_batch(batch)
