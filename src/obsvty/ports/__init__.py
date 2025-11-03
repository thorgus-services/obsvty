"""Abstract port interfaces for the obsvty application core.

Expose public APIs for messaging and storage ports to enforce decoupling
according to Hexagonal Architecture (Ports & Adapters).
"""

from .messaging import TraceIngestionPort, TraceBatchIngestionPort
from .storage import TraceStoragePort

__all__ = [
    "TraceIngestionPort",
    "TraceBatchIngestionPort",
    "TraceStoragePort",
]
