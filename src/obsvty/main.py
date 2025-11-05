"""Composition root and server entrypoint for dependency injection."""

import concurrent.futures
import logging
import signal
import sys
from types import FrameType
from typing import Any, Dict, Optional

import grpc

from .adapters.messaging.otlp_grpc import OTLPgRPCAdapter
from .config.settings import (
    OtlpGrpcSettings,
    load_grpc_settings,
    validate_settings,
    get_server_endpoint,
)
from .ports.storage import TraceStoragePort
from .use_cases import ProcessTraceUseCase


def build_use_cases(storage: TraceStoragePort) -> Dict[str, Any]:
    return {
        "process_trace": ProcessTraceUseCase(storage=storage),
    }


def build_otlp_grpc_adapter(
    storage: TraceStoragePort, config: OtlpGrpcSettings
) -> OTLPgRPCAdapter:
    use_cases = build_use_cases(storage)
    process_trace_use_case = use_cases["process_trace"]

    adapter = OTLPgRPCAdapter(
        process_trace_use_case=process_trace_use_case, config=config
    )

    return adapter


def configure_grpc_server(settings: OtlpGrpcSettings) -> grpc.Server:
    if not validate_settings(settings):
        raise ValueError("Invalid configuration settings provided")

    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_receive_message_length", settings.max_message_length),
            ("grpc.max_send_message_length", settings.max_message_length),
        ],
    )

    return server


def load_grpc_settings_with_fallback() -> OtlpGrpcSettings:
    settings = load_grpc_settings()

    if not validate_settings(settings):
        raise ValueError("Loaded configuration settings failed validation")

    return settings


def start_server_with_config(
    storage: TraceStoragePort, settings: OtlpGrpcSettings
) -> OTLPgRPCAdapter:
    adapter = build_otlp_grpc_adapter(storage, settings)
    adapter.start_server()
    return adapter


def setup_signal_handlers(adapter: OTLPgRPCAdapter) -> None:
    def signal_handler(signum: int, frame: Optional[FrameType]) -> None:
        print(f"\nReceived signal {signum}. Shutting down server gracefully...")
        adapter.stop_server()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    try:
        settings = load_grpc_settings_with_fallback()

        logger.info(
            f"Starting OTLP gRPC server with configuration: host={settings.host}, port={settings.port}"
        )

        endpoint = get_server_endpoint(settings)
        logger.info(f"Server endpoint: {endpoint}")
        print(f"OTLP gRPC server configured to start on {endpoint}")

        print("Note: Actual server startup requires concrete storage implementation.")
        print(
            "For full server functionality, provide a concrete TraceStoragePort implementation."
        )
        print(f"Configuration loaded successfully. Server would start on {endpoint}")

        return 0

    except Exception as e:
        logger.error(f"Failed to start OTLP gRPC server: {e}", exc_info=True)
        print(f"Error starting server: {e}")
        return 1
