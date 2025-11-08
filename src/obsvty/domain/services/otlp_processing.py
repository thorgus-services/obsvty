"""Domain services for OTLP processing."""

import logging
from typing import List, Any
from datetime import datetime

from opentelemetry.proto.trace.v1 import trace_pb2
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2

from obsvty.domain.models.otlp import Span, LogRecord, OTLPData
from obsvty.domain.exceptions import OTLPValidationError


logger = logging.getLogger(__name__)


def validate_span(span: Span) -> bool:
    """
    Validate a Span value object.

    Args:
        span: The span to validate

    Returns:
        True if valid, raises OTLPValidationError if invalid
    """
    # Validation happens in the Span constructor, so if we have a Span object,
    # it's already valid. This function can be extended to check business rules
    # if needed.
    try:
        # The Span is already validated during construction
        # Additional business rule validation could go here
        pass
    except Exception as e:
        raise OTLPValidationError(f"Invalid span: {e}") from e

    return True


def validate_log_record(log_record: LogRecord) -> bool:
    """
    Validate a LogRecord value object.

    Args:
        log_record: The log record to validate

    Returns:
        True if valid, raises OTLPValidationError if invalid
    """
    try:
        # The LogRecord is already validated during construction
        # Additional business rule validation could go here
        pass
    except Exception as e:
        raise OTLPValidationError(f"Invalid log record: {e}") from e

    return True


def parse_otlp_trace_data(trace_data: bytes) -> List[Span]:
    """
    Parse OTLP trace data from bytes into a list of Span value objects.

    Args:
        trace_data: Raw OTLP trace data as bytes

    Returns:
        List of parsed Span objects
    """
    try:
        # Parse the raw bytes into the OTLP protobuf structure
        request = trace_service_pb2.ExportTraceServiceRequest.FromString(trace_data)

        spans = []

        # Iterate through resource spans
        for resource_span in request.resource_spans:
            resource = resource_span.resource
            # Process instrumentation library spans
            for (
                instrumentation_library_span
            ) in resource_span.instrumentation_library_spans:
                instrumentation_library = (
                    instrumentation_library_span.instrumentation_library
                )

                for span_proto in instrumentation_library_span.spans:
                    span = _convert_proto_span_to_domain_span(
                        span_proto, resource, instrumentation_library
                    )
                    spans.append(span)

        return spans
    except Exception as e:
        logger.error(f"Error parsing OTLP trace data: {e}")
        raise OTLPValidationError(f"Failed to parse trace data: {e}") from e


def _convert_proto_span_to_domain_span(
    proto_span: trace_pb2.Span,
    resource: Any = None,
    instrumentation_library: Any = None,
) -> Span:
    """
    Convert a protobuf Span to a domain Span value object.

    Args:
        proto_span: The protobuf span
        resource: Resource information (optional)
        instrumentation_library: Instrumentation library info (optional)

    Returns:
        Domain Span object
    """
    # Convert attributes from protobuf to dict
    attributes = {
        attr.key: _convert_any_value(attr.value) for attr in proto_span.attributes
    }

    # Convert events
    events = []
    for event in proto_span.events:
        event_data = {
            "time_unix_nano": event.time_unix_nano,
            "name": event.name,
            "attributes": {
                attr.key: _convert_any_value(attr.value) for attr in event.attributes
            },
        }
        events.append(event_data)

    # Convert status
    status = {
        "code": int(proto_span.status.code) if proto_span.status.code else 0,
        "message": proto_span.status.message if proto_span.status.message else "",
    }

    # Convert trace and span IDs from bytes to hex strings
    trace_id = proto_span.trace_id.hex() if proto_span.trace_id else ""
    span_id = proto_span.span_id.hex() if proto_span.span_id else ""
    parent_span_id = (
        proto_span.parent_span_id.hex() if proto_span.parent_span_id else None
    )

    return Span(
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=parent_span_id,
        name=proto_span.name,
        kind=int(proto_span.kind),
        start_time_unix_nano=proto_span.start_time_unix_nano,
        end_time_unix_nano=proto_span.end_time_unix_nano,
        attributes=attributes,
        events=events,
        status=status,
    )


def _convert_any_value(any_value: Any) -> Any:
    """
    Convert a protobuf AnyValue to a Python value.

    Args:
        any_value: The protobuf AnyValue

    Returns:
        Python value (str, int, float, bool, or dict/list for complex types)
    """
    if any_value.HasField("string_value"):
        return any_value.string_value
    elif any_value.HasField("bool_value"):
        return any_value.bool_value
    elif any_value.HasField("int_value"):
        return any_value.int_value
    elif any_value.HasField("double_value"):
        return any_value.double_value
    elif any_value.HasField("array_value"):
        return [_convert_any_value(v) for v in any_value.array_value.values]
    elif any_value.HasField("kvlist_value"):
        return {
            kv.key: _convert_any_value(kv.value) for kv in any_value.kvlist_value.values
        }
    else:
        return None


def process_otlp_data(trace_data: bytes, buffer_port: Any) -> OTLPData:
    """
    Process OTLP data and store it in the buffer.

    Args:
        trace_data: Raw OTLP trace data as bytes
        buffer_port: Buffer port for temporary storage

    Returns:
        OTLPData object with the processed data
    """
    try:
        spans = parse_otlp_trace_data(trace_data)

        # Add spans to buffer
        for span in spans:
            buffer_port.add_span(span)

        # Create OTLPData object with the processed spans
        otlp_data = OTLPData(resource_spans=tuple(spans), received_at=datetime.now())

        logger.info(f"Successfully processed {len(spans)} spans from OTLP data")

        return otlp_data
    except Exception as e:
        logger.error(f"Error processing OTLP data: {e}")
        raise OTLPValidationError(f"Failed to process OTLP data: {e}") from e
