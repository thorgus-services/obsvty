"""Messaging ports for OTLP/gRPC ingestion.

Defines abstract interfaces (typing.Protocol) that inbound adapters must
implement to deliver telemetry data into the application core. These ports
are intentionally minimal to enforce decoupling from transport specifics.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable, Sequence
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
    ExportTraceServiceResponse,
)


@runtime_checkable
class ObservabilityIngestionPort(Protocol):
    """Inbound port for OTLP trace ingestion following the official specification.

    Adapters implementing the OTLP/gRPC protocol should use this interface to
    deliver trace data to the application core. This aligns with the official
    OpenTelemetry Protocol specification for trace collection.
    """

    def export_traces(
        self, request: ExportTraceServiceRequest
    ) -> ExportTraceServiceResponse:
        """Export trace data following the OTLP specification.

        Args:
            request: ExportTraceServiceRequest containing trace data in OTLP format

        Returns:
            ExportTraceServiceResponse with status information
        """
        ...


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
