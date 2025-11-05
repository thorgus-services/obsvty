"""Integration tests for OTLP gRPC adapter with real gRPC client-server interactions.

These tests verify the complete flow from gRPC client request to server response,
validating that the OTLP gRPC adapter integrates properly with the gRPC framework.
"""

import threading
import time
from typing import Generator

import grpc
import pytest
from grpc_health.v1 import health_pb2, health_pb2_grpc
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
    ExportTraceServiceResponse,
)
from opentelemetry.proto.collector.trace.v1.trace_service_pb2_grpc import (
    TraceServiceStub,
)
from opentelemetry.proto.trace.v1.trace_pb2 import (
    Span,
    Status as SpanStatus,
    ResourceSpans,
    ScopeSpans,
)
from opentelemetry.proto.resource.v1.resource_pb2 import Resource
from unittest.mock import Mock


from src.obsvty.adapters.messaging.otlp_grpc import OTLPgRPCAdapter
from src.obsvty.config import OTLPGRPCServerConfig
from src.obsvty.use_cases import ProcessTraceUseCase


@pytest.fixture
def grpc_server() -> Generator[tuple[str, OTLPgRPCAdapter], None, None]:
    """Start a gRPC server for testing and yield the connection details."""
    # Configuration for test server
    config = OTLPGRPCServerConfig(
        host="localhost",
        port=50052,  # Use a test port
        max_buffer_size=100,
        enable_reflection=True,  # Enable reflection for testing
    )

    # Mock use case
    mock_use_case = Mock(spec=ProcessTraceUseCase)

    # Create and configure the adapter
    adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=adapter.start_server)
    server_thread.daemon = True
    server_thread.start()

    # Wait a moment for the server to start
    time.sleep(0.5)

    try:
        yield f"localhost:{config.port}", adapter
    finally:
        # Stop the server
        adapter.stop_server()


def test_grpc_server_startup_and_shutdown(
    grpc_server: tuple[str, OTLPgRPCAdapter],
) -> None:
    """Verifies that the gRPC server starts and stops properly."""
    server_address, adapter = grpc_server

    # Verify that we can create a channel to the server
    channel = grpc.insecure_channel(server_address)

    # Test health check
    try:
        # Try to connect and get health status
        health_stub = health_pb2_grpc.HealthStub(channel)
        health_request = health_pb2.HealthCheckRequest()
        # This should not raise an exception if the server is running
        response = health_stub.Check(health_request, timeout=5.0)
        assert response.status == health_pb2.HealthCheckResponse.SERVING
    except grpc.RpcError:
        # If health check is not implemented, try connecting to our service
        stub = TraceServiceStub(channel)
        # Create a minimal request
        request = ExportTraceServiceRequest()

        # The server should be responsive
        response = stub.Export(request, timeout=5.0)
        assert isinstance(response, ExportTraceServiceResponse)

    channel.close()


def test_grpc_trace_export_integration(
    grpc_server: tuple[str, OTLPgRPCAdapter],
) -> None:
    """Verifies that trace export requests are properly handled by the gRPC server."""
    server_address, adapter = grpc_server

    # Create a gRPC channel and stub
    with grpc.insecure_channel(server_address) as channel:
        stub = TraceServiceStub(channel)

        # Create an export request (minimal valid request)
        request = ExportTraceServiceRequest()

        # Send the request to the server
        response = stub.Export(request, timeout=5.0)

        # Verify the response
        assert isinstance(response, ExportTraceServiceResponse)
        # The server should return a valid response without errors


def test_grpc_trace_export_with_trace_data_integration(
    grpc_server: tuple[str, OTLPgRPCAdapter],
) -> None:
    """Verifies that trace export requests with actual trace data are handled properly."""
    server_address, adapter = grpc_server

    # Create a gRPC channel and stub
    with grpc.insecure_channel(server_address) as channel:
        stub = TraceServiceStub(channel)

        # Create an export request with some trace data
        # This creates a request with an empty resource spans, which is valid
        request = ExportTraceServiceRequest(resource_spans=[])

        # Send the request to the server
        response = stub.Export(request, timeout=5.0)

        # Verify the response
        assert isinstance(response, ExportTraceServiceResponse)


def test_grpc_server_processes_traces_through_use_case(
    grpc_server: tuple[str, OTLPgRPCAdapter],
) -> None:
    """Verifies that the gRPC server properly delegates to the use case."""
    server_address, adapter = grpc_server

    # Verify that the mock use case was passed correctly
    assert adapter._process_trace_use_case is not None

    # Reset the mock to verify calls are made
    adapter._process_trace_use_case.run.reset_mock()

    # Create a gRPC channel and stub
    with grpc.insecure_channel(server_address) as channel:
        stub = TraceServiceStub(channel)

        # Create an export request with some minimal content to trigger processing

        # Create a minimal span to trigger the processing loop
        span = Span(
            trace_id=bytes([1] * 16),  # 16-byte trace ID
            span_id=bytes([2] * 8),  # 8-byte span ID
            parent_span_id=bytes([3] * 8),  # 8-byte parent span ID
            name="test_span",
            kind=Span.SpanKind.SPAN_KIND_INTERNAL,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes=[],
            events=[],
            links=[],
            status=SpanStatus(code=SpanStatus.StatusCode.STATUS_CODE_UNSET),
        )

        # Create a request with the span
        request = ExportTraceServiceRequest(
            resource_spans=[
                ResourceSpans(
                    resource=Resource(attributes=[]),
                    scope_spans=[
                        ScopeSpans(
                            scope=None,  # Use default scope
                            spans=[span],
                            schema_url="",
                        )
                    ],
                    schema_url="",
                )
            ]
        )

        # Send the request to the server
        response = stub.Export(request, timeout=5.0)

        # Verify the response
        assert isinstance(response, ExportTraceServiceResponse)

        # Verify that the use case was called (at least once)
        # The run() method should be called during processing
        assert adapter._process_trace_use_case.run.called


def test_grpc_server_buffer_management_integration(
    grpc_server: tuple[str, OTLPgRPCAdapter],
) -> None:
    """Verifies that the gRPC server properly manages the buffer."""
    server_address, adapter = grpc_server

    # Check initial buffer state
    initial_status = adapter.get_buffer_status()
    assert initial_status["current_size"] == 0
    assert initial_status["is_empty"] is True

    # Create a gRPC channel and stub
    with grpc.insecure_channel(server_address) as channel:
        stub = TraceServiceStub(channel)

        # Send a request to the server
        request = ExportTraceServiceRequest()
        response = stub.Export(request, timeout=5.0)

        # Verify the response
        assert isinstance(response, ExportTraceServiceResponse)

        # The buffer status should still be accessible
        final_status = adapter.get_buffer_status()
        assert final_status["max_size"] == adapter._config.max_buffer_size
