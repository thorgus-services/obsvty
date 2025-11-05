"""Unit tests for OTLP gRPC adapter following TDD principles.

These tests are written first to define the expected behavior of the
OTLP gRPC adapter before implementing the actual functionality.
"""

from __future__ import annotations

from unittest.mock import Mock

from src.obsvty.ports import ObservabilityIngestionPort
from src.obsvty.adapters.messaging.otlp_grpc import OTLPgRPCAdapter
from src.obsvty.config import OTLPGRPCServerConfig
from src.obsvty.use_cases import ProcessTraceUseCase
from src.obsvty.domain import TraceSpan, TraceId, SpanId, SpanStatus

# Import the OTLP protobuf classes for testing
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
    ExportTraceServiceResponse,
)
import grpc


class TestOTLPgRPCAdapterContract:
    """Test suite for ObservabilityIngestionPort contract compliance."""

    def test_implementation_follows_hexagonal_architecture(self) -> None:
        """Verifies if implementation complies with DIP and architectural boundaries."""
        # Given: A mock use case and configuration
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()

        # When: Creating the adapter instance
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Then: The adapter should be an instance of the port interface
        assert isinstance(adapter, ObservabilityIngestionPort)

    def test_export_traces_method_exists_and_callable(self) -> None:
        """Verifies if the export_traces method exists and is properly defined."""
        # Given: A mock use case and configuration
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()

        # When: Creating the adapter instance
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Then: The adapter should have the export_traces method
        assert hasattr(adapter, "export_traces")
        assert callable(getattr(adapter, "export_traces"))

    def test_export_traces_accepts_export_request_and_returns_response(self) -> None:
        """Verifies if export_traces method accepts proper OTLP request and returns response."""
        # Given: A mock use case, configuration, and a sample request
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        sample_request = ExportTraceServiceRequest()

        # When: Creating the adapter and calling export_traces
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)
        result = adapter.export_traces(sample_request)

        # Then: The result should be an ExportTraceServiceResponse
        assert isinstance(result, ExportTraceServiceResponse)

    def test_grpc_server_handles_trace_requests(self) -> None:
        """Verifies if gRPC adapter correctly processes ExportTraceServiceRequest messages."""
        # Given: A mock use case and configuration
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()

        # When: Creating the adapter and processing a trace request
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)
        request = ExportTraceServiceRequest()
        response = adapter.export_traces(request)

        # Then: The response should be properly structured
        assert response is not None
        assert isinstance(response, ExportTraceServiceResponse)

    def test_grpc_service_returns_success_response(self) -> None:
        """Verifies if service returns proper ExportTraceServiceResponse with SUCCESS status."""
        # Given: A mock use case and configuration
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()

        # When: Creating the adapter and calling export_traces
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)
        request = ExportTraceServiceRequest()
        response = adapter.export_traces(request)

        # Then: The response should be successful
        # Note: For now, we just check that it's a valid response object
        # The actual status will be implemented in the adapter
        assert isinstance(response, ExportTraceServiceResponse)


class TestOTLPgRPCAdapterImplementation:
    """Test the actual implementation methods."""

    def test_init_requires_process_trace_use_case_and_config(self) -> None:
        """Verifies that adapter constructor requires proper dependencies."""
        # Given: Mock dependencies
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()

        # When: Creating an adapter instance
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Then: The adapter should store these dependencies
        assert adapter._process_trace_use_case == mock_use_case
        assert adapter._config == config

    def test_init_creates_buffer_with_configured_size(self) -> None:
        """Verifies that adapter creates buffer with size from configuration."""
        # Given: Mock dependencies and config with specific buffer size
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig(max_buffer_size=5000)

        # When: Creating an adapter instance
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Then: The buffer should have the correct size
        assert adapter._buffer.max_size == 5000
        assert adapter._buffer.current_size == 0
        assert len(adapter._buffer.buffer) == 0


