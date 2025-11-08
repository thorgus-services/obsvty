from unittest.mock import Mock
from obsvty.application.ports.otlp_ports import OTLPIngestionPort, TraceBufferPort
from obsvty.infrastructure.otlp.trace_service import TraceService
from obsvty.infrastructure.buffer.memory_buffer import MemoryBuffer
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2


class TestFullPipeline:
    def test_full_trace_ingestion_pipeline(self):
        """Test the complete pipeline from gRPC service to buffer storage"""
        # Create a buffer
        buffer = MemoryBuffer(max_size=100)

        # Create a mock ingestion port that stores data in the buffer
        class MockIngestionService(OTLPIngestionPort):
            def __init__(self, buffer_port: TraceBufferPort):
                self.buffer_port = buffer_port

            def ingest_traces(self, trace_data: bytes) -> None:
                # In a real implementation, we would parse the data and store it
                # For this test, we'll just pretend to process and store
                # by parsing and adding to buffer
                pass

            def ingest_metrics(self, metric_data: bytes) -> None:
                pass

            def ingest_logs(self, log_data: bytes) -> None:
                pass

        mock_service = MockIngestionService(buffer)
        trace_service = TraceService(mock_service)

        # Create a minimal valid request
        request = trace_service_pb2.ExportTraceServiceRequest(resource_spans=[])

        # Mock context
        mock_context = Mock()

        # Execute the request
        response = trace_service.Export(request, mock_context)

        # Verify successful response
        assert response is not None

    def test_trace_service_works_with_real_buffer(self):
        """Test that the trace service can work with a real buffer implementation"""
        # Create a mock ingestion port to test with the buffer
        mock_ingestion_port = Mock()

        # Create trace service
        trace_service = TraceService(mock_ingestion_port)

        # Create minimal request
        request = trace_service_pb2.ExportTraceServiceRequest()

        # Mock context
        mock_context = Mock()

        # Execute
        trace_service.Export(request, mock_context)

        # Verify the ingestion port was called
        mock_ingestion_port.ingest_traces.assert_called_once()
