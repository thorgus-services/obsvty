"""OTLP Parsing Service converting OTLP gRPC objects to internal domain structures."""

from datetime import datetime
from typing import Any, Dict, List

from ...domain.observability import (
    SpanEvent,
    SpanId,
    SpanStatus,
    TraceId,
    TraceSpan,
    validate_attributes_format,
    validate_scope_spans_structure,
    validate_span_id_format,
    validate_span_structure,
)


class OTLPParsingService:
    """Service for parsing and validating OTLP data structures into domain entities."""

    def __init__(self) -> None:
        pass

    def parse_resource_spans(
        self, resource_spans_data: Dict[str, Any]
    ) -> List[TraceSpan]:
        """Parse ResourceSpans data into a list of TraceSpan entities."""
        if not isinstance(resource_spans_data, dict):
            raise ValueError("ResourceSpans data must be a dictionary")

        if not validate_resource_spans(resource_spans_data):
            raise ValueError("Invalid ResourceSpans structure")

        trace_spans: List[TraceSpan] = []

        scope_spans_list = resource_spans_data.get("scope_spans", [])
        instrumentation_spans_list = resource_spans_data.get(
            "instrumentation_library_spans", []
        )

        if scope_spans_list:
            for scope_span in scope_spans_list:
                trace_spans.extend(self._parse_scope_spans(scope_span))

        if instrumentation_spans_list:
            for instrumentation_span in instrumentation_spans_list:
                trace_spans.extend(self._parse_scope_spans(instrumentation_span))

        return trace_spans

    def _parse_scope_spans(self, scope_spans_data: Dict[str, Any]) -> List[TraceSpan]:
        """Parse ScopeSpans data into a list of TraceSpan entities."""
        if not validate_scope_spans_structure(scope_spans_data):
            raise ValueError("Invalid ScopeSpans structure")

        spans_list = scope_spans_data.get("spans", [])
        if not isinstance(spans_list, list):
            raise ValueError("Spans in ScopeSpans must be a list")

        trace_spans: List[TraceSpan] = []
        for span_data in spans_list:
            try:
                trace_span = self._parse_span(span_data)
                trace_spans.append(trace_span)
            except ValueError:
                continue

        return trace_spans

    def _parse_span(self, span_data: Dict[str, Any]) -> TraceSpan:
        """Parse a single Span data object into a TraceSpan entity."""
        if not validate_span_structure(span_data):
            raise ValueError("Invalid Span structure")

        trace_id_value = span_data["trace_id"]
        span_id_value = span_data["span_id"]
        name = span_data["name"]
        start_time_unix_nano = span_data["start_time_unix_nano"]
        end_time_unix_nano = span_data["end_time_unix_nano"]

        trace_id = TraceId(value=trace_id_value)
        span_id = SpanId(value=span_id_value)

        parent_span_id = None
        if "parent_span_id" in span_data and span_data["parent_span_id"]:
            parent_span_id_value = span_data["parent_span_id"]
            if validate_span_id_format(parent_span_id_value):
                parent_span_id = SpanId(value=parent_span_id_value)

        attributes = self._parse_attributes(span_data.get("attributes", []))
        events = self._parse_events(span_data.get("events", []))
        status = self._parse_status(span_data.get("status", {}))
        kind = span_data.get("kind", 0)

        return TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            start_time_unix_nano=start_time_unix_nano,
            end_time_unix_nano=end_time_unix_nano,
            attributes=attributes,
            events=events,
            status=status,
            kind=kind,
        )

    def _parse_attributes(
        self, attributes_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Parse attributes from OTLP format to internal dictionary format."""
        if not validate_attributes_format(attributes_data):
            raise ValueError("Invalid attributes format")

        attributes: Dict[str, Any] = {}

        if isinstance(attributes_data, dict):
            return attributes_data

        if isinstance(attributes_data, list):
            for attr in attributes_data:
                if isinstance(attr, dict) and "key" in attr and "value" in attr:
                    key = attr["key"]
                    value_data = attr["value"]
                    actual_value = self._extract_value_from_otlp_value(value_data)
                    attributes[key] = actual_value

        return attributes

    def _parse_events(self, events_data: List[Dict[str, Any]]) -> List[SpanEvent]:
        """Parse span events from OTLP format to internal SpanEvent objects."""
        events: List[SpanEvent] = []

        for event_data in events_data:
            if not isinstance(event_data, dict):
                continue

            name = event_data.get("name", "")
            if not name:
                continue  # Event name is required

            timestamp_unix_nano = event_data.get("time_unix_nano", 0)
            attributes = self._parse_attributes(event_data.get("attributes", []))

            timestamp = datetime.fromtimestamp(timestamp_unix_nano / 1_000_000_000)

            span_event = SpanEvent(
                name=name, timestamp=timestamp, attributes=attributes
            )

            events.append(span_event)

        return events

    def _parse_status(self, status_data: Dict[str, Any]) -> SpanStatus:
        """Parse span status from OTLP format to internal SpanStatus object."""
        if not isinstance(status_data, dict):
            return SpanStatus(code=0)  # UNSET

        code = status_data.get("code", 0)
        message = status_data.get("message")

        if message is not None and not isinstance(message, str):
            raise ValueError("Status message must be a string if provided")

        if not isinstance(code, int) or code not in (0, 1, 2):
            raise ValueError("Status code must be 0 (UNSET), 1 (OK), or 2 (ERROR)")

        return SpanStatus(code=code, message=message)

    def _extract_value_from_otlp_value(self, value_data: Dict[str, Any]) -> Any:
        """Extract the actual value from OTLP value object structure."""
        if not isinstance(value_data, dict):
            return value_data

        if "stringValue" in value_data:
            return value_data["stringValue"]
        elif "intValue" in value_data:
            return value_data["intValue"]
        elif "boolValue" in value_data:
            return value_data["boolValue"]
        elif "doubleValue" in value_data:
            return value_data["doubleValue"]
        elif "arrayValue" in value_data:
            array_values = value_data["arrayValue"]
            if isinstance(array_values, dict) and "values" in array_values:
                return [
                    self._extract_value_from_otlp_value(v)
                    for v in array_values["values"]
                ]
        elif "kvlistValue" in value_data:
            kvlist_values = value_data["kvlistValue"]
            if isinstance(kvlist_values, dict) and "values" in kvlist_values:
                return self._parse_attributes(kvlist_values["values"])
        else:
            return value_data


def validate_resource_spans(resource_spans_data: Dict[str, Any]) -> bool:
    """Validate ResourceSpans structure according to OTLP v1.9 specification."""
    if not isinstance(resource_spans_data, dict):
        return False

    has_scope_spans = "scope_spans" in resource_spans_data and isinstance(
        resource_spans_data["scope_spans"], list
    )
    has_instrumentation_spans = (
        "instrumentation_library_spans" in resource_spans_data
        and isinstance(resource_spans_data["instrumentation_library_spans"], list)
    )

    if not (has_scope_spans or has_instrumentation_spans):
        return False

    if "resource" in resource_spans_data:
        resource = resource_spans_data["resource"]
        if not isinstance(resource, dict):
            return False

    if "schema_url" in resource_spans_data:
        schema_url = resource_spans_data["schema_url"]
        if not isinstance(schema_url, str):
            return False

    return True


def parse_resource_spans(resource_spans_data: Dict[str, Any]) -> List[TraceSpan]:
    """Convenience function to parse ResourceSpans data using the OTLP parsing service."""
    service = OTLPParsingService()
    return service.parse_resource_spans(resource_spans_data)
