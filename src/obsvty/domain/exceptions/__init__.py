class OTLPValidationError(Exception):
    """Raised when OTLP data validation fails"""

    pass


class TraceProcessingError(Exception):
    """Raised when trace processing encounters an error"""

    pass


class MetricsProcessingError(Exception):
    """Raised when metrics processing encounters an error"""

    pass


class LogsProcessingError(Exception):
    """Raised when logs processing encounters an error"""

    pass
