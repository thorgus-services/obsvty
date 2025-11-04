"""Messaging adapters module initialization.

Exports concrete implementations of messaging ports that connect
to external services like message queues, notification systems,
and now OTLP/gRPC services following the Hexagonal Architecture.
"""

from .otlp_grpc import OTLPgRPCAdapter

__all__ = ["OTLPgRPCAdapter"]