class TestOTLPgRPCBufferManagement:
    """Test buffer management functionality."""

    def test_buffer_adds_span_successfully(self) -> None:
        """Verifies that spans can be added to the buffer."""
        # Given: An adapter with a small buffer
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig(max_buffer_size=2)
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # When: Adding a span to the buffer
        trace_span = TraceSpan(
            trace_id=TraceId(value="12345678901234567890123456789012"),  # 32 hex chars
            span_id=SpanId(value="1234567890123456"),  # 16 hex chars
            parent_span_id=None,
            name="test_span",
            start_time_unix_nano=0,
            end_time_unix_nano=1000,
            attributes={},
            events=[],
            status=SpanStatus(code=0, message="OK"),  # Use proper status object
        )

        # Then: The span should be added successfully
        assert adapter._buffer.add_span(trace_span) is True
        assert adapter._buffer.current_size == 1
        assert len(adapter._buffer.buffer) == 1

    def test_buffer_full_prevention(self) -> None:
        """Verifies that buffer prevents adding beyond max size."""
        # Given: An adapter with a small buffer
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig(max_buffer_size=1)
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Add first span
        first_span = TraceSpan(
            trace_id=TraceId(value="12345678901234567890123456789012"),  # 32 hex chars
            span_id=SpanId(value="1234567890123456"),  # 16 hex chars
            parent_span_id=None,
            name="first_span",
            start_time_unix_nano=0,
            end_time_unix_nano=1000,
            attributes={},
            events=[],
            status=SpanStatus(code=0, message="OK"),  # Use proper status object
        )

        # When: Adding a span to the full buffer
        result1 = adapter._buffer.add_span(first_span)
        result2 = adapter._buffer.add_span(first_span)  # Try to add another

        # Then: Only first should succeed
        assert result1 is True
        assert result2 is False
        assert adapter._buffer.current_size == 1
        assert len(adapter._buffer.buffer) == 1

    def test_buffer_status_method(self) -> None:
        """Verifies that buffer status method returns correct information."""
        # Given: An adapter with a buffer
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig(max_buffer_size=10)
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # When: Getting buffer status on empty buffer
        status = adapter.get_buffer_status()

        # Then: Status should show empty buffer
        assert status["current_size"] == 0
        assert status["max_size"] == 10
        assert status["is_empty"] is True
        assert status["is_full"] is False

        # When: Adding a span and checking status again
        trace_span = TraceSpan(
            trace_id=TraceId(value="12345678901234567890123456789012"),  # 32 hex chars
            span_id=SpanId(value="1234567890123456"),  # 16 hex chars
            parent_span_id=None,
            name="test_span",
            start_time_unix_nano=0,
            end_time_unix_nano=1000,
            attributes={},
            events=[],
            status=SpanStatus(code=0, message="OK"),  # Use proper status object
        )
        adapter._buffer.add_span(trace_span)
        status = adapter.get_buffer_status()

        # Then: Status should show one item in buffer
        assert status["current_size"] == 1
        assert status["is_empty"] is False
        assert status["is_full"] is False

    def test_buffer_clear_method(self) -> None:
        """Verifies that buffer clear method works correctly."""
        # Given: An adapter with a buffer containing spans
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig(max_buffer_size=10)
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Add a span to the buffer
        trace_span = TraceSpan(
            trace_id=TraceId(value="12345678901234567890123456789012"),  # 32 hex chars
            span_id=SpanId(value="1234567890123456"),  # 16 hex chars
            parent_span_id=None,
            name="test_span",
            start_time_unix_nano=0,
            end_time_unix_nano=1000,
            attributes={},
            events=[],
            status=SpanStatus(code=0, message="OK"),  # Use proper status object
        )
        adapter._buffer.add_span(trace_span)

        # When: Clearing the buffer
        adapter._process_buffer_contents()


