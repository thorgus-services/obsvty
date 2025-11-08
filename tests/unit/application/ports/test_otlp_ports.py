from obsvty.application.ports.otlp_ports import OTLPIngestionPort, TraceBufferPort


class TestOTLPIngestionPort:
    def test_port_has_required_methods(self):
        """Test that OTLPIngestionPort has the required methods"""
        # Check that the protocol has the required methods
        assert hasattr(OTLPIngestionPort, "ingest_traces")
        assert hasattr(OTLPIngestionPort, "ingest_metrics")
        assert hasattr(OTLPIngestionPort, "ingest_logs")


class TestTraceBufferPort:
    def test_port_has_required_methods(self):
        """Test that TraceBufferPort has the required methods"""
        # Check that the protocol has the required methods
        assert hasattr(TraceBufferPort, "add_span")
        assert hasattr(TraceBufferPort, "add_log")
        assert hasattr(TraceBufferPort, "add_metric")
        assert hasattr(TraceBufferPort, "get_spans")
        assert hasattr(TraceBufferPort, "get_logs")
        assert hasattr(TraceBufferPort, "size")
        assert hasattr(TraceBufferPort, "is_full")
