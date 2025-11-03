from __future__ import annotations

from typing import Sequence

from obsvty.use_cases import ProcessTraceUseCase
from obsvty.ports import TraceStoragePort


class FakeStorage(TraceStoragePort):
    def __init__(self) -> None:
        self.calls: list[tuple[str, bytes | list[bytes]]] = []

    def store_trace(self, trace_bytes: bytes) -> None:
        self.calls.append(("single", trace_bytes))

    def store_batch(self, batch: Sequence[bytes]) -> None:
        self.calls.append(("batch", list(batch)))


def test_run_calls_store_trace() -> None:
    storage = FakeStorage()
    use_case = ProcessTraceUseCase(storage)

    payload = b"trace-bytes"
    use_case.run(payload)

    assert storage.calls == [("single", payload)]


def test_run_batch_calls_store_batch() -> None:
    storage = FakeStorage()
    use_case = ProcessTraceUseCase(storage)

    batch = [b"t1", b"t2"]
    use_case.run_batch(batch)

    assert storage.calls == [("batch", batch)]
