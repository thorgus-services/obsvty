"""Configuration package for OTLP gRPC server settings.

This package contains the settings model and configuration loading functions
for the OTLP gRPC endpoint following the principles of Hexagonal Architecture
and environment-based configuration management.

This module re-exports the settings for backward compatibility.
"""

from .settings import (
    OtlpGrpcSettings,
    OTLPGRPCServerConfig,
    load_grpc_settings,
    load_otlp_grpc_config,
    validate_settings,
    get_server_endpoint,
)

__all__ = [
    "OtlpGrpcSettings",
    "OTLPGRPCServerConfig",
    "load_grpc_settings",
    "load_otlp_grpc_config",
    "validate_settings",
    "get_server_endpoint",
]
