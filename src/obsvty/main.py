"""Composition root (Dependency Injection bootstrap).

This module wires application use cases to concrete implementations of ports.
Adapters should be provided by the outer layers and passed into the builders
here. Keep this module free of business logic; it exists solely to compose.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

from .adapters.messaging.otlp_grpc import OTLPgRPCAdapter
from .config import load_otlp_grpc_config
from .ports.storage import TraceStoragePort
from .use_cases import ProcessTraceUseCase


def build_use_cases(storage: TraceStoragePort) -> Dict[str, Any]:
    """Build and return the application use cases.

    Args:
        storage: Concrete implementation of TraceStoragePort.

    Returns:
        A dictionary with instantiated use cases.
    """
    return {
        "process_trace": ProcessTraceUseCase(storage=storage),
    }


def build_otlp_grpc_adapter(storage: TraceStoragePort) -> OTLPgRPCAdapter:
    """Build and return the OTLP gRPC adapter.

    This function creates an instance of the OTLP gRPC adapter, configuring it
    with the appropriate use cases and server settings following the principles
    of dependency injection and hexagonal architecture.

    Args:
        storage: Concrete implementation of TraceStoragePort to be used by the adapter

    Returns:
        OTLPgRPCAdapter: Configured and ready-to-use OTLP gRPC adapter
    """
    # Build the use case first (dependency inversion principle)
    use_cases = build_use_cases(storage)
    process_trace_use_case = use_cases["process_trace"]

    # Load configuration
    config = load_otlp_grpc_config()

    # Create and return the adapter
    adapter = OTLPgRPCAdapter(
        process_trace_use_case=process_trace_use_case, config=config
    )

    return adapter


def main() -> int:
    """Entrypoint for ``python -m obsvty``.

    Loads environment variables and prints a quick status message.
    Actual adapter wiring should be done by callers that provide concrete
    implementations of the ports to :func:`build_use_cases` or :func:`build_otlp_grpc_adapter`.
    """
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        # Attempt project-root .env if running from inside src
        project_env = Path(__file__).resolve().parents[2] / ".env"
        if project_env.exists():
            load_dotenv(dotenv_path=project_env)

    print(
        "obsvty composition root loaded. Provide adapters to build_use_cases() or build_otlp_grpc_adapter()."
    )
    return 0