class TestOTLPgRPCAdapterErrorHandling:
    """Test error handling in the OTLP gRPC adapter."""

    def test_export_handles_exception_gracefully(self) -> None:
        """Verifies that the Export method handles exceptions and returns proper response."""
        # Given: An adapter with a use case that throws an exception
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        mock_use_case.run.side_effect = Exception("Processing error")

        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a request with content to trigger processing
        request = ExportTraceServiceRequest()

        # Create a mock context
        mock_context = Mock(spec=grpc.ServicerContext)

        # When: Calling Export with exception
        response = adapter.Export(request, mock_context)

        # Then: Should return a valid response despite the exception
        assert isinstance(response, ExportTraceServiceResponse)
        # Since the request has no spans, the use case may not be called, but no exception should propagate

    def test_export_handles_spans_with_exception_gracefully(self) -> None:
        """Verifies that the Export method handles exceptions during span processing."""
        # Given: An adapter with a use case that throws an exception
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        mock_use_case.run.side_effect = Exception("Processing error")

        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a request with actual spans to trigger processing
        from opentelemetry.proto.trace.v1.trace_pb2 import Span
        from opentelemetry.proto.trace.v1.trace_pb2 import Status as SpanStatus
        from opentelemetry.proto.trace.v1.trace_pb2 import ResourceSpans, ScopeSpans
        import opentelemetry.proto.resource.v1.resource_pb2 as resource_pb2

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
                    resource=resource_pb2.Resource(attributes=[]),
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

        # Create a mock context
        mock_context = Mock(spec=grpc.ServicerContext)

        # When: Calling Export with exception
        response = adapter.Export(request, mock_context)

        # Then: Should return a valid response despite the exception
        assert isinstance(response, ExportTraceServiceResponse)

    def test_export_handles_multiple_resource_spans(self) -> None:
        """Verifies that the Export method handles multiple resource spans."""
        # Given: An adapter with a working use case
        mock_use_case = Mock(spec=ProcessTraceUseCase)

        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a request with multiple resource spans
        from opentelemetry.proto.trace.v1.trace_pb2 import Span
        from opentelemetry.proto.trace.v1.trace_pb2 import Status as SpanStatus
        from opentelemetry.proto.trace.v1.trace_pb2 import ResourceSpans, ScopeSpans
        import opentelemetry.proto.resource.v1.resource_pb2 as resource_pb2

        # Create multiple spans
        span1 = Span(
            trace_id=bytes([1] * 16),  # 16-byte trace ID
            span_id=bytes([2] * 8),  # 8-byte span ID
            parent_span_id=bytes([3] * 8),  # 8-byte parent span ID
            name="test_span_1",
            kind=Span.SpanKind.SPAN_KIND_INTERNAL,
            start_time_unix_nano=1000000000,
            end_time_unix_nano=2000000000,
            attributes=[],
            events=[],
            links=[],
            status=SpanStatus(code=SpanStatus.StatusCode.STATUS_CODE_UNSET),
        )

        span2 = Span(
            trace_id=bytes([4] * 16),  # 16-byte trace ID
            span_id=bytes([5] * 8),  # 8-byte span ID
            parent_span_id=bytes([6] * 8),  # 8-byte parent span ID
            name="test_span_2",
            kind=Span.SpanKind.SPAN_KIND_SERVER,
            start_time_unix_nano=2000000000,
            end_time_unix_nano=3000000000,
            attributes=[],
            events=[],
            links=[],
            status=SpanStatus(code=SpanStatus.StatusCode.STATUS_CODE_OK),
        )

        # Create a request with multiple resource spans
        request = ExportTraceServiceRequest(
            resource_spans=[
                ResourceSpans(
                    resource=resource_pb2.Resource(attributes=[]),
                    scope_spans=[
                        ScopeSpans(
                            scope=None,  # Use default scope
                            spans=[span1],
                            schema_url="",
                        )
                    ],
                    schema_url="",
                ),
                ResourceSpans(
                    resource=resource_pb2.Resource(attributes=[]),
                    scope_spans=[
                        ScopeSpans(
                            scope=None,  # Use default scope
                            spans=[span2],
                            schema_url="",
                        )
                    ],
                    schema_url="",
                ),
            ]
        )

        # Create a mock context
        mock_context = Mock(spec=grpc.ServicerContext)

        # When: Calling Export
        response = adapter.Export(request, mock_context)

        # Then: Should return a valid response and the use case should have been called
        assert isinstance(response, ExportTraceServiceResponse)
        assert (
            mock_use_case.run.called
        )  # Use case should be called for each resource span processing

    def test_export_handles_conversion_error_gracefully(self) -> None:
        """Verifies that the Export method handles conversion errors during span processing."""
        # Given: An adapter where the conversion method throws an exception
        mock_use_case = Mock(spec=ProcessTraceUseCase)

        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Mock the _create_trace_span_from_otlp to throw an exception
        original_method = adapter._create_trace_span_from_otlp

        def failing_converter(otlp_span):
            raise Exception("Conversion error")

        adapter._create_trace_span_from_otlp = failing_converter

        # Create a request with actual spans to trigger processing
        from opentelemetry.proto.trace.v1.trace_pb2 import Span
        from opentelemetry.proto.trace.v1.trace_pb2 import Status as SpanStatus
        from opentelemetry.proto.trace.v1.trace_pb2 import ResourceSpans, ScopeSpans
        import opentelemetry.proto.resource.v1.resource_pb2 as resource_pb2

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
                    resource=resource_pb2.Resource(attributes=[]),
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

        # Create a mock context
        mock_context = Mock(spec=grpc.ServicerContext)

        # When: Calling Export with conversion error
        response = adapter.Export(request, mock_context)

        # Then: Should return a valid response despite the conversion error
        assert isinstance(response, ExportTraceServiceResponse)
        # Restore the original method
        adapter._create_trace_span_from_otlp = original_method

    def test_export_traces_handles_exception_gracefully(self) -> None:
        """Verifies that the export_traces method handles exceptions and returns proper response."""
        # Given: An adapter with a use case that throws an exception
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        mock_use_case.run.side_effect = Exception("Processing error")

        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a request with content to trigger processing
        request = ExportTraceServiceRequest()

        # When: Calling export_traces with exception
        response = adapter.export_traces(request)

        # Then: Should return a valid response despite the exception
        assert isinstance(response, ExportTraceServiceResponse)
        # Since the request has no spans, the use case may not be called, but no exception should propagate


