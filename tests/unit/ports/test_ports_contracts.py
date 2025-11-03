from __future__ import annotations

from typing import Sequence

from obsvty.ports import (
    TraceBatchIngestionPort,
    TraceIngestionPort,
    TraceStoragePort,
)


class IngestionAdapter:
    def __init__(self) -> None:
        self.received: list[bytes] = []

    def ingest(self, trace_bytes: bytes) -> None:  # matches TraceIngestionPort
        self.received.append(trace_bytes)

    def ingest_batch(
        self, batch: Sequence[bytes]
    ) -> None:  # matches TraceBatchIngestionPort
        self.received.extend(batch)


class StorageAdapter:
    def __init__(self) -> None:
        self.persisted: list[bytes] = []

    def store_trace(self, trace_bytes: bytes) -> None:  # matches TraceStoragePort
        self.persisted.append(trace_bytes)

    def store_batch(self, batch: Sequence[bytes]) -> None:  # matches TraceStoragePort
        self.persisted.extend(batch)


def test_ingestion_ports_runtime_checkable() -> None:
    adapter = IngestionAdapter()
    assert isinstance(adapter, TraceIngestionPort)
    assert isinstance(adapter, TraceBatchIngestionPort)


def test_storage_port_runtime_checkable_and_methods() -> None:
    storage = StorageAdapter()
    assert isinstance(storage, TraceStoragePort)

    storage.store_trace(b"x")
    storage.store_batch([b"y", b"z"])

    assert storage.persisted == [b"x", b"y", b"z"]
