from __future__ import annotations

from typing import Sequence

import obsvty
from obsvty.main import build_use_cases, main


class MemStorage(obsvty.TraceStoragePort):
    def __init__(self) -> None:
        self.items: list[bytes] = []

    def store_trace(self, trace_bytes: bytes) -> None:
        self.items.append(trace_bytes)

    def store_batch(self, batch: Sequence[bytes]) -> None:
        self.items.extend(batch)


def test_build_use_cases_and_execute() -> None:
    storage = MemStorage()
    ucs = build_use_cases(storage)

    assert "process_trace" in ucs
    ucs["process_trace"].run(b"abc")
    ucs["process_trace"].run_batch([b"def"])

    assert storage.items == [b"abc", b"def"]


def test_package_entrypoint_main_returns_zero() -> None:
    assert main() == 0