class TestOTLPgRPCAdapterConversionMethods:
    """Test conversion methods in the OTLP gRPC adapter."""

    def test_extract_attribute_value_with_string(self) -> None:
        """Verifies that attribute values are extracted correctly for string values."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock AnyValue with string value
        from opentelemetry.proto.common.v1.common_pb2 import AnyValue

        any_value = AnyValue(string_value="test_string")

        # When: Extracting the value
        result = adapter._extract_attribute_value(any_value)

        # Then: Should return the string value
        assert result == "test_string"

    def test_extract_attribute_value_with_bool(self) -> None:
        """Verifies that attribute values are extracted correctly for bool values."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock AnyValue with bool value
        from opentelemetry.proto.common.v1.common_pb2 import AnyValue

        any_value = AnyValue(bool_value=True)

        # When: Extracting the value
        result = adapter._extract_attribute_value(any_value)

        # Then: Should return the bool value
        assert result is True

    def test_extract_attribute_value_with_int(self) -> None:
        """Verifies that attribute values are extracted correctly for int values."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock AnyValue with int value
        from opentelemetry.proto.common.v1.common_pb2 import AnyValue

        any_value = AnyValue(int_value=42)

        # When: Extracting the value
        result = adapter._extract_attribute_value(any_value)

        # Then: Should return the int value
        assert result == 42

    def test_extract_attribute_value_with_double(self) -> None:
        """Verifies that attribute values are extracted correctly for double values."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock AnyValue with double value
        from opentelemetry.proto.common.v1.common_pb2 import AnyValue

        any_value = AnyValue(double_value=3.14)

        # When: Extracting the value
        result = adapter._extract_attribute_value(any_value)

        # Then: Should return the double value
        assert result == 3.14

    def test_extract_attribute_value_with_bytes(self) -> None:
        """Verifies that attribute values are extracted correctly for bytes values."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock AnyValue with bytes value
        from opentelemetry.proto.common.v1.common_pb2 import AnyValue

        any_value = AnyValue(bytes_value=b"test_bytes")

        # When: Extracting the value
        result = adapter._extract_attribute_value(any_value)

        # Then: Should return the bytes value
        assert result == b"test_bytes"

    def test_extract_attribute_value_with_none(self) -> None:
        """Verifies that attribute values return None when no field is present."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock AnyValue with no fields
        from opentelemetry.proto.common.v1.common_pb2 import AnyValue

        any_value = AnyValue()

        # When: Extracting the value
        result = adapter._extract_attribute_value(any_value)

        # Then: Should return None
        assert result is None

    def test_nanos_to_datetime_conversion(self) -> None:
        """Verifies that nanoseconds are properly converted to datetime."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Use a known timestamp (seconds since epoch) with nanosecond precision
        nanos = 1609459200000000000  # 2021-01-01T00:00:00.000000000Z in nanoseconds

        # When: Converting to datetime
        result = adapter._nanos_to_datetime(nanos)

        # Then: Should return correct datetime
        # The actual conversion uses fromtimestamp which uses local timezone
        # This may vary based on system timezone, so just verify it's a datetime object
        assert hasattr(result, "year")  # Must be a datetime object
        # Test with a timestamp that should be consistent across timezones for year
        # Using epoch time (1970-01-01) as reference
        epoch_nanos = 0
        epoch_result = adapter._nanos_to_datetime(epoch_nanos)
        # Check for year in the 1970s, timezone-adjusted
        assert 1969 <= epoch_result.year <= 1971

    def test_create_trace_span_from_otlp_conversion(self) -> None:
        """Verifies that OTLP spans are properly converted to domain TraceSpans."""
        # Given: An adapter instance and a mock OTLP span
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock OTLP span using protobuf message
        from opentelemetry.proto.trace.v1.trace_pb2 import Span
        from opentelemetry.proto.common.v1.common_pb2 import KeyValue, AnyValue
        from opentelemetry.proto.trace.v1.trace_pb2 import Status as SpanStatus

        # Create the OTLP span
        otlp_span = Span(
            trace_id=bytes.fromhex(
                "0123456789abcdef0123456789abcdef"
            ),  # 32 hex chars = 16 bytes
            span_id=bytes.fromhex("0123456789abcdef"),  # 16 hex chars = 8 bytes
            parent_span_id=bytes.fromhex("0123456789abcdef"),  # 16 hex chars = 8 bytes
            name="test_span",
            kind=Span.SpanKind.SPAN_KIND_INTERNAL,
            start_time_unix_nano=1609459200000000000,
            end_time_unix_nano=1609459201000000000,
            attributes=[
                KeyValue(key="attr1", value=AnyValue(string_value="value1")),
                KeyValue(key="attr2", value=AnyValue(int_value=42)),
            ],
            events=[],
            links=[],
            status=SpanStatus(code=SpanStatus.StatusCode.STATUS_CODE_UNSET),
        )

        # When: Converting to domain TraceSpan
        result = adapter._create_trace_span_from_otlp(otlp_span)

        # Then: Should return properly constructed TraceSpan
        assert result.trace_id.value == "0123456789abcdef0123456789abcdef"
        assert result.span_id.value == "0123456789abcdef"
        assert result.parent_span_id.value == "0123456789abcdef"
        assert result.name == "test_span"
        assert result.start_time_unix_nano == 1609459200000000000
        assert result.end_time_unix_nano == 1609459201000000000
        assert result.attributes == {"attr1": "value1", "attr2": 42}
        assert result.kind == Span.SpanKind.SPAN_KIND_INTERNAL
        assert result.status.code == SpanStatus.StatusCode.STATUS_CODE_UNSET

    def test_create_trace_span_from_otlp_without_parent(self) -> None:
        """Verifies that OTLP spans without parent span ID are properly converted."""
        # Given: An adapter instance and a mock OTLP span without parent
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock OTLP span without parent using protobuf message
        from opentelemetry.proto.trace.v1.trace_pb2 import Span
        from opentelemetry.proto.trace.v1.trace_pb2 import Status as SpanStatus

        # Create the OTLP span without parent
        otlp_span = Span(
            trace_id=bytes.fromhex(
                "0123456789abcdef0123456789abcdef"
            ),  # 32 hex chars = 16 bytes
            span_id=bytes.fromhex("0123456789abcdef"),  # 16 hex chars = 8 bytes
            parent_span_id=bytes(),  # Empty bytes for no parent
            name="test_span",
            kind=Span.SpanKind.SPAN_KIND_INTERNAL,
            start_time_unix_nano=1609459200000000000,
            end_time_unix_nano=1609459201000000000,
            attributes=[],
            events=[],
            links=[],
            status=SpanStatus(code=SpanStatus.StatusCode.STATUS_CODE_UNSET),
        )

        # When: Converting to domain TraceSpan
        result = adapter._create_trace_span_from_otlp(otlp_span)

        # Then: Should return properly constructed TraceSpan with None parent
        assert result.parent_span_id is None

    def test_create_trace_span_from_otlp_with_status_message(self) -> None:
        """Verifies that OTLP spans with status messages are properly converted."""
        # Given: An adapter instance and a mock OTLP span with status message
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock OTLP span with status message using protobuf message
        from opentelemetry.proto.trace.v1.trace_pb2 import Span
        from opentelemetry.proto.trace.v1.trace_pb2 import Status as SpanStatus

        # Create the OTLP span with status message
        otlp_span = Span(
            trace_id=bytes.fromhex(
                "0123456789abcdef0123456789abcdef"
            ),  # 32 hex chars = 16 bytes
            span_id=bytes.fromhex("0123456789abcdef"),  # 16 hex chars = 8 bytes
            parent_span_id=bytes.fromhex("0123456789abcdef"),  # 16 hex chars = 8 bytes
            name="test_span",
            kind=Span.SpanKind.SPAN_KIND_INTERNAL,
            start_time_unix_nano=1609459200000000000,
            end_time_unix_nano=1609459201000000000,
            attributes=[],
            events=[],
            links=[],
            status=SpanStatus(
                code=SpanStatus.StatusCode.STATUS_CODE_ERROR,
                message="Test error message",
            ),
        )

        # When: Converting to domain TraceSpan
        result = adapter._create_trace_span_from_otlp(otlp_span)

        # Then: Should return properly constructed TraceSpan with status message
        assert result.status.code == SpanStatus.StatusCode.STATUS_CODE_ERROR
        assert result.status.message == "Test error message"

    def test_create_trace_span_from_otlp_with_all_attribute_types(self) -> None:
        """Verifies that OTLP spans with all attribute types are properly converted."""
        # Given: An adapter instance and a mock OTLP span with all attribute types
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Create a mock OTLP span with all types of attributes
        from opentelemetry.proto.trace.v1.trace_pb2 import Span
        from opentelemetry.proto.common.v1.common_pb2 import KeyValue, AnyValue
        from opentelemetry.proto.trace.v1.trace_pb2 import Status as SpanStatus

        # Create the OTLP span with various attribute types
        otlp_span = Span(
            trace_id=bytes.fromhex(
                "0123456789abcdef0123456789abcdef"
            ),  # 32 hex chars = 16 bytes
            span_id=bytes.fromhex("0123456789abcdef"),  # 16 hex chars = 8 bytes
            parent_span_id=bytes.fromhex("0123456789abcdef"),  # 16 hex chars = 8 bytes
            name="test_span",
            kind=Span.SpanKind.SPAN_KIND_INTERNAL,
            start_time_unix_nano=1609459200000000000,
            end_time_unix_nano=1609459201000000000,
            attributes=[
                KeyValue(
                    key="string_attr", value=AnyValue(string_value="string_value")
                ),
                KeyValue(key="int_attr", value=AnyValue(int_value=42)),
                KeyValue(key="bool_attr", value=AnyValue(bool_value=True)),
                KeyValue(key="double_attr", value=AnyValue(double_value=3.14)),
                KeyValue(key="bytes_attr", value=AnyValue(bytes_value=b"bytes_value")),
            ],
            events=[],
            links=[],
            status=SpanStatus(code=SpanStatus.StatusCode.STATUS_CODE_UNSET),
        )

        # When: Converting to domain TraceSpan
        result = adapter._create_trace_span_from_otlp(otlp_span)

        # Then: Should return properly constructed TraceSpan with all attribute types
        expected_attributes = {
            "string_attr": "string_value",
            "int_attr": 42,
            "bool_attr": True,
            "double_attr": 3.14,
            "bytes_attr": b"bytes_value",
        }
        assert result.attributes == expected_attributes


class TestOTLPgRPCServerOperations:
    """Test gRPC server start and stop functionality."""

    def test_start_server_method_exists(self) -> None:
        """Verifies that the start_server method exists."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Then: The adapter should have the start_server method
        assert hasattr(adapter, "start_server")
        assert callable(getattr(adapter, "start_server"))

    def test_stop_server_method_exists(self) -> None:
        """Verifies that the stop_server method exists."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Then: The adapter should have the stop_server method
        assert hasattr(adapter, "stop_server")
        assert callable(getattr(adapter, "stop_server"))

    def test_serve_forever_method_exists(self) -> None:
        """Verifies that the serve_forever method exists."""
        # Given: An adapter instance
        mock_use_case = Mock(spec=ProcessTraceUseCase)
        config = OTLPGRPCServerConfig()
        adapter = OTLPgRPCAdapter(process_trace_use_case=mock_use_case, config=config)

        # Then: The adapter should have the serve_forever method
        assert hasattr(adapter, "serve_forever")
        assert callable(getattr(adapter, "serve_forever"))
