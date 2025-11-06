"""Test configuration and fixtures for migrated validation tests."""

import pytest
from typing import Generator

# Import opentelemetry proto dependencies (required for validation tests)
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.resource.v1 import resource_pb2
from opentelemetry.proto.trace.v1 import trace_pb2

import time

from src.obsvty.application.buffer_management import (
    RejectWhenFullBuffer,
    ObservabilityBuffer,
)
from src.obsvty.use_cases.process_trace import ProcessTraceUseCase
from src.obsvty.ports.storage import TraceStoragePort
from src.obsvty.config import OtlpGrpcSettings


@pytest.fixture
def buffer_manager() -> Generator[RejectWhenFullBuffer, None, None]:
    """Create a buffer manager for testing."""
    buffer_manager = RejectWhenFullBuffer(max_size=100)
    yield buffer_manager


@pytest.fixture
def simple_buffer_manager() -> Generator[ObservabilityBuffer, None, None]:
    """Create a simple buffer manager for testing."""
    buffer_manager = ObservabilityBuffer(max_size=100)
    yield buffer_manager


@pytest.fixture
def valid_trace_request():
    """Create a valid OTLP trace request."""
    # Create a simple trace request following OTLP v1.9 specification
    trace_request = trace_service_pb2.ExportTraceServiceRequest(
        resource_spans=[
            trace_pb2.ResourceSpans(
                resource=resource_pb2.Resource(
                    attributes=[
                        common_pb2.KeyValue(
                            key="service.name",
                            value=common_pb2.AnyValue(string_value="test-service"),
                        )
                    ]
                ),
                scope_spans=[
                    trace_pb2.ScopeSpans(
                        scope=common_pb2.InstrumentationScope(
                            name="test-instrumentation", version="1.0.0"
                        ),
                        spans=[
                            trace_pb2.Span(
                                trace_id=b"\x00" * 16,  # 16-byte trace ID
                                span_id=b"\x00" * 8,  # 8-byte span ID
                                name="test-span",
                                kind=trace_pb2.Span.SpanKind.SPAN_KIND_INTERNAL,
                                start_time_unix_nano=int(time.time() * 1_000_000_000),
                                end_time_unix_nano=int(time.time() * 1_000_000_000)
                                + 1000000,
                            )
                        ],
                    )
                ],
            )
        ]
    )
    return trace_request


class MockStorage(TraceStoragePort):
    def __init__(self):
        self.traces = []

    def store_trace(self, trace_bytes: bytes) -> None:
        self.traces.append(trace_bytes)

    def store_batch(self, batch: list[bytes]) -> None:
        self.traces.extend(batch)


@pytest.fixture
def mock_storage():
    return MockStorage()


@pytest.fixture
def process_trace_use_case(mock_storage):
    return ProcessTraceUseCase(mock_storage)


@pytest.fixture
def otlp_config():
    config = OtlpGrpcSettings(
        host="localhost",
        port=4317,
        max_message_length=4 * 1024 * 1024,  # 4MB
        enable_reflection=True,
        max_buffer_size=1000,
    )
    return config
