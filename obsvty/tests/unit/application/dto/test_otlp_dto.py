from obsvty.application.dto.otlp_dto import OTLPIngestionDTO


class TestOTLPIngestionDTO:
    def test_otlp_ingestion_dto_creation(self):
        """Test creating an OTLPIngestionDTO"""
        dto = OTLPIngestionDTO(
            trace_data=b"test_trace_data", source_endpoint="test_source"
        )

        assert dto.trace_data == b"test_trace_data"
        assert dto.source_endpoint == "test_source"

    def test_otlp_ingestion_dto_defaults(self):
        """Test OTLPIngestionDTO with default values"""
        dto = OTLPIngestionDTO(trace_data=b"test_trace_data")

        assert dto.trace_data == b"test_trace_data"
        assert dto.source_endpoint == ""
