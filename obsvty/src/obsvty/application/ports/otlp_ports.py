from typing import Protocol, List, Any
from obsvty.domain.models.otlp import Span, LogRecord


class OTLPIngestionPort(Protocol):
    """
    Primary port (driven by external actor) for OTLP ingestion.

    Following the hexagonal architecture pattern, this interface defines
    how the application receives OTLP data from external sources like
    gRPC services.
    """

    def ingest_traces(self, trace_data: bytes) -> None:
        """
        Ingest trace data in OTLP format.

        Args:
            trace_data: Raw OTLP trace data as bytes
        """
        ...

    def ingest_metrics(self, metric_data: bytes) -> None:
        """
        Ingest metric data in OTLP format.

        Args:
            metric_data: Raw OTLP metric data as bytes
        """
        ...

    def ingest_logs(self, log_data: bytes) -> None:
        """
        Ingest log data in OTLP format.

        Args:
            log_data: Raw OTLP log data as bytes
        """
        ...


class TraceBufferPort(Protocol):
    """
    Secondary port (driving external system) for buffer operations.

    This port defines how the application interacts with a buffer
    for temporary storage of telemetry data.
    """

    def add_span(self, trace_span: Span) -> bool:
        """
        Add a span to the buffer.

        Args:
            trace_span: The span to add

        Returns:
            True if successfully added, False otherwise
        """
        ...

    def add_log(self, log_record: LogRecord) -> bool:
        """
        Add a log record to the buffer.

        Args:
            log_record: The log record to add

        Returns:
            True if successfully added, False otherwise
        """
        ...

    def add_metric(self, metric_data: Any) -> bool:
        """
        Add metric data to the buffer.

        Args:
            metric_data: The metric data to add

        Returns:
            True if successfully added, False otherwise
        """
        ...

    def get_spans(self, count: int) -> List[Span]:
        """
        Get a specified number of spans from the buffer.

        Args:
            count: Number of spans to retrieve

        Returns:
            List of spans
        """
        ...

    def get_logs(self, count: int) -> List[LogRecord]:
        """
        Get a specified number of log records from the buffer.

        Args:
            count: Number of log records to retrieve

        Returns:
            List of log records
        """
        ...

    def size(self) -> int:
        """
        Get the current size of the buffer.

        Returns:
            Number of items in the buffer
        """
        ...

    def is_full(self) -> bool:
        """
        Check if the buffer is full.

        Returns:
            True if buffer is full, False otherwise
        """
        ...
