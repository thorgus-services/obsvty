from unittest.mock import Mock
import grpc
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
from obsvty.infrastructure.otlp.trace_service import TraceService
from obsvty.application.ports.otlp_ports import OTLPIngestionPort


class TestTraceServiceIntegration:
    def test_trace_service_export_with_mock_ingestion_port(self):
        """Test the TraceService Export method with a mock ingestion port"""
        # Create a mock ingestion port
        mock_ingestion_port = Mock(spec=OTLPIngestionPort)
        mock_ingestion_port.ingest_traces.return_value = None

        # Create the trace service with the mock port
        trace_service = TraceService(mock_ingestion_port)

        # Create a mock gRPC context
        mock_context = Mock(spec=grpc.ServicerContext)

        # Create a minimal valid request
        request = trace_service_pb2.ExportTraceServiceRequest(resource_spans=[])

        # Call the Export method
        trace_service.Export(request, mock_context)

        # Verify that the ingestion port was called
        assert mock_ingestion_port.ingest_traces.called
        # Verify that the context was not set with an error code
        assert not mock_context.set_code.called


class TestFullIngestionFlow:
    def test_full_traces_ingestion_flow(self):
        """Test the full flow from gRPC service to buffer"""
        # Create a mock ingestion port that implements the full interface
        mock_ingestion_port = Mock(spec=OTLPIngestionPort)

        # Create the trace service
        trace_service = TraceService(mock_ingestion_port)

        # Create a mock context
        mock_context = Mock(spec=grpc.ServicerContext)

        # Create a request with some minimal data
        request = trace_service_pb2.ExportTraceServiceRequest(resource_spans=[])

        # Execute the export
        trace_service.Export(request, mock_context)

        # Verify the mock ingestion port was called correctly
        assert mock_ingestion_port.ingest_traces.called
        args, kwargs = mock_ingestion_port.ingest_traces.call_args
        assert len(args) == 1  # Should have been called with request bytes
        assert isinstance(args[0], bytes)  # The data should be bytes

    def test_trace_service_error_handling(self):
        """Test that the trace service properly handles errors"""
        # Create a mock ingestion port that raises an exception
        mock_ingestion_port = Mock(spec=OTLPIngestionPort)
        mock_ingestion_port.ingest_traces.side_effect = Exception("Test error")

        # Create the trace service
        trace_service = TraceService(mock_ingestion_port)

        # Create a mock context
        mock_context = Mock(spec=grpc.ServicerContext)

        # Create a request
        request = trace_service_pb2.ExportTraceServiceRequest(resource_spans=[])

        # Execute the export - should handle the exception gracefully
        trace_service.Export(request, mock_context)

        # Verify that the context was set with error details
        mock_context.set_code.assert_called()
        mock_context.set_details.assert_called()
