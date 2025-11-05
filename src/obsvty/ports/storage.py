"""Storage ports for trace persistence.

Adapters implementing durable storage (e.g., DuckDB, files, other DBs)
must satisfy these protocol interfaces to be used by the application core.
"""

from typing import Protocol, runtime_checkable, Sequence


@runtime_checkable
class TraceStoragePort(Protocol):
    """Outbound port for storing trace payloads."""

    def store_trace(self, trace_bytes: bytes) -> None:
        """Persist a single serialized trace payload."""
        ...

    def store_batch(self, batch: Sequence[bytes]) -> None:
        """Persist a batch of serialized trace payloads."""
        ...
