"""Abstract port interfaces for the obsvty application core.

Expose public APIs for messaging and storage ports to enforce decoupling
according to Hexagonal Architecture (Ports & Adapters).
"""

from .messaging import (
    ObservabilityIngestionPort,
    TraceIngestionPort,
    TraceBatchIngestionPort,
)
from .storage import TraceStoragePort

__all__ = [
    "ObservabilityIngestionPort",
    "TraceIngestionPort",
    "TraceBatchIngestionPort",
    "TraceStoragePort",
]
