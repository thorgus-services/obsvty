import pytest
from unittest.mock import Mock
from obsvty.infrastructure.otlp.trace_service import TraceService


class TestTraceService:
    def test_trace_service_has_export_method(self):
        """Test that TraceService has the required export method"""
        mock_ingestion_port = Mock()
        trace_service = TraceService(mock_ingestion_port)

        assert hasattr(trace_service, "Export")

    def test_trace_service_export_method_exists(self):
        """Test that the export method can be called"""
        mock_ingestion_port = Mock()
        trace_service = TraceService(mock_ingestion_port)

        # Create a mock request
        mock_request = Mock()
        mock_context = Mock()

        # Should not raise an exception
        try:
            trace_service.Export(mock_request, mock_context)
        except AttributeError:
            pytest.fail("TraceService.Export method does not exist")
