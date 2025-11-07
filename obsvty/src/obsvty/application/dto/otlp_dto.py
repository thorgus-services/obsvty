"""DTOs for OTLP data exchange."""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class OTLPIngestionDTO:
    """
    DTO for OTLP ingestion operations.
    This DTO is used at the boundary between infrastructure and application layers.
    """

    trace_data: bytes
    source_endpoint: str = ""
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class TraceIngestionDTO:
    """
    DTO specifically for trace ingestion requests.
    """

    trace_id: str
    spans: bytes  # Serialized span data
    service_name: str
    resource_attributes: Dict[str, Any]


@dataclass(frozen=True)
class MetricsIngestionDTO:
    """
    DTO for metrics ingestion requests.
    """

    metrics_data: bytes  # Serialized metrics data
    service_name: str
    resource_attributes: Dict[str, Any]


@dataclass(frozen=True)
class LogsIngestionDTO:
    """
    DTO for logs ingestion requests.
    """

    logs_data: bytes  # Serialized logs data
    service_name: str
    resource_attributes: Dict[str, Any]


@dataclass(frozen=True)
class OTLPResponseDTO:
    """
    DTO for OTLP responses.
    """

    success: bool
    message: str = ""
    processed_items_count: int = 0
    error_details: Optional[Dict[str, Any]] = None
