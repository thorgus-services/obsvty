"""Messaging ports for OTLP/gRPC ingestion.

Defines abstract interfaces (typing.Protocol) that inbound adapters must
implement to deliver telemetry data into the application core. These ports
are intentionally minimal to enforce decoupling from transport specifics.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable, Sequence


@runtime_checkable
class TraceIngestionPort(Protocol):
    """Inbound port for single trace ingestion.

    Adapters (e.g., gRPC servers) should call this method with the serialized
    trace payload. The application core decides how to process/store it.
    """

    def ingest(self, trace_bytes: bytes) -> None:
        """Ingest a single trace payload provided as bytes."""
        ...


@runtime_checkable
class TraceBatchIngestionPort(Protocol):
    """Inbound port for batch trace ingestion."""

    def ingest_batch(self, batch: Sequence[bytes]) -> None:
        """Ingest a batch of serialized trace payloads."""
        ...
