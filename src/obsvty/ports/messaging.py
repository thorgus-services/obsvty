"""Messaging ports for OTLP/gRPC ingestion."""

from typing import Protocol, runtime_checkable, Sequence
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
    ExportTraceServiceResponse,
)


@runtime_checkable
class ObservabilityIngestionPort(Protocol):
    """Inbound port for OTLP trace ingestion."""

    def export_traces(
        self, request: ExportTraceServiceRequest
    ) -> ExportTraceServiceResponse:
        """Export trace data following the OTLP specification."""
        ...


@runtime_checkable
class TraceIngestionPort(Protocol):
    """Inbound port for single trace ingestion."""

    def ingest(self, trace_bytes: bytes) -> None:
        """Ingest a single trace payload provided as bytes."""
        ...


@runtime_checkable
class TraceBatchIngestionPort(Protocol):
    """Inbound port for batch trace ingestion."""

    def ingest_batch(self, batch: Sequence[bytes]) -> None:
        """Ingest a batch of serialized trace payloads."""
        ...
